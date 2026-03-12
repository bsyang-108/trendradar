#!/usr/bin/env python3
"""
TrendRadar 页面美化脚本
- 使用frontend-design skill优化样式
- 保持所有文字内容不变
- 只替换CSS样式
"""

import re

INPUT_FILE = "/var/www/trendradar/index.html"

# 美化后的CSS样式 - 现代优雅风格
BEAUTIFIED_CSS = '''
/* 基础样式 */
* { box-sizing: border-box; }

body {
    font-family: 'Noto Sans SC', -apple-system, BlinkMacSystemFont, 'PingFang SC', 'Hiragino Sans GB', sans-serif;
    margin: 0;
    padding: 24px;
    background: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%);
    color: #1e293b;
    line-height: 1.65;
    min-height: 100vh;
}

/* 容器 */
.container {
    max-width: 680px;
    margin: 0 auto;
    background: #ffffff;
    border-radius: 24px;
    overflow: hidden;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08), 0 1px 2px rgba(0, 0, 0, 0.04);
}

/* 头部 */
.header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #9f7aea 100%);
    color: white;
    padding: 40px 32px;
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
    font-size: 28px;
    font-weight: 800;
    margin: 0 0 28px 0;
    letter-spacing: -0.5px;
    text-shadow: 0 2px 20px rgba(0, 0, 0, 0.15);
}

.header-info {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
    font-size: 14px;
}

.info-item {
    text-align: center;
    padding: 14px 10px;
    background: rgba(255, 255, 255, 0.14);
    border-radius: 14px;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.18);
    transition: all 0.25s ease;
}

.info-item:hover {
    background: rgba(255, 255, 255, 0.2);
    transform: translateY(-2px);
}

.info-label {
    display: block;
    font-size: 11px;
    font-weight: 600;
    opacity: 0.85;
    margin-bottom: 5px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.info-value {
    font-weight: 700;
    font-size: 17px;
}

/* 保存按钮 */
.save-buttons {
    position: absolute;
    top: 18px;
    right: 18px;
    display: flex;
    gap: 10px;
}

.save-btn {
    background: rgba(255, 255, 255, 0.22);
    border: 1px solid rgba(255, 255, 255, 0.35);
    color: white;
    padding: 9px 18px;
    border-radius: 12px;
    cursor: pointer;
    font-size: 13px;
    font-weight: 600;
    transition: all 0.25s ease;
    backdrop-filter: blur(10px);
}

.save-btn:hover {
    background: rgba(255, 255, 255, 0.32);
    border-color: rgba(255, 255, 255, 0.5);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

/* 内容区域 */
.content {
    padding: 0 28px 28px;
}

/* AI 分析区块 */
.section-divider.ai-section {
    margin: 28px 0;
    padding: 0;
    background: linear-gradient(145deg, #faf5ff 0%, #f3e8ff 100%);
    border-radius: 20px;
    border: 1px solid #e9d5ff;
    overflow: hidden;
    box-shadow: 0 4px 16px rgba(139, 92, 246, 0.08);
}

.ai-section-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 20px 28px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-bottom: none;
}

.ai-section-title {
    font-size: 18px;
    font-weight: 700;
    color: white;
    display: flex;
    align-items: center;
    gap: 10px;
}

.ai-section-badge {
    background: rgba(255, 255, 255, 0.28);
    color: white;
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    padding: 5px 12px;
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.35);
}

.ai-blocks-container {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 0;
}

.ai-block {
    padding: 20px 28px;
    border-bottom: 1px solid #e9d5ff;
    border-right: 1px solid #e9d5ff;
    transition: all 0.25s ease;
    background: transparent;
}

.ai-block:nth-child(2n) {
    border-right: none;
}

.ai-block:nth-last-child(-n+2) {
    border-bottom: none;
}

.ai-block:hover {
    background: rgba(255, 255, 255, 0.7);
}

.ai-block-title {
    font-size: 15px;
    font-weight: 700;
    color: #7c3aed;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.ai-block-content {
    font-size: 13px;
    line-height: 1.75;
    color: #6b7280;
}

/* 新闻列表 */
.hotlist-section {
    margin-top: 0;
}

.word-group {
    margin-top: 28px;
    padding: 24px;
    background: linear-gradient(145deg, #f8fafc 0%, #f1f5f9 100%);
    border-radius: 20px;
    border: 1px solid #e2e8f0;
}

.word-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 18px;
    padding-bottom: 14px;
    border-bottom: 2px solid #e2e8f0;
}

.word-name {
    font-size: 17px;
    font-weight: 700;
    color: #1e293b;
}

.word-count {
    font-size: 13px;
    font-weight: 600;
    padding: 5px 14px;
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
    gap: 16px;
    padding: 16px;
    margin-bottom: 14px;
    background: white;
    border-radius: 14px;
    border: 1px solid #e2e8f0;
    transition: all 0.25s ease;
}

.news-item:hover {
    border-color: #c7d2fe;
    box-shadow: 0 6px 20px rgba(99, 102, 241, 0.1);
    transform: translateY(-2px);
}

.news-number {
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 10px;
    font-size: 14px;
    font-weight: 700;
    flex-shrink: 0;
}

.news-content { flex: 1; }

.news-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 8px;
    flex-wrap: wrap;
}

.source-name {
    font-size: 12px;
    font-weight: 600;
    color: #667eea;
}

.rank-num {
    font-size: 11px;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 8px;
    background: #fee2e2;
    color: #dc2626;
}

.time-info, .count-info {
    font-size: 11px;
    color: #94a3b8;
}

.news-title {
    font-size: 14px;
    line-height: 1.6;
}

.news-link {
    color: #1e293b;
    text-decoration: none;
    font-weight: 500;
    transition: color 0.2s;
}

.news-link:hover { color: #667eea; }

/* RSS 区块 */
.section-divider.rss-section {
    margin: 28px 0;
    padding: 0;
    background: linear-gradient(145deg, #f0fdf4 0%, #ecfdf5 100%);
    border-radius: 20px;
    border: 1px solid #d1fae5;
    overflow: hidden;
    box-shadow: 0 4px 16px rgba(16, 185, 129, 0.08);
}

.rss-section-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 20px 28px;
    border-bottom: 1px solid #d1fae5;
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
}

.rss-section-title {
    font-size: 18px;
    font-weight: 700;
    color: white;
}

.rss-section-count {
    font-size: 13px;
    font-weight: 600;
    padding: 5px 14px;
    background: rgba(255, 255, 255, 0.28);
    color: white;
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.35);
}

.feed-group { margin-bottom: 20px; padding: 0 8px; }
.feed-group:first-child { padding-top: 8px; }
.feed-group:last-child { margin-bottom: 8px; }

.feed-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 14px;
    padding-bottom: 10px;
    border-bottom: 2px solid #10b981;
}

.feed-name {
    font-size: 15px;
    font-weight: 700;
    color: #059669;
}

.feed-count {
    font-size: 13px;
    font-weight: 600;
    color: #059669;
}

.rss-item {
    margin-bottom: 12px;
    padding: 16px;
    background: white;
    border-radius: 12px;
    border-left: 4px solid #10b981;
    transition: all 0.25s ease;
}

.rss-item:hover {
    box-shadow: 0 4px 12px rgba(16, 185, 129, 0.12);
    transform: translateX(4px);
}

.rss-item:last-child { margin-bottom: 0; }

.rss-meta {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 10px;
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
    line-height: 1.6;
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
    padding: 28px;
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
    color: #667eea;
    text-decoration: none;
    font-weight: 600;
    transition: color 0.2s;
}

.footer-link:hover {
    color: #764ba2;
}

/* 响应式设计 */
@media (max-width: 640px) {
    body { padding: 12px; }
    
    .header { padding: 32px 24px; }
    .header-title { font-size: 24px; }
    .header-info { grid-template-columns: repeat(2, 1fr); gap: 10px; }
    .info-item { padding: 12px 8px; }
    .info-value { font-size: 15px; }
    
    .content { padding: 0 20px 20px; }
    
    .ai-blocks-container { grid-template-columns: 1fr; }
    .ai-block { border-right: none; padding: 18px 24px; }
    .ai-block:nth-child(2n) { border-right: none; }
    
    .word-group { padding: 20px; }
    .news-item { padding: 14px; }
    
    .feed-group { padding: 0 4px; }
}

/* 动画效果 */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.header { animation: fadeInUp 0.5s ease-out; }
.section-divider.ai-section { animation: fadeInUp 0.5s ease-out 0.1s both; }
.word-group { animation: fadeInUp 0.5s ease-out 0.15s both; }
.section-divider.rss-section { animation: fadeInUp 0.5s ease-out 0.2s both; }
.footer { animation: fadeInUp 0.5s ease-out 0.25s both; }
'''

def beautify_page():
    """美化页面 - 只替换CSS样式，保持内容不变"""
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 只替换<style>标签中的CSS样式
    style_pattern = r'<style>.*?</style>'
    new_style = f'<style>\n{BEAUTIFIED_CSS}\n    </style>'
    content = re.sub(style_pattern, new_style, content, flags=re.DOTALL)
    
    # 写回文件
    with open(INPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ 页面美化完成")
    print("   - CSS样式已优化")
    print("   - 内容保持不变")

if __name__ == "__main__":
    beautify_page()