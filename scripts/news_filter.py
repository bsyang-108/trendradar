#!/usr/bin/env python3
"""
新闻过滤脚本
功能：1. 去重（基于标题相似度） 2. 限制数量（Top N）
"""

import sys
from difflib import SequenceMatcher
from collections import defaultdict

# 配置
SIMILARITY_THRESHOLD = 0.7  # 相似度阈值
MAX_NEWS_PER_GROUP = 2      # 每个关键词组最多新闻数
MAX_TOTAL_NEWS = 8          # 总新闻数上限

def calculate_similarity(str1, str2):
    """计算两个字符串的相似度"""
    return SequenceMatcher(None, str1, str2).ratio()

def remove_duplicates(news_list):
    """基于标题相似度去重"""
    if not news_list:
        return []
    
    # 按关键词分组
    groups = defaultdict(list)
    for news in news_list:
        keyword = news.get('keyword', '未知')
        groups[keyword].append(news)
    
    result = []
    for keyword, items in groups.items():
        # 按热度排序（假设有heat_score字段）
        items_sorted = sorted(items, 
                            key=lambda x: x.get('heat_score', 0), 
                            reverse=True)
        
        # 去重并限制数量
        unique_items = []
        for item in items_sorted:
            # 检查是否与已选项目重复
            is_duplicate = False
            for selected in unique_items:
                if calculate_similarity(
                    item.get('title', ''),
                    selected.get('title', '')
                ) > SIMILARITY_THRESHOLD:
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                unique_items.append(item)
                if len(unique_items) >= MAX_NEWS_PER_GROUP:
                    break
        
        result.extend(unique_items)
    
    # 全局按热度排序并限制总数
    result_sorted = sorted(result, 
                          key=lambda x: x.get('heat_score', 0), 
                          reverse=True)
    
    return result_sorted[:MAX_TOTAL_NEWS]

def test_filter():
    """测试过滤功能"""
    test_news = [
        {'keyword': '华为', 'title': '华为发布新手机', 'heat_score': 95},
        {'keyword': '华为', 'title': '华为发布新款智能手机', 'heat_score': 90},
        {'keyword': '华为', 'title': '华为5G技术突破', 'heat_score': 85},
        {'keyword': 'AI', 'title': 'AI技术最新进展', 'heat_score': 88},
        {'keyword': 'AI', 'title': '人工智能新突破', 'heat_score': 92},
        {'keyword': 'AI', 'title': 'AI应用广泛扩展', 'heat_score': 80},
        {'keyword': '比亚迪', 'title': '比亚迪销量创新高', 'heat_score': 87},
        {'keyword': '特斯拉', 'title': '特斯拉降价促销', 'heat_score': 89},
    ]
    
    filtered = remove_duplicates(test_news)
    print(f"原始新闻数: {len(test_news)}")
    print(f"过滤后新闻数: {len(filtered)}")
    
    for news in filtered:
        print(f"- {news['keyword']}: {news['title']} (热度: {news['heat_score']})")

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        test_filter()
    else:
        print("用法: python3 news_filter.py test")
