#!/usr/bin/env python3
"""
TrendRadar 页面优化脚本
- 修改AI分析标题
- 调整布局顺序
- 使用frontend-design skill优化样式
"""

import os
import re

INPUT_FILE = "/var/www/trendradar/index.html"
OUTPUT_FILE = "/var/www/trendradar/index.html"

# 优化后的CSS样式
OPTIMIZED_CSS = '''
/* 基础样式 */
* { box-sizing: border-box; }

body {
    font-family: 'Noto Sans SC', -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
    margin: 0;
    padding: 20px;
    background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
    color: #1e293b;
    line-height: 1.6;
    min-height: 100vh;
}

/* 容器 */
.container {
    max-width: 680px;
    margin: 0 auto;
    background: white;
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0 4px 32px rgba(0, 0, 0, 0.08), 0 1px 2px rgba(0, 0, 0, 0.04);
}

/* 头部 */
.header {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a855f7 100%);
    color: white;
    padding: 36px 28px;
    text-align: center;
    position: relative;
    overflow: hidden;
}

.header::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: url("data:image/svg+xml,%3Csvg viewBox='0 0 400 400' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E");
    opacity: 0.04;
    pointer-events: none;
}

.header-title {
    font-size: 26px;
    font-weight: 800;
    margin: 0 0 24px 0;
    letter-spacing: -0.5px;
    text-shadow: 0 2px 20px rgba(0, 0, 0, 0.15);
}

.header-info {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    font-size: 14px;
}

.info-item {
    text-align: center;
    padding: 12px 8px;
    background: rgba(255, 255, 255, 0.12);
    border-radius: 12px;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.15);
    transition: all 0.2s ease;
}

.info-item:hover {
    background: rgba(255, 255, 255, 0.18);
    transform: translateY(-2px);
}

.info-label {
    display: block;
    font-size: 11px;
    font-weight: 500;
    opacity: 0.85;
    margin-bottom: 4px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.info-value {
    font-weight: 700;
    font-size: 16px;
}

/* 保存按钮 */
.save-buttons {
    position: absolute;
    top: 16px;
    right: 16px;
    display: flex;
    gap: 8px;
}

.save-btn {
    background: rgba(255, 255, 255, 0.2);
    border: 1px solid rgba(255, 255, 255, 0.3);
    color: white;
    padding: 8px 16px;
    border-radius: 10px;
    cursor: pointer;
    font-size: 13px;
    font-weight: 600;
    transition: all 0.2s ease;
    backdrop-filter: blur(10px);
}

.save-btn:hover {
    background: rgba(255, 255, 255, 0.3);
    border-color: rgba(255, 255, 255, 0.5);
    transform: translateY(-1px);
}

/* 内容区域 */
.content {
    padding: 0 24px 24px;
}

/* AI 分析区块 */
.section-divider.ai-section {
    margin: 24px 0;
    padding: 0;
    background: linear-gradient(145deg, #f8fafc 0%, #f1f5f9 100%);
    border-radius: 16px;
    border: 1px solid #e2e8f0;
    overflow: hidden;
}

.ai-section-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 18px 24px;
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
    border-bottom: none;
}

.ai-section-title {
    font-size: 17px;
    font-weight: 700;
    color: white;
    display: flex;
    align-items: center;
    gap: 8px;
}

.ai-section-badge {
    background: rgba(255, 255, 255, 0.25);
    color: white;
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    padding: 4px 10px;
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.3);
}

.ai-blocks-container {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 0;
}

.ai-block {
    padding: 18px 24px;
    border-bottom: 1px solid #e2e8f0;
    border-right: 1px solid #e2e8f0;
    transition: all 0.2s ease;
}

.ai-block:nth-child(2n) {
    border-right: none;
}

.ai-block:nth-last-child(-n+2) {
    border-bottom: none;
}

.ai-block:hover {
    background: white;
}

.ai-block-title {
    font-size: 14px;
    font-weight: 700;
    color: #6366f1;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.ai-block-content {
    font-size: 13px;
    line-height: 1.7;
    color: #64748b;
}

/* 新闻列表 */
.hotlist-section {
    margin-top: 0;
}

.word-group {
    margin-top: 24px;
    padding: 20px;
    background: #f8fafc;
    border-radius: 16px;
    border: 1px solid #e2e8f0;
}

.word-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
    padding-bottom: 12px;
    border-bottom: 2px solid #e2e8f0;
}

.word-name {
    font-size: 16px;
    font-weight: 700;
    color: #1e293b;
}

.word-count {
    font-size: 13px;
    font-weight: 600;
    padding: 4px 12px;
    border-radius: 20px;
}

.word-count.warm { background: #fef3c7; color: #92400e; }
.word-count.hot { background: #fee2e2; color: #991b1b; }

.word-index {
    font-size: 13px;
    color: #94a3b8;
}

.news-item {
    display: flex;
    gap: 14px;
    padding: 14px;
    margin-bottom: 12px;
    background: white;
    border-radius: 12px;
    border: 1px solid #e2e8f0;
    transition: all 0.2s ease;
}

.news-item:hover {
    border-color: #cbd5e1;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    transform: translateY(-1px);
}

.news-number {
    width: 30px;
    height: 30px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
    color: white;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 700;
    flex-shrink: 0;
}

.news-content { flex: 1; }

.news-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 6px;
    flex-wrap: wrap;
}

.source-name {
    font-size: 12px;
    font-weight: 600;
    color: #6366f1;
}

.rank-num {
    font-size: 11px;
    font-weight: 600;
    padding: 2px 8px;
    border-radius: 6px;
    background: #fee2e2;
    color: #dc2626;
}

.time-info, .count-info {
    font-size: 11px;
    color: #94a3b8;
}

.news-title {
    font-size: 14px;
    line-height: 1.5;
}

.news-link {
    color: #1e293b;
    text-decoration: none;
    font-weight: 500;
    transition: color 0.2s;
}

.news-link:hover { color: #6366f1; }

/* RSS 区块 */
.section-divider.rss-section {
    margin: 24px 0;
    padding: 0;
    background: linear-gradient(145deg, #f0fdf4 0%, #ecfdf5 100%);
    border-radius: 16px;
    border: 1px solid #d1fae5;
    overflow: hidden;
}

.rss-section-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 18px 24px;
    border-bottom: 1px solid #d1fae5;
}

.rss-section-title {
    font-size: 17px;
    font-weight: 700;
    color: #059669;
}

.rss-section-count {
    font-size: 13px;
    font-weight: 600;
    padding: 4px 12px;
    background: #d1fae5;
    color: #059669;
    border-radius: 20px;
}

.feed-group { margin-bottom: 16px; }
.feed-group:last-child { margin-bottom: 0; }

.feed-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 12px;
    padding-bottom: 8px;
    border-bottom: 2px solid #10b981;
}

.feed-name {
    font-size: 15px;
    font-weight: 700;
    color: #059669;
}

.feed-count {
    font-size: 13px;
    font-weight: 500;
    color: #059669;
}

.rss-item {
    margin-bottom: 10px;
    padding: 14px;
    background: white;
    border-radius: 10px;
    border-left: 3px solid #10b981;
    transition: all 0.2s ease;
}

.rss-item:hover {
    box-shadow: 0 2px 8px rgba(16, 185, 129, 0.1);
}

.rss-item:last-child { margin-bottom: 0; }

.rss-meta {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 8px;
}

.rss-time {
    font-size: 12px;
    color: #6b7280;
}

.rss-author {
    font-size: 12px;
    font-weight: 600;
    color: #059669;
}

.rss-title {
    font-size: 14px;
    line-height: 1.5;
}

.rss-link {
    color: #1f2937;
    text-decoration: none;
    font-weight: 500;
}

.rss-link:hover {
    color: #059669;
}

/* Footer */
.footer {
    padding: 24px;
    background: #f8fafc;
    border-top: 1px solid #e2e8f0;
    text-align: center;
}

.footer-content {
    font-size: 13px;
    color: #64748b;
}

.project-name {
    font-weight: 700;
    color: #475569;
}

.footer-link {
    color: #6366f1;
    text-decoration: none;
    font-weight: 500;
    transition: color 0.2s;
}

.footer-link:hover {
    color: #8b5cf6;
}

/* 响应式设计 */
@media (max-width: 640px) {
    body { padding: 12px; }
    
    .header { padding: 28px 20px; }
    .header-title { font-size: 22px; }
    .header-info { grid-template-columns: repeat(2, 1fr); gap: 10px; }
    .info-item { padding: 10px 6px; }
    .info-value { font-size: 14px; }
    
    .content { padding: 0 16px 16px; }
    
    .ai-blocks-container { grid-template-columns: 1fr; }
    .ai-block { border-right: none; }
    .ai-block:nth-child(2n) { border-right: none; }
    
    .word-group { padding: 16px; }
    .news-item { padding: 12px; }
}

/* 动画 */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(16px); }
    to { opacity: 1; transform: translateY(0); }
}

.header { animation: fadeInUp 0.5s ease-out; }
.section-divider.ai-section { animation: fadeInUp 0.5s ease-out 0.1s both; }
.hotlist-section { animation: fadeInUp 0.5s ease-out 0.2s both; }
.section-divider.rss-section { animation: fadeInUp 0.5s ease-out 0.3s both; }
'''

def optimize_page():
    """优化页面"""
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. 替换AI分析标题
    title_mapping = {
        "核心热点态势": "📊 核心内容",
        "异动与弱信号": "🏢 关键动态",
        "RSS 深度洞察": "💡 技术应用",
        "研判策略建议": "⚠️ 政策风险"
    }
    
    for old_title, new_title in title_mapping.items():
        content = content.replace(
            f'<div class="ai-block-title">{old_title}</div>',
            f'<div class="ai-block-title">{new_title}</div>'
        )
    
    # 2. 重新排列AI分析块的顺序
    # 提取每个AI块的内容
    ai_block_pattern = r'<div class="ai-block">(.*?)</div>\s*</div>'
    ai_blocks = re.findall(ai_block_pattern, content, re.DOTALL)
    
    if len(ai_blocks) >= 4:
        # 创建标题到内容的映射
        block_map = {}
        for block in ai_blocks:
            title_match = re.search(r'<div class="ai-block-title">(.*?)</div>', block)
            if title_match:
                title = title_match.group(1)
                content_match = re.search(r'<div class="ai-block-content">(.*?)</div>', block, re.DOTALL)
                if content_match:
                    block_content = content_match.group(1).strip()
                    block_map[title] = block_content
        
        # 按新顺序重新排列：📊核心内容、🏢关键动态、⚠️政策风险、💡技术应用
        new_order = ["📊 核心内容", "🏢 关键动态", "⚠️ 政策风险", "💡 技术应用"]
        
        new_ai_blocks = ""
        for title in new_order:
            if title in block_map:
                new_ai_blocks += f'''
                    <div class="ai-block">
                        <div class="ai-block-title">{title}</div>
                        <div class="ai-block-content">{block_map[title]}</div>
                    </div>
'''
        
        # 替换原来的AI块
        ai_section_pattern = r'(<div class="ai-blocks-container">)(.*?)(</div>\s*</div>\s*</div>)'
        match = re.search(ai_section_pattern, content, re.DOTALL)
        if match:
            content = content[:match.start()] + f'<div class="ai-blocks-container">{new_ai_blocks}                </div>' + content[match.end():]
    
    # 3. 替换CSS样式
    style_pattern = r'<style>.*?</style>'
    new_style = f'<style>\n{OPTIMIZED_CSS}\n    </style>'
    content = re.sub(style_pattern, new_style, content, flags=re.DOTALL)
    
    # 4. 将AI分析区块移到header后面
    # 提取AI分析区块
    ai_section_pattern = r'(<div class="section-divider ai-section">.*?</div>\s*</div>\s*</div>)'
    ai_match = re.search(ai_section_pattern, content, re.DOTALL)
    
    if ai_match:
        ai_section = ai_match.group(1)
        
        # 从原位置删除
        content = content[:ai_match.start()] + content[ai_match.end():]
        
        # 找到header-info结束的位置，在其后插入AI分析区块
        header_end_pattern = r'(</div>\s*</div>\s*</div>\s*<div class="content">)'
        header_match = re.search(header_end_pattern, content)
        
        if header_match:
            insert_pos = header_match.start() + len('</div>\s*</div>\s*</div>')
            content = content[:insert_pos] + '\n            ' + ai_section + '\n            ' + content[insert_pos:]
    
    # 保存优化后的页面
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ 页面优化完成")
    print(f"   - AI分析标题已更新")
    print(f"   - 布局顺序已调整")
    print(f"   - 样式已优化")

if __name__ == "__main__":
    optimize_page()
    optimize_page()
    optimize_page()