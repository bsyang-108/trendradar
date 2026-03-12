#!/usr/bin/env python3
"""
TrendRadar 智能同步脚本
从 Docker 报告提取数据，注入到 nginx 首页的结构中
保持 nginx 首页的样式和布局不变
"""

import re
import sys
from pathlib import Path

NGINX_INDEX = Path("/var/www/trendradar/index.html")
DOCKER_LATEST = Path("/root/trendradar/output/html/latest/daily.html")

def extract_docker_data(html_content: str) -> dict:
    """从 Docker 报告提取关键数据"""
    data = {}
    
    # 提取统计数据（顺序：报告类型、新闻总数、热点新闻、生成时间）
    stats_match = re.findall(r'<span class="info-value">([^<]+)</span>', html_content)
    if len(stats_match) >= 4:
        # stats_match[0] = 报告类型（全天汇总）
        # stats_match[1] = 新闻总数（476 条）
        # stats_match[2] = 热点新闻（22 条）
        # stats_match[3] = 生成时间（03-08 10:49）
        data['news_total'] = stats_match[1]  # 新闻总数
        data['hot_count'] = stats_match[2]   # 热点新闻
        data['gen_time'] = stats_match[3]    # 生成时间
    
    # 提取 AI 分析内容
    ai_blocks = {}
    patterns = {
        'core_trends': r'<div class="ai-block-title">核心热点态势</div>\s*<div class="ai-block-content">([^<]+)</div>',
        'signals': r'<div class="ai-block-title">异动与弱信号</div>\s*<div class="ai-block-content">([^<]+)</div>',
        'outlook_strategy': r'<div class="ai-block-title">研判策略建议</div>\s*<div class="ai-block-content">([^<]+)</div>',
        'rss_insights': r'<div class="ai-block-title">RSS 深度洞察</div>\s*<div class="ai-block-content">([^<]+)</div>',
    }
    
    # 也尝试匹配 nginx 首页的标题格式
    nginx_patterns = {
        'core_content': r'<div class="ai-block-title">📊 核心内容</div>\s*<div class="ai-block-content">([^<]+)</div>',
        'key_dynamics': r'<div class="ai-block-title">🏢 关键动态</div>\s*<div class="ai-block-content">([^<]+)</div>',
        'policy_risk': r'<div class="ai-block-title">⚠️ 政策风险</div>\s*<div class="ai-block-content">([^<]+)</div>',
        'tech_app': r'<div class="ai-block-title">💡 中东热点关注</div>\s*<div class="ai-block-content">([^<]+)</div>',
    }
    
    for key, pattern in patterns.items():
        match = re.search(pattern, html_content)
        if match:
            ai_blocks[key] = match.group(1)
    
    for key, pattern in nginx_patterns.items():
        match = re.search(pattern, html_content)
        if match:
            ai_blocks[key] = match.group(1)
    
    if ai_blocks:
        data['ai_blocks'] = ai_blocks
    
    return data

def update_nginx_index(nginx_html: str, docker_data: dict) -> str:
    """更新 nginx 首页的数据"""
    html = nginx_html
    
    # 找到所有带"条"的 span，一次性替换
    # nginx 首页顺序：新闻总数、热点新闻
    # Docker 数据顺序：news_total、hot_count
    
    matches = list(re.finditer(r'(<span class="info-value">)(\d+ 条)(</span>)', html))
    
    if len(matches) >= 2 and 'news_total' in docker_data and 'hot_count' in docker_data:
        # 从后往前替换，避免位置偏移
        # 第二个匹配是热点新闻
        start2, end2 = matches[1].span()
        html = html[:start2] + f'<span class="info-value">{docker_data["hot_count"]}</span>' + html[end2:]
        
        # 重新查找第一个匹配的位置（因为内容长度可能变化）
        matches = list(re.finditer(r'(<span class="info-value">)(\d+ 条)(</span>)', html))
        start1, end1 = matches[0].span()
        html = html[:start1] + f'<span class="info-value">{docker_data["news_total"]}</span>' + html[end1:]
    
    # 更新生成时间
    if 'gen_time' in docker_data:
        html = re.sub(
            r'(<span class="info-value">)\d{2}-\d{2} \d{2}:\d{2}(</span>)',
            f'\\g<1>{docker_data["gen_time"]}\\g<2>',
            html
        )
    
    # 更新 AI 分析内容
    if 'ai_blocks' in docker_data:
        ai = docker_data['ai_blocks']
        
        # 更新核心内容
        if 'core_content' in ai or 'core_trends' in ai:
            content = ai.get('core_content') or ai.get('core_trends', '')
            html = re.sub(
                r'(<div class="ai-block-title">📊 核心内容</div>\s*<div class="ai-block-content">)[^<]*(</div>)',
                f'\\g<1>{content}\\g<2>',
                html
            )
        
        # 更新关键动态
        if 'key_dynamics' in ai or 'signals' in ai:
            content = ai.get('key_dynamics') or ai.get('signals', '')
            html = re.sub(
                r'(<div class="ai-block-title">🏢 关键动态</div>\s*<div class="ai-block-content">)[^<]*(</div>)',
                f'\\g<1>{content}\\g<2>',
                html
            )
        
        # 更新政策风险
        if 'policy_risk' in ai or 'outlook_strategy' in ai:
            content = ai.get('policy_risk') or ai.get('outlook_strategy', '')
            html = re.sub(
                r'(<div class="ai-block-title">⚠️ 政策风险</div>\s*<div class="ai-block-content">)[^<]*(</div>)',
                f'\\g<1>{content}\\g<2>',
                html
            )
        
        # 更新中东热点关注/RSS 深度洞察（如果没有 rss_insights，使用默认文本）
        content = ai.get('rss_insights', '')
        if not content:
            content = "今日无重大中东局势变化，油价稳定，在中东中国企业运营正常"
        # 尝试匹配两种标题格式
        html = re.sub(
            r'(<div class="ai-block-title">💡 RSS 深度洞察</div>\s*<div class="ai-block-content">)[^<]*(</div>)',
            f'\\g<1>{content}\\g<2>',
            html
        )
        html = re.sub(
            r'(<div class="ai-block-title">💡 中东热点关注</div>\s*<div class="ai-block-content">)[^<]*(</div>)',
            f'\\g<1>{content}\\g<2>',
            html
        )
    
    return html

def main():
    # 检查文件
    if not DOCKER_LATEST.exists():
        print("❌ Docker 最新报告不存在")
        sys.exit(1)
    
    # 读取 Docker HTML（作为基础，保留关键词分组）
    docker_html = DOCKER_LATEST.read_text(encoding='utf-8')
    
    # 提取 AI 分析区块（包含所有 4 个子区块）
    # 匹配从 ai-section 开始到完整的 ai-grid 结束
    ai_section_match = re.search(
        r'(<div class="section-divider ai-section">.*?</div>\s*</div>\s*</div>\s*</div>)',
        docker_html,
        re.DOTALL
    )
    
    if not ai_section_match:
        print("⚠️ Docker 报告缺少 AI 分析区块")
        sys.exit(0)
    
    ai_section = ai_section_match.group(1)
    
    # 从旧的 Nginx HTML 中提取 RSS 部分（使用.bak3 文件）
    nginx_backup = Path(str(NGINX_INDEX) + '.bak3')
    rss_section = ""
    if nginx_backup.exists():
        nginx_old_html = nginx_backup.read_text(encoding='utf-8')
        rss_match = re.search(
            r'(<div class="section-divider rss-section">.*?</div>\s*</div>\s*</div>)',
            nginx_old_html,
            re.DOTALL
        )
        if rss_match:
            rss_section = rss_match.group(1)
            print(f"✅ 提取 RSS 部分成功")
    
    # 从 Docker HTML 中删除 AI 分析区块（后面会插入到前面）
    # 删除完整的 ai-section 区块（包含所有 4 个子区块）
    docker_html_no_ai = re.sub(
        r'\s*<div class="section-divider ai-section">.*?</div>\s*</div>\s*</div>\s*</div>',
        '',
        docker_html,
        flags=re.DOTALL
    )
    
    # 在 header 后面插入 AI 分析
    # Docker HTML 使用 <div class="header"> 和 <div class="content">
    header_end_match = re.search(
        r'(<div class="header">.*?</div>\s*)(<div class="content">)',
        docker_html_no_ai,
        re.DOTALL
    )
    
    if not header_end_match:
        print("⚠️ 未找到插入位置，直接复制 Docker HTML")
        import shutil
        shutil.copy(str(DOCKER_LATEST), str(NGINX_INDEX))
        print(f"✅ 已复制 Docker 完整页面")
        return
    
    # 插入 AI 分析到 header 后面
    insert_pos = header_end_match.start(2)
    nginx_html = docker_html_no_ai[:insert_pos] + ai_section + "\n            " + docker_html_no_ai[insert_pos:]
    
    # 在热点新闻列表后面插入 RSS 部分（在页脚之前）
    if rss_section:
        # 找到 hotlist-section 或 footer 的位置
        # 尝试匹配 footer 或 </div> 结束标签
        footer_match = re.search(
            r'(</div>\s*)(<div class="footer">)',
            nginx_html,
            re.DOTALL
        )
        if footer_match:
            rss_insert_pos = footer_match.start(1)
            nginx_html = nginx_html[:rss_insert_pos] + "\n            " + rss_section + "\n            " + nginx_html[rss_insert_pos:]
            print(f"✅ 已插入 RSS 部分到新闻列表后面")
        else:
            # 备用方案：在 AI 分析后面插入
            ai_end_match = re.search(
                r'(<div class="section-divider ai-section">.*?</div>\s*</div>\s*</div>)',
                nginx_html,
                re.DOTALL
            )
            if ai_end_match:
                rss_insert_pos = ai_end_match.end()
                nginx_html = nginx_html[:rss_insert_pos] + "\n            " + rss_section + "\n            " + nginx_html[rss_insert_pos:]
                print(f"✅ 已插入 RSS 部分")
    
    # 提取统计数据
    stats_match = re.findall(r'<span class="info-value">([^<]+)</span>', docker_html)
    if len(stats_match) >= 4:
        news_total = stats_match[1]  # 新闻总数
        hot_count = stats_match[2]   # 热点新闻
        gen_time = stats_match[3]    # 生成时间
        
        # 更新 Nginx HTML 的统计数据
        matches = list(re.finditer(r'(<span class="info-value">)(\d+ 条)(</span>)', nginx_html))
        if len(matches) >= 2:
            # 替换热点新闻（从后往前）
            start2, end2 = matches[1].span()
            nginx_html = nginx_html[:start2] + f'<span class="info-value">{hot_count}</span>' + nginx_html[end2:]
            
            # 重新查找并替换新闻总数
            matches = list(re.finditer(r'(<span class="info-value">)(\d+ 条)(</span>)', nginx_html))
            start1, end1 = matches[0].span()
            nginx_html = nginx_html[:start1] + f'<span class="info-value">{news_total}</span>' + nginx_html[end1:]
        
        # 更新生成时间
        nginx_html = re.sub(
            r'(<span class="info-value">)\d{2}-\d{2} \d{2}:\d{2}(</span>)',
            f'\\g<1>{gen_time}\\g<2>',
            nginx_html
        )
    
    # 提取 AI 分析内容
    ai_blocks = {}
    patterns = {
        'core_trends': r'<div class="ai-block-title">核心热点态势</div>\s*<div class="ai-block-content">([^<]+)</div>',
        'signals': r'<div class="ai-block-title">异动与弱信号</div>\s*<div class="ai-block-content">([^<]+)</div>',
        'outlook_strategy': r'<div class="ai-block-title">研判策略建议</div>\s*<div class="ai-block-content">([^<]+)</div>',
        'rss_insights': r'<div class="ai-block-title">RSS 深度洞察</div>\s*<div class="ai-block-content">([^<]+)</div>',
    }
    
    for key, pattern in patterns.items():
        match = re.search(pattern, docker_html)
        if match:
            ai_blocks[key] = match.group(1)
    
    # 更新 Nginx HTML 的 AI 分析内容
    if ai_blocks:
        # 核心内容
        if 'core_trends' in ai_blocks:
            nginx_html = re.sub(
                r'(<div class="ai-block-title">📊 AI 技术核心内容</div>\s*<div class="ai-block-content">)[^<]*(</div>)',
                f'\\g<1>{ai_blocks["core_trends"]}\\g<2>',
                nginx_html
            )
        
        # 关键动态
        if 'signals' in ai_blocks:
            nginx_html = re.sub(
                r'(<div class="ai-block-title">🏢 技术公司关键动态</div>\s*<div class="ai-block-content">)[^<]*(</div>)',
                f'\\g<1>{ai_blocks["signals"]}\\g<2>',
                nginx_html
            )
        
        # 政策风险
        if 'outlook_strategy' in ai_blocks:
            nginx_html = re.sub(
                r'(<div class="ai-block-title">⚠️ 政策风险</div>\s*<div class="ai-block-content">)[^<]*(</div>)',
                f'\\g<1>{ai_blocks["outlook_strategy"]}\\g<2>',
                nginx_html
            )
        
        # 中东热点关注
        content = ai_blocks.get('rss_insights', '')
        if not content:
            content = "今日无重大中东局势变化，油价稳定，在中东中国企业运营正常"
        nginx_html = re.sub(
            r'(<div class="ai-block-title">💡 中东热点关注</div>\s*<div class="ai-block-content">)[^<]*(</div>)',
            f'\\g<1>{content}\\g<2>',
            nginx_html
        )
    
    # 替换 AI 分析标题为用户自定义的标题
    title_mapping = {
        '核心热点态势': '📊 AI 技术核心内容',
        '异动与弱信号': '🏢 技术公司关键动态',
        'RSS 深度洞察': '💡 中东热点关注',
        '研判策略建议': '⚠️ 政策风险'
    }
    
    for old_title, new_title in title_mapping.items():
        nginx_html = nginx_html.replace(
            f'<div class="ai-block-title">{old_title}</div>',
            f'<div class="ai-block-title">{new_title}</div>'
        )
    
    # 保存
    NGINX_INDEX.rename(str(NGINX_INDEX) + '.bak2')
    NGINX_INDEX.write_text(nginx_html, encoding='utf-8')
    
    print(f"✅ 已同步（AI 分析在上，热点新闻在下，保留关键词分组）")

if __name__ == "__main__":
    main()