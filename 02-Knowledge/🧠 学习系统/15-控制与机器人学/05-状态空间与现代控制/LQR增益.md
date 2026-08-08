---
type: study
topic: "LQR增益"
course: "控制与机器人学"
created: 2026-04-18
updated: 2026-08-07
status: completed
difficulty: advanced
stage_moc: "[[🧭 阶段5-状态空间与现代控制]]"
flow: knowledge
kind: derivation
concept: ["LQR增益", "最优状态反馈", "Riccati"]
prerequisites: ["ARE", "LQR代价函数"]
related: ["ARE", "LQR稳定性", "LQR调参"]
upstream: ["[[ARE]]"]
source: "Modern Control Engineering (Ogata) Ch.10"
tags: [学习, 控制与机器人学, LQR]
---

# LQR增益

## 0. 为什么学它

LQR 的输出就是**最优状态反馈增益 $K$**：$u=-Kx$。$K$ 由 ARE 解 $P$ 直接得到，自动在性能与控制能量间最优权衡——与手选极点的状态反馈相比，LQR 增益是"最优的极点位置"。

## 1. 核心公式

**连续 LQR 最优增益**：

$$K=R^{-1}B^\top P,$$

其中 $P$ 为 ARE 正定解。控制律 $u=-Kx+v$。

**离散**：$K=(R+B^\top PB)^{-1}B^\top PA$。

**闭环**：$\dot x=(A-BK)x$，极点由 $Q,R$ 隐含决定（越"重状态"极点越远）。

## 2. 最小可手算例子

**题目**：$A=\begin{pmatrix}0&1\\0&-1\end{pmatrix},B=(0,1)^\top,Q=I_2,R=1$，求 $K$。

**解**：解 ARE 得 $P=\begin{pmatrix}2.73&1\\1&0.73\end{pmatrix}$（近似）；$K=R^{-1}B^\top P=(1,\ 0.73)$。闭环 $A-BK=\begin{pmatrix}0&1\\-1&-1.73\end{pmatrix}$ 特征值 $-0.87\pm j0.5$（稳定欠阻尼）✓。

**易错点**：$K$ 是行向量；$B^\top P$ 的维度；用数值求解器验证。

## 3. 常见误区

| 误区 | 正确理解 |
|:---|:---|
| $K$ 与极点配置无关 | LQR 隐含配置"最优"极点 |
| 权重改变 $K$ 不变 | $Q,R$ 变则 $P,K$ 变 |
| 忽略离散/连续区别 | 连续与离散的 $K$ 公式不同 |

## 4. 与后续知识连接

- [[ARE]]：来源；
- [[LQR稳定性]]：闭环性质；
- [[LQR调参]]：权重→增益；
- [[状态反馈]]：一般框架。

## 5. 检索练习（闭卷）

1. 写出 $K$ 公式；
2. 求简单系统的 $K$；
3. 说明 $Q,R$ 与 $K$ 的关系；
4. 与极点配置的区别。

## 6. 通过标准

- 能求 LQR 增益；
- 能分析闭环；
- 能理解最优性。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/系统与硬件/15-控制与机器人学"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 复习

- 下次复习：3 天后重求 $K$；
- 薄弱点写入 [[控制与机器人学错题漏洞入口]]。
