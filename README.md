---
type: index
topic: "个人知识库核心仓库"
created: 2026-04-29
updated: 2026-11-09
status: active
tags: [说明, Git, Obsidian]
---

# Personal knowledge vault

[中文](README.zh-CN.md) · [Repository](https://github.com/b1ue13e/-)

An Obsidian knowledge vault for study paths, reusable notes, paper and book reading, assignments, research projects, and review. This is a collection of Markdown materials, rather than an application requiring a build or server.

## Start reading

Open the cloned repository directory as an Obsidian vault. Start with [[🏠 主页]] and [[📋 使用说明]]. GitHub displays Markdown text; Dataview and Templater views require Obsidian and the corresponding plugins.

| Area | Purpose |
| --- | --- |
| `00-Inbox/` | Capture notes before routing them into the vault |
| `01-Active Sprint/` | Current focused work and sprint navigation |
| `02-Knowledge/` | Study paths, concept notes and reusable knowledge |
| `03-Projects/` | Assignments, project code, data references and reports |
| `04-Review/` | Review material and weak-point recovery |
| `99-System/` | Templates, tools and vault maintenance |

Books, papers and reading notes use their existing resource indexes. Follow vault links rather than maintaining a parallel course and assignment map in this README.

## Maintaining the vault

The root [AGENTS.md](AGENTS.md) defines frontmatter, wikilinks, course navigation, file placement and Git safety. Preserve Unicode names, note metadata and the single authoritative location for each relationship. Large local resources and workspace state are governed by `.gitignore`.

For reviewed documentation changes, stage explicit paths:

```sh
git add README.md README.zh-CN.md
git diff --cached --stat
git commit -m "docs: update vault navigation"
git push origin main
```

The remote default branch is `main`; local working branches may differ. This documentation does not move or rewrite study notes, project materials or resources.
