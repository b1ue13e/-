---
type: project
project_type: homework
course: "数值分析"
assignment_id: "数值分析-HW06"
assignment_level: lesson
assignment_format: lab
stage_id: "03"
requires: ["[[03-非线性与ODE数值解/数值分析-非线性方程求解与Newton法|数值分析-非线性方程求解与Newton法]]"]
source_type: official_assignment
created: 2026-08-08
updated: 2026-08-08
status: active
flow: project
tags: [作业, 课后作业, 数值分析, 非线性求解, Newton法, 雅可比矩阵, 阻尼线搜索]
---

# 数值分析-课后作业-06-非线性方程求解与Newton法

> 对齐官方源：**MIT 18.330 Problem Set 4 (Nonlinear Equations & Newton's Method)** 与 **FNC Chapter 6**

---

## 1. 学习目标与动机
- 深刻理解单变量与多维非线性方程组求根的局部二阶代数收敛性；
- 独立编写多维 Newton-Raphson 求解器，解析推导并组装雅可比矩阵（Jacobian Matrix）；
- 引入 Armijo 阻尼线搜索（Backtracking Line Search），克服初值远离根时的发散问题。

---

## 2. 任务边界与输入输出
- **输入**：非线性向量函数 $F: \mathbb{R}^n \to \mathbb{R}^n$、解析雅可比矩阵函数 $J_F(x)$、初值 $x_0$ 及残差容差 $\tau = 10^{-12}$。
- **输出**：近似根 $x^*$、迭代步数、残差范数序列与局部二次收敛率比值 $\|e_{k+1}\| / \|e_k\|^2$。

---

## 3. 详细实验任务与算法规范

### 任务 1：一维 Newton 法与收敛阶实测
对非线性方程 $f(x) = x^3 - 2x - 5 = 0$（真根 $x^* \approx 2.0945514815423265$）：
1. 编写 Newton 迭代 $x_{k+1} = x_k - \frac{f(x_k)}{f'(x_k)}$；
2. 验证误差序列 $e_k = |x_k - x^*|$，实测渐近误差常数 $C = \lim \frac{e_{k+1}}{e_k^2} = \frac{|f''(x^*)|}{2|f'(x^*)|}$。

### 任务 2：多维非线性系统阻尼 Newton-Raphson 求解器
求解二维非线性方程组：
$$\begin{cases}
f_1(x_1, x_2) = x_1^2 + x_2^2 - 4 = 0 \\
f_2(x_1, x_2) = e^{x_1} + x_2 - 1 = 0
\end{cases}$$
1. 解析求出雅可比矩阵 $J(x_1, x_2) = \begin{bmatrix} 2x_1 & 2x_2 \\ e^{x_1} & 1 \end{bmatrix}$；
2. 每次迭代求解线性增量方程 $J(x_k) \Delta x_k = -F(x_k)$；
3. 引入步长 $\alpha \in (0, 1]$，更新 $x_{k+1} = x_k + \alpha \Delta x_k$，满足 Armijo 充分下降准则 $\|F(x_k + \alpha \Delta x_k)\| < (1 - 10^{-4}\alpha) \|F(x_k)\|$。

---

## 4. 提交产物与代码规范
- 代码文件：`03-Projects/35-数值分析/scripts/hw06_newton_raphson.py`
- 自动化测试：集成至 `03-Projects/35-数值分析/tests/test_numerical_analysis.py`

---

## 5. 验收标准（Rubric）

| 验收维度 | 达标分 | 满分要点 |
| :--- | :---: | :--- |
| **单变量二次收敛** | 30 | 误差比值 $\|e_{k+1}\| / \|e_k\|^2$ 收敛至理论常数（偏差 $< 10^{-2}$） |
| **多维 Newton 求解** | 40 | 二维非线性系统在 10 步内收敛至残差范数 $< 10^{-12}$ |
| **阻尼线搜索鲁棒性** | 30 | 在远离根的不良初值（如 $(5, 5)$）下依然能稳定收敛至真解 |

---

## 6. 引导自检与易错陷阱
- **陷阱**：直接对雅可比矩阵求逆 `inv(J) @ (-F)`，不仅运算昂贵且极度不稳定；必须调用 `solve(J, -F)` 求解增量方程。

---

## 7. Starter Code 与可执行基线

```python
import numpy as np

def newton_nd(F_func, J_func, x0, tol=1e-12, max_iter=50):
    x = x0.copy().astype(np.float64)
    for it in range(max_iter):
        F_val = F_func(x)
        if np.linalg.norm(F_val) < tol:
            return x, it, True
        J_val = J_func(x)
        delta_x = np.linalg.solve(J_val, -F_val)
        # 阻尼线搜索
        alpha = 1.0
        while np.linalg.norm(F_func(x + alpha * delta_x)) >= np.linalg.norm(F_val) and alpha > 1e-4:
            alpha *= 0.5
        x += alpha * delta_x
    return x, max_iter, False
```
