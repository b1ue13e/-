---
type: index
topic: "个人知识库核心仓库"
created: 2026-04-29
updated: 2026-11-09
status: active
tags: [说明, Git, Obsidian]
---

# 个人知识库核心仓库

[English](README.md) · [远程仓库](https://github.com/b1ue13e/-)

这是以 Obsidian 为界面的 Markdown 知识库，保存课程学习路径、概念笔记、论文与书籍阅读、作业项目和复习材料。它不是需要构建或启动服务的软件项目。

## 从哪里开始

将克隆得到的仓库目录作为 Obsidian 仓库打开，从 [[🏠 主页]] 和 [[📋 使用说明]] 进入。GitHub 可以阅读 Markdown 正文；Dataview 查询和 Templater 模板需要在 Obsidian 中配合相应插件使用。

| 目录 | 用途 |
| --- | --- |
| `00-Inbox/` | 临时捕捉与待分流材料 |
| `01-Active Sprint/` | 当前主攻任务与执行导航 |
| `02-Knowledge/` | 课程学习路径、知识卡和可复用知识 |
| `03-Projects/` | 作业、实验、项目与报告 |
| `04-Review/` | 复习材料与薄弱点回收 |
| `99-System/` | 模板、工具和知识库维护 |

书库、论文库和阅读笔记沿用现有资源索引，本说明不另建一套课程、知识卡与作业关系表。

## 日常维护

完整规则见根目录 [AGENTS.md](AGENTS.md)，包括 Frontmatter、双链、学习路径、文件位置和 Git 操作。保留中文与 Emoji 文件名、已有元数据及关系的唯一事实源；大型本地资源和工作区状态按 `.gitignore` 处理。

核对后只暂存本次修改的具体路径：

```sh
git add README.md README.zh-CN.md
git diff --cached --stat
git commit -m "docs: update vault navigation"
git push origin main
```

远程默认分支为 `main`，本地工作分支可能不同。本次说明整理不移动或改写知识卡、作业和资源文件。
