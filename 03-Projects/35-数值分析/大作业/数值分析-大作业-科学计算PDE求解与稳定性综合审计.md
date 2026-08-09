---
type: project
project_type: homework
course: "数值分析"
assignment_id: "数值分析-Capstone"
assignment_level: capstone
assignment_format: reproduction
stage_id: "04"
requires: ["[[01-误差与数值线代/数值分析-浮点算术与误差分析|数值分析-浮点算术与误差分析]]", "[[01-误差与数值线代/数值分析-LU分解与数值稳定性|数值分析-LU分解与数值稳定性]]", "[[04-PDE数值与科学计算/数值分析-迭代法CG与GMRES|数值分析-迭代法CG与GMRES]]", "[[04-PDE数值与科学计算/数值分析-PDE有限差分离散|数值分析-PDE有限差分离散]]"]
source_type: local_integration_task
created: 2026-08-08
updated: 2026-08-08
status: active
flow: project
tags: [作业, 大作业, Capstone, 数值分析, 科学计算, 综合审计, MMS收敛性]
---

# 数值分析-大作业-科学计算PDE求解与稳定性综合审计

> 本项目是「数值分析」全课程的跨阶段终极大作业（Capstone）。它要求将浮点后向误差分析、稀疏矩阵组装、非线性 Newton-Raphson 阻尼迭代、PDE 隐式差分离散与大规模 Krylov 预条件迭代求解器熔铸为一体，完成一个包含严密数学证明、完整 Python 工程实现、制造解法（MMS）网格收敛阶审计与误差分析的综合科学计算报告。

---

## 1. 学习目标与动机
- 攻克科学计算中最具挑战性的非线性初边值偏微分方程系统求解；
- 实现从连续微分方程 -> 空间差分离散 -> 时间隐式积分 -> 每步非线性 Newton 求解 -> 增量方程 Krylov 预条件迭代的工业级完整工作流；
- 运用制造解法（Method of Manufactured Solutions, MMS）精确测量时间和空间双对数网格收敛斜率，严格审计数值算法的向后稳定性与保精度能力。

---

## 2. 任务边界与输入输出
- **输入**：二维非线性反应扩散方程（Schnakenberg 斑图动力系统），在计算域 $\Omega = (0, 1)^2$ 上，时间区间 $t \in [0, T]$。
- **输出**：
  1. 完整可执行 Python 科学计算求解包；
  2. 制造解法在网格序列 $N = 16, 32, 64, 128$ 与步长序列 $\Delta t$ 下的误差收敛阶表；
  3. 100 分制 Capstone 科学计算审计与复现报告。

---

## 3. 核心数学模型与详细工程任务

### 模型方程定义
考虑二维非线性反应扩散系统：
$$\begin{cases}
\frac{\partial u}{\partial t} = D_u \Delta u + a - u + u^2 v \\
\frac{\partial v}{\partial t} = D_v \Delta v + b - u^2 v
\end{cases} \quad (x, y) \in (0, 1)^2$$
边界条件为 Neumann 齐次无通量边界：$\left. \frac{\partial u}{\partial n} \right|_{\partial \Omega} = \left. \frac{\partial v}{\partial n} \right|_{\partial \Omega} = 0$。

### 模块 1：空间 CSR 稀疏五点差分离散与 Ghost Points
- 采用二阶中心差分 5 点模板离散 Laplace 算子 $\Delta u$；
- 引入 Ghost Points 消除边界导数，使边界截断误差与内部严格统一为 $O(h^2)$；
- 构造 CSR 格式稀疏矩阵，并分析其谱半径与条件数 $\kappa(A) = O(h^{-2})$。

### 模块 2：时间 Crank-Nicolson 隐式离散与 Newton-Raphson 求解器
- 采用二阶无条件稳定的 Crank-Nicolson 隐式离散；
- 每时间步构造大型非线性代数方程组 $F(U^{n+1}, V^{n+1}) = 0$；
- 编写多维 Newton-Raphson 求解器，解析推导并组装稀疏雅可比矩阵 $J_F$。

### 模块 3：Krylov 预条件迭代求解（GMRES / BiCGSTAB + ILU）
- 针对 Newton 增量方程 $J_F \Delta W = -F$，采用 Krylov 子空间迭代求解器；
- 配置 ILU(0) 不完全 LU 分解预条件技术，将单步迭代次数稳定压制在 10 步以内。

### 模块 4：制造解法（MMS）收敛阶严苛审计
- 设定解析制造解 $u_{\text{mms}}(x, y, t) = \cos(\pi x) \cos(\pi y) e^{-t}$；
- 自动代入方程计算源项 $S(x, y, t)$，在不同时空网格下实测空间与时间收敛阶：
  $$\text{Spatial Order} = \frac{\log(E(h_1) / E(h_2))}{\log(h_1 / h_2)} \approx 2.0$$

---

## 4. 提交产物与代码规范
- 代码主入口：`03-Projects/35-数值分析/scripts/capstone_pde_mms_solver.py`
- 自动化测试与收敛阶验证：集成至 `03-Projects/35-数值分析/tests/test_numerical_analysis.py`

---

## 5. 验收标准（100分制 Rubric）

| 维度 | 分值 | 验收要点与达标依据 |
| :--- | :---: | :--- |
| **数学推导与相容性证明** | 25 | 空间 5 点模板与 Crank-Nicolson 局部截断误差证明严格完整 |
| **稀疏矩阵与 Newton 求解** | 25 | CSR 稀疏组装无误，多维 Newton 迭代每步在 5 步内收敛至 $< 10^{-10}$ |
| **制造解法 MMS 实验** | 25 | MMS 自动化实测空间双对数收敛阶在 $[1.92, 2.05]$ 之间，完全符合理论 |
| **预条件 Krylov 求解加速** | 15 | 正确集成 ILU 预条件，比未预条件迭代步数减少 80% 以上 |
| **代码工程质量与文档规范** | 10 | 代码注释完备、通过全部自动化测试、无任何硬编码报错 |

---

## 6. 引导自检与易错陷阱
- **陷阱**：在利用 MMS 制造解法时，如果漏掉了时间偏导项 $\frac{\partial u}{\partial t}$ 的源项补偿，实测收敛阶会严重偏离 2.0。

---

## 7. Starter Code 与可执行基线

```python
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

def mms_manufactured_solution(x, y, t):
    """制造解析解 u(x, y, t) = cos(pi*x)*cos(pi*y)*exp(-t)"""
    return np.cos(np.pi * x) * np.cos(np.pi * y) * np.exp(-t)
```
