---
type: index
topic: "Git仓库说明"
created: 2026-04-29
status: active
tags: [说明, Git, Obsidian]
---

# 📋 Git仓库说明

当前长期使用的 Git 仓库目录是：

- `E:\GitHub\-core`

原始完整仓库目录是：

- `E:\GitHub\-`

## 你以后应该在哪工作

如果目标是：

- 持续提交
- 持续推 GitHub
- 保持仓库轻量可同步

那么建议你以后直接打开：

- `E:\GitHub\-core`

不要再把 `E:\GitHub\-` 当作主 Git 仓库使用。

## 为什么拆成两个库

因为原始仓库里包含很多超大 PDF / 资源文件，GitHub 普通仓库无法稳定推送。

核心仓库只保留：

- 笔记
- 模板
- 说明页
- 必要的 Obsidian 配置

## 推送命令

```powershell
git add .
git commit -m "vault update"
git push origin main
```

## 注意

`E:\GitHub\-` 和 `E:\GitHub\-core` 不会自动同步。  
如果你在原始库里改内容，需要手动再整理到核心库。

