---
type: study
topic: "LQI"
course: "控制与机器人学"
created: 2026-04-18
updated: 2026-08-07
status: completed
difficulty: advanced
stage_moc: "[[🧭 阶段5-状态空间与现代控制]]"
flow: knowledge
kind: derivation
concept: ["LQI", "积分增广", "无差跟踪"]
prerequisites: ["LQR增益", "LQR伺服"]
related: ["LQR伺服", "参考增益"]
upstream: ["[[LQR伺服]]"]
source: "Modern Control Engineering (Ogata) Ch.10; 伺服系统教材"
tags: [学习, 控制与机器人学, LQR]
---

# LQI

## 0. 为什么学它

纯 LQR 对参考跟踪有稳态误差（模型不精确时前馈失效）。**LQI（LQR with Integral）**把输出误差的积分加入状态，自动消除稳态误差——"最优的 PI 控制"，跟踪控制的稳健解。

## 1. 核心方法（积分增广）

对系统 $\dot x=Ax+Bu,\ y=Cx$，引入 $\dot x_I = r-y = e$（误差积分），增广：

$$\frac{d}{dt}\begin{pmatrix}x\\x_I\end{pmatrix}=\begin{pmatrix}A&0\\-C&0\end{pmatrix}\begin{pmatrix}x\\x_I\end{pmatrix}+\begin{pmatrix}B\\0\end{pmatrix}u+\begin{pmatrix}0\\1\end{pmatrix}r.$$

对增广系统做 LQR（权重含 $Q_I$ 对应 $x_I$），得 $u=-Kx-K_I x_I$。

**性质**：积分项使稳态误差为零（型别提升）；代价是相位滞后（需要合适 $Q_I$）。

## 2. 最小可手算例子（概念验证）

**题目**：一阶系统 $\dot x=ax+bu$，LQI 控制结构？

**解**：增广状态 $(x,x_I)$，$u=-k_x x-k_I x_I$。稳态 $x\to r$ 时 $x_I$ 为常数，$\dot x_I=0$ 即 $r-y=0$ → 无稳态误差 ✓。

**易错点**：$Q_I$ 过大积分过强 → 振荡；增广后能控性需重新检查。

## 3. 常见误区

| 误区 | 正确理解 |
|:---|:---|
| LQI 不需要模型 | 仍基于模型，只是鲁棒到模型误差 |
| 积分权重随意 | $Q_I$ 决定积分强度，需调 |
| 增广后仍是原系统能控 | 增广系统能控性需重验 |

## 4. 与后续知识连接

- [[LQR伺服]]：伺服框架；
- [[参考增益]]：前馈替代；
- [[I控制]]：经典对应；
- 工程：位置伺服、横向跟踪。

## 5. 检索练习（闭卷）

1. 写出 LQI 增广系统；
2. 解释无差跟踪机制；
3. 说明 $Q_I$ 的作用；
4. 与前馈伺服的取舍。

## 6. 通过标准

- 能构造 LQI；
- 能解释消差；
- 能权衡与前馈。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/系统与硬件/15-控制与机器人学"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 复习

- 下次复习：3 天后重构造 LQI；
- 薄弱点写入 [[控制与机器人学错题漏洞入口]]。
