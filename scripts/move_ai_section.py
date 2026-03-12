#!/usr/bin/env python3
"""
移动AI分析区块到标题下面
"""

import re

INPUT_FILE = "/var/www/trendradar/index.html"

# 读取文件
with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    content = f.read()

# 找到AI分析区块
ai_pattern = r'(<div class="section-divider ai-section">.*?</div>\s*</div>)\s*</div>\s*(<div class="footer">)'
ai_match = re.search(ai_pattern, content, re.DOTALL)

if not ai_match:
    print("❌ 未找到AI分析区块")
    exit(1)

ai_section = ai_match.group(1)
print(f"✅ 找到AI分析区块，长度: {len(ai_section)} 字符")

# 从原位置删除AI分析区块
content = content[:ai_match.start()] + "            </div>\n\n            " + ai_match.group(2)

# 找到header-info结束的位置
header_pattern = r'(</div>\s*</div>\s*</div>\s*<div class="content">)'
header_match = re.search(header_pattern, content)

if not header_match:
    print("❌ 未找到header结束位置")
    exit(1)

# 在header之后插入AI分析区块
insert_pos = header_match.start() + len('</div>\s*</div>\s*</div>')
content = content[:insert_pos] + "\n            " + ai_section + "\n            " + content[insert_pos:]

# 写回文件
with open(INPUT_FILE, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ AI分析区块已移动到标题下面")