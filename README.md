---
type: index
topic: "个人知识库核心仓库"
created: 2026-04-29
status: active
tags: [说明, Git, Obsidian]
---

# 个人知识库核心仓库

这是一个**长期使用的 Git 版核心仓库**，对应目录：

- `E:\GitHub\-core`

原始大仓库保留不动，仍在：

- `E:\GitHub\-`

## 这个仓库的定位

- 用于长期 Git 管理
- 用于同步到 GitHub
- 用于保留 Obsidian 可直接打开的核心知识库

如果你以后要继续用 Git 管理知识库，**优先在 `E:\GitHub\-core` 里工作**。

## 建议的日常使用方式

1. 在 Obsidian 里打开文件夹：
   - `E:\GitHub\-core`
2. 日常编辑、整理、提交都在这个仓库进行
3. 推送时直接用：

```powershell
git add .
git commit -m "vault update"
git push origin main
```

## 当前保留范围

- `.obsidian`
- `🧠 学习系统`
- `📚 书库/书籍笔记`
- `📚 书库/鸢尾花丛书`
- `📚 论文库/论文笔记`
- `📚 论文库/论文初稿`
- `📚 论文库/prompt`
- 若干主页、模板、索引说明文件

## 当前排除范围

为避免 GitHub 推送失败，以下内容**不放进这个长期 Git 仓库**：

- `📚 书库/书籍资源`
- `📚 论文库/PDF库/*.pdf`
- 本地同步临时目录
- 本地 UI 状态文件
- 同步插件的敏感配置文件

## 已忽略的本地文件

详见 `.gitignore`，重点包括：

- `.tmp.driveupload/`
- `.tmp.drivedownload/`
- `.obsidian/workspace.json`
- `.obsidian/workspaces.json`
- `cursor-positions.json`
- `remotely-save/data.json`
- `google-drive-sync/data.json`

## 重要提醒

`E:\GitHub\-` 和 `E:\GitHub\-core` 现在是两个独立目录：

- `E:\GitHub\-`：原始大仓库 / 本地全集
- `E:\GitHub\-core`：可长期 Git 管理的核心仓库

它们**不会自动双向同步**。

如果你继续在原始仓库里写内容，这些修改不会自动进入核心仓库。

## 远端仓库

- `origin`: [https://github.com/b1ue13e/-](https://github.com/b1ue13e/-)

---

*README 更新：2026-04-29。*
