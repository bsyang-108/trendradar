# TrendRadar - 趋势雷达

> 自动化新闻追踪与 AI 分析系统

[![Status](https://img.shields.io/badge/status-running-success)](https://github.com/bsyang-108/trendradar)
[![Last Update](https://img.shields.io/badge/last%20update-2026--03--12-blue)](https://github.com/bsyang-108/trendradar/commits/main)

## 📋 项目简介

TrendRadar 是一个自动化的新闻追踪系统，能够：

- 📰 **多源抓取**：监控 11+ 个新闻平台（今日头条、百度、微博、知乎等）
- 🤖 **AI 分析**：使用 Kimi K2 自动生成新闻摘要
- 🔄 **智能去重**：基于相似度算法自动去重
- 📊 **数量控制**：每组关键词最多 2 条，总计最多 8 条
- 📤 **定时推送**：每天 12:00（北京时间）自动推送到飞书

## 🚀 快速开始

### Docker 部署

```bash
# 克隆项目
git clone https://github.com/bsyang-108/trendradar.git
cd trendradar

# 启动服务
docker-compose up -d
```

### 配置文件

主要配置文件位于 `config/` 目录：

- `config.yaml` - 主配置文件
- `timeline.yaml` - 定时任务配置
- `frequency_words.txt` - 关键词列表
- `ai_analysis_prompt.txt` - AI 分析提示词
- `report_template.md` - 报告模板

## 📁 项目结构

```
trendradar/
├── config/              # 配置文件
│   ├── config.yaml
│   ├── timeline.yaml
│   ├── frequency_words.txt
│   └── ai_analysis_prompt.txt
├── scripts/             # 工具脚本
│   ├── push_daily_filtered.py
│   ├── smart_sync.py
│   └── beautify_page.py
├── docker/              # Docker 配置
│   └── docker-compose.yml
├── custom/              # 自定义文件
└── output/              # 输出目录（运行时生成）
    ├── html/           # HTML 报告
    ├── txt/            # 文本报告
    └── news/           # 新闻数据库
```

## ⚙️ 核心功能

### AI 分析
- **模型**: moonshot/kimi-k2-thinking-turbo
- **功能**: 自动生成 30-50 字新闻摘要
- **提示词**: 可自定义 `config/ai_analysis_prompt.txt`

### 新闻去重
- **算法**: SequenceMatcher 相似度计算
- **阈值**: 0.7（可配置）
- **应用**: 推送前自动执行

### 推送配置
- **渠道**: 飞书机器人
- **时间**: 每天 12:00（北京时间）
- **格式**: Markdown 优化

## 📊 监控平台

已配置的新闻源：

- 今日头条
- 百度热搜
- 微博热搜
- 知乎热榜
- 新浪财经
- 36Kr
- 虎嗅
- 界面新闻
- 澎湃新闻
- 中国青年报
- 新华网
- Hacker News (RSS)
- 阮一峰博客 (RSS)

## 🔧 脚本工具

### 推送脚本
```bash
# 手动推送
python3 scripts/push_daily_filtered.py
```

### 页面美化
```bash
# 优化 HTML 报告
python3 scripts/beautify_page.py
```

### 智能同步
```bash
# 同步到 Nginx
./scripts/sync_to_nginx.sh
```

## 📝 日志查看

```bash
# 查看推送日志
tail -f output/push.log

# 查看定时任务日志
tail -f output/cron.log

# 查看 Docker 日志
docker logs trendradar --tail 50
```

## 🛠️ 手动测试

```bash
# 手动执行一次完整流程
docker exec -e TZ=Asia/Shanghai -w /app trendradar python -m trendradar

# 检查配置
docker exec trendradar env | grep AI
```

## 📅 定时任务

系统使用 Cron 定时任务：

```cron
# 每天 UTC 4:00 (北京时间 12:00)
0 4 * * * cd /app && python -m trendradar
```

## 🔐 安全提示

- ⚠️ 不要提交 `.env` 文件到公开仓库
- ⚠️ API Key 请使用 GitHub Secrets 管理
- ⚠️ 生产环境建议使用私有仓库

## 📈 运行状态

查看当前运行状态：

```bash
docker ps | grep trendradar
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 📞 联系方式

- GitHub: [@bsyang-108](https://github.com/bsyang-108)
- Email: yangbingshu108@gmail.com

---

**最后更新**: 2026-03-12  
**版本**: v1.0  
**提交**: [6397da6](https://github.com/bsyang-108/trendradar/commit/6397da666f6879e08e2ef70de3143c821b6f49c0)
