---
type: study
topic: "LQR代价函数"
course: "控制与机器人学"
created: 2026-04-18
updated: 2026-08-07
status: completed
difficulty: advanced
stage_moc: "[[🧭 阶段5-状态空间与现代控制]]"
flow: knowledge
kind: derivation
concept: ["LQR", "代价函数", "最优控制"]
prerequisites: ["状态反馈", "状态空间与LQR控制"]
related: ["ARE", "LQR增益", "LQR稳定性"]
upstream: ["[[状态反馈]]"]
source: "Modern Control Engineering (Ogata) Ch.10; 最优控制经典"
tags: [学习, 控制与机器人学, LQR]
---

# LQR代价函数

## 0. 为什么学它

极点配置"拍脑袋"选极点，而 **LQR（线性二次调节）** 把控制问题变成**优化**：最小化"状态偏差 + 控制能量"的加权二次代价。它自动给出**最优**的状态反馈增益，是 MPC 的线性特例。

## 1. 核心代价函数

**连续 LQR**：最小化

$$J=\int_0^\infty \big(x^\top Q x + u^\top R u\big)\,dt,$$

- $Q\succeq0$：状态权重（越大 → 状态越快归零，代价越大）；
- $R\succ0$：控制权重（越大 → 控制越省力）。

**离散 LQR**：$J=\sum_{k=0}^\infty (x_k^\top Q x_k+u_k^\top R u_k)$。

**意义**：$x^\top Qx$ 惩罚状态偏差（性能），$u^\top Ru$ 惩罚控制量（能耗/饱和）——$Q,R$ 的比值决定"快 vs 省"的权衡。

## 2. 权重选择直觉

| 场景 | 权重倾向 |
|:---|:---|
| 快速镇定 | $Q$ 大（尤其对应状态） |
| 节能/防饱和 | $R$ 大 |
| 均衡 | $Q/R$ 折中，Bryson 规则：$Q_{ii}=1/x_{i,max}^2,\ R_{jj}=1/u_{j,max}^2$ |

## 3. 最小可手算例子（Bryson 规则）

**题目**：状态最大允许 $x_{max}=1$，控制最大 $u_{max}=2$，给 $Q,R$ 初值。

**解**：$Q=1/1^2=1$，$R=1/2^2=0.25$——从物理量级出发的合理起点，再调比例。

**易错点**：$Q,R$ 是**相对**权重（同乘常数不改变最优 $K$）；$R$ 必须正定。

## 4. 常见误区

| 误区 | 正确理解 |
|:---|:---|
| 权重越大性能越好 | 状态权重过大 → 控制饱和 |
| $Q,R$ 绝对大小重要 | 相对比值决定 $K$ |
| LQR 处理约束 | 无约束优化；约束需 MPC |

## 5. 与后续知识连接

- [[ARE]]：解的方程；
- [[LQR增益]]：结果；
- [[LQR稳定性]]：为何闭环稳定；
- [[LQR调参]]：权重选择；
- [[MPC代价函数]]：加约束的推广。

## 6. 检索练习（闭卷）

1. 写出 LQR 代价函数；
2. 解释 $Q,R$ 含义；
3. 用 Bryson 规则给初值；
4. 与 MPC 的关系。

## 7. 通过标准

- 能写代价函数；
- 能选权重；
- 能理解与 MPC 的联系。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/系统与硬件/15-控制与机器人学"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 复习

- 下次复习：3 天后重选权重；
- 薄弱点写入 [[控制与机器人学错题漏洞入口]]。
