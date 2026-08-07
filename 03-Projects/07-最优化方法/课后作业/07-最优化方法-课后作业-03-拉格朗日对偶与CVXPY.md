---
type: project
project_type: homework
course: 07-最优化方法
assignment_id: 07-最优化方法-课后作业-03
assignment_level: lesson
assignment_format: problem-set
stage_id: '02'
requires:
  - "[[最优化方法-凸优化与拉格朗日对偶]]"
  - "[[最优化方法-强对偶与Slater条件]]"
  - "[[最优化方法-CVXPY建模与求解器]]"
  - "[[最优化方法-内点法原理]]"
  - "[[最优化方法-罚函数法与障碍法]]"
source_type: official_assignment
created: 2026-08-06
status: active
flow: project
tags:
  - 作业
  - 课后作业
  - 最优化方法
  - 对偶理论
---
# 07-最优化方法-课后作业-03：拉格朗日对偶推导与 CVXPY 组合优化

> **本作业来源与出处**：Stanford EE364A Homework 3 & 4 / Boyd《Convex Optimization》Chapter 5 对偶与金融应用改编。

---

## 1. 学习目标

掌握拉格朗日对偶问题推导与 Markowitz 投资组合优化的 CVXPY 求解。

## 2. 任务边界与知识依赖

对偶理论（Duality）是整个最优化中最具艺术性的部分。从原问题（Primal）构造对偶问题（Dual），不仅可以降维求解、获得影子价格，更可以通过 KKT 条件解出闭式解。本作业将结合对偶证明与金融界经典的 Markowitz 资产组合配置模型，让你真正体会“强对偶性”与对偶变量的魅力。

---

### 关联知识点与前置定理

做题前，请确保已复习以下知识卡：
1. **[[最优化方法-凸优化与拉格朗日对偶]]**：
   - **拉格朗日函数**：$L(x, \lambda, \nu) = f_0(x) + \sum \lambda_i f_i(x) + \sum \nu_i h_i(x)$。
   - **对偶函数**：$g(\lambda, \nu) = \inf_{x} L(x, \lambda, \nu)$。
   - **弱对偶性**：$d^\star \le p^\star$ 永远成立。
2. **[[最优化方法-强对偶与Slater条件]]**：
   - **Slater 条件**：凸优化问题若存在严格可行点（Strictly Feasible Point），则强对偶成立 $d^\star = p^\star$。
3. **[[最优化方法-二次规划与CVXPY]]**：
   - 使用 CVXPY 求解二次规划并提取对偶变量（`constraint.dual_value`）。

---

## 3. 详细题目与要求

### 题目 1：标准线性规划 (LP) 的对偶函数推导（手推题）

**原问题 (Primal)**：
$$\min_{x \in \mathbf{R}^n} c^T x \quad \text{s.t.} \quad A x = b, \ x \succeq 0$$

**任务**：
1. 完整写出拉格朗日函数 $L(x, \lambda, \nu)$（注：$\lambda \succeq 0$ 对应 $x \succeq 0$ 的约束）。
2. 推导下确界 $g(\lambda, \nu) = \inf_{x} L(x, \lambda, \nu)$，并给出对偶问题 (Dual) 的标准形式。
3. 验证对偶问题也是一个线性规划。

#### 💡 小白解题提示 (Hints)：

1. **提示 1 (写出拉格朗日函数)**：由于约束为 $-x \le 0$ 和 $Ax - b = 0$，故 $L(x, \lambda, \nu) = c^T x - \lambda^T x + \nu^T (Ax - b) = (c - \lambda + A^T \nu)^T x - b^T \nu$。
2. **提示 2 (求关于 $x$ 的 infimum)**：因为 $(c - \lambda + A^T \nu)^T x$ 关于 $x$ 是线性的，如果系数向量不全为 0，对 $x$ 取下界就会趋于 $-\infty$！
3. **提示 3 (得出对偶隐式约束)**：因此只有当 $c - \lambda + A^T \nu = 0$ 时，对偶函数才有有限值 $-b^T \nu$。结合 $\lambda \succeq 0$，推导出对偶问题约束 $A^T \nu \le c$。

---

### 题目 2：Markowitz 均值-方差投资组合优化（编程与金融建模题）

**背景**：投资者希望选择 $n$ 种资产的投资权重 $w \in \mathbf{R}^n$，在满足期望收益不低于 $\mu_{\mathrm{target}}$ 的前提下，最小化投资组合的风险（方差）：
$$\min_{w} w^T \Sigma w \quad \text{s.t.} \quad \mathbf{1}^T w = 1, \ \mu^T w \ge \mu_{\mathrm{target}}, \ w \ge 0$$
其中 $\Sigma$ 是资产协方差矩阵，$\mu$ 是期望收益率向量。

**任务**：
1. 使用 Python 中的 `cvxpy` 库构建该二次规划模型。
2. 扫描不同的 $\mu_{\mathrm{target}}$，绘制**有效前沿 (Efficient Frontier)** 曲线。
3. 打印出约束 $\mathbf{1}^T w = 1$ 的对偶变量（影子价格）。

## 运行环境与依赖

- **Python 环境**：Python 3.10+，包含 `cvxpy`, `numpy`, `matplotlib`
- **运行命令**：`python hw03_markowitz.py`

#### Python Starter Code 框架：

```python
import cvxpy as cp
import numpy as np
import matplotlib.pyplot as plt

# 模拟 4 只股票的数据
np.random.seed(42)
n = 4
mu = np.array([0.12, 0.10, 0.15, 0.08])
# 生成正定协方差矩阵
A = np.random.randn(n, n)
Sigma = A.T @ A + 0.05 * np.eye(n)

# 构建有效前沿扫描
target_returns = np.linspace(0.08, 0.14, 20)
portfolio_risks = []
dual_values = []

for r_target in target_returns:
    w = cp.Variable(n)
    risk = cp.quad_form(w, Sigma)
    
    eq_constraint = (cp.sum(w) == 1)
    ineq_constraint = (mu.T @ w >= r_target)
    bound_constraint = (w >= 0)
    
    prob = cp.Problem(cp.Minimize(risk), [eq_constraint, ineq_constraint, bound_constraint])
    prob.solve()
    
    portfolio_risks.append(np.sqrt(prob.value))
    dual_values.append(eq_constraint.dual_value)

# 可视化有效前沿
plt.figure(figsize=(8, 5))
plt.plot(portfolio_risks, target_returns, 'b-o', label='Efficient Frontier')
plt.xlabel('Portfolio Volatility (Standard Deviation)')
plt.ylabel('Expected Return')
plt.title('Markowitz Portfolio Optimization')
plt.grid(True)
plt.legend()
plt.show()

# 检验断言
print("影子价格（对偶变量样本）:", dual_values[0])
assert len(portfolio_risks) == 20, "前沿计算点数不符合要求"
```

---

## 📊 100 分制评分 Rubric

| 维度 | 分值 | 得分标准 |
|:---|:---:|:---|
| **题目 1 (LP 对偶推导)** | 40 分 | - 准确写出拉格朗日函数 $L(x,\lambda,\nu)$（15分）；<br>- 准确推导出对偶约束 $A^T \nu \le c$ 与对偶目标（25分）。 |
| **题目 2 (Markowitz 建模)** | 40 分 | - CVXPY 模型约束与目标函数构建正确（20分）；<br>- 成功提取对偶变量并成功绘制有效前沿图（20分）。 |
| **测试与断言校验** | 10 分 | - 代码顺利运行，测试断言通过。 |
| **文档与格式规范** | 10 分 | - 推导严谨，符号完整统一。 |


---

## 提交产物与格式

1. **提交产物**：完整代码与推导实验报告。
2. **验收标准**：代码无 Error，计算结果与理论推导完全匹配。


---

## 6. 引导提示与自检

- 检查梯度与 Hessian 计算公式推导。
- 验证凸性与约束条件可行性。


---

## 7. 来源与后续入口

- **来源**：EE364A / Numerical Optimization。
- **后续入口**：参见阶段 MOC 与课程总索引。
