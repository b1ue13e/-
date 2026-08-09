---
type: study
topic: "阶段3-非线性与ODE数值解"
course: "数值分析"
created: 2026-08-08
updated: 2026-08-08
status: active
flow: knowledge
kind: moc
tags: [MOC, 阶段MOC, 数值分析, 非线性求解, ODE数值解, 刚性方程]
---

# 🧭 阶段3：非线性方程与常微分方程数值解

> “真实物理与工程系统绝大多数无法求出闭式解析解。本阶段攻克多维非线性系统的局部/全局收敛 Newton 迭代、显式 Runge-Kutta 积分器，以及多时间尺度刚性方程的 A-稳定性与隐式积分器。”

---

## 📋 本阶段有序知识卡清单

```dataview
LIST
FROM "02-Knowledge/🧠 学习系统/35-数值分析/03-非线性与ODE数值解"
WHERE type = "study" AND !contains(file.name, "🧭")
SORT file.name ASC
```

---

## 🎯 阶段目标与能力构建

1. **非线性多维求根与阻尼 Newton**：掌握不动点迭代的压缩映射原理、单变量 Newton 二阶局部收敛证明，以及多维 Newton-Raphson 雅可比阻尼线搜索技术。
2. **显式 Runge-Kutta 几何与代数阶**：理解单步法局部截断误差与全局误差累积，掌握 Butcher 表格与经典四阶 RK4 的代数匹配推导。
3. **刚性系统与绝对稳定性（A-Stability）**：深入理解快慢多时间尺度系统的刚性本质，掌握测试方程 $y' = \lambda y$ 下的稳定区域分析、Dahlquist 屏障定理，以及后向 Euler 与 Crank-Nicolson 隐式积分器。

---

## 🧮 阶段验收与对应作业

- [[03-Projects/35-数值分析/课后作业/数值分析-课后作业-06-非线性方程求解与Newton法|HW06：非线性方程求解与多维Newton法]]
- [[03-Projects/35-数值分析/课后作业/数值分析-课后作业-07-ODE初值问题与Runge-Kutta|HW07：ODE初值问题与Runge-Kutta单步法]]
- [[03-Projects/35-数值分析/阶段作业/数值分析-阶段作业-03-刚性微分方程与隐式积分器|Stage 3 阶段综合大作业：刚性微分方程与隐式积分器]]

---

## 🔗 阶段衔接

- 完成本阶段所有作业并自测通过后，进入：[[04-PDE数值与科学计算/🧭 阶段4-PDE数值与科学计算|🧭 阶段4：PDE有限差分与科学计算]]
