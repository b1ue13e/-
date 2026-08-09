---
type: project
project_type: homework
course: "数值分析"
assignment_id: "数值分析-HW05"
assignment_level: lesson
assignment_format: lab
stage_id: "02"
requires: ["[[02-插值积分与逼近/数值分析-数值积分与Gauss求积|数值分析-数值积分与Gauss求积]]"]
source_type: official_assignment
created: 2026-08-08
updated: 2026-08-08
status: active
flow: project
tags: [作业, 课后作业, 数值分析, 数值积分, Gauss求积, 复合Simpson]
---

# 数值分析-课后作业-05-数值积分与Gauss求积

> 对齐官方源：**MIT 18.330 Problem Set 3 (Numerical Quadrature)** 与 **FNC Chapter 5**

---

## 1. 学习目标与动机
- 掌握代数精度的本质，理解 $n$ 点 Gauss-Legendre 为什么能达到 $2n-1$ 次代数精度；
- 独立编写 Golub-Welsch 算法，通过对称三对角矩阵特征值直接求解 Gauss 节点与权重；
- 实现自适应复合 Simpson 积分器与 Gauss-Legendre 求积器，并在高震荡/平滑函数上对比收敛速度。

---

## 2. 任务边界与输入输出
- **输入**：积分被积函数 $f(x)$、积分区间 $[a, b]$ 及容许误差容差 $\tau$。
- **输出**：积分数值近似值 $I_{\text{approx}}$ 与实际函数调用次数。

---

## 3. 详细实验任务与算法规范

### 任务 1：Golub-Welsch 算法计算 Gauss-Legendre 节点与权重
利用 Legendre 多项式三项递推系数构建对角线为 0、次对角线为 $\beta_k = \frac{k}{\sqrt{4k^2 - 1}}$ 的对称 Jacobi 矩阵。
调用对称特征值求解器，特征值即为积分节点 $x_k$，特征向量第一分量的平方乘以 2 即为权重 $w_k$。

### 任务 2：区间变换与 Gauss 求积器
将 $[-1, 1]$ 上的标准求积公式仿射映射至任意区间 $[a, b]$：
$$I(f) \approx \frac{b-a}{2} \sum_{k=1}^n w_k f\left( \frac{b-a}{2} x_k + \frac{a+b}{2} \right)$$

### 任务 3：收敛阶验证
在积分 $I = \int_0^1 e^x dx = e - 1$ 与 $I_{\text{smooth}} = \int_{-1}^1 \frac{1}{1 + 16x^2} dx$ 上，实测误差随 Gauss 节点数 $n \in [2, 20]$ 的指数衰减行为。

---

## 4. 提交产物与代码规范
- 代码文件：`03-Projects/35-数值分析/scripts/hw05_gauss_quadrature.py`
- 自动化测试：集成至 `03-Projects/35-数值分析/tests/test_numerical_analysis.py`

---

## 5. 验收标准（Rubric）

| 验收维度 | 达标分 | 满分要点 |
| :--- | :---: | :--- |
| **Golub-Welsch 算法** | 35 | 计算得到的 5 点 Gauss-Legendre 节点与解析真值误差 $< 10^{-15}$ |
| **多项式代数精度** | 35 | 5 点 Gauss 求积对任意 9 次多项式精确成立（误差 $< 10^{-14}$） |
| **指数收敛验证** | 30 | 在光滑函数上展示出随点数增加的谱精度指数收敛 |

---

## 6. 引导自检与易错陷阱
- **陷阱**：在将标准区间 $[-1, 1]$ 映射到 $[a, b]$ 时，漏乘以 Jacobian 比例系数 $\frac{b-a}{2}$。

---

## 7. Starter Code 与可执行基线

```python
import numpy as np

def golub_welsch_gauss_legendre(n):
    k = np.arange(1, n)
    beta = k / np.sqrt(4.0 * k**2 - 1.0)
    J = np.diag(beta, -1) + np.diag(beta, 1)
    eigenvalues, eigenvectors = np.linalg.eigh(J)
    nodes = eigenvalues
    weights = 2.0 * (eigenvectors[0, :] ** 2)
    return nodes, weights
```
