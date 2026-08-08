---
type: study
topic: "Lyapunov稳定"
course: "控制与机器人学"
created: 2026-04-18
updated: 2026-08-07
status: completed
difficulty: advanced
stage_moc: "[[🧭 阶段5-状态空间与现代控制]]"
flow: knowledge
kind: derivation
concept: ["Lyapunov稳定", "李雅普诺夫函数", "非线性稳定性"]
prerequisites: ["特征值分析", "Jacobian线性化"]
related: ["LQR稳定性", "特征值分析"]
upstream: ["[[特征值分析]]"]
source: "Modern Control Engineering (Ogata) Ch.9; 非线性系统经典教材"
tags: [学习, 控制与机器人学, 稳定性]
---

# Lyapunov稳定

## 0. 为什么学它

特征值只能判**线性**系统的稳定性；非线性系统（摆、倒立摆、车辆极限）需更一般的理论。**Lyapunov 稳定**通过"能量函数单调下降"的思想判断稳定性，不求解方程——是现代控制与 LQR 稳定性证明的基础。

## 1. 核心方法

**基本思想**：找候选李雅普诺夫函数 $V(x)>0$（能量），若 $\dot V(x)<0$（能量单调降），则系统渐近稳定。

**线性系统**（Lyapunov 方程）：$\dot x=Ax$ 渐近稳定 ⟺ 对任意 $Q>0$，存在 $P>0$ 满足

$$A^\top P+PA=-Q.$$

此时 $V(x)=x^\top P x$ 为李雅普诺夫函数（$\dot V=-x^\top Qx<0$）。

**LQR 连接**：Riccati 方程的解 $P$ 正是 Lyapunov 方程的解 → LQR 闭环稳定由 $V=x^\top Px$ 直接证明（见 [[LQR稳定性]]）。

## 2. 最小可手算例子（线性 Lyapunov 方程）

**题目**：$A=\begin{pmatrix}0&1\\-2&-3\end{pmatrix}$，$Q=I$，求 $P$ 验证稳定。

**解**：解 $A^\top P+PA=-I$：设 $P=\begin{pmatrix}p_{11}&p_{12}\\p_{12}&p_{22}\end{pmatrix}$，逐元素解方程组得 $P=\begin{pmatrix}1.25&0.25\\0.25&0.25\end{pmatrix}$（正定 ✓）。$V=x^\top Px$ 为李雅普诺夫函数 → 渐近稳定（与特征值 $-1,-2$ 一致）。

**易错点**：$P$ 必须正定；解 Lyapunov 方程按元素对齐。

## 3. 常见误区

| 误区 | 正确理解 |
|:---|:---|
| $V$ 选择唯一 | 不唯一，找到一个即可证稳定 |
| $\dot V\le0$ 就渐近稳定 | 需 $\dot V<0$（或不变集论证）才渐近 |
| 线性化稳定=全局稳定 | 李雅普诺夫局部结论，非线性需全局分析 |

## 4. 与后续知识连接

- [[LQR稳定性]]：Riccati ↔ Lyapunov；
- [[特征值分析]]：线性特例；
- [[状态转移]]：稳定性基础；
- 工程：非线性控制器稳定性证明。

## 5. 检索练习（闭卷）

1. 陈述 Lyapunov 稳定思想；
2. 写线性 Lyapunov 方程；
3. 解简单系统的 $P$；
4. 说明 LQR 与 Lyapunov 的联系。

## 6. 通过标准

- 能使用 Lyapunov 方程；
- 能证明线性系统稳定；
- 能理解非线性扩展。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/系统与硬件/15-控制与机器人学"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 复习

- 下次复习：3 天后重解方程；
- 薄弱点写入 [[控制与机器人学错题漏洞入口]]。
