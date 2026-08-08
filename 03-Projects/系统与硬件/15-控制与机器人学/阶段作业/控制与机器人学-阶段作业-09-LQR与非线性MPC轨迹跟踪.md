---
type: project
project_type: homework
course: "控制与机器人学"
assignment_id: "15-控制与机器人学-阶段作业-09-01"
assignment_level: stage
assignment_format: lab
stage_id: "09"
requires: ["[[状态空间与LQR控制]]", "[[模型预测控制(MPC)]]", "[[预测方程]]", "[[QP标准形式]]"]
source_type: open_source_project_task
adapted_from: "MIT 6.832 Underactuated Robotics (pydrake) 与 PythonRobotics 轨迹跟踪 demo；原文件见 .recovery-hold/2026-08-06 的 HW01 阶梯作业说明"
source_url: "https://underactuated.csail.mit.edu/"
license: "MIT (pydrake / Drake) [待验证]"
created: 2026-08-06
updated: 2026-08-06
status: planned
flow: project
tags: [作业, 控制与机器人学, LQR, MPC]
---

# 控制与机器人学-阶段作业-09-LQR 与非线性 MPC 轨迹跟踪

> 本作业为阶段作业，验收 **LQR 最优控制** 与 **非线性 MPC 轨迹跟踪** 的完整闭环。
> 非官方中文版：基于 MIT 6.832 Underactuated Robotics 与 PythonRobotics 的开放材料本地化改编。

## 1. 作业身份

| 项 | 值 |
|:---|:---|
| 课程 | 控制与机器人学（15-控制与机器人学） |
| 规模层级 | `stage`（阶段作业） |
| 任务形态 | `lab`（编程实验 + 报告） |
| 所属阶段 | 阶段 9：MPC 深入 |
| 来源类型 | `open_source_project_task` |
| 来源 | MIT 6.832 Underactuated Robotics（pydrake）；PythonRobotics `lqr_steering_control.py`、`model_predictive_speed_and_steering_control.py`（MIT） |

## 2. 学习目标

完成本作业后，学习者能够：

- 用拉格朗日方程建立倒立摆/简单车辆动力学模型并线性化；
- 手解连续/离散时间代数 Riccati 方程，构建 LQR 状态反馈 $u = -Kx$；
- 在仿真环境中实现非线性 MPC 轨迹跟踪，理解预测时域、代价函数与约束的作用；
- 对比 LQR 与 MPC 在约束处理与跟踪精度上的差异，输出可复现的误差报告。

## 3. 所需知识

- `requires`（frontmatter 已声明）：
  - [[状态空间与LQR控制]]（阶段 5）
  - [[模型预测控制(MPC)]]（阶段 9 总览卡）
  - [[预测方程]]（阶段 9）
  - [[QP标准形式]]（阶段 9）
- 正文依赖（已在前序知识卡教授）：状态空间建模、能控性、LQR 代价函数、MPC 预测方程、QP 标准形式。
- 可选扩展：iLQR / 障碍约束（不设隐性前置）。

## 4. 任务背景与边界

- **场景**：二维平面内的轨迹跟踪控制。基准场景为参考路径（如八字绕环或正弦路径），被控对象为自行车模型或倒立摆（任选其一，两种场景二选一完成主任务）。
- **输入**：参考轨迹（时间参数化位置序列）、初始状态、模型参数表（质量/长度/摩擦等）。
- **输出**：控制输入序列、仿真轨迹、跟踪误差曲线。
- **禁止事项**：不得直接 import 官方 demo 的求解函数作为自写实现；官方代码仅作对照基线。

## 5. 详细题目

**题目 1（基础）：状态空间建模与线性化（10 分）**
1a. 选择倒立摆或自行车模型，写出其非线性动力学方程；
1b. 在平衡点附近做 Jacobian 线性化，得到 $\dot{x} = Ax + Bu$，给出 $A,B$ 数值矩阵；
1c. 用 `scipy.signal.cont2discrete` 或手写零阶保持离散化。

**题目 2（基础）：LQR 控制器（25 分）**
2a. 选取权重 $Q \succeq 0, R \succ 0$，手解（或推导）代数 Riccati 方程，给出增益 $K$；
2b. 验证闭环 $A - BK$ 的特征值实部为负；
2c. 至少做一组 $Q/R$ 网格扫描（如 $Q_{11} \in \{1,10,100\}$），报告"权重 → 收敛时间/控制能量"曲线。

**题目 3（进阶）：非线性 MPC（35 分）**
3a. 构建预测模型、代价函数（跟踪误差 + 控制增量）与约束（输入幅值/速率）；
3b. 用 CVXPY 或 CasADi 实现滚动时域求解器，设定预测时域 $N$ 与采样时间 $dt$；
3c. 实现轨迹跟踪闭环，报告横向/纵向误差 RMS；
3d. 扫描预测时域 $N$，分析 $N$ 对误差与求解时间的影响。

**题目 4（综合）：对比与报告（30 分）**
4a. 在**同一固定场景、同一随机种子**下对比：纯 LQR、LQR+前馈、MPC；
4b. 输出三组轨迹叠加图与误差指标表（RMS/Max）；
4c. 报告：方法原理、参数选择依据、失败案例与改进方向。

## 6. 环境与复现

- Python ≥ 3.11；`numpy`, `scipy`, `matplotlib`, `cvxpy`（或 `casadi`）；可选 `pydrake`（Underactuated 环境）。
- 随机种子固定：`np.random.seed(42)`；所有仿真参数写入 `config.yaml` 或代码顶部常量。
- 运行命令：`python run_trajectory_tracking.py --method {lqr,mpc}`。
- 预计运行范围：单次仿真 < 60s（CPU 笔记本）。

## 7. 提交产物

- `scripts/`：建模、求解器、仿真运行代码（自写，不含官方函数 import）；
- `tests/test_track.py`：最小断言（见 §9 检查点）；
- `report.md`：建模推导、参数表、误差对比表、参数敏感性曲线与结论；
- `results/`：三组轨迹图 + 误差数据（CSV）。

## 8. 验收标准与 Rubric

| 维度 | 分值 | 标准 |
|:---|:---:|:---|
| 官方复现对照 | 40 | 官方 demo 在固定场景跑通并保存输出；自写实现与官方结果误差可比 |
| 自写实现正确性 | 30 | LQR 闭环稳定；MPC 跟踪误差有界且随 $N$ 合理变化 |
| 报告完整度 | 20 | 推导、参数、对比表、敏感性分析完整 |
| 可复现性 | 10 | 固定种子 + 固定参数可一键复现，tests 通过 |

> 门槛：总分 ≥ 60 且题目 2、3 均得分 > 50%。

## 9. 引导与自检（不泄露答案）

**检查点**：
- [ ] 线性化后 $A$ 矩阵维度与物理量纲正确（角速度/位置单位）；
- [ ] Riccati 解出的 $K$ 使闭环特征值实部 < 0；
- [ ] MPC 求解器对空约束退化为 LQR 解（自检一致性）；
- [ ] 误差曲线不发散（若发散：检查 $dt$ 与 $N$、代价权重、约束可行性）。

**常见失败模式**：
- 状态变量顺序不一致导致 $A,B$ 错位 → 打印维度与单位核对；
- 预测时域过小导致约束不可行 → 加松弛变量或增大 $N$；
- 离散化错误（零阶保持 vs 前向欧拉混用）→ 统一用零阶保持。

**提交前自检**：代码可一键运行；随机种子固定；报告包含参数表与误差表；未引用官方求解函数。

## 10. 知识依赖与后续

- 完成后进入阶段 10（状态估计）或作为课程大作业（端到端定位-规划-跟踪闭环）的前置实验。
- 复盘：将失败案例与参数结论写入 `04-Review` 或对应知识卡「主动回忆区」。

## 11. 来源与改编说明

- MIT 6.832 Underactuated Robotics：https://underactuated.csail.mit.edu/（pydrake 讲义与作业，开放许可）
- PythonRobotics：https://github.com/AtsushiSakai/PythonRobotics（MIT License）
- 本作业为本地融合任务（`open_source_project_task`），非 MIT 官方作业的完整翻译；原 4-Tier 阶梯说明（已清退）中的难度递进改写为「基础 / 进阶 / 综合」。
