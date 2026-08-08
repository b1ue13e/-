---
type: study
topic: "避障MPC"
course: "控制与机器人学"
created: 2026-08-07
updated: 2026-08-08
status: completed
difficulty: advanced
stage_moc: "[[🧭 阶段9-MPC深入]]"
flow: knowledge
kind: concept
concept: ["避障约束", "动态障碍"]
prerequisites: ["联合MPC设计", "碰撞检测"]
related: ["联合MPC设计", "横向避障", "横向MPC设计"]
upstream: ["[[联合MPC设计]]", "[[碰撞检测]]"]
source: "车辆避障 MPC 文献；PythonRobotics（MIT）"
tags: [学习, 控制与机器人学, MPC]
---

# 避障MPC

> **一句话**：把"别撞障碍"写成优化约束——避障 MPC 在预测时域内同时保证安全（不碰障碍）与性能（跟踪目标），是主动安全的核心技术。

## 0. 为什么学它

避障是自动驾驶/机器人的安全底线。MPC 的优势在于：把障碍写成时域约束，预测式地绕开（而非触发才反应），并能处理动态障碍——本卡是阶段 9 车辆 MPC 的收尾应用。

## 1. 障碍约束表达

### 1.1 静态障碍（位置约束）

$$\lVert \mathbf{p}_k - \mathbf{p}_{obs,i} \rVert \ge d_{safe} + r_{obs} + r_{car}$$

对每个预测时刻、每个障碍写不等式——线性化后进 QP。

### 1.2 动态障碍（时空约束）

障碍位置随时间变化 $\mathbf{p}_{obs}(t_k)$：

$$\lVert \mathbf{p}_k - \mathbf{p}_{obs}(t_k) \rVert \ge d_{safe}(t_k)$$

## 2. 与联合 MPC 的关系

避障 MPC = 联合 MPC（纵横向协调）+ 避障约束：

$$\min_{\delta, a} \sum \ell(\mathbf{x}_k - \mathbf{x}_{ref,k}) \quad \text{s.t. 动力学、摩擦圆、} \lVert \mathbf{p}_k - \mathbf{p}_{obs} \rVert \ge d_{safe}$$

## 3. 最小可手算例子（约束可行性）

**题目**：$t_k$ 时刻车距障碍 $d = 3$ m，要求 $d_{safe} = 4$ m。判定与处理。

**步骤**：
1. $3 < 4$ 违反避障约束 → 该控制序列不可行；
2. 优化器需减速/转向增大距离；
3. 若物理上已无法（$a_{min}$ 不够）→ 软约束/松弛兜底（见[[松弛变量]]），保证有解。

**含义**：避障约束本质是硬安全红线，但需松弛机制防止求解失败。

## 4. 常见误区

| 误区 | 正确理解 |
|:---|:---|
| 障碍当静态 | 动态障碍必须预测位置（时间维度） |
| 只避最近障碍 | 预测时域内所有障碍都要检查 |
| 避障 MPC 一定成功 | 物理极限下仍需松弛/降级策略 |

## 5. 工程要点

- 障碍膨胀按车宽+裕量（见[[碰撞检测]]）；
- 动态障碍用运动预测（恒速/意图模型）；
- 与决策层（左绕/右绕）配合（见[[横向避障]]）。

## 6. 检索练习（闭卷）

1. 写出静态/动态障碍约束；
2. 手算一个约束判定；
3. 说明与联合 MPC 关系。

## 7. 通过标准

- 能写避障约束；
- 能手算判定；
- 能说明工程要点。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/系统与硬件/15-控制与机器人学"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 复习

- 薄弱点写入 [[控制与机器人学错题漏洞入口]]；下次复习：重做约束判定。
