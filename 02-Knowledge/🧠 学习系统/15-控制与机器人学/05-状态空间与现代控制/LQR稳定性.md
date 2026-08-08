---
type: study
topic: "LQR稳定性"
course: "控制与机器人学"
created: 2026-04-18
updated: 2026-08-07
status: completed
difficulty: advanced
stage_moc: "[[🧭 阶段5-状态空间与现代控制]]"
flow: knowledge
kind: derivation
concept: ["LQR稳定性", "Lyapunov", "最优控制性质"]
prerequisites: ["LQR增益", "Lyapunov稳定"]
related: ["Lyapunov稳定", "ARE", "MPC稳定性"]
upstream: ["[[LQR增益]]"]
source: "Modern Control Engineering (Ogata) Ch.10; 最优控制经典"
tags: [学习, 控制与机器人学, LQR]
---

# LQR稳定性

## 0. 为什么学它

"最优"不等于"稳定"——但 **LQR 的闭环必定渐近稳定**（能控 + 适当 $Q$ 下）。这个保证来自 ARE 解 $P$ 恰好是 Lyapunov 函数，一石二鸟：LQR 顺便自带稳定性证明。

## 1. 核心定理

**LQR 稳定性**：$(A,B)$ 能控，$Q\succeq0,\ R\succ0$（且 $(A,Q^{1/2})$ 能观）⟹ LQR 闭环 $A-BK$ **渐近稳定**。

**证明思路**：ARE $A^\top P+PA-PBR^{-1}B^\top P+Q=0$ 整理为

$$(A-BK)^\top P+P(A-BK)=-(Q+K^\top RK)<0.$$

这是 Lyapunov 方程 → $V(x)=x^\top Px$ 为李雅普诺夫函数（$P>0,\dot V<0$）→ 渐近稳定 ✓。

**含义**：LQR 的"最优"自动包含"稳定"——无需再单独验证。

## 2. 最小可手算例子（验证）

**题目**：$A=0,B=1,Q=1,R=1$，验证 LQR 闭环稳定。

**解**：$P=1,\ K=1$，闭环 $A-BK=-1<0$ 稳定 ✓；Lyapunov：$(A-BK)^\top P+P(A-BK)=-2<0$ ✓。

**易错点**：$(A,Q^{1/2})$ 能观条件（防止状态"免费"偏离）；半正定 $Q$ 时需该条件保证稳定。

## 3. 常见误区

| 误区 | 正确理解 |
|:---|:---|
| 最优控制不保证稳定 | LQR 在能控+能观条件下必然稳定 |
| 只验证 $A-BK$ 特征值 | Lyapunov 证明更本质，且适用于数值病态 |
| 忽略能观条件 | $Q$ 半正定且 $(A,Q^{1/2})$ 不可观时可能不稳定 |

## 4. 与后续知识连接

- [[Lyapunov稳定]]：证明工具；
- [[ARE]]：方程来源；
- [[MPC稳定性]]：LQR 是 MPC 稳定性的特例（终端代价）。

## 5. 检索练习（闭卷）

1. 陈述 LQR 稳定性定理；
2. 用 Lyapunov 证明闭环稳定；
3. 说明能观条件；
4. 与 MPC 稳定性的联系。

## 6. 通过标准

- 能证明/理解 LQR 稳定性；
- 能说明前提条件；
- 能关联 MPC。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/系统与硬件/15-控制与机器人学"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 复习

- 下次复习：3 天后重做证明；
- 薄弱点写入 [[控制与机器人学错题漏洞入口]]。
