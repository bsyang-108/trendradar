#!/usr/bin/env python3
"""
修复TrendRadar生成的HTML：
1. 替换AI分析标题
2. 修复HTML结构（四个块并列）
3. 将AI热点分析移到标题下面、新闻列表上面
"""

import os
import re

def fix_html_structure(html_content):
    """修复AI分析区块的HTML结构并调整位置"""
    
    # 标题映射
    title_mapping = {
        "核心热点态势": "📊 AI核心内容",
        "异动与弱信号": "🏢 技术公司动态",
        "RSS 深度洞察": "💡 中东热点关注",
        "研判策略建议": "⚠️ 政策风险"
    }
    
    # 替换标题
    for old_title, new_title in title_mapping.items():
        pattern = f'<div class="ai-block-title">{old_title}</div>'
        replacement = f'<div class="ai-block-title">{new_title}</div>'
        html_content = html_content.replace(pattern, replacement)
    
    # 提取AI分析区块（从原位置）
    ai_pattern = r'<div class="section-divider ai-section">.*?</div>\s*</div>\s*(?=<div class="footer">)'
    ai_match = re.search(ai_pattern, html_content, re.DOTALL)
    
    if not ai_match:
        print("⚠️ 未找到AI分析区块")
        return html_content
    
    ai_section_html = ai_match.group(0)
    
    # 修复AI分析区块内部结构（四个块并列）
    # 提取每个ai-block的内容
    block_pattern = r'<div class="ai-block">\s*<div class="ai-block-title">(.*?)</div>\s*<div class="ai-block-content">(.*?)</div>'
    blocks = re.findall(block_pattern, ai_section_html, re.DOTALL)
    
    if len(blocks) >= 4:
        # 按用户要求的顺序重新排列
        desired_order = ["📊 AI核心内容", "🏢 技术公司动态", "⚠️ 政策风险", "💡 中东热点关注"]
        
        # 创建标题到内容的映射
        block_map = {}
        for title, content in blocks:
            block_map[title] = content.strip()
        
        # 重新生成正确的HTML结构（四个块并列）
        new_blocks_html = ""
        for title in desired_order:
            if title in block_map:
                new_blocks_html += f'''
                    <div class="ai-block">
                        <div class="ai-block-title">{title}</div>
                        <div class="ai-block-content">{block_map[title]}</div>
                    </div>'''
        
        # 生成完整的AI分析区块HTML
        new_ai_section = f'''<div class="section-divider ai-section">
                    <div class="ai-section-header">
                        <div class="ai-section-title">✨ AI 热点分析</div>
                        <span class="ai-section-badge">AI</span>
                    </div>
                    {new_blocks_html}
                </div>'''
    else:
        new_ai_section = ai_section_html
    
    # 从原位置删除AI分析区块
    html_content = html_content[:ai_match.start()] + html_content[ai_match.end():]
    
    # 找到header结束位置（</header>或header-info之后的</div>）
    # 在</header>之后、<div class="content">之前插入AI分析区块
    header_end_pattern = r'(</div>\s*</div>\s*)(<div class="content">)'
    header_match = re.search(header_end_pattern, html_content)
    
    if header_match:
        # 在header结束后、content开始前插入AI分析区块
        insert_pos = header_match.start() + len('</div>\s*</div>\s*')
        html_content = html_content[:insert_pos] + "\n            " + new_ai_section + "\n            " + html_content[insert_pos:]
        print("✅ AI分析区块已移到正确位置")
    else:
        print("⚠️ 未找到插入位置")
    
    return html_content

def process_html_file(filepath):
    """处理单个HTML文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    fixed_content = fix_html_structure(content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    
    print(f"✅ 已修复: {filepath}")

def main():
    # 修复主页面
    index_html = "/root/trendradar/output/index.html"
    if os.path.exists(index_html):
        process_html_file(index_html)
    
    # 修复今天的HTML文件
    from datetime import datetime
    today = datetime.now().strftime('%Y-%m-%d')
    html_dir = f"/root/trendradar/output/html/{today}"
    
    if os.path.exists(html_dir):
        for filename in os.listdir(html_dir):
            if filename.endswith('.html'):
                filepath = os.path.join(html_dir, filename)
                process_html_file(filepath)
    
    # 同步到自定义页面
    custom_page = "/var/www/trendradar/index.html"
    if os.path.exists(index_html):
        import shutil
        shutil.copy(index_html, custom_page)
        print(f"✅ 已同步到: {custom_page}")

if __name__ == "__main__":
    main()
