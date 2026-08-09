---
type: project
project_type: homework
course: "数值分析"
assignment_id: "数值分析-Stage04"
assignment_level: stage
assignment_format: project
stage_id: "04"
requires: ["[[04-PDE数值与科学计算/数值分析-PDE有限差分离散|数值分析-PDE有限差分离散]]", "[[04-PDE数值与科学计算/数值分析-迭代法CG与GMRES|数值分析-迭代法CG与GMRES]]"]
source_type: local_integration_task
created: 2026-08-08
updated: 2026-08-08
status: active
flow: project
tags: [作业, 阶段作业, 数值分析, 科学计算, 热传导, CrankNicolson, Krylov, CG迭代]
---

# 数值分析-阶段作业-04-二维热传导与Krylov稀疏求解

> 本阶段作业是「阶段4：PDE有限差分与科学计算」的综合大作业。要求综合运用空间五点差分离散、时间 Crank-Nicolson 隐式格式与大规模稀疏预条件共轭梯度法（PCG），完成一个工业级非定常二维热传导方程的完整求解与性能分析。

---

## 1. 学习目标与动机
- 掌握非定常初边值抛物型 PDE 的时空联合差分离散；
- 实现基于 SciPy 稀疏矩阵的 Crank-Nicolson 无条件稳定时间积分器；
- 独立编写共轭梯度法（CG）及其不完全 Cholesky 预条件器，攻克高分辨率网格的大规模稀疏求解瓶颈。

---

## 2. 任务边界与输入输出
- **输入**：二维区域 $\Omega = (0, 1)^2$、热扩散系数 $\alpha = 0.01$、初始温度分布 $u_0(x, y)$ 与网格尺寸 $N \times N$（$N \in [64, 256]$）。
- **输出**：不同时刻的温度云图数据、CG 迭代步数与收敛残差历史、时空二阶精度误差表。

---

## 3. 详细实验任务与算法规范

### 模块 A：时空 Crank-Nicolson 隐式离散
考虑二维非定常热传导方程：
$$\frac{\partial u}{\partial t} = \alpha \left( \frac{\partial^2 u}{\partial x^2} + \frac{\partial^2 u}{\partial y^2} \right) = \alpha \Delta u$$
1. 空间采用标准二阶中心差分算子 $L_h$；
2. 时间采用二阶 Crank-Nicolson 格式：
   $$\left( I - \frac{\alpha \Delta t}{2} L_h \right) U^{n+1} = \left( I + \frac{\alpha \Delta t}{2} L_h \right) U^n$$
3. 证明系统矩阵 $A = I - \frac{\alpha \Delta t}{2} L_h$ 是严格对称正定（SPD）的。

### 模块 B：大规模稀疏共轭梯度法（CG）与预条件加速
1. 实现无矩阵/稀疏矩阵的自定义 CG 迭代求解器；
2. 比较未预条件 CG 与带对角（Jacobi）/ 不完全分解预条件 PCG 的收敛代数迭代步数；
3. 验证当网格从 $N=64$ 加密至 $N=256$ 时，条件数 $\kappa(A)$ 随网格的变化及 PCG 的迭代平稳性。

---

## 4. 提交产物与代码规范
- 代码文件：`03-Projects/35-数值分析/scripts/stage04_heat_krylov.py`
- 自动化测试：集成至 `03-Projects/35-数值分析/tests/test_numerical_analysis.py`

---

## 5. 验收标准（Rubric）

| 验收维度 | 达标分 | 满分要点 |
| :--- | :---: | :--- |
| **时空离散正确性** | 35 | Crank-Nicolson 格式无条件稳定，在较大时间步长下不产生数值发散 |
| **CG / PCG 求解器** | 35 | 自编 CG 算法与 `scipy.sparse.linalg.cg` 解残差一致，残差 $< 10^{-10}$ |
| **网格细化收敛性** | 30 | 实测时间与空间二阶精度收敛阶 $O(\Delta t^2 + h^2)$ |

---

## 6. 引导自检与易错陷阱
- **陷阱**：在组装右端项时漏掉了边界条件的贡献，导致非齐次边界热通量计算错误。

---

## 7. Starter Code 与可执行基线

```python
import numpy as np
import scipy.sparse as sp

def custom_cg(A, b, tol=1e-10, max_iter=500):
    x = np.zeros_like(b)
    r = b - A @ x
    p = r.copy()
    rsold = np.dot(r, r)
    for i in range(max_iter):
        if np.sqrt(rsold) < tol:
            return x, i
        Ap = A @ p
        alpha = rsold / np.dot(p, Ap)
        x += alpha * p
        r -= alpha * Ap
        rsnew = np.dot(r, r)
        p = r + (rsnew / rsold) * p
        rsold = rsnew
    return x, max_iter
```
