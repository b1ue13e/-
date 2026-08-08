---
type: study
topic: "MPC横向预测"
course: "控制与机器人学"
created: 2026-04-18
updated: 2026-08-07
status: completed
difficulty: advanced
stage_moc: "[[🧭 阶段6-横向控制]]"
flow: knowledge
kind: derivation
concept: ["MPC横向", "预测模型", "横向控制"]
prerequisites: ["横向系统矩阵", "预测方程"]
related: ["MPC横向约束", "MPC横向代价", "MPC横向求解"]
upstream: ["[[横向系统矩阵]]"]
source: "PythonRobotics model_predictive_control.py; MPC 文献"
tags: [学习, 控制与机器人学, MPC横向]
---

# MPC横向预测

## 0. 为什么学它

横向 MPC 在 LQR 基础上**显式处理约束**（转向角/速率限制）并**滚动优化**：每步用预测模型推出未来 $N$ 步误差，求最优转向序列，只执行第一步。**预测模型**是它的"水晶球"。

## 1. 核心模型

**离散预测模型**（误差状态，ZOH 离散）：

$$x_{k+1}=F x_k + G \delta_k + D\,\ddot\psi_{r,k},$$

- $F,G$：$(A_e,B_e)$ 的离散化（见 [[横向系统矩阵]]、[[系统离散化]]）；
- $D\ddot\psi_r$：参考曲率扰动（弯道项）。

**预测**（$N$ 步）：由当前 $x_0$ 递推

$$x_{k+1}=F x_k+G\delta_k+D w_k,\qquad k=0,\dots,N-1.$$

**优化变量**：转向序列 $\delta_0,\dots,\delta_{N-1}$；目标：误差最小 + 转向平顺（代价函数见 [[MPC横向代价]]）。

## 2. 最小可手算例子（概念验证）

**题目**：为什么 MPC 能"预知"弯道？

**解**：预测模型含参考项 $D w_k$（未来曲率）→ 优化器提前规划转向（前馈式行为），而非 LQR 只对当前状态反应——弯道跟踪更平滑 ✓。

**易错点**：$F,G$ 需按采样时间离散；预测时域 $N$ 影响效果与耗时。

## 3. 常见误区

| 误区 | 正确理解 |
|:---|:---|
| 预测模型必须非线性 | 线性 MPC 横向即可（误差系统线性化） |
| $N$ 越大越好 | 大 $N$ 计算量大，且预测更依赖模型 |
| 忽略曲率项 | 弯道需参考项或前馈 |

## 4. 与后续知识连接

- [[MPC横向约束]]、[[MPC横向代价]]、[[MPC横向求解]]：完整 MPC；
- [[预测方程]]：一般形式；
- [[LQR横向状态]]：无约束特例。

## 5. 检索练习（闭卷）

1. 写出横向预测模型；
2. 说明滚动优化流程；
3. 解释弯道预知；
4. $N$ 的权衡。

## 6. 通过标准

- 能建预测模型；
- 能理解滚动优化；
- 能处理参考项。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/系统与硬件/15-控制与机器人学"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 复习

- 下次复习：3 天后重推预测；
- 薄弱点写入 [[控制与机器人学错题漏洞入口]]。
