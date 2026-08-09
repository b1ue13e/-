---
type: project
project_type: homework
course: "数值分析"
assignment_id: "数值分析-HW08"
assignment_level: lesson
assignment_format: lab
stage_id: "04"
requires: ["[[04-PDE数值与科学计算/数值分析-PDE有限差分离散|数值分析-PDE有限差分离散]]"]
source_type: official_assignment
created: 2026-08-08
updated: 2026-08-08
status: active
flow: project
tags: [作业, 课后作业, 数值分析, 偏微分方程, 有限差分, Poisson方程, CSR稀疏]
---

# 数值分析-课后作业-08-PDE差分离散与椭圆方程

> 对齐官方源：**MIT 18.335J Problem Set 5 (PDE Discretization & Sparse Solvers)** 与 **FNC Chapter 8**

---

## 1. 学习目标与动机
- 掌握二维偏微分方程空间五点差分模板的构造原理；
- 利用 SciPy 稀疏矩阵工具包（`scipy.sparse.csr_matrix`）高效组装 Kronecker 积离散算子；
- 准确实现 Dirichlet 边界吸纳与二阶精度网格收敛阶验证。

---

## 2. 任务边界与输入输出
- **输入**：二维区域 $\Omega = (0, 1)^2$、源项函数 $f(x, y)$、边界函数 $g(x, y)$ 与网格剖分数 $N$。
- **输出**：离散系数矩阵 $A_{\text{csr}}$、解网格矩阵 $U \in \mathbb{R}^{(N+1) \times (N+1)}$ 及最大模误差。

---

## 3. 详细实验任务与算法规范

### 任务 1：二维 Poisson 五点差分 Kronecker 积稀疏组装
实现函数 `assemble_poisson_2d(N)`：
1. 构造一维三对角差分矩阵 $T_1 = \operatorname{tridiag}(-1, 2, -1) \in \mathbb{R}^{(N-1) \times (N-1)}$；
2. 利用 Kronecker 积组装二维矩阵 $A = \frac{1}{h^2} (I \otimes T_1 + T_1 \otimes I)$，并转为 CSR 格式。

### 任务 2：Dirichlet 边界条件吸收
实现函数 `solve_poisson_dirichlet(f_src, g_bc, N)`：
1. 评估网格内部源项向量 $b = f(X_{1:-1}, Y_{1:-1})$；
2. 遍历四条边界，将已知边界函数值除以 $h^2$ 并累加至相邻的内部右端项中；
3. 调用稀疏直接求解器 `scipy.sparse.linalg.spsolve`。

### 任务 3：制造解法（MMS）收敛阶实测
设定解析制造解为 $u^*(x, y) = \sin(\pi x) \sin(\pi y)$，其对应源项为 $f(x, y) = 2\pi^2 \sin(\pi x) \sin(\pi y)$。
取网格尺寸 $N = 16, 32, 64, 128$，计算误差 $E(h) = \|U_{\text{calc}} - U_{\text{exact}}\|_\infty$，验证其双对数收敛斜率是否严格等于 2.0。

---

## 4. 提交产物与代码规范
- 代码文件：`03-Projects/35-数值分析/scripts/hw08_pde_poisson.py`
- 自动化测试：集成至 `03-Projects/35-数值分析/tests/test_numerical_analysis.py`

---

## 5. 验收标准（Rubric）

| 验收维度 | 达标分 | 满分要点 |
| :--- | :---: | :--- |
| **稀疏矩阵组装** | 35 | CSR 矩阵非零元结构正确，内存占用与网格成线性关系 $O(N^2)$ |
| **边界吸纳正确性** | 35 | 边界条件无缝贴合，内部方程满足离散最大值原理 |
| **空间二阶收敛阶** | 30 | 在 $N=16, 32, 64, 128$ 下实测收敛阶在 $[1.95, 2.05]$ 之间 |

---

## 6. 引导自检与易错陷阱
- **陷阱**：直接使用稠密矩阵（`np.zeros((N^2, N^2))`），在 $N=128$ 时矩阵占用超数吉字节内存导致崩溃；必须使用 `scipy.sparse` 稀疏矩阵。

---

## 7. Starter Code 与可执行基线

```python
import numpy as np
import scipy.sparse as sp

def assemble_poisson_2d(N):
    h = 1.0 / N
    n_in = N - 1
    T1 = sp.diags([-1, 2, -1], [-1, 0, 1], shape=(n_in, n_in))
    I = sp.eye(n_in)
    A = (sp.kron(I, T1) + sp.kron(T1, I)) / (h**2)
    return A.tocsr()
```
