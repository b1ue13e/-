---
type: index
topic: "Git仓库说明"
created: 2026-04-29
updated: 2026-08-06
status: active
tags: [说明, Git, Obsidian]
---

# 📋 Git仓库说明

当前长期使用的 Git 仓库目录是：

- `F:\-`

远端仓库：

- `https://github.com/b1ue13e/-`

## 你以后应该在哪工作

- 持续提交与推送：`F:\-`
- 日常编辑与整理：`F:\-`（Obsidian 直接打开该文件夹）

> 历史文档曾采用 `E:\GitHub\-` 与 `E:\GitHub\-core` 的双仓库方案（核心库只保留笔记、模板、说明页）。当前已收敛为单仓库 `F:\-`，`.gitignore` 负责排除超大 PDF 与本地状态文件，因此不再需要维护两个不同步的仓库。

## 内容分布

- 课程知识：`02-Knowledge/🧠 学习系统/<路径>/`
- 作业与项目：`03-Projects/<路径>/`
- 系统治理：`99-System/`
- 书籍/论文：`02-Knowledge/📚 书库/`、`02-Knowledge/📚 论文库/`

## 推送命令

```powershell
git add <本次修改路径>
git commit -m "vault update"
git push origin main
```

> 安全约束：禁止无审查的 `git add .`；大批量修改前先做快照或安全提交；破坏性命令（`reset --hard`、`checkout --`）除非用户明确要求否则禁止使用。详见 `AGENTS.md` §7。

## 恢复隔离区

`.recovery-hold/` 是 gitignored 的恢复隔离区。治理中的清退、归档和治理前快照都放入其中；确认内容已合并或安全后再决定是否永久删除。
