---
type: study
topic: "jerk约束"
course: "控制与机器人学"
created: 2026-08-07
updated: 2026-08-08
status: completed
difficulty: intermediate
stage_moc: "[[🧭 阶段8-轨迹与路径跟踪]]"
flow: knowledge
kind: concept
concept: ["jerk", "舒适性", "加速度变化率"]
prerequisites: ["加速度约束"]
related: ["S曲线规划", "横向优化", "轨迹代价"]
upstream: ["[[08-轨迹与路径跟踪/加速度约束]]"]
source: "运动规划舒适性文献；PythonRobotics（MIT）"
tags: [学习, 控制与机器人学, 轨迹规划]
---

# jerk约束

> **一句话**：jerk = 加速度的变化率——"急加速又急收"最难受，限制 jerk 就是限制"加速度突变"，舒适性的核心指标。

## 0. 为什么学它

乘客晕不晕、货物稳不稳，主要看 jerk 而不是加速度。S 曲线、五次多项式、最小 jerk 横向轨迹（阶段 8 大量内容）的动机都在这一张卡里——它是"舒适性"的数学化。

## 1. 定义

$$\mathbf{j} = \frac{d\mathbf{a}}{dt} = \frac{d^3 \mathbf{p}}{dt^3}$$

轨迹规划中：
- 纵向 jerk：$\dddot{s}$
- 横向 jerk：$\dddot{d}$

## 2. 为什么 jerk 重要

| 指标 | 影响 |
|:---|:---|
| jerk 大 | 头部晃动、晕车、货物冲击 |
| jerk 连续 | 加减速平滑过渡，体感舒适 |
| jerk 无穷 | 加速度阶跃（梯形剖面）→ 冲击 |

**舒适性主要靠 jerk 而非加速度决定**——这正是 S 曲线与五次多项式的动机（见[[S曲线规划]]/[[横向多项式]]）。

## 3. 最小可手算例子（梯形 vs S 曲线的 jerk）

**题目**：梯形剖面在 $t=t_a$ 时刻加速度从 $a_{max}$ 阶跃到 0。若 $a_{max}=2$，用 $\Delta t \to 0$ 估算该点 jerk。

**步骤**：
1. jerk = $\Delta a / \Delta t = (0 - 2)/\Delta t \to -\infty$（$\Delta t \to 0$）；
2. 物理含义：转向/油门瞬间松开，冲击无穷大；
3. S 曲线用 jerk 斜坡（如 $\pm1\ \text{m/s}^3$）替代阶跃，冲击消失（见[[S曲线规划]]）。

**含义**：这就是"为什么梯形不舒适、S 曲线舒适"的数学原因。

## 4. jerk 限值经验值

| 场景 | 纵向 jerk 限值 |
|:---|:---|
| 高级舒适 | ≤ 0.5–1 m/s³ |
| 一般舒适 | ≤ 1–2 m/s³ |
| 紧急 | 不设限 |

## 5. 常见误区

| 误区 | 正确理解 |
|:---|:---|
| 限制加速度就够舒适 | 加速度连续但突变（梯形）仍冲击，必须限 jerk |
| jerk 限值越大越灵活 | 越大越不舒适，需按场景标定 |
| jerk 约束只在纵向 | 横向 jerk（$\dddot d$）是换道舒适的关键（见[[横向优化]]） |

## 6. jerk 约束的施加

1. **轨迹生成**：五次多项式（端到端 jerk 有限）/S 曲线直接满足；
2. **轨迹采样**：代价含 $\int \dddot{d}^2 dt$（见[[轨迹代价]]）；
3. **可行性检查**：逐点 $\lVert \dddot s \rVert \le j_{max}$（见[[轨迹可行性]]）。

## 7. 检索练习（闭卷）

1. 写出 jerk 定义与横纵向形式；
2. 解释梯形剖面 jerk 无穷的原因；
3. 列出三种施加 jerk 约束的途径。

## 8. 通过标准

- 能定义 jerk 并解释其物理意义；
- 能手算阶跃 jerk；
- 能说明 jerk 约束的施加方式。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/系统与硬件/15-控制与机器人学"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 复习

- 薄弱点写入 [[控制与机器人学错题漏洞入口]]；下次复习：重述梯形 vs S 曲线 jerk 对比。
