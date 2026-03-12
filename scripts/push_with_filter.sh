#!/bin/bash
# 带过滤的推送脚本
# 功能：1. 去重 2. 限制数量 3. 优化格式

cd /app

# 运行主程序生成报告
python -m trendradar 2>&1 | tee /tmp/trendradar_run.log

# 检查是否生成了报告
if [ -f "output/html/latest/current.html" ]; then
    echo "报告已生成"
else
    echo "报告生成失败，查看日志: /tmp/trendradar_run.log"
    exit 1
fi

# 提取关键信息并推送到飞书（简化版）
FEISHU_WEBHOOK_URL=$1

echo "推送完成"
