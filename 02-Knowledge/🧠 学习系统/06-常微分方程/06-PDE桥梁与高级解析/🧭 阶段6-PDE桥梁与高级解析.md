---
type: index
topic: PDE桥梁与高级解析
tags:
- 常微分方程
- 阶段MOC
created: 2026-08-06
status: active
course: 常微分方程
flow: knowledge
kind: moc
---



# 🟤 第六阶段：PDE桥梁与高级解析

> "通过级数解与特征值问题，搭建通往偏微分方程(PDE)的桥梁。"

---

## 📊 阶段目标与导学说明

- **为什么现在学**：变系数方程与边值问题是通往偏微分方程（PDE，如热传导、波动方程）的必经之路。
- **推荐学习顺序**：掌握标准的变系数方程——欧拉-柯西方程（01）；学习泰勒与 Frobenius 幂级数解法（02）；深入 Sturm-Liouville 理论与正交函数展开（03）。
- **能力目标**：理解特殊函数的级数来源，掌握边值问题中的特征值与特征函数展开法。

## 📚 知识卡片清单

1. [[常微分方程-欧拉-柯西方程]]
2. [[常微分方程-级数解法与Frobenius方法]]
3. [[常微分方程-边值问题与Sturm-Liouville理论]]

---

## 🧪 阶段验收与作业

完成本阶段知识后，学习者应能够用级数解法与 Sturm-Liouville 理论处理变系数方程与边值问题，并完成以下课后作业：

- [[03-Projects/数学底座/06-常微分方程/课后作业/常微分方程-课后作业-04-级数解法与边值问题\|课后作业 04：级数解法与边值问题]]

```dataview
LIST
FROM "03-Projects/数学底座/06-常微分方程"
WHERE contains(requires, this.file.link) OR (
  file.folder != null AND 
  contains(file.folder, "03-Projects") AND 
  stage_id != null AND 
  stage_id == "06"
)
SORT assignment_level ASC, file.name ASC
```

---

## 🔗 阶段导航

| ⬅️ 上一阶段 | 📋 总览 | 下一阶段 ➡️ |
|:---:|:---:|:---:|
| [[🧭 阶段5-现代非线性动力系统\|返回第五阶段]] | [[02-Knowledge/🧠 学习系统/06-常微分方程/🗺️ 常微分方程学习路径\|返回总览]] | [[🧭 阶段7-精通与专题\|进入第七阶段]] |

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/数学底座/06-常微分方程"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
