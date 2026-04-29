---
tags: [PARA, 知识管理, 导航]
created: 2026-04-11
type: index
topic: "PARA知识管理主页"
status: active
---

# 🗂️ PARA知识管理主页

> **PARA** 是组织信息的四分类法：
> - **P**rojects（项目）- 有截止日的目标
> - **A**reas（领域）- 长期责任范围
> - **R**esources（资源）- 参考材料
> - **A**rchives（归档）- 已完成项目

---

## 📊 PARA概览

```dataviewjs
const projects = dv.pages('"🧠 学习系统/20-PARA知识管理/1-Projects(项目)"').length;
const areas =
    dv.pages('"🧠 学习系统/20-PARA知识管理/2-Areas(领域)"').length +
    dv.pages('"🧠 学习系统/20-PARA知识管理/02-领域"').length;
const resources = dv.pages('"🧠 学习系统/20-PARA知识管理/3-Resources(资源)"').length;
const archives = dv.pages('"🧠 学习系统/20-PARA知识管理/4-Archives(归档)"').length;

dv.table(
    ["分类", "数量", "说明"],
    [
        ["📂 项目", projects, "有截止日的目标"],
        ["📁 领域", areas, "长期责任范围"],
        ["📚 资源", resources, "参考材料"],
        ["📦 归档", archives, "已完成项目"],
    ]
);
```

---

## 📂 Projects（项目）

> **项目** = 有明确目标和截止日期的任务集合

### 活跃项目
```dataviewjs
const normalizeStatus = status => {
    if (status === "已完成") return "completed";
    if (status === "进行中") return "active";
    return status || "active";
};
const labelStatus = status => ({
    active: "进行中",
    paused: "暂停",
    completed: "已完成"
}[status] || status || "进行中");

dv.table(
    ["项目", "状态", "截止日期", "进度"],
    dv.pages('"🧠 学习系统/20-PARA知识管理/1-Projects(项目)"')
        .where(p => normalizeStatus(p.status) !== "completed")
        .map(p => [p.file.link, labelStatus(normalizeStatus(p.status)), p.due || p.deadline || "-", p.progress || "⬜⬜⬜⬜⬜"])
);
```

### 快速入口
- [[📊 项目追踪|查看项目追踪]]
- [[📓 学习笔记模板|新建项目笔记]]

---

## 📁 Areas（领域）

> **领域** = 需要长期维护的责任范围（没有截止日期）

### 核心领域
| 领域 | 说明 | 入口 |
|:---:|:---|:---:|
| 学习管理 | 学习节奏、目标与复盘 | [[🧠 学习系统/20-PARA知识管理/2-Areas(领域)/学习管理看板\|进入]] |
| 学习笔记 | 学习项目与主题目录 | [[🧠 学习系统/20-PARA知识管理/02-领域/学习笔记/📚 学习笔记目录\|进入]] |

### 全部领域
```dataviewjs
dv.list([
    ...dv.pages('"🧠 学习系统/20-PARA知识管理/2-Areas(领域)"').file.link.array(),
    ...dv.pages('"🧠 学习系统/20-PARA知识管理/02-领域"').file.link.array()
]);
```

---

## 📚 Resources（资源）

> **资源** = 感兴趣的主题、参考材料、灵感来源

### 资源分类
| 分类 | 说明 | 入口 |
|:---:|:---|:---:|
| 学习资源 | 教程、课程、书籍 | 目录建设中 |
| 工具资源 | 软件、工具、插件 | 目录建设中 |
| 灵感资源 | 想法、灵感、创意 | 目录建设中 |
| 待读清单 | 稍后阅读、待看影视 | 目录建设中 |

---

## 📦 Archives（归档）

> **归档** = 已完成的项目、不再活跃的领域、过时的资源

### 已归档项目
```dataviewjs
const normalizeStatus = status => {
    if (status === "已完成") return "completed";
    if (status === "进行中") return "active";
    return status || "active";
};

dv.table(
    ["项目", "完成日期", "成果"],
    dv.pages('"🧠 学习系统/20-PARA知识管理/4-Archives(归档)"')
        .where(p => normalizeStatus(p.status) === "completed")
        .sort(p => p.completedDate || p.updateTime, 'desc')
        .limit(10)
        .map(p => [p.file.link, p.completedDate || p.updateTime || "-", p.result || "-"])
);
```

---

## 🔄 PARA工作流

### 日常流程
```
1. 捕获 → 将新想法放入 Resources 或 Projects
2. 整理 → 定期审查并分类
3. 执行 → 推进 Projects 中的任务
4. 维护 → 持续关注 Areas
5. 归档 → 完成的项目移至 Archives
```

### 定期审查
| 频率 | 审查内容 |
|:---:|:---|
| 每周 | 活跃项目进度、下周计划 |
| 每月 | 领域健康度、资源整理 |
| 每季 | 大目标对齐、归档清理 |

---

## 🛠️ 快速工具

| 操作 | 模板 |
|:---:|:---:|
| 新建项目 | [[📊 项目追踪\|项目追踪]] |
| 新建笔记 | [[📓 学习笔记模板\|笔记模板]] |
| 新建学习项目 | [[🧠 学习系统/20-PARA知识管理/02-领域/学习笔记/📚 学习笔记目录\|学习项目]] |

---

*[[🏠 主页|返回主页]] | [[🗂️ 资源总索引|系统索引]]*
