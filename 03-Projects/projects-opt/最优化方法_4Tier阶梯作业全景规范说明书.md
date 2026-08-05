---
title: "最优化方法 4-Tier 阶梯作业全景规范说明书"
type: project
topic: "最优化方法 4-Tier 阶梯作业规范"
course: "最优化方法"
created: 2026-08-02
updated: 2026-08-02
status: active
flow: project
kind: moc
tags: [最优化方法, 4Tier作业, 阶梯作业, 编程实战, PyTest, EE364A]
---

# 📐 最优化方法 4-Tier 阶梯作业全景规范说明书 (Boyd & Stanford EE364A 范式)

> 本说明书为 **07-最优化方法** 路径（基于 Boyd & Vandenberghe 《Convex Optimization》与 Stanford EE364A）提供严格的 **4-Tier Baseline** 划分标准与测试校验 Harness 规范。

---

## 🧭 4-Tier Baseline 梯队划分原则

```
🟢 L1 - Simple Baseline   │ CVXPY / SciPy.optimize 调包 / 基础一阶梯度求解 / 算例比对
🟡 L2 - Medium Baseline   │ 回溯回退 Line Search / Nesterov 加速 / KKT 最优性条件求解
🔴 L3 - Strong Baseline   │ [核心] 不调用 CVXPY，从零手撕牛顿法、内点法 (Barrier Method)、ADMM 优化器
👑 L4 - Boss Baseline     │ 大规模分布式优化 / Lean 4 定理形式化证明 (凸集分离/弱对偶性)
```

---

## 🎯 最优化方法阶梯作业 4-Tier 细化规格清单

### 1. HW01 - 凸集与凸函数判定 (Convex Sets & Convex Functions)
- **开源溯源**：Boyd Ch 2 & 3 / EE364A Homework 1
- 🟢 **L1**: 在 CVXPY 中建模判定二次规划 (QP) 目标函数的凸性。
- 🟡 **L2**: 验证 Hessian 矩阵正半定性 $\nabla^2 f(x) \succeq 0$。
- 🔴 **L3 (手撕核心)**：**独立完成 Jensen 不等式 $f(\theta x + (1-\theta)y) \le \theta f(x) + (1-\theta)f(y)$ 的严格数学推导与反例构造**。
- 👑 **L4 (Lean 4)**：在 Lean 4 中完成凸集交集仍为凸集的形式化定理证明。

### 2. HW02 - 无约束优化：梯度下降与牛顿法 (Unconstrained Optimization)
- **开源溯源**：Boyd Ch 9 / EE364A Homework 4
- 🟢 **L1**: 使用 SciPy `minimize(method='BFGS')` 求解逻辑回归目标函数。
- 🟡 **L2**: 实现 Armijo 回溯直线搜索 (Backtracking Line Search $\alpha \leftarrow \beta \alpha$)。
- 🔴 **L3 (手撕核心)**：**从零手撕牛顿法 (Newton's Method) 优化器（带 Hessian 矩阵逆与牛顿递减量 $\lambda^2 = \nabla f(x)^T \nabla^2 f(x)^{-1} \nabla f(x)$ 停止准则）**。
- 👑 **L4**: 实现 Nesterov 加速梯度算法 (NAG) 并证明 $O(1/k^2)$ 收敛速率。

### 3. HW03 - 等式约束优化与 Lagrange 对偶 (Equality Constrained Optimization & Duality)
- **开源溯源**：Boyd Ch 5 & 10 / EE364A Homework 5
- 🟢 **L1**: 使用 CVXPY 求解带线性约束的二分投资组合优化问题。
- 🟡 **L2**: 写出拉格朗日对偶函数 $g(\lambda, \nu) = \inf_x L(x, \lambda, \nu)$ 并验证弱对偶定理 $d^* \le p^*$。
- 🔴 **L3 (手撕核心)**：**手撕带等式约束的牛顿法 (Newton's Method with Equality Constraints)**：
  $$ \begin{bmatrix} \nabla^2 f(x) & A^T \\ A & 0 \end{bmatrix} \begin{bmatrix} \Delta x_{nt} \\ w \end{bmatrix} = \begin{bmatrix} -\nabla f(x) \\ 0 \end{bmatrix} $$
- 👑 **L4**: 证明 Slater 条件满足时强对偶性 (Strong Duality $d^* = p^*$) 成立。

### 4. HW04 - 不等式约束与内点法 (Interior-Point Barrier Method)
- **开源溯源**：Boyd Ch 11 / EE364A Homework 7
- 🟢 **L1**: 在 CVXPY 中求解带上下界约束的二次规划问题。
- 🟡 **L2**: 构造对数障碍函数 $\phi(x) = -\sum_{i=1}^m \ln(-f_i(x))$ 并画出中心路径 (Central Path)。
- 🔴 **L3 (手撕核心)**：**从零手撕 Barrier Method (内点法) 主循环与 Centering Step 牛顿内部循环**：
  $$ \text{minimize } t f_0(x) + \phi(x) $$
  逐步递增 $t \leftarrow \mu t$，直到对偶间隙 $m/t < \epsilon$。
- 👑 **L4**: 实现 Primal-Dual Interior-Point Method (主双重内点法)。

### 5. HW05 - 稀疏优化与 ADMM (ADMM & Proximal Gradient)
- **开源溯源**：Boyd ADMM Monograph (2011) / EE364B
- 🟢 **L1**: 使用 scikit-learn Lasso 跑通稀疏特征选择。
- 🟡 **L2**: 实现 Proximal Gradient Descent (近邻梯度下降) 求解 Lasso。
- 🔴 **L3 (手撕核心)**：**从零手撕 ADMM (Alternating Direction Method of Multipliers) 分块更新算法**：
  $$ x^{k+1} := \arg\min_x \left( f(x) + \frac{\rho}{2} \| Ax + B z^k - c + u^k \|_2^2 \right) $$
  $$ z^{k+1} := \arg\min_z \left( g(z) + \frac{\rho}{2} \| A x^{k+1} + B z - c + u^k \|_2^2 \right) $$
  $$ u^{k+1} := u^k + A x^{k+1} + B z^{k+1} - c $$
- 👑 **L4**: 实现分布式 ADMM (Consensus ADMM) 在多节点上的并行求解。

---

## 🧪 测试校验 Harness 规范 (`pytest`)

在 `03-Projects/projects-opt/tests/` 目录下运行单元测试：

```bash
pytest 03-Projects/projects-opt/tests/test_hw02_newton.py
pytest 03-Projects/projects-opt/tests/test_hw04_barrier.py
pytest 03-Projects/projects-opt/tests/test_hw05_admm.py
```
