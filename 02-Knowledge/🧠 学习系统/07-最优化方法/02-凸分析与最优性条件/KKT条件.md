---
type: study
topic: "KKT条件"
created: 2026-04-18
updated: 2026-08-01
status: completed
difficulty: advanced
concept: ["KKT条件", "拉格朗日对偶", "约束最优性"]
prerequisites: ["拉格朗日乘子法", "凸优化", "对偶问题"]
related: ["Slater条件", "互补松弛", "约束资格条件"]
tags: [学习, 最优化方法, KKT]
flow: knowledge
kind: derivation
---

# KKT 条件

Karush–Kuhn–Tucker（KKT）条件把约束优化问题的最优点描述为原问题可行性、对偶可行性、驻点条件和互补松弛的联合解。

## 1. 问题与拉格朗日函数

考虑可微问题

$$
\begin{aligned}
\min_x\quad & f_0(x)\\
\text{s.t.}\quad & f_i(x)\le 0,\quad i=1,\ldots,m,\\
& h_j(x)=0,\quad j=1,\ldots,p.
\end{aligned}
$$

定义拉格朗日函数

$$
L(x,\lambda,\nu)=f_0(x)+\sum_{i=1}^m\lambda_i f_i(x)+\sum_{j=1}^p\nu_j h_j(x),
$$

其中不等式乘子要求 $\lambda_i\ge0$，等式乘子 $\nu_j$ 不限符号。

## 2. 四组 KKT 条件

候选点 $(x^\star,\lambda^\star,\nu^\star)$ 满足：

1. **原始可行性**
   $$f_i(x^\star)\le0,\qquad h_j(x^\star)=0.$$
2. **对偶可行性**
   $$\lambda_i^\star\ge0.$$
3. **驻点条件**
   $$\nabla f_0(x^\star)+\sum_i\lambda_i^\star\nabla f_i(x^\star)+\sum_j\nu_j^\star\nabla h_j(x^\star)=0.$$
4. **互补松弛**
   $$\lambda_i^\star f_i(x^\star)=0.$$

互补松弛表示：约束若未激活，即 $f_i(x^\star)<0$，其乘子必须为 0；乘子若为正，对应约束必须取等号。

## 3. 必要还是充分

- 对一般非凸问题，KKT 通常需要约束资格条件才能成为局部最优的必要条件；满足 KKT 仍可能只是局部最优、极大点或鞍点。
- 若 $f_0,f_i$ 为凸函数、$h_j$ 为仿射函数，那么任何满足 KKT 的点都是全局最优。
- 若该凸问题还满足 Slater 条件，则强对偶成立，KKT 对最优性既必要又充分。

所以不能省略“凸性”和“约束资格条件”就直接写“KKT 等价于最优”。

## 4. 最小算例

求

$$
\min_x (x-2)^2\quad\text{s.t.}\quad x\le1.
$$

写成 $f_1(x)=x-1\le0$，拉格朗日函数

$$
L=(x-2)^2+\lambda(x-1).
$$

KKT 条件为

$$
x\le1,\quad\lambda\ge0,\quad2(x-2)+\lambda=0,\quad\lambda(x-1)=0.
$$

若约束不激活，则 $\lambda=0$ 得 $x=2$，违反 $x\le1$，排除。故约束激活，$x^\star=1$；代入驻点条件得 $\lambda^\star=2$。目标值为 1。

验证：无约束最小点 2 位于可行域右侧，投影到可行区间 $(-\infty,1]$ 的边界正是 1，与 KKT 解一致。

## 5. 解题流程

1. 把不等式统一写成 $f_i(x)\le0$，避免乘子符号写反。
2. 写出完整拉格朗日函数。
3. 列四组条件，不只写梯度为零。
4. 按活跃约束组合求候选解。
5. 检查原始/对偶可行性并排除非法候选。
6. 根据凸性、二阶条件或目标值比较判断候选解性质。

## 6. 常见误区

- 把互补松弛误写为“$\lambda_i=0$ 且 $f_i(x)=0$”；实际是乘积为零，二者至少一个为零。
- 改变不等式方向后忘记同步改变乘子符号约定。
- 在非凸问题中把任意 KKT 点当作全局最优。
- 未验证约束资格条件，就声称局部最优一定满足 KKT。

## 7. 验证与自测

- 重新解上面的单变量例子，并验证 $x^\star=1$ 同时满足四组条件。
- 若把约束改成 $x\ge1$，先统一写成 $1-x\le0$，再检查最优点和乘子符号。
- 说明[[02-Knowledge/🧠 学习系统/07-最优化方法/02-凸分析与最优性条件/Slater条件|Slater 条件]]为什么能把凸问题中的 KKT 从充分条件提升为必要且充分条件。

## 参考资料

- Boyd, S. & Vandenberghe, L. *Convex Optimization*, Chapter 5, Stanford 官方开放版：https://web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf
- Boyd & Vandenberghe, *Duality and KKT Conditions* 课程讲义：https://web.stanford.edu/~boyd/cvxbook/bv_cvxslides.pdf
