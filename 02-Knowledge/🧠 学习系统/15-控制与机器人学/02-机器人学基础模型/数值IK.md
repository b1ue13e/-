---
type: study
topic: "数值IK"
course: "控制与机器人学"
created: 2026-04-18
updated: 2026-08-07
status: completed
difficulty: advanced
stage_moc: "[[🧭 阶段2-机器人学基础模型]]"
flow: knowledge
kind: derivation
concept: ["数值IK", "牛顿拉夫森", "雅可比迭代"]
prerequisites: ["几何Jacobian", "解析逆运动学"]
related: ["几何法IK", "IK多解", "奇异位形"]
upstream: ["[[02-机器人学基础模型/解析逆运动学]]"]
source: "Modern Robotics (Lynch & Park), Ch.6"
tags: [学习, 控制与机器人学, 机器人学]
---

# 数值IK

## 0. 为什么学它

非 Pieper 构型或冗余机械臂没有封闭解，只能**数值迭代**求解。**数值 IK** 基于 Jacobian 或牛顿-拉夫森法：给定初始关节角，反复修正直到末端位姿误差小于阈值。通用性强，是运动学库的兜底方案。

## 1. 核心方法（Jacobian 伪逆法）

目标：$f(q)=T_{06}(q)$ 逼近目标 $T^*$。

误差：$\Delta x$（位置误差 + 旋转误差的向量形式，如 $[e_p; e_o]$）。

迭代：
$$q_{k+1}=q_k + J^\dagger(q_k)\,\Delta x,\qquad J^\dagger=J^\top(JJ^\top)^{-1}\ (\text{伪逆})$$

**牛顿-拉夫森变体**：$J\,\Delta q = \Delta x \Rightarrow \Delta q=J^\dagger\Delta x$，逐步线性化。

**阻尼最小二乘（DLS）**：$J^\dagger=(J^\top J+\lambda^2 I)^{-1}J^\top$——奇异附近稳定（$\lambda$ 为阻尼）。

## 2. 收敛判据与失败

- 收敛：$\lVert\Delta x\rVert < \epsilon$（如 $10^{-6}$）或关节增量足够小；
- 失败：迭代超上限、卡在局部极小（初始值不好）、穿越奇异（$JJ^\top$ 病态）→ 用 DLS / 多初始值重试。

## 3. 最小可手算例子（1 自由度概念验证）

**题目**：1 关节臂 $x=l\cos\theta$，目标 $x^*$，用牛顿迭代求 $\theta$。

**解**：$J=-l\sin\theta$（标量）。迭代 $\theta_{k+1}=\theta_k+(-l\sin\theta_k)^{-1}(x^*-l\cos\theta_k)$。
取 $l=1,\ x^*=0.5,\ \theta_0=0$：$J=0$（奇异！）→ 换初始 $\theta_0=0.5$ 继续迭代至收敛。

**易错点**：初始值在奇异处（$J=0$）迭代停滞；忘记检查 Jacobian 条件数。

## 4. 常见误区

| 误区 | 正确理解 |
|:---|:---|
| 数值 IK 一定能收敛 | 依赖初始值，可能局部极小 |
| 伪逆无阻尼 | 奇异附近需 DLS 阻尼 |
| 每步都从零开始 | 轨迹跟踪用上一时刻解作热启动 |

## 5. 与后续知识连接

- [[几何Jacobian]]：迭代的引擎；
- [[奇异位形]]：迭代失效的原因；
- [[解析逆运动学]]、[[几何法IK]]：可解析时优先用；
- 工程：MoveIt! IK、机械臂仿真。

## 6. 检索练习（闭卷）

1. 写出 Jacobian 伪逆迭代公式；
2. 解释 DLS 为何在奇异附近稳定；
3. 判断迭代是否收敛的判据；
4. 为什么轨迹跟踪用热启动。

## 7. 通过标准

- 能写出伪逆/DLS 迭代；
- 能理解收敛与失败条件；
- 能处理奇异附近的不稳定。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/系统与硬件/15-控制与机器人学"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 复习

- 下次复习：3 天后重推 DLS；
- 薄弱点写入 [[控制与机器人学错题漏洞入口]]。
