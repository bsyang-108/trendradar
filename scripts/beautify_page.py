#!/usr/bin/env python3
"""
美化TrendRadar页面
- 改进颜色方案
- 优化卡片样式
- 添加更好的视觉层次
"""

import os
import re

# 美化后的CSS样式
BEAUTIFIED_CSS = '''
/* 美化后的全局样式 */
* { box-sizing: border-box; }
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', system-ui, sans-serif;
    margin: 0;
    padding: 20px;
    background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%);
    color: #333;
    line-height: 1.6;
    min-height: 100vh;
}

.container {
    max-width: 640px;
    margin: 0 auto;
    background: white;
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 4px 24px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.04);
}

/* 美化后的头部样式 */
.header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 36px 24px;
    text-align: center;
    position: relative;
}

.save-buttons {
    position: absolute;
    top: 16px;
    right: 16px;
    display: flex;
    gap: 8px;
}

.save-btn {
    background: rgba(255, 255, 255, 0.25);
    border: 1px solid rgba(255, 255, 255, 0.4);
    color: white;
    padding: 8px 16px;
    border-radius: 8px;
    cursor: pointer;
    font-size: 13px;
    font-weight: 500;
    transition: all 0.2s ease;
    backdrop-filter: blur(10px);
}

.save-btn:hover {
    background: rgba(255, 255, 255, 0.35);
    transform: translateY(-1px);
}

.header-title {
    font-size: 24px;
    font-weight: 700;
    margin: 0 0 24px 0;
    letter-spacing: 0.5px;
}

.header-info {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    font-size: 14px;
}

.info-item {
    text-align: center;
    padding: 8px;
    background: rgba(255,255,255,0.1);
    border-radius: 8px;
}

.info-label {
    display: block;
    font-size: 11px;
    opacity: 0.85;
    margin-bottom: 4px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.info-value {
    font-weight: 600;
    font-size: 15px;
}

/* 美化后的内容区域 */
.content {
    padding: 0 20px 20px;
}

/* 美化后的热点词组样式 */
.word-group {
    margin-top: 20px;
    padding: 20px;
    background: #f8fafc;
    border-radius: 12px;
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
    font-weight: 600;
    color: #1e293b;
}

.word-count {
    font-size: 13px;
    padding: 4px 10px;
    border-radius: 12px;
    font-weight: 500;
}

.word-count.warm { background: #fef3c7; color: #92400e; }
.word-count.hot { background: #fee2e2; color: #991b1b; }

.word-index {
    font-size: 13px;
    color: #94a3b8;
}

/* 美化后的新闻条目样式 */
.news-item {
    display: flex;
    gap: 12px;
    padding: 14px;
    margin-bottom: 12px;
    background: white;
    border-radius: 10px;
    border: 1px solid #e2e8f0;
    transition: all 0.2s ease;
}

.news-item:hover {
    border-color: #cbd5e1;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

.news-number {
    width: 28px;
    height: 28px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 8px;
    font-size: 13px;
    font-weight: 600;
    flex-shrink: 0;
}

.news-content { flex: 1; }

.news-header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 6px;
    flex-wrap: wrap;
}

.source-name {
    font-size: 12px;
    color: #64748b;
    font-weight: 500;
}

.rank-num {
    font-size: 11px;
    padding: 2px 6px;
    border-radius: 4px;
    background: #f1f5f9;
    color: #475569;
}

.rank-num.high { background: #fee2e2; color: #dc2626; }

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

.news-link:hover { color: #667eea; }

/* 美化后的AI分析区块样式 */
.ai-section {
    margin: 24px 20px;
    padding: 24px;
    background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
    border-radius: 16px;
    border: 1px solid #bae6fd;
}

.ai-section-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 20px;
}

.ai-section-title {
    font-size: 18px;
    font-weight: 700;
    color: #0369a1;
}

.ai-section-badge {
    background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%);
    color: white;
    font-size: 11px;
    font-weight: 600;
    padding: 4px 10px;
    border-radius: 6px;
}

.ai-block {
    margin-bottom: 16px;
    padding: 16px;
    background: white;
    border-radius: 12px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    border-left: 4px solid #0ea5e9;
}

.ai-block:last-child { margin-bottom: 0; }

.ai-block-title {
    font-size: 15px;
    font-weight: 600;
    color: #0369a1;
    margin-bottom: 8px;
}

.ai-block-content {
    font-size: 14px;
    line-height: 1.7;
    color: #334155;
}

/* 美化后的RSS部分样式 */
.rss-section {
    margin: 24px 20px;
    padding-top: 24px;
    border-top: 1px solid #e2e8f0;
}

.rss-section-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 20px;
}

.rss-section-title {
    font-size: 18px;
    font-weight: 700;
    color: #059669;
}

.rss-section-count {
    color: #6b7280;
    font-size: 14px;
    background: #d1fae5;
    padding: 4px 12px;
    border-radius: 12px;
}

.feed-group { margin-bottom: 20px; }
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
    font-weight: 600;
    color: #059669;
}

.feed-count {
    color: #666;
    font-size: 13px;
    font-weight: 500;
}

.rss-item {
    margin-bottom: 12px;
    padding: 14px;
    background: linear-gradient(135deg, #f0fdf4 0%, #ecfdf5 100%);
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
    color: #6b7280;
    font-size: 12px;
}

.rss-author {
    color: #059669;
    font-size: 12px;
    font-weight: 500;
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
    text-decoration: underline;
}

/* 美化后的底部样式 */
.footer {
    padding: 20px 24px;
    background: #f8fafc;
    border-top: 1px solid #e2e8f0;
    text-align: center;
}

.footer-content {
    font-size: 13px;
    color: #64748b;
}

.project-name {
    font-weight: 600;
    color: #475569;
}

.footer-link {
    color: #667eea;
    text-decoration: none;
}

.footer-link:hover {
    text-decoration: underline;
}

/* 响应式设计 */
@media (max-width: 640px) {
    body { padding: 12px; }
    .header { padding: 24px 16px; }
    .header-title { font-size: 20px; }
    .header-info { grid-template-columns: repeat(2, 1fr); }
    .content { padding: 0 16px 16px; }
    .ai-section, .rss-section { margin: 20px 16px; padding: 20px; }
}
'''

def beautify_page(filepath):
    """美化页面"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 替换CSS部分
    # 找到<style>标签
    style_start = content.find('<style>')
    style_end = content.find('</style>') + len('</style>')
    
    if style_start != -1 and style_end != -1:
        new_content = content[:style_start] + f'<style>\n{BEAUTIFIED_CSS}\n    </style>' + content[style_end:]
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✅ 已美化: {filepath}")
    else:
        print(f"⚠️ 未找到CSS部分: {filepath}")

def main():
    # 美化主页面
    index_html = "/var/www/trendradar/index.html"
    if os.path.exists(index_html):
        beautify_page(index_html)
    
    print("✅ 页面美化完成")

if __name__ == "__main__":
    main()