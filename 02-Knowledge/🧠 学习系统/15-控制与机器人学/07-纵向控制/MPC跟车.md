---
type: study
topic: "MPC跟车"
course: "控制与机器人学"
created: 2026-04-18
updated: 2026-08-07
status: completed
difficulty: advanced
stage_moc: "[[🧭 阶段7-纵向控制]]"
flow: knowledge
kind: derivation
concept: ["MPC跟车", "ACC优化", "约束控制"]
prerequisites: ["间距误差", "MPC横向预测"]
related: ["间距误差", "ACC切换逻辑"]
upstream: ["[[07-纵向控制/间距误差]]"]
source: "ACC MPC 文献; PythonRobotics model_predictive_speed_and_steering_control.py"
tags: [学习, 控制与机器人学, ACC]
---

# MPC跟车

## 0. 为什么学它

经典 ACC 用固定反馈，难以处理**加速度/舒适性约束**与**前车未来行为**。**MPC 跟车**在预测域内优化加速度序列，显式处理制动/加速限制与安全间距约束——更平滑、更安全的 ACC。

## 1. 核心方法

**预测模型**（间距/速度误差动态）：

$$e_{d,k+1}=e_{d,k}+\Delta t(v_{f,k}-v_k),\qquad v_{k+1}=v_k+\Delta t\,a_k.$$

**代价**：$J=\sum_{k}\big(q_d e_d^2+q_v e_v^2+r a_k^2+s\Delta a_k^2\big)$。

**约束**：
- 加速度限制：$a_{min}\le a_k\le a_{max}$（舒适/安全）；
- 安全间距：$d_k\ge d_0+h v_k$（硬约束或软约束）；
- 速度限制：$0\le v_k\le v_{max}$。

**滚动优化**：每步求解 QP，执行首步。

## 2. 最小可手算例子（概念验证）

**题目**：前车急刹，MPC 与经典 ACC 的区别？

**解**：MPC 预知前车减速轨迹（预测模型）→ 提前规划减速序列、约束保证间距安全 → 平滑制动；经典 ACC 事后反应、可能急刹 ✓。

**易错点**：预测模型依赖前车行为估计；约束需松弛（见 [[松弛变量]]）防无解。

## 3. 常见误区

| 误区 | 正确理解 |
|:---|:---|
| MPC 跟车免约束 | 约束（舒适/安全）正是其价值 |
| 预测前车精确 | 前车行为需估计/保守假设 |
| 约束过紧 | 需松弛防不可行 |

## 4. 与后续知识连接

- [[间距误差]]：误差模型；
- [[MPC横向预测]]：方法通用；
- [[ACC切换逻辑]]：与经典切换结合。

## 5. 检索练习（闭卷）

1. 写出 MPC 跟车代价与约束；
2. 说明前车急刹响应；
3. 约束松弛；
4. 与经典 ACC 对比。

## 6. 通过标准

- 能建 MPC 跟车；
- 能处理约束；
- 能理解预测优势。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/系统与硬件/15-控制与机器人学"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 复习

- 下次复习：3 天后重写代价；
- 薄弱点写入 [[控制与机器人学错题漏洞入口]]。
