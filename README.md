# Personal-AI-OS

<div align="center">

**企业级 AI 智能体工作空间 | Enterprise-Grade AI Agent Workspace**

基于 OpenClaw 框架，集成飞书生态、自进化技能系统与认知模型架构

Built on OpenClaw Framework, integrating Feishu ecosystem, self-evolving skill system, and cognitive model architecture

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![OpenClaw](https://img.shields.io/badge/powered%20by-OpenClaw-ff69b4.svg)](https://github.com/openclaw/openclaw)

</div>

---

## 📖 项目介绍 | About

### 中文

**Personal-AI-OS** 是一个基于 **OpenClaw 框架** 的企业级 AI 智能体工作空间。它不仅仅是一个代码仓库，更是一个完整的 AI 操作系统，能够：

-  **认知记忆** - 通过 MemoryPalace 实现长期记忆存储与智能检索
- 🔌 **技能自进化** - 支持动态加载、更新和优化 AI 技能模块
- 📱 **飞书集成** - 深度整合飞书 IM、日历、任务、多维表格、云文档
- 🤖 **多智能体协作** - 支持子智能体生成、任务委派和结果聚合
- 📊 **GitHub 监控** - 自动追踪热门仓库和技术趋势

本项目适用于企业知识库管理、个人 AI 助手、智能工作流自动化等场景。

### English

**Personal-AI-OS** is an enterprise-grade AI agent workspace built on the **OpenClaw Framework**. It's not just a code repository, but a complete AI operating system that enables:

- 🧠 **Cognitive Memory** - Long-term memory storage and intelligent retrieval via MemoryPalace
- 🔌 **Self-Evolving Skills** - Dynamic loading, updating, and optimization of AI skill modules
- 📱 **Feishu Integration** - Deep integration with Feishu IM, Calendar, Tasks, Bitable, and Cloud Docs
- 🤖 **Multi-Agent Collaboration** - Sub-agent spawning, task delegation, and result aggregation
- 📊 **GitHub Monitoring** - Automatic tracking of trending repositories and tech trends

This project is suitable for enterprise knowledge management, personal AI assistants, and intelligent workflow automation.

---

## ✨ 核心特性 | Core Features

| 特性 Feature | 描述 Description |
|-------------|-----------------|
| 🧠 MemoryPalace | 记忆宫殿系统，支持对话挖掘、实体识别、知识图谱 |
| 🔌 技能系统 | 自进化技能框架，支持动态扩展和热更新 |
| 📱 飞书生态 | 完整的飞书 API 集成（IM/日历/任务/多维表格/文档） |
| 🤖 智能体编排 | 子智能体生成、任务委派、结果聚合 |
| 📊 GitHub 监控 | 自动追踪 GitHub 热点仓库，定时推送通知 |
| 🔄 持续学习 | 从交互中学习，持续优化响应策略 |

---

## 🚀 快速开始 | Quick Start

### 1. 克隆项目 | Clone Repository

```bash
# 首次克隆 | First-time clone
git clone git@github.com:AUrlius/Personal-AI-OS.git
cd Personal-AI-OS
```

### 2. 拉取更新 | Pull Updates

```bash
# 如果已有本地仓库 | If you already have a local repository
git pull origin main
git submodule update --init --recursive
```

### 3. 快捷更新脚本 | Quick Update Script

创建 `update.sh` 脚本（推荐）| Create `update.sh` script (recommended):

```bash
#!/bin/bash
git pull origin main
git submodule update --init --recursive
echo "✅ 更新完成 | Update complete"
```

使用方法 | Usage:
```bash
chmod +x update.sh
./update.sh
```

### 4. Git 别名配置 | Git Alias Configuration

配置全局别名 | Configure global aliases:

```bash
git config --global alias.up 'pull origin main'
git config --global alias.sync '!git pull origin main && git submodule update --init --recursive'
```

之后使用 | Then use:
```bash
git up      # 快速拉取 | Quick pull
git sync    # 完整同步 | Full sync
```

---

## 📁 项目结构 | Project Structure

```
Personal-AI-OS/
├── analysis/           # 分析脚本与工具 | Analysis scripts and tools
├── docs/              # 文档 | Documentation
├── examples/          # 示例 | Examples
├── integration/       # 集成模块（子模块）| Integration modules (submodule)
│   ├── mempalace/    # MemoryPalace 记忆宫殿系统
│   ├── hermes-agent-orange-book/  # Hermes Agent 橙皮书
│   └── ...           # 其他集成项目 | Other integration projects
├── src/              # 源代码 | Source code
├── README.md         # 项目说明 | Project overview
└── requirements.txt  # 依赖 | Dependencies
```

---

## 🛠️ 环境要求 | Requirements

- **Node.js** v22+ (OpenClaw 运行时 | OpenClaw runtime)
- **Python** 3.10+ (技能模块 | Skill modules)
- **Git** (子模块支持 | Submodule support)
- **飞书开放平台账号** | Feishu Open Platform account

---

## 📧 联系方式 | Contact

| 方式 Method | 信息 Info |
|------------|----------|
| 📧 Email | hrr1225@163.com |
| 🐦 X/Twitter | [@YLan1410549509](https://twitter.com/YLan1410549509) |
| 💼 GitHub | [@AUrlius](https://github.com/AUrlius) |

---

## 📄 许可证 | License

MIT License - 详见 [LICENSE](LICENSE) 文件 | See [LICENSE](LICENSE) file

---

<div align="center">

**Made with ❤️ by AUrlius**

⭐ 如果这个项目对你有帮助，请给一个 Star！| If this project helps you, please give a Star!

</div>
