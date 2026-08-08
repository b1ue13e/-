---
title: 随机微分方程SDE数值模拟与应用
type: project
topic: 常微分方程-大作业-随机微分方程SDE数值模拟与应用
course: 常微分方程
created: 2026-04-18
status: active
flow: project
project_type: homework
asset_eligibility: eligible
eligibility_audited: 2026-08-06
difficulty_tier: T3
source_type: open_source_project_task
source_url: https://ocw.mit.edu/courses/18-03-differential-equations-spring-2010/pages/assignments/
source_course: Stochastic Differential Equations / Higham 2001 Algorithmic Introduction
license: 本地原创作业规格；外部文献 link-only 引用
adaptation: original
dataset_version: 几何布朗运动 (GBM) 与 Ornstein-Uhlenbeck 随机过程
starter_code: 03-Projects/06-常微分方程/scripts/ode_solvers.py
tests: 03-Projects/06-常微分方程/tests/test_ode_solvers.py
baseline: 确定性常微分方程漂移项对照
acceptance_test: Euler-Maruyama 仿真数值正性与 PyTest 单元测试通过
compute_budget: medium
solution_visibility: private
tags:
  - 作业
  - 常微分方程
  - 随机微分方程
  - SDE
  - 大作业
assignment_level: capstone
stage_id: '07'
assignment_id: 常微分方程-大作业-随机微分方程SDE数值模拟与应用
requires:
  - "[[常微分方程-随机微分方程基础]]"
  - "[[常微分方程-数值解法基础与仿真]]"
assignment_format: project
---

# 🏆 常微分方程 大作业 03：随机微分方程 (SDE) 数值模拟与应用

> **所属路径**：[[02-Knowledge/🧠 学习系统/06-常微分方程/🗺️ 常微分方程学习路径\|常微分方程学习路径]]  
> **所属阶段**：[[02-Knowledge/🧠 学习系统/06-常微分方程/07-精通与专题/🧭 阶段7-精通与专题\|阶段7-精通与专题]]  
> **理论支撑**：Higham, "An Algorithmic Introduction to Numerical Simulation of Stochastic Differential Equations", SIAM Review 2001  

---

## 1. 学习目标与项目背景

真实物理系统与金融市场不可避免地受到环境噪声干扰。随机微分方程（SDE）在经典 ODE 的漂移项（Drift）基础上引入了维纳过程（Wiener Process / 布朗运动）驱动的扩散项（Diffusion）：
$$dy(t) = a(t, y) dt + b(t, y) dW(t)$$

其中 $dW(t) \sim \mathcal{N}(0, dt)$。

本大作业要求你掌握 **Euler-Maruyama 强收敛离散算法**，实现对几何布朗运动（Geometric Brownian Motion, GBM）与 Ornstein-Uhlenbeck 均值回归过程的数值模拟，分析随机波动的统计规律。

---

## 2. 任务边界与前置依赖

需学习阶段 7 的高阶专题卡：
- [[常微分方程-随机微分方程基础]]
- [[常微分方程-数值解法基础与仿真]]

环境与计算边界：
- 环境依赖：`numpy`, `pytest`
- 随机种子设置：在模拟时冻结随机种子以保证结果可复核。

---

## 3. 详细任务说明

### 任务 1：SDE 离散化与 Euler-Maruyama 算法
对于离散网格 $t_n = n \Delta t$，Euler-Maruyama 格式为：
$$y_{n+1} = y_n + a(t_n, y_n) \Delta t + b(t_n, y_n) \Delta W_n$$
其中增量 $\Delta W_n = \sqrt{\Delta t} \cdot \xi_n$，$\xi_n \sim \mathcal{N}(0, 1)$。

在 `scripts/ode_solvers.py` 中实现 `simulate_sde_euler_maruyama(drift, diffusion, y0, t_eval, seed)`。

### 任务 2：几何布朗运动 (GBM) 统计模拟
以资产价格模型 $dy = \mu y dt + \sigma y dW$ 为例（取 $\mu = 0.1, \sigma = 0.2, y(0) = 100$）：
1. **理论期望与方差**：精确表达式为 $\mathbb{E}[y(t)] = y_0 e^{\mu t}$。
2. **蒙特卡洛模拟**：产生 $M=1000$ 条独立的随机轨线，验证样本均值在 $t=1.0$ 时逼近理论值 $100 e^{0.1} \approx 110.517$。

### 任务 3：均值回归 Ornstein-Uhlenbeck 过程
求解 $dy = \theta (\mu - y) dt + \sigma dW$：
- 观察当初始值偏离 $\mu$ 时，轨迹在漂移项作用下向均值 $\mu$ 回退的动力学特征。
- 分析稳态分布的方差 $\text{Var}(y(\infty)) = \frac{\sigma^2}{2\theta}$。

---

## 4. 提交产物与测试入口

算法代码实现：
- `scripts/ode_solvers.py` (`simulate_sde_euler_maruyama`)

PyTest 单元测试：
- `tests/test_ode_solvers.py::test_sde_simulation`

运行测试命令：
```bash
pytest 03-Projects/06-常微分方程/tests/test_ode_solvers.py -k "test_sde_simulation"
```

---

## 5. 验收标准与评分 Rubric

| 维度 | 分值 | 说明 |
| :--- | :---: | :--- |
| **SDE 数学公式与维纳增量** | 25 | 理解 $\Delta W \sim \sqrt{\Delta t} \mathcal{N}(0,1)$ |
| **Euler-Maruyama 代码实现** | 25 | 函数实现正确，处理随机种子固定 |
| **几何布朗运动蒙特卡洛验证** | 25 | 模拟均值收敛于理论期望 $\mathbb{E}[y(t)]$ |
| **PyTest 单元测试通过** | 25 | 仿真测试逻辑正确无误 |
| **总分** | **100** | **达到 85 分通过本大作业验收** |

---

## 6. 引导与自检清单

- [ ] 检查布朗运动增量标准差是否为 $\sqrt{\Delta t}$。
- [ ] 检查 GBM 在 $\sigma$ 较大时数值解正性保护机制。
- [ ] 运行 `pytest` 确认 SDE 模拟单元测试无损通过。

---

## 📌 返回导航

- **学习路径**：[[02-Knowledge/🧠 学习系统/06-常微分方程/🗺️ 常微分方程学习路径\|常微分方程学习路径]]
- **阶段 MOC**：[[02-Knowledge/🧠 学习系统/06-常微分方程/07-精通与专题/🧭 阶段7-精通与专题\|阶段7-精通与专题]]