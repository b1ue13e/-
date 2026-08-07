---
title: "jerk约束"
type: concept
course: "15-控制与机器人学"
stage_moc: "[[🧭 阶段8-轨迹与路径跟踪]]"
flow: knowledge
kind: concept
importance: "A"
status: completed
created: 2026-08-07
updated: 2026-08-07
tags: [学习, 控制与机器人学, 轨迹规划]
upstream:
  - "[[加速度约束]]"
concept: ["jerk", "舒适性"]
prerequisites: ["加速度约束"]
related: ["S曲线规划", "横向优化", "轨迹代价"]
---

# jerk约束

> **一句话**:jerk = 加速度的变化率——"急加速又急收"最难受,限制 jerk 就是限制"加速度突变",舒适性的核心指标。

## 定义

$$\mathbf{j} = \frac{d\mathbf{a}}{dt} = \frac{d^3 \mathbf{p}}{dt^3}$$

轨迹规划中:
- 纵向 jerk:$\dddot{s}$
- 横向 jerk:$\dddot{d}$

## 为什么 jerk 重要

| 指标 | 影响 |
|:---|:---|
| jerk 大 | 头部晃动、晕车、货物冲击 |
| jerk 连续 | 加减速平滑过渡,体感舒适 |
| jerk 无穷 | 加速度阶跃(梯形剖面)→ 冲击 |

**舒适性主要靠 jerk 而非加速度决定**——这正是 S 曲线与五次多项式的动机(见[[S曲线规划]]/[[横向多项式]])。

## jerk 限值经验值

| 场景 | 纵向 jerk 限值 |
|:---|:---|
| 高级舒适 | ≤ 0.5–1 m/s³ |
| 一般舒适 | ≤ 1–2 m/s³ |
| 紧急 | 不设限 |

## jerk 约束的施加

1. **轨迹生成**:五次多项式(端到端 jerk 有限)/S 曲线直接满足
2. **轨迹采样**:代价含 $\int \dddot{d}^2 dt$(见[[轨迹代价]])
3. **可行性检查**:逐点 $\|\dddot s\| \le j_{max}$(见[[轨迹可行性]])

## 自检

- [ ] jerk 的物理意义与定义?
- [ ] 为什么 jerk 比加速度更影响舒适?
- [ ] 三种施加 jerk 约束的途径?
