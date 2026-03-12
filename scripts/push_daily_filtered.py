#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TrendRadar 每日推送脚本
- 纯文本格式（适配飞书）
- 只推送 AI技术 或 能源行业AI应用 相关热点
- 总共 5-10 条
"""

import os
import re
import sqlite3
from datetime import datetime
from typing import List, Dict
import requests
import subprocess

# ============ 配置 ============
FEISHU_WEBHOOK_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/5cd1a972-f3d1-45a8-8143-2f9e3c1b488c"
DB_DIR = "/root/trendradar/output"
TOP_N_MIN = 5   # 最少推送条数
TOP_N_MAX = 10  # 最多推送条数

# 修复AI分析标题和顺序
def fix_ai_titles():
    """运行修复脚本"""
    try:
        subprocess.run(["python3", "/root/trendradar/scripts/fix_ai_titles.py"], 
                      check=True, capture_output=True)
        print("✅ AI分析标题已修复")
    except Exception as e:
        print(f"⚠️ 修复AI标题失败: {e}")

# 关键词过滤：AI技术 或 能源行业AI应用
AI_KEYWORDS = [
    # AI技术相关
    "AI", "人工智能", "GPT", "ChatGPT", "Claude", "Gemini", "DeepSeek", "大模型", "LLM",
    "机器学习", "深度学习", "生成式AI", "多模态", "OpenAI", "Anthropic", "智谱", "文心",
    "通义", "Kimi", "AI应用", "智能体", "Agent", "RAG", "向量数据库", "机器人",
    # 能源+AI相关
    "能源AI", "智能电网", "智慧能源", "新能源AI",  "储能AI",
    "能源数字化", "智慧电力", "智能运维",  "智能勘探", 
    "新能源", "数据治理", "智能炼油", "智能化工", "智能制造", 
]


def strip_html_tags(text: str) -> str:
    """移除 HTML 标签，保留文本内容"""
    text = re.sub(r"<font color='[^']*'>([^<]*)</font>", r"\1", text)
    text = re.sub(r"<[^>]+>", "", text)
    return text


def is_ai_related(title: str) -> bool:
    """判断标题是否与AI技术或能源AI相关"""
    title_lower = title.lower()
    for keyword in AI_KEYWORDS:
        if keyword.lower() in title_lower:
            return True
    return False


def query_ai_news(limit_min: int = TOP_N_MIN, limit_max: int = TOP_N_MAX) -> List[Dict]:
    """从数据库查询AI技术/能源AI相关的热点新闻"""
    db_path = os.path.join(DB_DIR, "news", f"{datetime.now().strftime('%Y-%m-%d')}.db")
    if not os.path.exists(db_path):
        print(f"数据库不存在: {db_path}")
        return []
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # 查询所有新闻，按抓取次数排序
    cursor.execute("""
        SELECT 
            title,
            platform_id as source,
            url,
            mobile_url,
            crawl_count as count,
            rank
        FROM news_items
        WHERE crawl_count > 0
        ORDER BY rank ASC, crawl_count DESC
        LIMIT 200
    """)
    
    rows = cursor.fetchall()
    conn.close()
    
    news_items = []
    seen_titles = set()
    
    for row in rows:
        title = strip_html_tags(row["title"])
        
        # 关键词过滤
        if not is_ai_related(title):
            continue
        
        # 去重
        title_key = title[:25].lower()
        if title_key in seen_titles:
            continue
        seen_titles.add(title_key)
        
        # 来源映射
        source_map = {
            "toutiao": "今日头条",
            "baidu": "百度热搜",
            "weibo": "微博",
            "zhihu": "知乎",
            "xinhua": "新华社",
            "people": "人民日报",
            "cctv": "央视新闻",
            "caixin": "财新",
            "reuters": "Reuters",
            "bloomberg": "Bloomberg",
            "wallstreetcn": "华尔街见闻",
            "china_energy_news": "中国能源报",
            "china_petroleum_news": "中国石油报",
            "china_chemical_news": "中国化工报",
            "scitech_daily": "科技日报",
            "thepaper": "澎湃新闻",
            "jiemian": "界面新闻",
            "yicai": "第一财经",
            "36kr": "36氪",
            "jiqizhixin": "机器之心",
            "liangziwei": "量子位",
            "aitechreview": "AI科技评论",
            "energymagazine": "能源杂志",
        }
        
        news_items.append({
            "title": title,
            "source": source_map.get(row["source"], row["source"] or "未知"),
            "url": row["mobile_url"] or row["url"] or "",
            "count": row["count"],
            "rank": row["rank"] or 0,
        })
        
        if len(news_items) >= limit_max:
            break
    
    # 如果匹配数量不足最少条数，也返回已找到的
    return news_items[:limit_max]


def query_ai_rss(limit: int = 5) -> List[Dict]:
    """从RSS数据库查询AI相关条目"""
    db_path = os.path.join(DB_DIR, "rss", f"{datetime.now().strftime('%Y-%m-%d')}.db")
    if not os.path.exists(db_path):
        return []
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT r.title, r.url, r.crawl_count, f.name as feed_name
        FROM rss_items r
        LEFT JOIN rss_feeds f ON r.feed_id = f.id
        ORDER BY r.crawl_count DESC
        LIMIT 50
    """)
    
    rows = cursor.fetchall()
    conn.close()
    
    rss_items = []
    for row in rows:
        title = strip_html_tags(row["title"])
        if is_ai_related(title):
            rss_items.append({
                "title": title,
                "source": row["feed_name"] or "Hacker News",
                "url": row["url"] or "",
            })
            if len(rss_items) >= limit:
                break
    
    return rss_items


def format_daily_report(news_items: List[Dict]) -> str:
    """格式化每日报告"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    lines = [
        f"📰 AI技术热点日报 - {today} \n",
    ]
    
    for i, item in enumerate(news_items, 1):
        lines.append(f"【{i}】{item['title']}")
        lines.append(f"    来源: {item['source']}")
        if item.get('url'):
            lines.append(f"    链接: {item['url']}")
        lines.append("")
    
    lines.append("━" * 20)
    lines.append(f"更新: {datetime.now().strftime('%H:%M')}")
    
    return "\n".join(lines)


def send_to_feishu(message: str) -> bool:
    """发送消息到飞书"""
    payload = {
        "msg_type": "text",
        "content": {"text": message}
    }
    
    try:
        response = requests.post(FEISHU_WEBHOOK_URL, json=payload, timeout=30)
        result = response.json()
        if result.get("code") == 0 or result.get("StatusCode") == 0:
            print("✅ 推送成功")
            return True
        print(f"❌ 推送失败: {result}")
        return False
    except Exception as e:
        print(f"❌ 推送异常: {e}")
        return False


def main():
    print("=" * 40)
    print("AI技术热点推送")
    print(datetime.now().strftime("%Y-%m-%d %H:%M"))
    print("=" * 40)
    
    # 先修复AI分析标题和顺序
    fix_ai_titles()
    
    # 查询AI相关热点
    print(f"\n筛选AI/能源相关热点...")
    news_items = query_ai_news()
    print(f"找到 {len(news_items)} 条")
    
    # RSS补充
    rss_items = query_ai_rss(3)
    print(f"RSS补充 {len(rss_items)} 条")
    
    # 合并，总数控制在10条内
    all_items = news_items[:8] + rss_items[:2]
    all_items = all_items[:10]
    
    if not all_items:
        print("\n没有相关热点，跳过推送")
        return
    
    # 推送
    report = format_daily_report(all_items)
    print(f"\n推送 {len(all_items)} 条...")
    send_to_feishu(report)
    
    print("\n" + "=" * 40)


if __name__ == "__main__":
    main()
