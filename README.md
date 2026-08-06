---
type: index
topic: "个人知识库核心仓库"
created: 2026-04-29
updated: 2026-08-06
status: active
tags: [说明, Git, Obsidian]
---

# 个人知识库核心仓库

这是一个**长期使用的 Git 版核心仓库**，对应目录：

- `F:\-`

远端仓库：

- `origin`: [https://github.com/b1ue13e/-](https://github.com/b1ue13e/-)

## 这个仓库的定位

- 用于长期 Git 管理
- 用于同步到 GitHub
- 用于保留 Obsidian 可直接打开的核心知识库

> 说明：历史文档曾把工作目录记为 `E:\GitHub\-core`（与 `E:\GitHub\-` 拆分为两个库）。当前实际部署为单仓库 `F:\-`，所有内容（知识、项目、系统治理）都在其中；Git 通过 `.gitignore` 排除超大 PDF 与本地状态文件。

## 目录契约（AGENTS.md）

- `00-Inbox/` — 快速捕捉，24 小时内分流
- `01-Active Sprint/` — 当前主攻 Sprint（唯一 `sprint: current`）
- `02-Knowledge/` — 可复用知识（课程路径、阶段 MOC、知识卡、错题）
- `03-Projects/` — 实验与验收（作业、代码、数据、报告、质量审计）
- `04-Review/` — 复习回收（Anki FSRS 薄弱点）
- `99-System/` — 系统治理（模板、工具、计划系统、审计脚本）
- `📚 书库/`、`📚 论文库/` — 书籍与论文（资源与笔记分离）

> 完整治理规则以根目录 `AGENTS.md` 为准，本文档只说明仓库定位与日常用法。

## 建议的日常使用方式

1. 在 Obsidian 里打开文件夹：
   - `F:\-`
2. 日常编辑、整理、提交都在这个仓库进行：
   - 课程内容 → `02-Knowledge/🧠 学习系统/<路径>/`
   - 作业与项目 → `03-Projects/<路径>/`
3. 推送时直接用：

```powershell
git add <本次修改路径>
git commit -m "vault update"
git push origin main
```

> 禁止无审查的 `git add .`；大批量修改前先创建可恢复快照或安全提交（见 `AGENTS.md` §7）。

## 已忽略的本地文件

详见 `.gitignore`，重点包括：

- `.tmp.driveupload/`、`.tmp.drivedownload/`
- `.obsidian/workspace.json`、`.obsidian/workspaces.json`
- `cursor-positions.json`
- `remotely-save/data.json`、`google-drive-sync/data.json`
- `.recovery-hold/`（恢复隔离区，治理清退内容先入此处）

## 当前分支说明

- 默认分支：`main`
- 进行中的治理分支：`codex/knowledge-base-cleanup`（当前工作分支，未推送的本地提交在推送前需确认与主分支合并策略）

---

*README 更新：2026-08-06。*
