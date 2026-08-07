---
type: project
project_type: homework
course: 07-最优化方法
assignment_id: 07-最优化方法-课后作业-00
assignment_level: lesson
assignment_format: lab
stage_id: '01'
requires: ["[[最优化方法-多元梯度与海森矩阵]]", "[[最优化方法-二次型与特征值变分性]]", "[[最优化方法-二次规划与CVXPY]]"]
source_type: local_integration_task
created: 2026-08-06
status: completed
flow: project
tags:
  - 作业
  - 课后作业
  - 数学基础
  - NumPy
---



# 07-最优化方法-课后作业-00-数学基础与NumPy计算

## 1. 学习目标

本作业旨在检验学习者对最优化方法基础数学工具的掌握情况。通过求解多元函数的梯度与海森矩阵，分析二次型的正定性与 Rayleigh 商，学习者将能熟练使用 NumPy 完成最优化中的基础线性代数与多元微积分数值计算。

---

## 2. 任务边界与知识依赖

* [[最优化方法-多元梯度与海森矩阵]]
* [[最优化方法-二次型与特征值变分性]]
* [[最优化方法-二次规划与CVXPY]]

---

### 前置依赖

* 完成 [[最优化方法-多元梯度与海森矩阵]] 的阅读与推导
* 具备 Python 3.8+ 与 NumPy 基础

---

### 问题背景

最优化算法的绝大多数迭代公式（如最速下降、牛顿法）都需要高效计算函数在特定点上的梯度向量 $\nabla f(x)$ 和 Hessian 矩阵 $\nabla^2 f(x)$。理解 Hessian 矩阵的特征值与正定性是分析算法收敛速率及二次型曲率分布的基础。

---

## 3. 详细题目与要求

### 任务 1：多元梯度与 Hessian 矩阵推导及数值验证

考虑经典的 Rosenbrock 函数（香蕉函数）：
$$f(x_1, x_2) = 100(x_2 - x_1^2)^2 + (1 - x_1)^2$$

1. **解析推导**：手工推导其梯度 $\nabla f(x)$ 与 Hessian 矩阵 $\nabla^2 f(x)$ 的闭形式表达。
2. **NumPy 实现**：编写 Python 函数 `rosenbrock_grad_hess(x)`，输入 $x = [x_1, x_2]^T$，返回标量值 $f(x)$、梯度向量与 Hessian 矩阵。
3. **数值验证**：计算在点 $x^{(1)} = [0, 0]^T$ 和 $x^{(2)} = [1, 1]^T$ 处的函数值、梯度与 Hessian 矩阵，判断 Hessian 在该点是否正定。

### 任务 2：二次型变分与 Rayleigh 商

已知对称矩阵：
$$A = \begin{bmatrix} 4 & 1 \\ 1 & 3 \end{bmatrix}$$

1. 使用 `numpy.linalg.eigh` 计算 $A$ 的特征值与特征向量。
2. 构造单位圆上的向量网格 $x(\theta) = [\cos\theta, \sin\theta]^T$，绘制 Rayleigh 商 $R(x) = \frac{x^T A x}{x^T x}$ 随角度 $\theta \in [0, 2\pi]$ 的变分曲线。
3. 验证 Rayleigh 商的最大值与最小值分别等于 $A$ 的最大与最小特征值。

---

## 运行环境与依赖

* **Python 环境**：Python 3.10+，包含 `numpy`, `scipy`, `matplotlib`
* **输入规范**：$2 \times 1$ 实数向量 $x \in \mathbb{R}^2$。
* **输出规范**：
  * `f`: float
  * `grad`: ndarray of shape `(2,)`
  * `hess`: ndarray of shape `(2, 2)`

---

## 提交产物与格式

### 1. 提交文件
- 脚本文件 `homework_00_math_basics.py`

### 2. 评分标准 (Rubric)
| 检查项 | 满分 | 判定条件 |
| :--- | :--- | :--- |
| Rosenbrock 解析与代码对应 | 40分 | 代码计算结果与解析解完全一致，在 $[1, 1]^T$ 处梯度为零 |
| Hessian 正定性判定 | 30分 | 正确给出 $x^{(1)}$ 与 $x^{(2)}$ 处 Hessian 的特征值并准确判断正定性 |
| Rayleigh 商变分验证 | 30分 | 正确画出变分曲线并严格论证特征值界限 |

---

## 6. 引导提示与自检

* **错误 1**：在计算 $100(x_2 - x_1^2)^2$ 梯度时漏乘复合导数项。
* **错误 2**：混淆二阶偏导求导顺序导致 Hessian 不对称。


---

## 7. 来源与后续入口

- **来源**：本题综合考查《Mathematics for Machine Learning》第 5-7 章多元微积分与二次型计算。
- **后续入口**：完成本作业后，可继续完成 [[07-最优化方法-阶段作业-01-数学基础与CVXPY建模]]。
