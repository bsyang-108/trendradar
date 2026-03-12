#!/usr/bin/env python3
"""
TrendRadar 页面样式优化 - 深色主题
- 基于用户提供的图片样式
- 保持所有内容不变
"""

import re

INPUT_FILE = "/var/www/trendradar/index.html"

# 深色主题CSS样式
DARK_THEME_CSS = '''
/* 基础样式 */
* { box-sizing: border-box; }

body {
    font-family: 'Noto Sans SC', -apple-system, BlinkMacSystemFont, 'PingFang SC', sans-serif;
    margin: 0;
    padding: 20px;
    background: #0a0a0f;
    color: #f0f0f5;
    line-height: 1.6;
    min-height: 100vh;
}

/* 容器 */
.container {
    max-width: 680px;
    margin: 0 auto;
    background: #12121a;
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
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
    top: 0; left: 0; right: 0; bottom: 0;
    background: url("data:image/svg+xml,%3Csvg viewBox='0 0 400 400' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='4'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
    opacity: 0.04;
    pointer-events: none;
}

.header-title {
    font-size: 28px;
    font-weight: 800;
    margin: 0 0 28px 0;
    letter-spacing: -0.5px;
    text-shadow: 0 2px 20px rgba(0, 0, 0, 0.2);
}

.header-info {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
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

.save-buttons {
    position: absolute;
    top: 18px; right: 18px;
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
}

.save-btn:hover {
    background: rgba(255, 255, 255, 0.32);
    transform: translateY(-2px);
}

/* 内容区域 */
.content {
    padding: 24px;
}

/* AI 分析区块 */
.section-divider.ai-section {
    margin-top: 0;
    margin-bottom: 32px;
    padding: 0;
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(139, 92, 246, 0.15) 100%);
    border-radius: 16px;
    border: 1px solid rgba(99, 102, 241, 0.3);
    overflow: hidden;
}

.ai-section-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 20px 24px;
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
    gap: 1px;
    background: rgba(99, 102, 241, 0.2);
}

.ai-block {
    padding: 20px 24px;
    background: #1a1a24;
    border: none;
    transition: background 0.25s ease;
}

.ai-block:hover {
    background: #22222e;
}

.ai-block-title {
    font-size: 15px;
    font-weight: 700;
    color: #a5b4fc;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.ai-block-content {
    font-size: 13px;
    line-height: 1.75;
    color: #94a3b8;
}

/* 分割线 */
.section-divider {
    margin-top: 32px;
    padding-top: 24px;
    border-top: 1px solid #2a2a3a;
}

/* 新闻列表 */
.hotlist-section {
    margin-top: 0;
}

.word-group {
    margin-bottom: 40px;
}

.word-group:first-child {
    margin-top: 0;
}

.word-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 18px;
    padding-bottom: 14px;
    border-bottom: 2px solid #2a2a3a;
}

.word-name {
    font-size: 17px;
    font-weight: 700;
    color: #f0f0f5;
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
    color: #64748b;
}

.news-item {
    margin-bottom: 20px;
    padding: 16px 0;
    border-bottom: 1px solid #2a2a3a;
    position: relative;
    display: flex;
    gap: 12px;
    align-items: center;
}

.news-item:last-child {
    margin-bottom: 0;
    border-bottom: none;
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
    color: #a5b4fc;
}

.rank-num {
    font-size: 11px;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 8px;
    background: rgba(239, 68, 68, 0.2);
    color: #f87171;
}

.time-info, .count-info {
    font-size: 11px;
    color: #64748b;
}

.news-title {
    font-size: 14px;
    line-height: 1.6;
}

.news-link {
    color: #f0f0f5;
    text-decoration: none;
    font-weight: 500;
    transition: color 0.2s;
}

.news-link:hover { color: #a5b4fc; }

/* RSS 区块 */
.section-divider.rss-section {
    margin-top: 32px;
    padding: 0;
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(5, 150, 105, 0.1) 100%);
    border-radius: 16px;
    border: 1px solid rgba(16, 185, 129, 0.3);
    overflow: hidden;
    border-top: none;
}

.rss-section-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 20px 24px;
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    border-bottom: 1px solid rgba(16, 185, 129, 0.3);
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

.feed-group { margin-bottom: 20px; padding: 0 24px; }
.feed-group:first-child { padding-top: 20px; }
.feed-group:last-child { margin-bottom: 20px; }

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
    color: #6ee7b7;
}

.feed-count {
    font-size: 13px;
    font-weight: 600;
    color: #6ee7b7;
}

.rss-item {
    margin-bottom: 12px;
    padding: 16px;
    background: rgba(16, 185, 129, 0.05);
    border-radius: 12px;
    border-left: 4px solid #10b981;
    transition: all 0.25s ease;
}

.rss-item:hover {
    background: rgba(16, 185, 129, 0.1);
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
    color: #64748b;
}

.rss-author {
    font-size: 12px;
    font-weight: 600;
    color: #6ee7b7;
}

.rss-title {
    font-size: 14px;
    line-height: 1.6;
}

.rss-link {
    color: #f0f0f5;
    text-decoration: none;
    font-weight: 500;
}

.rss-link:hover {
    color: #6ee7b7;
}

/* Footer */
.footer {
    padding: 28px;
    background: #1a1a24;
    border-top: 1px solid #2a2a3a;
    text-align: center;
}

.footer-content {
    font-size: 13px;
    color: #64748b;
}

.project-name {
    font-weight: 700;
    color: #94a3b8;
}

.footer-link {
    color: #a5b4fc;
    text-decoration: none;
    font-weight: 600;
}

.footer-link:hover {
    color: #c4b5fd;
}

/* 响应式 */
@media (max-width: 640px) {
    body { padding: 12px; }
    .header { padding: 32px 24px; }
    .header-title { font-size: 24px; }
    .header-info { grid-template-columns: repeat(2, 1fr); gap: 10px; }
    .info-item { padding: 12px 8px; }
    .info-value { font-size: 15px; }
    .content { padding: 20px; }
    .ai-blocks-container { grid-template-columns: 1fr; }
    .ai-block { padding: 18px 20px; }
    .feed-group { padding: 0 20px; }
}

/* 动画 */
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

def apply_dark_theme():
    """应用深色主题"""
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 替换CSS样式
    style_pattern = r'<style>.*?</style>'
    new_style = f'<style>\n{DARK_THEME_CSS}\n    </style>'
    content = re.sub(style_pattern, new_style, content, flags=re.DOTALL)
    
    # 写回文件
    with open(INPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ 深色主题已应用")

if __name__ == "__main__":
    apply_dark_theme()