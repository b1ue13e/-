---
type: project
project_type: homework
course: "随机过程"
assignment_id: "SP-L06"
assignment_level: lesson
assignment_format: lab
stage_id: "04"
requires: ["[[随机过程-SDE存在唯一性与典型扩散]]", "[[随机过程-Euler-Maruyama路径模拟与误差]]"]
source_type: local_integration_task
source: "本地原创实验；数值口径参考 Higham 2001"
source_url: "https://doi.org/10.1137/S0036144500378302"
license: "本地原创任务；外部论文 link-only"
created: 2026-08-08
updated: 2026-08-08
status: planned
flow: project
tags: [作业, 随机过程, SDE, Euler-Maruyama, 数值误差]
---

# 随机过程｜课后作业 06：SDE 与 Euler 误差审计

## 学习目标

判断 SDE 的解口径与存在唯一性条件，使用解析解/解析矩建立数值基线，并通过耦合 Brownian 增量区分强误差、弱误差和 Monte Carlo 误差。

## 任务边界与环境

- Python 3.11+ 标准库；运行目录 `03-Projects/24-随机过程/`。
- 强误差必须共享同一 Brownian 路径；粗增量必须等于对应细增量之和。
- 至少使用四个步长和三个预先声明的随机种子，不得运行后删掉不理想种子。
- 解析量、离散偏差、抽样误差与稳定性失败必须分栏报告。

## 题目

### Q1｜解的口径与系数条件（20 分）

1. 写出强解、路径唯一性和分布唯一性的区别。
2. 陈述全局 Lipschitz 与线性增长的标准存在唯一性结论。
3. 检查 GBM 与 OU 的系数是否满足这些充分条件。
4. 给出一个系数不满足全局 Lipschitz、因而需要额外定理或非爆炸分析的例子，只说明风险，不擅自下结论。

### Q2｜解析基线（20 分）

1. 推导 GBM 的解析解、均值与二阶矩。
2. 推导 OU 的解析均值与方差。
3. 解释为何“终点均值正确”不能证明路径级强误差小。
4. 为两个模型分别指定至少一个强误差检查量和一个弱误差检查量。

### Q3｜耦合 GBM 误差阶（35 分）

调用：

```python
from stochastic_process_lab import simulate_gbm_error_study
```

固定 `mu=0.08, sigma=0.3, s0=1, T=1`：

1. 使用步数 `16, 32, 64, 128, 256` 和至少 3,000 条路径。
2. 解释函数如何从最细网格聚合粗增量，并在代码中验证一次聚合恒等式。
3. 报告每档强 MAE、弱均值误差和 Monte Carlo 标准误。
4. 对 $\log(\text{strong MAE})$ 与 $\log(h)$ 回归，报告估计强阶及其与 $1/2$ 的差异。
5. 使用三个种子重复，报告强阶估计范围，不只报告均值。

### Q4｜OU 稳定性失败（25 分）

固定 $\kappa=3,\theta=0,\sigma=0.5,X_0=1,T=10$：

1. 从 EM 更新系数 $1-\kappa h$ 推导确定性均值稳定边界。
2. 选择边界内外各至少两个步长，模拟终点和路径最大绝对值。
3. 与 OU 解析均值/方差比较，保留过大步长产生的振荡、爆炸或异常量级。
4. 区分模型不稳定、数值不稳定和一次极端随机路径。

## 提交产物

```text
submission/SP-L06/
├── answers.md
├── gbm_error_study.py
├── ou_stability_study.py
├── gbm-errors.csv
├── ou-stability.csv
└── run.log
```

## 100 分 Rubric

| 维度 | 分值 | 通过证据 |
| :--- | ---: | :--- |
| 解与条件 | 20 | 强/弱口径和充分条件无混淆 |
| 解析基线 | 20 | GBM/OU 的矩正确且能服务验收 |
| 强弱误差实验 | 30 | 耦合、多步长、多种子和阶估计齐全 |
| 稳定性失败 | 20 | 边界推导、失败保留和原因区分正确 |
| 复现 | 10 | 参数、种子、环境、原始输出可复核 |

## 提示、硬失败与自检

- **必要提示**：弱误差小于一个标准误时，只能说“未分辨出偏差”，不能说偏差为零。
- **硬失败**：粗细网格使用独立随机数却报告强阶；只测一个步长；删除发散路径；把 EM 结果当解析解。
- **自检**：每个表格是否同时包含 `dt, paths, seed, estimate, theory, error, standard_error`？

通过线为 80/100 且无硬失败。完成后进入[[随机过程-阶段作业-04-SDE数值与误差审计]]。

