#!/bin/bash
# TrendRadar 智能同步脚本
# 只有当新报告包含 AI 分析区块时，才更新 nginx 首页

LATEST_DAILY="/root/trendradar/output/html/latest/daily.html"
NGINX_INDEX="/var/www/trendradar/index.html"

# 检查最新报告是否存在
if [ ! -f "$LATEST_DAILY" ]; then
    echo "❌ 最新报告不存在: $LATEST_DAILY"
    exit 1
fi

# 检查是否包含 AI 分析区块
if grep -q "ai-section\|AI 热点分析\|核心热点态势" "$LATEST_DAILY"; then
    # 检查内容是否有实际文字（不是空的 AI 区块）
    AI_CONTENT=$(grep -oP '(?<=<div class="ai-block-content">)[^<]+' "$LATEST_DAILY" | head -1)
    if [ -n "$AI_CONTENT" ] && [ ${#AI_CONTENT} -gt 20 ]; then
        cp "$LATEST_DAILY" "$NGINX_INDEX"
        echo "✅ 已同步最新报告到 nginx 首页 (含 AI 分析)"
        
        # 更新时间戳
        TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
        echo "[$TIMESTAMP] 同步成功" >> /root/trendradar/output/sync.log
    else
        echo "⚠️ AI 分析区块为空，跳过同步"
    fi
else
    echo "⚠️ 最新报告缺少 AI 分析区块，跳过同步"
    
    # 记录跳过原因
    TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
    echo "[$TIMESTAMP] 跳过同步（无 AI 分析）" >> /root/trendradar/output/sync.log
fi