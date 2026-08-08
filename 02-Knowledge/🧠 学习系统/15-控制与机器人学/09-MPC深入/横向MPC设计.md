---
type: study
topic: "横向MPC设计"
course: "控制与机器人学"
created: 2026-08-07
updated: 2026-08-08
status: completed
difficulty: advanced
stage_moc: "[[🧭 阶段9-MPC深入]]"
flow: knowledge
kind: concept
concept: ["横向控制", "轨迹跟踪MPC"]
prerequisites: ["线性车辆MPC", "横向动力学"]
related: ["纵向MPC设计", "联合MPC设计", "线性车辆MPC"]
upstream: ["[[线性车辆MPC]]", "[[横向动力学]]"]
source: "车辆 MPC 文献；PythonRobotics model_predictive_control（MIT）"
tags: [学习, 控制与机器人学, MPC]
---

# 横向MPC设计

> **一句话**：横向 MPC 用预测模型直接优化"转向角序列"使横向误差最小——对比 Stanley/PP，它天然处理约束（转向角/率上限）与未来参考（提前转弯）。

## 0. 为什么学它

阶段 6 的 PP/Stanley 是"反应式"横向控制；横向 MPC 是"预测式"——能提前看向前方轨迹、显式处理转向约束，是阶段作业-09 与自动驾驶横向控制的高配方案。

## 1. 设计要素

| 要素 | 内容 |
|:---|:---|
| 状态 | $[y_{err}, \dot y_{err}, \theta_{err}, \dot\theta_{err}]$（横向误差模型） |
| 控制量 | 转向角 $\delta$ 或转向率 $\dot\delta$ |
| 模型 | 横向动力学线性化（见[[横向动力学]]） |
| 约束 | $\lvert\delta\rvert \le \delta_{max},\ \lvert\dot\delta\rvert \le \dot\delta_{max}$ |
| 代价 | $Q$ 惩罚横向误差、$R$ 惩罚转向动作 |

## 2. 相对 Stanley/PP 的优势

| 对比项 | Stanley/PP | 横向 MPC |
|:---|:---|:---|
| 前瞻性 | 单点预瞄 | 全时域预测（提前转向） |
| 约束 | 事后限幅 | 优化内显式处理 |
| 高速性能 | 调参敏感 | 模型+预测更稳 |
| 计算 | 极低 | 中等（QP） |

## 3. 最小可手算例子（代价权衡）

**题目**：横向误差 $e = 0.5$ m，转向 $\delta = 0.1$ rad。$Q = 10, R = 1$ 与 $Q = 1, R = 10$ 的单步代价对比。

**步骤**：
1. $Q=10,R=1$：$J = 10\times0.25 + 1\times0.01 = 2.51$——误差主导，控制器激进压误差；
2. $Q=1,R=10$：$J = 0.25 + 10\times0.01 = 0.35$——转向昂贵，控制器温和；
3. 权重决定"贴线 vs 平稳"，与 LQR 调参同构。

**含义**：横向 MPC 调参就是调 $Q/R$ 找到"误差小 + 转向顺"的平衡。

## 4. 常见误区

| 误区 | 正确理解 |
|:---|:---|
| 状态只用位置误差 | 需含航向/转向率误差，否则振荡 |
| 约束可省 | 无转向率约束会算出猛打方向 |
| 横向 MPC 一定优于 Stanley | 计算成本高，简单场景 Stanley 更实用 |

## 5. 检索练习（闭卷）

1. 写出横向 MPC 设计要素；
2. 手算权重对比；
3. 对比 Stanley/PP。

## 6. 通过标准

- 能设计横向 MPC；
- 能手算权重权衡；
- 能说明取舍。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/系统与硬件/15-控制与机器人学"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 复习

- 薄弱点写入 [[控制与机器人学错题漏洞入口]]；下次复习：重做权重手算。
