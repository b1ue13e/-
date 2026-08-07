---
title: ODE求解器基础实现
type: project
topic: 常微分方程-阶段作业-01-ODE求解器基础实现
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
difficulty_tier: T2
source_type: open_source_project_task
source_url: https://ocw.mit.edu/courses/18-03-differential-equations-spring-2010/pages/assignments/
source_course: MIT 18.03
license: 本地原创作业规格；外部课程与素材保持 link-only
adaptation: original
dataset_version: 谐振子与指数衰减测试集；参数写入配置表
starter_code: 03-Projects/数学底座/06-常微分方程/scripts/ode_solvers.py
tests: 03-Projects/数学底座/06-常微分方程/tests/test_ode_solvers.py
baseline: 显式 Euler 法与解析解误差对照
acceptance_test: PyTest 通过且 4 阶收敛阶定量校验通过
compute_budget: low
solution_visibility: private
tags:
  - 作业
  - 常微分方程
  - 数值求解器
assignment_level: stage
stage_id: '01'
assignment_id: 常微分方程-阶段作业-01-ODE求解器基础实现
requires:
  - "[[常微分方程-一阶方程的存在唯一性定理]]"
  - "[[常微分方程-数值解法基础与仿真]]"
assignment_format: lab
---

# 📝 常微分方程 阶段作业 01：ODE 求解器基础实现 (显式 Euler & RK4)

> **所属路径**：[[02-Knowledge/🧠 学习系统/06-常微分方程/🗺️ 常微分方程学习路径\|常微分方程学习路径]]  
> **所属阶段**：[[02-Knowledge/🧠 学习系统/06-常微分方程/01-一阶基石与数值启蒙/🧭 阶段1-一阶基石与数值启蒙\|阶段1-一阶基石与数值启蒙]]  
> **开源映射**：MIT 18.03 SC Numerical Methods / Notes on Diffy Qs §1.7  

---

## 1. 学习目标与任务结果

本阶段作业要求你从零构建 Python 数值求解库，实现 **显式 Euler 法 (`solve_euler`)** 与 **经典 4 阶 Runge-Kutta 法 (`solve_rk4`)**，并对其收敛阶数与截断误差进行定量化科学验证。

你需要证明：
1. 理解一阶及一阶向量方程数值离散化公式。
2. 能够编写稳健的 Python 求解器，支持标量与多维向量状态。
3. 能够通过步长减半实验（Grid Refinement Study）定量推导并验证 RK4 的 $\mathcal{O}(h^4)$ 理论收敛阶。

---

## 2. 任务边界与前置依赖

做本作业前，请确保已学习以下知识卡：
- [[常微分方程-数值解法基础与仿真]]
- [[常微分方程-一阶方程的存在唯一性定理]]

工具与环境配置：
- Python 3.10+
- `numpy`, `pytest`
- 代码位于：`03-Projects/数学底座/06-常微分方程/scripts/ode_solvers.py`

---

## 3. 任务分步说明 (Step-by-Step Requirements)

### 任务 1：显式 Euler 求解器实现
在 `scripts/ode_solvers.py` 中实现函数 `solve_euler(f, y0, t_eval)`：
- 公式：$y_{n+1} = y_n + \Delta t \cdot f(t_n, y_n)$
- 参数校验：检查 `t_eval` 是否单调递增，长度是否 $\ge 2$。

### 任务 2：经典 4 阶 RK4 求解器实现
在 `scripts/ode_solvers.py` 中实现函数 `solve_rk4(f, y0, t_eval)`：
- 公式：
  $$\begin{aligned}
  k_1 &= f(t_n, y_n) \\
  k_2 &= f(t_n + 0.5 \Delta t, y_n + 0.5 \Delta t \cdot k_1) \\
  k_3 &= f(t_n + 0.5 \Delta t, y_n + 0.5 \Delta t \cdot k_2) \\
  k_4 &= f(t_n + \Delta t, y_n + \Delta t \cdot k_3) \\
  y_{n+1} &= y_n + \frac{\Delta t}{6} (k_1 + 2 k_2 + 2 k_3 + k_4)
  \end{aligned}$$

### 任务 3：定量收敛阶校验 (Convergence Rate Analysis)
解一阶衰减方程 $y' = -y, y(0)=1$（精确解为 $y(t) = e^{-t}$）：
- 分别使用步长 $h_1 = 0.05$（$N=20$）与 $h_2 = 0.025$（$N=40$）计算 $t=1.0$ 时的绝对误差 $E(h_1)$ 与 $E(h_2)$。
- 验证误差比率 $\frac{E(h_2)}{E(h_1)} \approx (1/2)^4 = 0.0625$。

---

## 4. 提交产物与代码接口 (Starter & Test Interface)

依赖的底层算法代码位于：
- `03-Projects/数学底座/06-常微分方程/scripts/ode_solvers.py`

单测试自动化入口：
- `03-Projects/数学底座/06-常微分方程/tests/test_ode_solvers.py`

运行单元测试：
```bash
pytest 03-Projects/数学底座/06-常微分方程/tests/test_ode_solvers.py -k "test_euler_accuracy or test_rk4"
```

---

## 5. 验收标准与评分 Rubric

| 维度 | 分值 | 验收说明 |
| :--- | :---: | :--- |
| **API 接口规范性** | 20 | 能够正确处理标量与向量 `y0`，对非法 `t_eval` 正确抛出 `ValueError` |
| **显式 Euler 算法正确性** | 25 | 在 $y'=-y$ 测试中误差在 $\mathcal{O}(h)$ 范围内，PyTest 通过 |
| **RK4 算法正确性** | 30 | 在简谐振子 $y''+y=0$ 中达到 $\mathcal{O}(h^4)$ 精度，PyTest 通过 |
| **定量收敛阶验证** | 25 | 步长减半比率落在 $[0.05, 0.08]$ 之间 |
| **总分** | **100** | **达到 85 分方可判定本阶段作业合格** |

---

## 6. 引导与自检清单

- [ ] 检查 `solve_euler` 和 `solve_rk4` 对 1D 数组与 2D 数组返回形状 `(len(t_eval), len(y0))` 是否一致。
- [ ] 检查算法内部循环步长 `dt = t_eval[i+1] - t_eval[i]` 是否动态适应非均匀网格（如有）。
- [ ] 运行 `pytest test_ode_solvers.py` 确保全通过。

---

## 📌 返回导航

- **学习路径**：[[02-Knowledge/🧠 学习系统/06-常微分方程/🗺️ 常微分方程学习路径\|常微分方程学习路径]]
- **阶段 MOC**：[[02-Knowledge/🧠 学习系统/06-常微分方程/01-一阶基石与数值启蒙/🧭 阶段1-一阶基石与数值启蒙\|阶段1-一阶基石与数值启蒙]]
- **下一个作业包**：[[03-Projects/数学底座/06-常微分方程/课后作业/常微分方程-课后作业-02-二阶常系数与受迫振动\|课后作业 02：二阶常系数与受迫振动]]