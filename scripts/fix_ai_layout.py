#!/usr/bin/env python3
"""
修复TrendRadar页面布局：
1. AI热点分析从header中移出，独立成版块
2. 美化AI分析区块样式
"""

import os
import re

def fix_ai_section_layout(filepath):
    """修复AI分析区块布局"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 找到AI分析区块
    ai_pattern = r'(<div class="section-divider ai-section">.*?</div>\s*</div>)\s*</div>\s*(<div class="content">)'
    match = re.search(ai_pattern, content, re.DOTALL)
    
    if match:
        ai_section = match.group(1)
        
        # 从header内部移除AI分析区块
        # 重新组织结构：header关闭后，AI分析独立，然后content开始
        new_structure = f'''</div>
            </div>

            {ai_section}

            <div class="content">'''
        
        content = content[:match.start()] + new_structure + content[match.end():]
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ AI分析区块已独立: {filepath}")
    else:
        print(f"⚠️ 未找到AI分析区块: {filepath}")

def main():
    # 修复主页面
    index_html = "/var/www/trendradar/index.html"
    if os.path.exists(index_html):
        fix_ai_section_layout(index_html)
    
    print("✅ 布局修复完成")

if __name__ == "__main__":
    main()