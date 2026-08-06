---
type: study
topic: "Ackermann"
course: "控制与机器人学"
created: 2026-04-18
updated: 2026-08-07
status: completed
difficulty: advanced
stage_moc: "[[🧭 阶段5-状态空间与现代控制]]"
flow: knowledge
kind: derivation
concept: ["Ackermann公式", "极点配置", "状态反馈"]
prerequisites: ["状态反馈", "能控性矩阵"]
related: ["状态反馈", "极点选择"]
upstream: ["[[05-状态空间与现代控制/状态反馈]]"]
source: "Modern Control Engineering (Ogata) Ch.10; Ackermann (1972)"
tags: [学习, 控制与机器人学, 状态反馈]
---

# Ackermann

## 0. 为什么学它

极点配置用标准型对比系数需要做相似变换；**Ackermann 公式**直接在原坐标系由能控性矩阵与期望特征多项式一步求出 $K$——省去变换，编程友好。

## 1. 核心公式

期望闭环特征多项式 $\phi(s)=s^n+\alpha_{n-1}s^{n-1}+\cdots+\alpha_0$（期望极点给定），则

$$K=[0\ \cdots\ 0\ 1]\,\mathcal{C}^{-1}\,\phi(A),$$

其中 $\mathcal{C}=[B\ AB\ \cdots\ A^{n-1}B]$ 为能控性矩阵，$\phi(A)=A^n+\alpha_{n-1}A^{n-1}+\cdots+\alpha_0 I$。

**前提**：$(A,B)$ 能控（$\mathcal{C}$ 可逆）。

## 2. 最小可手算例子

**题目**：$A=\begin{pmatrix}0&1\\-2&-3\end{pmatrix},\ B=(0,1)^\top$，期望极点 $-5,-6$（$\phi(s)=s^2+11s+30$），用 Ackermann 求 $K$。

**解**：$\mathcal{C}=\begin{pmatrix}0&1\\1&-3\end{pmatrix}$，$\mathcal{C}^{-1}=\begin{pmatrix}3&1\\1&0\end{pmatrix}$。
$\phi(A)=A^2+11A+30I=\begin{pmatrix}28&8\\-16&-28\end{pmatrix}$。
$K=[0\ 1]\mathcal{C}^{-1}\phi(A)=[0\ 1]\begin{pmatrix}3&1\\1&0\end{pmatrix}\begin{pmatrix}28&8\\-16&-28\end{pmatrix}$。
$=[1\ 0]\begin{pmatrix}28&8\\-16&-28\end{pmatrix}=(28,8)$ ✓（与对比系数法一致）。

**易错点**：$\phi(A)$ 矩阵代入；$[0\cdots1]$ 行向量位置；$\mathcal{C}^{-1}$ 顺序。

## 3. 常见误区

| 误区 | 正确理解 |
|:---|:---|
| Ackermann 不需要能控 | 必须能控（$\mathcal{C}$ 可逆） |
| 高维病态 | 高阶系统数值敏感，用标准型更稳 |
| 与 LQR 混淆 | Ackermann 是任意配极点，LQR 是最优 |

## 4. 与后续知识连接

- [[状态反馈]]：同目标；
- [[极点选择]]：极点来源；
- [[LQR增益]]：另一种求解。

## 5. 检索练习（闭卷）

1. 写出 Ackermann 公式；
2. 用公式求 $K$；
3. 说明能控前提；
4. 与对比系数法的取舍。

## 6. 通过标准

- 能用 Ackermann 求 $K$；
- 能理解前提；
- 能选择求解方法。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/系统与硬件/15-控制与机器人学"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 复习

- 下次复习：3 天后重算 $K$；
- 薄弱点写入 [[控制与机器人学错题漏洞入口]]。
