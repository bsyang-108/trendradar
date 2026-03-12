#!/bin/bash
# TrendRadar 智能同步脚本
# 只更新数据，不改变页面结构和样式

NGINX_INDEX="/var/www/trendradar/index.html"
DOCKER_LATEST="/root/trendradar/output/html/latest/daily.html"

# 检查文件是否存在
if [ ! -f "$DOCKER_LATEST" ]; then
    echo "❌ Docker 最新报告不存在"
    exit 1
fi

# 检查 Docker 报告是否包含 AI 分析
if ! grep -q "ai-section-title\|AI 热点分析" "$DOCKER_LATEST"; then
    echo "⚠️ Docker 报告缺少 AI 分析，跳过同步"
    exit 0
fi

# 创建临时文件
TMP_FILE=$(mktemp)

# 1. 提取 nginx 首页的完整样式（<style> 到 </style>）
# 2. 提取 Docker 报告的数据部分
# 3. 组合成新页面

# 提取 Docker 报告中的统计数据
NEWS_TOTAL=$(grep -oP '(?<=<span class="info-value">)\d+ 条(?=</span>)' "$DOCKER_LATEST" | head -1 | sed 's/ 条//')
HOT_COUNT=$(grep -oP '(?<=<span class="info-value">)\d+ 条(?=</span>)' "$DOCKER_LATEST" | sed -n '2p' | sed 's/ 条//')
GEN_TIME=$(grep -oP '(?<=<span class="info-value">)[^<]+(?=</span>)' "$DOCKER_LATEST" | sed -n '4p')

echo "Docker 数据: 总数=$NEWS_TOTAL, 热点=$HOT_COUNT, 时间=$GEN_TIME"

# 提取 Docker 报告中的 AI 分析内容
AI_CONTENT=$(sed -n '/<div class="ai-section-title">/,/<\/div>.*<\/div>.*<\/div>/p' "$DOCKER_LATEST" | head -50)

if [ -z "$AI_CONTENT" ]; then
    echo "⚠️ 无法提取 AI 分析内容"
    exit 0
fi

# 更新 nginx 首页
cp "$NGINX_INDEX" "${NGINX_INDEX}.bak"

# 更新统计数据
sed -i "s/<span class=\"info-value\">[0-9]* 条<\/span>/<span class=\"info-value\">${NEWS_TOTAL} 条<\/span>/1" "$NGINX_INDEX"
sed -i "s/<span class=\"info-value\">[0-9]* 条<\/span>/<span class=\"info-value\">${HOT_COUNT} 条<\/span>/2" "$NGINX_INDEX"

# 更新生成时间
sed -i "s/<span class=\"info-value\">[0-9-]* [0-9:]*/<span class=\"info-value\">${GEN_TIME}/" "$NGINX_INDEX"

echo "✅ 已更新 nginx 首页数据"