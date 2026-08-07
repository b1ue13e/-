---
title: Lorenz混沌系统仿真与分岔分析
type: project
topic: 常微分方程-大作业-Lorenz混沌系统仿真与分岔分析
course: 常微分方程
created: 2026-04-18
updated: 2026-08-06
status: active
progress: 0%
flow: project
kind: project
project_type: homework
asset_eligibility: eligible
eligibility_audited: 2026-08-06
difficulty_tier: T3
source_type: local_integration_task
source_url: https://ocw.mit.edu/courses/18-03-differential-equations-spring-2010/pages/assignments/
source_course: MIT 18.03 & Strogatz Nonlinear Dynamics
license: 本地原创作业规格；外部课程与素材保持 link-only
adaptation: original
dataset_version: Lorenz 三维非线性动力方程组（sigma=10, rho=28, beta=8/3）
starter_code: 03-Projects/数学底座/06-常微分方程/scripts/ode_solvers.py
tests: 03-Projects/数学底座/06-常微分方程/tests/test_ode_solvers.py
baseline: 线性化平衡点雅可比矩阵分析
acceptance_test: 三维双蝶翼相轨线重构与 PyTest 仿真无爆炸验证
compute_budget: medium
solution_visibility: private
tags:
  - 作业
  - 常微分方程
  - 混沌动力系统
  - 大作业
assignment_level: capstone
stage_id: '05'
assignment_id: 常微分方程-大作业-Lorenz混沌系统仿真与分岔分析
requires:
  - "[[常微分方程-二维线性系统平衡点分类]]"
  - "[[常微分方程-迹-行列式平面(Trace-Det)判别法]]"
  - "[[常微分方程-非线性动力系统与定性理论]]"
  - "[[常微分方程-非线性系统的局部线性化（雅可比矩阵）]]"
  - "[[常微分方程-一维自治系统与基本分岔]]"
  - "[[常微分方程-分岔理论基础]]"
  - "[[常微分方程-Poincaré-Bendixson定理与极限环]]"
assignment_format: project
---

# 🏆 常微分方程 大作业 01：Lorenz 混沌系统仿真与分岔定性分析

> **所属路径**：[[02-Knowledge/🧠 学习系统/06-常微分方程/🗺️ 常微分方程学习路径\|常微分方程学习路径]]  
> **所属阶段**：[[02-Knowledge/🧠 学习系统/06-常微分方程/05-现代非线性动力系统/🧭 阶段5-现代非线性动力系统\|阶段5-现代非线性动力系统]]  
> **理论支撑**：Strogatz《Nonlinear Dynamics and Chaos》/ MIT 18.03  

---

## 1. 学习目标与项目背景

Lorenz 系统是现代非线性动力学与混沌理论的基石。1963 年，爱德华·洛伦兹（Edward Lorenz）在简化大气对流模型时提出了如下三维非线性微分方程组：
$$\begin{aligned}
\frac{dx}{dt} &= \sigma (y - x) \\
\frac{dy}{dt} &= x (\rho - z) - y \\
\frac{dz}{dt} &= x y - \beta z
\end{aligned}$$

当参数取经典值 $\sigma = 10, \beta = 8/3, \rho = 28$ 时，系统展现出惊人的“奇异吸引子”（Strange Attractor）与蝴蝶效应（初值敏感性）。

本大作业要求你兼顾**解析定性分析**与**高精度数值仿真**，完成从平衡点线性化到混沌轨迹三维可视化的全流程研究。

---

## 2. 任务边界与前置依赖

需掌握阶段 3 与阶段 5 的定性理论核心卡：
- [[常微分方程-非线性系统的局部线性化（雅可比矩阵）]]
- [[常微分方程-二维线性系统平衡点分类]]
- [[常微分方程-非线性动力系统与定性理论]]
- [[常微分方程-一维自治系统与基本分岔]]

环境与资源要求：
- Python 3.10+, `numpy`, `matplotlib`, `pytest`
- 代码位于 `03-Projects/数学底座/06-常微分方程/scripts/ode_solvers.py`

---

## 3. 详细任务说明

### 任务 1：解析求解平衡点与雅可比矩阵线性化
1. **求平衡点**：令 $\dot{x}=\dot{y}=\dot{z}=0$，导出系统的所有平衡点（当 $\rho < 1$ 时与 $\rho > 1$ 时）。
2. **雅可比矩阵**：计算三维系统的雅可比矩阵 $J(x,y,z)$：
   $$J(x, y, z) = \begin{pmatrix} -\sigma & \sigma & 0 \\ \rho - z & -1 & -x \\ y & x & -\beta \end{pmatrix}$$
3. **稳定性判定**：当 $\rho=28$ 时，分析原点 $(0,0,0)$ 与非对称平衡点 $C_\pm = (\pm \sqrt{\beta(\rho-1)}, \pm \sqrt{\beta(\rho-1)}, \rho-1)$ 的特征值，证明其均为不稳定鞍点/螺旋点。

### 任务 2：数值仿真与轨迹生成
在 `scripts/ode_solvers.py` 中调用 `simulate_lorenz(y0, t_eval)`（基于 RK4）：
- 模拟初值 $y_0 = [1.0, 1.0, 1.0]$，在 $t \in [0, 50]$ 范围内的状态轨迹。
- 证明数值解在计算时间内保持有界（无数值发散或 `NaN`）。

### 任务 3：初值敏感性（蝴蝶效应）实验
- 给定两个微小偏差的初值 $y_0^{(1)} = [1.0, 1.0, 1.0]$ 与 $y_0^{(2)} = [1.0, 1.0, 1.00001]$。
- 绘制状态欧氏距离 $d(t) = \|y^{(1)}(t) - y^{(2)}(t)\|$ 随时间演化的半对数曲线 $\ln d(t)$，观察指数级分离现象并估算最大李雅普诺夫指数（Lyapunov Exponent）。

---

## 4. 提交产物与测试入口

依赖代码：
- `scripts/ode_solvers.py` (`lorenz_deriv`, `simulate_lorenz`)

单元测试验收：
- `tests/test_ode_solvers.py::test_lorenz_simulation`

命令行测试：
```bash
pytest 03-Projects/数学底座/06-常微分方程/tests/test_ode_solvers.py -k "test_lorenz_simulation"
```

---

## 5. 验收标准与评分 Rubric

| 维度 | 分值 | 说明 |
| :--- | :---: | :--- |
| **平衡点与雅可比推导** | 25 | 解析证明完整，特征值计算无误 |
| **数值求解器仿真** | 25 | `simulate_lorenz` 正确运行且 PyTest 通过 |
| **三维相空间与双蝶翼重构** | 25 | 能说明轨线在 $C_+$ 与 $C_-$ 两翼间随机交替跳跃 |
| **初值敏感性与李雅普诺夫估计** | 25 | 给出指数分离证据与边界说明 |
| **总分** | **100** | **达到 85 分通过本大作业验收** |

---

## 6. 引导与自检清单

- [ ] 检查雅可比矩阵在原点 $(0,0,0)$ 处的特征多项式计算。
- [ ] 检查三维 Plot 渲染中各坐标轴刻度与标签是否清晰。
- [ ] 运行 `pytest` 确认 Lorenz 仿真测试通过。

---

## 📌 返回导航

- **学习路径**：[[02-Knowledge/🧠 学习系统/06-常微分方程/🗺️ 常微分方程学习路径\|常微分方程学习路径]]
- **阶段 MOC**：[[02-Knowledge/🧠 学习系统/06-常微分方程/05-现代非线性动力系统/🧭 阶段5-现代非线性动力系统\|阶段5-现代非线性动力系统]]