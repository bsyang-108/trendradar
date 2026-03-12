#!/usr/bin/env python3
"""
TrendRadar 动态模板生成器
- 使用深色主题 + 紫蓝渐变设计
- 自动从TrendRadar数据生成页面
- 支持PC端和移动端响应式
"""

import os
import json
import sqlite3
from datetime import datetime
from pathlib import Path

# 输出目录
OUTPUT_DIR = "/root/trendradar/output"
CUSTOM_PAGE = "/var/www/trendradar/index.html"

def get_db_path():
    """获取数据库路径"""
    today = datetime.now().strftime('%Y-%m-%d')
    return os.path.join(OUTPUT_DIR, 'news', f'{today}.db')

def get_rss_db_path():
    """获取RSS数据库路径"""
    today = datetime.now().strftime('%Y-%m-%d')
    return os.path.join(OUTPUT_DIR, 'rss', f'{today}.db')

def get_ai_analysis():
    """获取AI分析结果"""
    html_dir = os.path.join(OUTPUT_DIR, 'html', datetime.now().strftime('%Y-%m-%d'))
    latest_html = None
    
    if os.path.exists(html_dir):
        files = sorted(os.listdir(html_dir), reverse=True)
        if files:
            latest_html = os.path.join(html_dir, files[0])
    
    if not latest_html or not os.path.exists(latest_html):
        return None
    
    # 从HTML中提取AI分析
    with open(latest_html, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取AI分析内容
    ai_blocks = {}
    import re
    
    # 尝试匹配AI分析区块
    patterns = {
        'core_trends': r'核心热点态势.*?<div class="ai-block-content">(.*?)</div>',
        'signals': r'异动与弱信号.*?<div class="ai-block-content">(.*?)</div>',
        'rss_insights': r'RSS 深度洞察.*?<div class="ai-block-content">(.*?)</div>',
        'outlook_strategy': r'研判策略建议.*?<div class="ai-block-content">(.*?)</div>'
    }
    
    for key, pattern in patterns.items():
        match = re.search(pattern, content, re.DOTALL)
        if match:
            ai_blocks[key] = match.group(1).strip()
    
    return ai_blocks if ai_blocks else None

def get_hot_news():
    """获取热点新闻"""
    db_path = get_db_path()
    if not os.path.exists(db_path):
        return []
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 获取热点新闻：rank <= 30 或抓取次数 >= 3
    cursor.execute("""
        SELECT title, url, platform_id, rank, first_crawl_time, last_crawl_time, crawl_count
        FROM news_items
        WHERE rank <= 30 OR crawl_count >= 3
        ORDER BY rank ASC, crawl_count DESC
        LIMIT 50
    """)
    
    news = []
    for row in cursor.fetchall():
        news.append({
            'title': row[0],
            'url': row[1],
            'source': row[2],
            'rank': row[3],
            'first_seen': row[4],
            'last_seen': row[5],
            'count': row[6]
        })
    
    conn.close()
    return news

def get_rss_updates():
    """获取RSS更新"""
    db_path = get_rss_db_path()
    if not os.path.exists(db_path):
        return []
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 获取RSS更新
    cursor.execute("""
        SELECT title, url, feed_id, published_at
        FROM rss_items
        ORDER BY published_at DESC
        LIMIT 20
    """)
    
    rss = []
    for row in cursor.fetchall():
        rss.append({
            'title': row[0],
            'url': row[1],
            'source': row[2],
            'time': row[3]
        })
    
    conn.close()
    return rss

def get_stats():
    """获取统计数据"""
    db_path = get_db_path()
    if not os.path.exists(db_path):
        return {'total': 0, 'hot': 0}
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM news_items")
    total = cursor.fetchone()[0]
    
    # 热点新闻：rank <= 20 或抓取次数 >= 3
    cursor.execute("SELECT COUNT(*) FROM news_items WHERE rank <= 20 OR crawl_count >= 3")
    hot = cursor.fetchone()[0]
    
    conn.close()
    return {'total': total, 'hot': hot}

def format_time(timestamp):
    """格式化时间"""
    if not timestamp:
        return ''
    try:
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        return dt.strftime('%H:%M')
    except:
        return timestamp[:5] if len(timestamp) >= 5 else timestamp

def generate_html():
    """生成HTML页面"""
    stats = get_stats()
    news = get_hot_news()
    rss = get_rss_updates()
    ai_analysis = get_ai_analysis()
    
    # 按来源分组新闻
    news_by_category = {}
    for item in news:
        source = item.get('source', '其他')
        if source not in news_by_category:
            news_by_category[source] = []
        news_by_category[source].append(item)
    
    # AI分析内容
    ai_content = {
        'core_trends': '政策重心转向 AI 就业赋能与岗位创造，AIGC 内容生产边际成本趋近于零引发行业结构性重塑。',
        'signals': 'OpenAI GPT-5.4 实现自主电脑操作与编程闭环但推理成本高企；商汤重构多模态架构移除中间编码器；360 建立纳米漫剧工业化流水线。',
        'outlook_strategy': '人社部介入 AI 岗位替代舆论，企业需规避"裁员替代"合规风险；自动驾驶人为接管事故频发，L3 级以上责任界定监管即将收紧。',
        'rss_insights': 'AI 短剧单部成本 3000 元获 5 亿播放，验证文娱行业 ROI 模型；无问智科发布物理 AI 数据基座，突破具身智能数据瓶颈。'
    }
    
    if ai_analysis:
        ai_content.update(ai_analysis)
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TrendRadar - 热点新闻分析</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700;900&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-primary: #0a0a0f;
            --bg-secondary: #12121a;
            --bg-card: #1a1a24;
            --bg-elevated: #22222e;
            --text-primary: #f0f0f5;
            --text-secondary: #9090a0;
            --text-muted: #606070;
            --accent-primary: #6366f1;
            --accent-secondary: #8b5cf6;
            --accent-tertiary: #a855f7;
            --accent-success: #10b981;
            --accent-warning: #f59e0b;
            --accent-danger: #ef4444;
            --border-color: #2a2a3a;
            --gradient-hero: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a855f7 100%);
            --gradient-card: linear-gradient(145deg, #1a1a24 0%, #22222e 100%);
            --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.3);
            --shadow-md: 0 4px 20px rgba(0, 0, 0, 0.4);
            --shadow-lg: 0 8px 40px rgba(0, 0, 0, 0.5);
            --shadow-glow: 0 0 40px rgba(99, 102, 241, 0.15);
            --radius-sm: 8px;
            --radius-md: 12px;
            --radius-lg: 16px;
            --radius-xl: 24px;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Noto Sans SC', -apple-system, BlinkMacSystemFont, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
            min-height: 100vh;
            overflow-x: hidden;
        }}

        .bg-pattern {{
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-image: 
                radial-gradient(circle at 20% 20%, rgba(99, 102, 241, 0.08) 0%, transparent 50%),
                radial-gradient(circle at 80% 80%, rgba(168, 85, 247, 0.08) 0%, transparent 50%),
                radial-gradient(circle at 40% 60%, rgba(139, 92, 246, 0.05) 0%, transparent 40%);
            pointer-events: none;
            z-index: 0;
        }}

        .container {{
            position: relative;
            z-index: 1;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }}

        .header {{
            background: var(--gradient-hero);
            border-radius: var(--radius-xl);
            padding: 40px 32px;
            margin-bottom: 24px;
            position: relative;
            overflow: hidden;
            box-shadow: var(--shadow-lg), var(--shadow-glow);
        }}

        .header::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url("data:image/svg+xml,%3Csvg viewBox='0 0 400 400' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E");
            opacity: 0.03;
            pointer-events: none;
        }}

        .header-title {{
            font-size: 32px;
            font-weight: 900;
            letter-spacing: -0.5px;
            margin-bottom: 24px;
            text-shadow: 0 2px 20px rgba(0, 0, 0, 0.2);
        }}

        .header-stats {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
        }}

        .stat-item {{
            text-align: center;
            padding: 16px 12px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: var(--radius-md);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: transform 0.2s ease, background 0.2s ease;
        }}

        .stat-item:hover {{
            transform: translateY(-2px);
            background: rgba(255, 255, 255, 0.15);
        }}

        .stat-label {{
            font-size: 11px;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 1px;
            opacity: 0.8;
            margin-bottom: 6px;
        }}

        .stat-value {{
            font-family: 'Space Mono', monospace;
            font-size: 20px;
            font-weight: 700;
        }}

        .ai-section {{
            background: var(--gradient-card);
            border-radius: var(--radius-xl);
            margin-bottom: 24px;
            overflow: hidden;
            border: 1px solid var(--border-color);
            box-shadow: var(--shadow-md);
        }}

        .ai-header {{
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(139, 92, 246, 0.2) 100%);
            padding: 20px 24px;
            border-bottom: 1px solid var(--border-color);
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}

        .ai-title {{
            font-size: 18px;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .ai-badge {{
            font-family: 'Space Mono', monospace;
            font-size: 10px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            padding: 4px 10px;
            background: var(--accent-primary);
            border-radius: 20px;
        }}

        .ai-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 1px;
            background: var(--border-color);
        }}

        .ai-block {{
            background: var(--bg-card);
            padding: 20px 24px;
            transition: background 0.2s ease;
        }}

        .ai-block:hover {{
            background: var(--bg-elevated);
        }}

        .ai-block-title {{
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .ai-block-title .emoji {{
            font-size: 18px;
        }}

        .ai-block-content {{
            font-size: 13px;
            line-height: 1.7;
            color: var(--text-secondary);
        }}

        .news-section {{
            background: var(--gradient-card);
            border-radius: var(--radius-xl);
            margin-bottom: 24px;
            overflow: hidden;
            border: 1px solid var(--border-color);
            box-shadow: var(--shadow-md);
        }}

        .news-header {{
            padding: 20px 24px;
            border-bottom: 1px solid var(--border-color);
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}

        .news-category {{
            font-size: 16px;
            font-weight: 700;
        }}

        .news-count {{
            font-family: 'Space Mono', monospace;
            font-size: 12px;
            padding: 4px 12px;
            background: rgba(16, 185, 129, 0.15);
            color: var(--accent-success);
            border-radius: 20px;
        }}

        .news-list {{
            padding: 8px;
        }}

        .news-item {{
            display: flex;
            gap: 16px;
            padding: 16px;
            border-radius: var(--radius-md);
            margin-bottom: 8px;
            transition: background 0.2s ease;
        }}

        .news-item:last-child {{
            margin-bottom: 0;
        }}

        .news-item:hover {{
            background: var(--bg-elevated);
        }}

        .news-number {{
            width: 32px;
            height: 32px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: var(--gradient-hero);
            border-radius: var(--radius-sm);
            font-family: 'Space Mono', monospace;
            font-size: 14px;
            font-weight: 700;
            flex-shrink: 0;
        }}

        .news-content {{
            flex: 1;
            min-width: 0;
        }}

        .news-meta {{
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 8px;
            flex-wrap: wrap;
        }}

        .news-source {{
            font-size: 12px;
            font-weight: 500;
            color: var(--accent-primary);
        }}

        .news-rank {{
            font-family: 'Space Mono', monospace;
            font-size: 11px;
            padding: 2px 8px;
            background: rgba(239, 68, 68, 0.15);
            color: var(--accent-danger);
            border-radius: 4px;
        }}

        .news-time {{
            font-size: 11px;
            color: var(--text-muted);
        }}

        .news-title {{
            font-size: 14px;
            font-weight: 500;
            line-height: 1.5;
        }}

        .news-link {{
            color: var(--text-primary);
            text-decoration: none;
            transition: color 0.2s ease;
        }}

        .news-link:hover {{
            color: var(--accent-primary);
        }}

        .rss-section {{
            background: var(--gradient-card);
            border-radius: var(--radius-xl);
            margin-bottom: 24px;
            overflow: hidden;
            border: 1px solid var(--border-color);
            box-shadow: var(--shadow-md);
        }}

        .rss-header {{
            padding: 20px 24px;
            border-bottom: 1px solid var(--border-color);
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}

        .rss-title {{
            font-size: 16px;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .rss-count {{
            font-family: 'Space Mono', monospace;
            font-size: 12px;
            padding: 4px 12px;
            background: rgba(16, 185, 129, 0.15);
            color: var(--accent-success);
            border-radius: 20px;
        }}

        .rss-list {{
            padding: 8px;
        }}

        .rss-item {{
            padding: 16px;
            border-radius: var(--radius-md);
            margin-bottom: 8px;
            background: rgba(16, 185, 129, 0.05);
            border-left: 3px solid var(--accent-success);
            transition: background 0.2s ease;
        }}

        .rss-item:last-child {{
            margin-bottom: 0;
        }}

        .rss-item:hover {{
            background: rgba(16, 185, 129, 0.1);
        }}

        .rss-meta {{
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 8px;
        }}

        .rss-time {{
            font-size: 11px;
            color: var(--text-muted);
        }}

        .rss-source {{
            font-size: 12px;
            font-weight: 500;
            color: var(--accent-success);
        }}

        .rss-new {{
            font-size: 10px;
            font-weight: 700;
            padding: 2px 6px;
            background: var(--accent-danger);
            color: white;
            border-radius: 4px;
        }}

        .rss-title-text {{
            font-size: 14px;
            font-weight: 500;
        }}

        .rss-link {{
            color: var(--text-primary);
            text-decoration: none;
            transition: color 0.2s ease;
        }}

        .rss-link:hover {{
            color: var(--accent-success);
        }}

        .footer {{
            text-align: center;
            padding: 32px 24px;
            color: var(--text-muted);
            font-size: 13px;
        }}

        .footer-link {{
            color: var(--accent-primary);
            text-decoration: none;
            font-weight: 500;
            transition: color 0.2s ease;
        }}

        .footer-link:hover {{
            color: var(--accent-secondary);
        }}

        @media (max-width: 768px) {{
            .container {{
                padding: 12px;
            }}

            .header {{
                padding: 28px 20px;
                border-radius: var(--radius-lg);
            }}

            .header-title {{
                font-size: 24px;
            }}

            .header-stats {{
                grid-template-columns: repeat(2, 1fr);
                gap: 12px;
            }}

            .stat-item {{
                padding: 12px 8px;
            }}

            .stat-value {{
                font-size: 16px;
            }}

            .ai-grid {{
                grid-template-columns: 1fr;
            }}

            .ai-block {{
                padding: 16px 20px;
            }}

            .news-section,
            .rss-section,
            .ai-section {{
                border-radius: var(--radius-lg);
            }}

            .news-header,
            .rss-header,
            .ai-header {{
                padding: 16px 20px;
            }}

            .news-list,
            .rss-list {{
                padding: 4px;
            }}

            .news-item,
            .rss-item {{
                padding: 12px;
            }}
        }}

        @keyframes fadeInUp {{
            from {{
                opacity: 0;
                transform: translateY(20px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}

        .header {{
            animation: fadeInUp 0.6s ease-out;
        }}

        .ai-section {{
            animation: fadeInUp 0.6s ease-out 0.1s both;
        }}

        .news-section {{
            animation: fadeInUp 0.6s ease-out 0.2s both;
        }}

        .rss-section {{
            animation: fadeInUp 0.6s ease-out 0.3s both;
        }}

        .footer {{
            animation: fadeInUp 0.6s ease-out 0.4s both;
        }}
    </style>
</head>
<body>
    <div class="bg-pattern"></div>
    
    <div class="container">
        <header class="header">
            <h1 class="header-title">热点新闻分析</h1>
            <div class="header-stats">
                <div class="stat-item">
                    <div class="stat-label">报告类型</div>
                    <div class="stat-value">全天</div>
                </div>
                <div class="stat-item">
                    <div class="stat-label">新闻总数</div>
                    <div class="stat-value">{stats['total']}</div>
                </div>
                <div class="stat-item">
                    <div class="stat-label">热点新闻</div>
                    <div class="stat-value">{stats['hot']}</div>
                </div>
                <div class="stat-item">
                    <div class="stat-label">生成时间</div>
                    <div class="stat-value">{datetime.now().strftime('%H:%M')}</div>
                </div>
            </div>
        </header>

        <section class="ai-section">
            <div class="ai-header">
                <div class="ai-title">✨ AI 热点分析</div>
                <div class="ai-badge">AI</div>
            </div>
            <div class="ai-grid">
                <div class="ai-block">
                    <div class="ai-block-title"><span class="emoji">📊</span>核心内容</div>
                    <div class="ai-block-content">{ai_content.get('core_trends', '')}</div>
                </div>
                <div class="ai-block">
                    <div class="ai-block-title"><span class="emoji">🏢</span>关键动态</div>
                    <div class="ai-block-content">{ai_content.get('signals', '')}</div>
                </div>
                <div class="ai-block">
                    <div class="ai-block-title"><span class="emoji">⚠️</span>政策风险</div>
                    <div class="ai-block-content">{ai_content.get('outlook_strategy', '')}</div>
                </div>
                <div class="ai-block">
                    <div class="ai-block-title"><span class="emoji">💡</span>技术应用</div>
                    <div class="ai-block-content">{ai_content.get('rss_insights', '')}</div>
                </div>
            </div>
        </section>
'''
    
    # 添加新闻列表
    if news:
        news_items_html = ''
        for i, item in enumerate(news, 1):
            time_str = format_time(item.get('first_seen', ''))
            news_items_html += f'''
                <div class="news-item">
                    <div class="news-number">{i}</div>
                    <div class="news-content">
                        <div class="news-meta">
                            <span class="news-source">{item.get('source', '未知')}</span>
                            <span class="news-rank">热度 {item.get('rank', '-')}</span>
                            <span class="news-time">{time_str}</span>
                        </div>
                        <div class="news-title">
                            <a href="{item.get('url', '#')}" target="_blank" class="news-link">{item.get('title', '')}</a>
                        </div>
                    </div>
                </div>
'''
        
        html += f'''
        <section class="news-section">
            <div class="news-header">
                <div class="news-category">热点新闻</div>
                <div class="news-count">{len(news)} 条</div>
            </div>
            <div class="news-list">
                {news_items_html}
            </div>
        </section>
'''
    
    # 添加RSS更新
    if rss:
        rss_items_html = ''
        for item in rss:
            rss_items_html += f'''
                <div class="rss-item">
                    <div class="rss-meta">
                        <span class="rss-time">{format_time(item.get('time', ''))}</span>
                        <span class="rss-source">{item.get('source', '未知')}</span>
                        <span class="rss-new">NEW</span>
                    </div>
                    <div class="rss-title-text">
                        <a href="{item.get('url', '#')}" target="_blank" class="rss-link">{item.get('title', '')}</a>
                    </div>
                </div>
'''
        
        html += f'''
        <section class="rss-section">
            <div class="rss-header">
                <div class="rss-title">📰 RSS 新增更新</div>
                <div class="rss-count">{len(rss)} 条</div>
            </div>
            <div class="rss-list">
                {rss_items_html}
            </div>
        </section>
'''
    
    html += '''
        <footer class="footer">
            由 <strong>TrendRadar</strong> 生成 · 
            <a href="https://github.com/sansan0/TrendRadar" target="_blank" class="footer-link">GitHub 开源项目</a>
        </footer>
    </div>
</body>
</html>'''
    
    return html

def main():
    """主函数"""
    print("=" * 40)
    print("TrendRadar 动态模板生成器")
    print(datetime.now().strftime("%Y-%m-%d %H:%M"))
    print("=" * 40)
    
    # 生成HTML
    html = generate_html()
    
    # 保存到自定义页面
    with open(CUSTOM_PAGE, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ 页面已生成: {CUSTOM_PAGE}")
    
    # 同时保存到输出目录
    output_path = os.path.join(OUTPUT_DIR, 'index.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ 页面已同步: {output_path}")

if __name__ == "__main__":
    main()