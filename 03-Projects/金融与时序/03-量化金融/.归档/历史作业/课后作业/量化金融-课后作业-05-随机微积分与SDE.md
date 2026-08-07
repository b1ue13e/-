---
type: project
project_type: homework
course: "量化金融"
assignment_id: "MIT-18S096-PS05"
assignment_level: lesson
assignment_format: problem-set
stage_id: "04"
requires: ["[[量化金融-随机过程-伊藤引理与随机微分方程]]", "[[Black-Scholes 期权定价模型 (Black-Scholes Option Pricing Model)]]"]
source_type: open_textbook_exercise
source: "MIT OCW 18.S096, adapted local problem set"
source_url: "https://ocw.mit.edu/courses/18-s096-topics-in-mathematics-with-applications-in-finance-fall-2013/pages/assignments/"
accessed: 2026-08-06
license: "MIT OCW Creative Commons; local adaptation marked as adapted"
adapted_from: "MIT OCW 18.S096 Problem Set 5"
translation_status: adapted_summary
solution_visibility: private
created: 2026-08-06
status: active
flow: project
tags: [作业, 量化金融, MIT-OCW]
---
# 量化金融-课后作业-05-随机微积分与SDE

## 学习目标与任务

解释布朗运动与伊藤积分，应用伊藤引理推导价格变换；用 Euler-Maruyama 模拟几何布朗运动，比较离散路径与闭式期望/方差，并指出数值误差与风险中性边界。

## 环境与执行

使用 Python 3.11、NumPy、SciPy；提交推导、模拟代码、收敛图、误差表和假设清单。评分：推导 35，模拟 25，误差分析 20，解释 10，可复现性 10。

## 任务边界

- 覆盖布朗运动、伊藤引理、几何布朗运动和 Euler–Maruyama；不要求完整连续时间最优控制推导。
- 模拟必须区分物理测度与风险中性测度，避免把数值路径当作市场预测。

## 提交产物

- 伊藤引理推导、模拟代码、收敛图、理论/模拟矩与误差表、假设清单和日志。
- 记录步长、路径数、随机种子和数值稳定性处理。

## 验收标准

- 模拟均值/方差随步长和路径数变化的方向符合理论；误差来源有量化说明。
- 推导、代码和图表使用同一符号与时间单位，不能只提交推导截图。

## 引导自检

- [ ] 先验证一维布朗运动的增量性质。
- [ ] 再实现 Euler–Maruyama 并做小规模手工核对。
- [ ] 最后改变步长、路径数和随机种子检查收敛。

## 运行证据与失败判定

- 保存 Euler–Maruyama 伪代码、手算路径、步长/路径数网格、随机种子和收敛表。
- 增量未按平方根步长缩放、把同一噪声误用于所有路径或未报告离散误差时，判定为失败。
- 至少比较一个具有已知矩的过程，并用均值、方差和尾部分位数核对模拟偏差。

## 最小执行协议

1. 冻结过程方程、参数、初值、期限、步长、路径数和种子；先用标准布朗运动核对增量均值、方差与独立性。
2. 对一个短路径手算 Euler–Maruyama 更新，再运行向量化实现；同一时点不同路径必须使用独立随机增量。
3. 用至少三档步长与两档路径数生成收敛表，比较已知矩或解析解；离散误差与蒙特卡洛误差分开报告。
4. 检查负值、爆炸、NaN 和边界吸收等失败情形，说明所选离散方法在哪些 SDE 上不适用。
5. 提交方程说明、脚本、配置、种子、收敛表、失败路径和命令日志；只给模拟图不通过。

**最低通过判据**：短路径手算一致，增量尺度与已知矩检查通过，步长缩小时误差趋势可解释；若数值发散或不收敛，必须标明适用边界而非筛除路径。

