---
type: project
project_type: homework
course: 07-最优化方法
assignment_id: 07-最优化方法-阶段作业-01
assignment_level: stage
assignment_format: project
stage_id: '01'
requires: ["[[最优化方法-二次型与特征值变分性]]", "[[最优化方法-二次规划与CVXPY]]", "[[最优化方法-CVXPY建模与求解器]]"]
source_type: open_source_project_task
created: 2026-08-06
status: completed
flow: project
tags:
  - 作业
  - 阶段作业
  - 凸优化
  - CVXPY
  - 建模
---



# 07-最优化方法-阶段作业-01-数学基础与CVXPY建模

## 1. 学习目标

本阶段作业旨在检验学习者对最优化数学底座与 CVXPY 自动化求解工具的综合运用能力。学习者需要将现实中的组合资产配置与投资组合优化问题转化为二次规划（QP）标准型，并分别手写 KKT 条件求解与使用 CVXPY 求解器对比验证。

---

## 2. 任务边界与知识依赖

* [[最优化方法-多元梯度与海森矩阵]]
* [[最优化方法-二次型与特征值变分性]]
* [[最优化方法-二次规划与CVXPY]]

---

### 前置依赖

* 完成阶段 1 的全部 3 张知识卡学习
* 完成 [[07-最优化方法-课后作业-00-数学基础与NumPy计算]]

---

### 问题背景

马科维茨（Markowitz）均值-方差投资组合理论是最优化方法在金融工程中的经典应用。在给定资产期望收益与协方差矩阵的情况下，投资者希望在满足目标收益约束与权重归一化约束的同时，最小化投资组合的总方差风险：
$$\min_{w} \quad \frac{1}{2} w^T \Sigma w$$
$$\text{s.t.} \quad \mathbf{1}^T w = 1, \quad \mu^T w \ge r_{target}, \quad w \ge 0$$

---

## 运行环境与依赖

- **Python 环境**：Python 3.10+，包含 `cvxpy`, `numpy`, `matplotlib`
- **运行命令**：`python stage_01_portfolio_optimization.py`

基于 CVXPY 求解凸二次规划。

### 任务 1：从真实协方差到 QP 标准型

1. 给定 4 种资产的历史日收益率数据（或模拟高斯随机生成 $N=4$ 的无正定协方差矩阵 $\Sigma$ 与收益率向量 $\mu$）。
2. 将该问题严格配方为标准二次规划（QP）形式：
   $$\min_{w} \frac{1}{2} w^T P w + q^T w \quad \text{s.t.} \quad A w = b, \quad G w \le h$$

### 任务 2：使用 CVXPY 构建高效求解器

1. 使用 `cvxpy.Variable(4)` 声明变量。
2. 构造 `cvxpy.QuadForm(w, Sigma)` 目标函数与约束集。
3. 调用 `OSQP` 或 `ECOS` 求解器，求解不同目标收益率 $r_{target}$ 下的最优权重分配。

### 任务 3：有效前沿曲线绘制与风险分析

1. 改变 $r_{target}$ 从最低收益到最高收益生成 50 个采样点。
2. 计算每个点对应的方差（标准差），绘制收益-风险有效前沿曲线（Efficient Frontier）。

---

## 提交产物与格式

### 1. 提交内容
- 交互式代码脚本或 Notebook `stage_01_portfolio_optimization.py`

### 2. 评分标准 (Rubric)
| 检查项 | 满分 | 判定条件 |
| :--- | :--- | :--- |
| QP 矩阵标准化变换 | 35分 | 正确写出 $P, q, A, b, G, h$ 对应数值表达式 |
| CVXPY 模型表达规范 | 35分 | 变量与约束条件严格符合 DCP (Disciplined Convex Programming) 规则 |
| 有效前沿绘制与收敛验证 | 30分 | 绘制平滑的前沿曲线并准确指出最小方差组合 (GMVP) |

---

## 七、 常见错误提示

* **错误 1**：协方差矩阵未保证对称半正定，导致求解器报 `DCPError` 或无法收敛。
* **错误 2**：忽略了权重归一化 $\sum w_i = 1$ 约束，求解得到平凡发散解。


---

## 6. 引导提示与自检

- 检查梯度与 Hessian 计算公式推导。
- 验证凸性与约束条件可行性。


---

## 7. 来源与后续入口

- **来源**：EE364A / Numerical Optimization。
- **后续入口**：参见阶段 MOC 与课程总索引。
