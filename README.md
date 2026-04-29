---
type: index
topic: "个人知识管理系统"
created: 2026-04-14
status: active
tags: [说明, 导航]
---

# 🏠 个人知识管理系统

> 一个基于 Obsidian 的个人知识操作系统，围绕学习、论文、书籍、项目四条主线组织内容。

---

## ✨ 当前优化重点

- **首页改为行动面板**：先决定“现在做什么”，再进入具体目录
- **新增学科分组导航**：36 条路径先按大类分组，再进入详细路径页
- **项目模板与项目追踪分层**：统一 `project_type`、`focus`、`status`
- **增加知识库体检脚本**：统一检查 frontmatter、类型和状态枚举

---

## 📁 目录结构

```text
.
├── 🏠 主页.md
├── 🗂️ 资源总索引.md
├── 📋 使用说明.md
├── 📓 学习笔记模板.md
├── 📓 快速笔记模板.md
├── 📄 论文笔记模板.md
├── 📘 读书笔记模板.md
├── 📁 项目模板.md
├── 📚 论文库/
├── 📚 书库/
└── 🧠 学习系统/
    ├── 🎓 学习入口.md
    ├── 🧭 学科分组导航.md
    ├── 🔍 概念自动索引.md
    ├── 🕸️ 知识依赖图谱.md
    └── 🏷️ 标签云索引.md
```

---

## 🧠 三层入口设计

1. **总控入口**：`🏠 主页.md`、`🗂️ 资源总索引.md`、`📋 使用说明.md`
2. **资源导航层**：学习系统 / 论文库 / 书库 / 项目追踪
3. **执行入口层**：学习模板 / 论文模板 / 读书模板 / 项目模板

这样做的目标是：**首页不堆结构，入口先服务行动。**

---

## 🧩 Frontmatter 约定

### 核心类型

- 学习笔记：`type: study`
- 阶段页：`type: stage`
- 论文笔记：`type: paper`
- 读书笔记：`type: book`
- 项目页：`type: project`
- 索引 / 说明页：`type: index`

### 推荐治理字段

- `template: true`：标记模板文件，避免统计和体检混入模板
- `domain`：标记领域，如 `ai / math / stats / cs / paper / book / project`
- `project_type`：`learning / research / implementation / reading`
- `focus`：`now / next / later`

### 统一状态体系

- 学习 / 阶段：`planned | ongoing | completed`
- 项目：`active | paused | completed`
- 论文 / 书籍：`unread | reading | finished`
- 索引：`active`

---

## 🚀 使用方式

1. 从 [🏠 主页](./🏠%20主页.md) 进入行动面板。
2. 如果要选学习方向，先打开 [🧭 学科分组导航](./🧠%20学习系统/🧭%20学科分组导航.md)。
3. 如果要进入具体路径细节，再打开 [🎓 学习入口](./🧠%20学习系统/🎓%20学习入口.md)。
4. 新建内容时，优先使用对应模板。
5. 定期运行 `scan_frontmatter.ps1` 做知识库体检。

---

## 🔍 知识库体检

在仓库根目录运行：

```powershell
.\scan_frontmatter.ps1
```

它会检查：

- frontmatter 是否缺失
- `type` 是否规范
- `status` 是否符合该页面类型
- 关键字段是否缺失
- 模板文件数量与治理字段覆盖情况

---

*README 更新：2026-04-20。*
