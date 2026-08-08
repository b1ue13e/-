---
type: project
project_type: homework
course: "控制与机器人学"
assignment_id: "15-控制与机器人学-阶段作业-06"
assignment_level: stage
assignment_format: lab
stage_id: "06"
requires:
  - "[[纯跟踪与Stanley控制器]]"
  - "[[Stanley公式]]"
  - "[[横向偏差]]"
  - "[[自行车模型]]"
source_type: open_source_project_task
adapted_from: "PythonRobotics（MIT）pure_pursuit.py / stanley_control.py"
source_url: "https://github.com/AtsushiSakai/PythonRobotics"
license: "MIT（PythonRobotics）"
created: 2026-08-09
updated: 2026-08-09
status: planned
flow: project
tags: [作业, 控制与机器人学, 横向控制, PurePursuit, Stanley]
---

# 控制与机器人学-阶段作业-06-纯跟踪与Stanley横向控制

> 阶段作业（stage · lab）：验收阶段 6「横向控制」的 PP/Stanley 编程实现与参数敏感性闭环。非官方中文版：基于 PythonRobotics 开放材料本地化改编。

## 1. 作业身份

| 项 | 值 |
|:---|:---|
| 课程 | 控制与机器人学（15-控制与机器人学） |
| 规模层级 | `stage`（阶段作业） |
| 任务形态 | `lab`（编程实验 + 报告） |
| 所属阶段 | 阶段 6：横向控制 |
| 来源类型 | `open_source_project_task` |
| 来源 | PythonRobotics `pure_pursuit.py`、`stanley_control.py`（MIT） |

## 2. 学习目标

完成后能够：
- 实现 Pure Pursuit 的预瞄点搜索与转向角计算；
- 实现 Stanley 的航向误差 + 横向偏差融合；
- 在固定路径（八字绕环/正弦）上做误差对比实验；
- 完成前视距离/增益的参数敏感性分析并给出结论。

## 3. 所需知识

- `requires`：纯跟踪与Stanley控制器、Stanley公式、横向偏差、自行车模型；
- 前置支撑：阶段 6 模块 A（预瞄点/横向误差模型）与课后作业-06（手算铺垫）；
- 可选扩展：LQR 横向对比（不设隐性前置）。

## 4. 任务背景与边界

- **场景**：自行车模型车辆跟踪固定参考路径（八字绕环、正弦路径），车速给定；
- **输入**：参考路径点序列、车辆初始位姿、控制器参数（$L_d, k$）；
- **输出**：跟踪轨迹、横向误差曲线、指标表；
- **禁止**：直接 import 官方实现；官方代码仅对照基线。

## 5. 详细题目

**题目 1（基础，25 分）：Pure Pursuit 实现**
1a. 实现预瞄点搜索（最近于前视距离的路径点 + 插值）；
1b. 实现转向角 $\delta = \arctan(2L\sin\alpha/L_d)$；
1c. 在八字绕环路径上跑通，报告横向误差 RMS/Max。

**题目 2（基础，25 分）：Stanley 实现**
2a. 实现最近路径点搜索与前轴横向偏差 $e_{fa}$；
2b. 实现 $\delta = \psi_e + \arctan(k e_{fa}/v)$（含低速保护）；
2c. 同一路径对比 PP 与 Stanley 的误差。

**题目 3（核心，30 分）：参数敏感性分析**
3a. 扫 PP 前视距离 $L_d \in \{1, 2, 4, 8\}$ m，画"$L_d$ → RMS"曲线；
3b. 扫 Stanley 增益 $k \in \{0.5, 1, 2, 4\}$，画"$k$ → RMS"曲线；
3c. 低速（2 m/s）与高速（10 m/s）各测一组，给出"高速该用什么参数"的结论。

**题目 4（进阶，20 分）：鲁棒性检查**
4a. 加初始横向偏差 1 m，比较两种算法的收敛速度；
4b. 路径加噪声（±0.1 m），检查跟踪稳定性；
4c. 报告失败案例（参数导致振荡/发散）与调试过程。

## 6. 环境与复现

- Python 3.10+，依赖 `numpy`、`matplotlib`；
- 固定随机种子、固定路径生成参数（振幅/频率/车速）；
- 报告注明官方 commit hash。

## 7. 提交产物

- 报告：算法说明、轨迹对比图、误差曲线、敏感性图、结论；
- 自写代码 + README；
- 指标汇总表（各参数组合的 RMS/Max/到达时间）。

## 8. 验收标准与 Rubric

| 维度 | 分值 | 通过要求 |
|:---|:---:|:---|
| PP 实现 | 25 | 跟踪稳定、误差可报告 |
| Stanley 实现 | 25 | 同上，且含低速保护 |
| 敏感性分析 | 30 | 曲线与机理解释一致 |
| 鲁棒性 | 15 | 失败案例有分析与调试记录 |
| 报告复现 | 5 | 种子/路径参数完整 |
| **总计** | **100** | **≥ 85 且敏感性分析 ≥ 25** |

## 9. 引导与自检

- 常见失败：$L_d$ 太小振荡、Stanley 低速抖动、预瞄点跳变（路径稀疏）、误差符号错误；
- 调试路径：先跑官方 demo 校准环境 → 自写 PP（正弦路径）→ Stanley → 敏感性；
- 自查清单：
  - [ ] 误差符号与坐标系一致（左正右负）；
  - [ ] 低速保护生效（$v + \epsilon$）；
  - [ ] 敏感性曲线可复现（同种子）；
  - [ ] 与官方 demo 的误差在同一量级。

## 10. 后续入口

- 完成后进入 [[🧭 阶段6-横向控制|阶段 6]] 检查点；
- 横向控制器输出供阶段作业-08 的轨迹做跟踪验证（横向链闭环）；
- 错误复盘写入 [[控制与机器人学错题漏洞入口]]。
