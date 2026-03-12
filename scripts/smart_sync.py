#!/usr/bin/env python3
"""
TrendRadar 智能同步脚本
从 Docker 报告提取数据，注入到 nginx 首页的结构中
保持 nginx 首页的样式和布局不变
"""

import re
import sys
from pathlib import Path

NGINX_INDEX = Path("/var/www/trendradar/index.html")
DOCKER_LATEST = Path("/root/trendradar/output/html/latest/daily.html")

def extract_docker_data(html_content: str) -> dict:
    """从 Docker 报告提取关键数据"""
    data = {}
    
    # 提取统计数据（顺序：报告类型、新闻总数、热点新闻、生成时间）
    stats_match = re.findall(r'<span class="info-value">([^<]+)</span>', html_content)
    if len(stats_match) >= 4:
        # stats_match[0] = 报告类型（全天汇总）
        # stats_match[1] = 新闻总数（476 条）
        # stats_match[2] = 热点新闻（22 条）
        # stats_match[3] = 生成时间（03-08 10:49）
        data['news_total'] = stats_match[1]  # 新闻总数
        data['hot_count'] = stats_match[2]   # 热点新闻
        data['gen_time'] = stats_match[3]    # 生成时间
    
    # 提取 AI 分析内容
    ai_blocks = {}
    patterns = {
        'core_trends': r'<div class="ai-block-title">核心热点态势</div>\s*<div class="ai-block-content">([^<]+)</div>',
        'signals': r'<div class="ai-block-title">异动与弱信号</div>\s*<div class="ai-block-content">([^<]+)</div>',
        'outlook_strategy': r'<div class="ai-block-title">研判策略建议</div>\s*<div class="ai-block-content">([^<]+)</div>',
        'rss_insights': r'<div class="ai-block-title">RSS 深度洞察</div>\s*<div class="ai-block-content">([^<]+)</div>',
    }
    
    # 也尝试匹配 nginx 首页的标题格式
    nginx_patterns = {
        'core_content': r'<div class="ai-block-title">📊 核心内容</div>\s*<div class="ai-block-content">([^<]+)</div>',
        'key_dynamics': r'<div class="ai-block-title">🏢 关键动态</div>\s*<div class="ai-block-content">([^<]+)</div>',
        'policy_risk': r'<div class="ai-block-title">⚠️ 政策风险</div>\s*<div class="ai-block-content">([^<]+)</div>',
        'tech_app': r'<div class="ai-block-title">💡 技术应用</div>\s*<div class="ai-block-content">([^<]+)</div>',
    }
    
    for key, pattern in patterns.items():
        match = re.search(pattern, html_content)
        if match:
            ai_blocks[key] = match.group(1)
    
    for key, pattern in nginx_patterns.items():
        match = re.search(pattern, html_content)
        if match:
            ai_blocks[key] = match.group(1)
    
    if ai_blocks:
        data['ai_blocks'] = ai_blocks
    
    return data

def update_nginx_index(nginx_html: str, docker_data: dict) -> str:
    """更新 nginx 首页的数据"""
    html = nginx_html
    
    # 找到所有带"条"的 span，一次性替换
    # nginx 首页顺序：新闻总数、热点新闻
    # Docker 数据顺序：news_total、hot_count
    
    matches = list(re.finditer(r'(<span class="info-value">)(\d+ 条)(</span>)', html))
    
    if len(matches) >= 2 and 'news_total' in docker_data and 'hot_count' in docker_data:
        # 从后往前替换，避免位置偏移
        # 第二个匹配是热点新闻
        start2, end2 = matches[1].span()
        html = html[:start2] + f'<span class="info-value">{docker_data["hot_count"]}</span>' + html[end2:]
        
        # 重新查找第一个匹配的位置（因为内容长度可能变化）
        matches = list(re.finditer(r'(<span class="info-value">)(\d+ 条)(</span>)', html))
        start1, end1 = matches[0].span()
        html = html[:start1] + f'<span class="info-value">{docker_data["news_total"]}</span>' + html[end1:]
    
    # 更新生成时间
    if 'gen_time' in docker_data:
        html = re.sub(
            r'(<span class="info-value">)\d{2}-\d{2} \d{2}:\d{2}(</span>)',
            f'\\g<1>{docker_data["gen_time"]}\\g<2>',
            html
        )
    
    # 更新 AI 分析内容
    if 'ai_blocks' in docker_data:
        ai = docker_data['ai_blocks']
        
        # 更新核心内容
        if 'core_content' in ai or 'core_trends' in ai:
            content = ai.get('core_content') or ai.get('core_trends', '')
            html = re.sub(
                r'(<div class="ai-block-title">📊 核心内容</div>\s*<div class="ai-block-content">)[^<]*(</div>)',
                f'\\g<1>{content}\\g<2>',
                html
            )
        
        # 更新关键动态
        if 'key_dynamics' in ai or 'signals' in ai:
            content = ai.get('key_dynamics') or ai.get('signals', '')
            html = re.sub(
                r'(<div class="ai-block-title">🏢 关键动态</div>\s*<div class="ai-block-content">)[^<]*(</div>)',
                f'\\g<1>{content}\\g<2>',
                html
            )
        
        # 更新政策风险
        if 'policy_risk' in ai or 'outlook_strategy' in ai:
            content = ai.get('policy_risk') or ai.get('outlook_strategy', '')
            html = re.sub(
                r'(<div class="ai-block-title">⚠️ 政策风险</div>\s*<div class="ai-block-content">)[^<]*(</div>)',
                f'\\g<1>{content}\\g<2>',
                html
            )
        
        # 更新技术应用
        if 'tech_app' in ai or 'rss_insights' in ai:
            content = ai.get('tech_app') or ai.get('rss_insights', '')
            html = re.sub(
                r'(<div class="ai-block-title">💡 技术应用</div>\s*<div class="ai-block-content">)[^<]*(</div>)',
                f'\\g<1>{content}\\g<2>',
                html
            )
    
    return html

def main():
    # 检查文件
    if not DOCKER_LATEST.exists():
        print("❌ Docker 最新报告不存在")
        sys.exit(1)
    
    if not NGINX_INDEX.exists():
        print("❌ nginx 首页不存在")
        sys.exit(1)
    
    # 读取文件
    docker_html = DOCKER_LATEST.read_text(encoding='utf-8')
    nginx_html = NGINX_INDEX.read_text(encoding='utf-8')
    
    # 检查 Docker 报告是否有 AI 分析
    if 'AI 热点分析' not in docker_html and 'ai-section' not in docker_html:
        print("⚠️ Docker 报告缺少 AI 分析，跳过同步")
        sys.exit(0)
    
    # 提取数据
    docker_data = extract_docker_data(docker_html)
    
    if not docker_data:
        print("⚠️ 无法从 Docker 报告提取数据")
        sys.exit(0)
    
    print(f"Docker 数据: {docker_data}")
    
    # 更新 nginx 首页
    updated_html = update_nginx_index(nginx_html, docker_data)
    
    # 备份并保存
    NGINX_INDEX.rename(str(NGINX_INDEX) + '.bak')
    NGINX_INDEX.write_text(updated_html, encoding='utf-8')
    
    print("✅ 已更新 nginx 首页数据（保持原有样式）")

if __name__ == "__main__":
    main()