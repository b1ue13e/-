---
type: stage
topic: "第4阶段：Bootstrap与现代应用"
created: 2026-08-08
status: active
course: "非参数统计"
tags: [非参数统计, 阶段4, Bootstrap, 置换检验, 选型决策]
flow: knowledge
kind: moc
phase: 4
concept: ["置换检验", "Bootstrap重采样", "BCa置信区间", "方法选型决策树"]
prerequisites: ["[[03-平滑与估计/🧭 阶段3-平滑与估计]]"]
---

# 🧭 第4阶段：Bootstrap与现代应用

> 这一阶段聚焦：将计算密集型重抽样（Resampling）与现代数据分析工作流结合，推导置换检验的精确条件分布与 Bootstrap 置信区间（Percentile、Studentized、BCa）的二阶精度，建立最终的统计推断选型决策全景。

---

## 📌 阶段定位与学习目标

- **为什么现在学**：当检验统计量形式极其复杂（如两个非线性模型预测误差之比、中位数相关系数），无法写出解析标准误时，Bootstrap 与置换检验是唯一的科学推断通路。
- **核心抓手**：置换检验可交换性 (Exchangeability) 前提、Bootstrap 插件原理 (Plug-in Principle)、百分位与 BCa 置信区间覆盖误差 $O(1/n)$、参数 vs 非参数决策树。
- **学完能做什么**：能够独立编写无偏置换检验算法，对任意非平滑统计量构建高阶精度 Bootstrap 区间，并在面对真实复杂数据时输出端到端的分析报告与选型理由。
- **进入下一阶段门槛**：掌握置换与 Bootstrap 理论，通过阶段作业 01 与 Capstone 大作业全部实证实验。

---

## 🗂️ 有序知识卡清单

1. [[非参数统计-置换检验Permutation-Test]] —— 可交换性假设、精确条件分布、Monte Carlo 近似与非参数独立性检验
2. [[非参数统计-Bootstrap重采样与置信区间]] —— 插件原理、Bootstrap 标准误、经验百分位区间与 BCa 二阶精度修正
3. [[非参数统计-参数与非参数方法选型决策]] —— 样本量/偏态/离群点诊断清单、非参数检验选型全景矩阵与实际陷阱

---

## 🎯 阶段验收与作业

```dataview
TABLE assignment_level AS "规模", requires AS "依赖知识点"
FROM "03-Projects/32-非参数统计"
WHERE contains(stage_id, "04") OR contains(assignment_level, "capstone")
SORT file.name ASC
```

- **阶段作业入口**：[[03-Projects/32-非参数统计/阶段作业/非参数统计-阶段作业-01-置换检验与Bootstrap置信区间对比|阶段作业 01：置换检验与 Bootstrap 置信区间对比]]
- **大作业入口 (Capstone)**：[[03-Projects/32-非参数统计/大作业/非参数统计-大作业-非参数推断与平滑方法全景实证研究|大作业：非参数推断与平滑方法全景实证研究]]

---

## 🔗 阶段导航
| ⬅️ 上一阶段 | 🧭 课程主线 | 终极验收 🎓 |
|:---:|:---:|:---:|
| [[03-平滑与估计/🧭 阶段3-平滑与估计\|03-平滑与估计]] | [[🗺️ 非参数统计学习路径\|返回学习路径]] | [[03-Projects/32-非参数统计/大作业/非参数统计-大作业-非参数推断与平滑方法全景实证研究\|大作业 (Capstone)]] |
