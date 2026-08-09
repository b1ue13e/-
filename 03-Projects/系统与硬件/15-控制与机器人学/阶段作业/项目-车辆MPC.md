---
type: project
project_type: homework
course: "控制与机器人学"
assignment_id: "15-控制与机器人学-项目-09-01-车辆MPC"
assignment_level: stage
assignment_format: lab
stage_id: "09"
requires:
  - "[[09-MPC深入/线性车辆MPC]]"
  - "[[09-MPC深入/预测方程]]"
  - "[[09-MPC深入/QP标准形式]]"
  - "[[09-MPC深入/OSQP]]"
source_type: local_integration_task
adapted_from: "PythonRobotics model_predictive_speed_and_steering_control.py（MIT，本地化任务）"
license: "MIT（PythonRobotics）"
created: 2026-04-18
updated: 2026-08-09
status: planned
flow: project
tags: [作业, 控制与机器人学, MPC, 车辆控制]
---

# 项目-车辆MPC

> 阶段作业（stage · lab）：实现车辆线性 MPC（预测 + QP 求解 + 滚动执行），验证轨迹跟踪精度与约束满足。

## 1. 作业身份

| 项 | 值 |
|:---|:---|
| 课程 | 控制与机器人学（15-控制与机器人学） |
| 规模层级 | `stage`（阶段作业） |
| 任务形态 | `lab`（编程实验 + 报告） |
| 所属阶段 | 阶段 9：MPC 深入 |
| 来源类型 | `local_integration_task`（本地化改编） |

## 2. 学习目标

完成后能够：
- 建立线性化车辆模型与预测方程（$z = \Psi x_k + \Theta u$）；
- 将 MPC 代价 + 约束写成 QP 标准形式；
- 用 OSQP/CVXPY 滚动求解并执行第一步；
- 验证约束满足与轨迹跟踪精度。

## 3. 所需知识

- `requires`：线性车辆MPC、预测方程、QP标准形式、OSQP；
- 前置支撑：车辆误差模型（阶段 3）、LQR（阶段 5）。

## 4. 任务背景与边界

- **场景**：PythonRobotics `model_predictive_speed_and_steering_control.py` 场景（转向角 + 加速度双输入 MPC）；
- **输入**：参考轨迹、预测时域 $N$、权重 $Q, R$、约束；
- **输出**：跟踪轨迹、误差、约束满足检查；
- **禁止**：直接 import 官方 MPC 类；QP 必须自装配。

## 5. 详细题目

**题目 1（基础，25 分）：模型与预测**
1a. 建立线性化车辆模型（状态 $[x, y, \psi, v]$，控制 $[\delta, a]$）；
1b. 推导预测方程矩阵形式 $z = \Psi x_k + \Theta u$（$N = 10$）；
1c. 验证预测与实际仿真的一致性。

**题目 2（核心，30 分）：QP 装配与求解**
2a. 写 MPC 代价（状态误差 + 控制量 + 控制增量）为 QP；
2b. 加约束（$|\delta| \le 0.5$、$|a| \le 2$）；
2c. 用 CVXPY/OSQP 求解，滚动执行，跟踪正弦轨迹。

**题目 3（进阶，25 分）：参数分析**
3a. 扫预测时域 $N \in \{5, 10, 20\}$，报告误差与求解时间；
3b. 扫权重 $Q/R$ 比值，报告跟踪 vs 控制量的权衡；
3c. 输出"参数 → 误差/耗时"曲线。

**题目 4（应用，20 分）：约束验证**
4a. 施加紧约束（$|\delta| \le 0.2$），验证 MPC 不越界；
4b. 故意给不可行约束，演示软约束/可行性处理；
4c. 结论：MPC vs LQR 在约束场景的差异。

## 6. 环境与复现

- Python 3.10+，`numpy`、`matplotlib`、`cvxpy` 或 `osqp`；
- 固定参考轨迹、种子、仿真步长；
- 报告注明 $N, Q, R$ 与求解器版本。

## 7. 提交产物

- 报告：预测推导、QP 装配、跟踪结果、参数分析、结论；
- 代码 + README；
- 数据表（$N$/权重 vs 误差/耗时）。

## 8. 验收标准与 Rubric

| 维度 | 分值 | 通过要求 |
|:---|:---:|:---|
| 预测方程 | 25 | 预测与实际一致 |
| QP 求解 | 30 | 跟踪误差与约束满足 |
| 参数分析 | 25 | $N$/权重曲线完整 |
| 约束验证 | 20 | 紧约束/不可行处理 |
| **总计** | **100** | **≥ 85 且 QP 求解 ≥ 25** |

## 9. 引导与自检

- 常见失败：$\Theta$ 矩阵推导错、QP 不可行（约束太紧）、控制增量项缺失导致抖动；
- 调试路径：开环预测验证 → QP 单步 → 滚动闭环 → 参数扫描；
- 自查清单：
  - [ ] 预测开环与实际仿真一致；
  - [ ] 约束全程满足（画控制量曲线核对）；
  - [ ] $N$ 扫描有耗时记录；
  - [ ] 不可行场景有软约束演示。

## 10. 后续入口

- 完成后进入 [[09-MPC深入/🧭 阶段9-MPC深入|阶段 9]] 检查点；
- 车辆 MPC 复用于阶段作业-09 与 MPC 车辆工程实现；
- 错误复盘写入 [[控制与机器人学错题漏洞入口]]。
