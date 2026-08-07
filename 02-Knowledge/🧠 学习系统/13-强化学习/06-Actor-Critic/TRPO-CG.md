---
type: study
topic: "TRPO-CG"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段6-Actor-Critic]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["TRPO-CG", "TRPO 共轭梯度"]
upstream: ["[[TRPO-KL]]", "[[TRPO-信任区域]]"]
tags: [学习, 强化学习]
---

# TRPO-CG

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段6-Actor-Critic|返回阶段页]]

## 动机
TRPO 需解"带 KL 约束的自然梯度"——用共轭梯度（CG）近似，避免显式求大 Fisher 逆。

## 正式定义 / 公式
用 CG 解 F x = g（F 为 Fisher 矩阵，g 为策略梯度），得自然梯度方向；再线搜满足 KL≤δ 的步长。
F 用 Hessian-vector product 近似，不显式构造矩阵。

## 最小手算例子
<!-- NUMEX -->共轭梯度解 Ax=b：A=[2,1; 1,2]，b=[3,3]，精确解 x=[1,1]（验证 A·[1,1]=[3,3]）。CG 用步长 α=(r·r)/(p·Ap) 沿共轭方向迭代，k 维问题至多 k 步收敛。

每次更新：CG 迭代若干次得方向，沿该方向试步长直到 KL 达标。

## 对比与常见错误
- 与 NPG：NGP 显式 F^{−1}；TRPO 用 CG 近似，省内存更可行。
- 常见错误：以为 TRPO 直接求 F^{−1}——它刻意避免以省开销。

## 闭卷自测
1. TRPO 用什么求自然梯度？
2. 为何避免显式 F^{−1}？
## 学完后可以完成

```dataview
TABLE assignment_level, source_type FROM "03-Projects"
WHERE contains(requires, this.file.link)
```

## 相关下游知识

```dataview
LIST FROM "02-Knowledge/🧠 学习系统"
WHERE contains(upstream, this.file.link)
```
