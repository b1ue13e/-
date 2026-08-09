---
type: project
project_type: homework
course: "随机过程"
assignment_id: "SP-S04"
assignment_level: stage
assignment_format: lab
stage_id: "04"
requires: ["[[随机过程-Ito积分与Ito等距]]", "[[随机过程-Ito公式生成元与鞅构造]]", "[[随机过程-SDE存在唯一性与典型扩散]]", "[[随机过程-Euler-Maruyama路径模拟与误差]]"]
source_type: local_integration_task
source: "本地原创阶段实验；数值口径参考 Higham 2001 与 MIT 15.070J Lectures 14–19"
source_url: "https://doi.org/10.1137/S0036144500378302; https://ocw.mit.edu/courses/15-070j-advanced-stochastic-processes-fall-2013/pages/lecture-notes/"
license: "本地原创任务；外部材料 link-only"
created: 2026-08-09
updated: 2026-08-09
status: planned
flow: project
tags: [作业, 阶段作业, SDE, Ito积分, Euler-Maruyama]
---

# 随机过程｜阶段作业 04：Itô、SDE 与数值误差审计

## 学习目标

完成本阶段后，学习者应能从 Itô 等距和公式推导解析基线，设计耦合 Euler-Maruyama 实验，并区分离散偏差、抽样误差和稳定性失败。

## 任务身份与目标

完成从积分定义到数值算法的端到端审计：先用解析推导确定基线，再用耦合实验估计误差，最后用过大步长证明“可运行”不等于“可信”。

## 任务边界

只使用本课程已讲的 Itô 积分、生成元、GBM、OU 和 Euler-Maruyama；强误差必须共享 Brownian 驱动，弱误差必须报告 Monte Carlo 不确定性。不得用单次运行替代误差阶。

## 必做模块

### A｜Itô 恒等式（25 分）

1. 从左端点和式验证 $\int_0^T W_t\,dW_t=(W_T^2-T)/2$ 的数值行为。
2. 对 $f(x)=x^2,x^4$ 写出 Itô 公式并推导一个矩结论。
3. 写出 OU 生成元，并说明何时 $u(t,X_t)$ 是鞅。

### B｜GBM 强弱误差（45 分）

1. 使用 `simulate_gbm_error_study` 的耦合增量接口，至少五个步长、3,000 条路径和三个种子。
2. 报告强 MAE、弱均值误差、Monte Carlo 标准误和强阶估计。
3. 解释弱误差落在标准误内时应如何表述。
4. 验证粗增量等于细增量之和；若破坏耦合，新增一组对照实验并解释结果。

### C｜OU 稳定性（30 分）

1. 推导 EM 均值稳定边界。
2. 选择稳定与不稳定步长，比较终点矩和路径最大绝对值。
3. 保留至少一个爆炸或振荡样本，判断失败来自模型、算法还是随机波动。

## 提交产物

```text
submission/SP-S04/
├── report.md
├── ito_sde_audit.py
├── ito-results.csv
├── gbm-results.csv
├── ou-stability.csv
└── run.log
```

## Rubric（100 分）

| 维度 | 分值 | 通过证据 |
| :--- | ---: | :--- |
| Itô 公式与生成元 | 25 | 二阶项、矩方程和鞅条件完整 |
| 强误差实验 | 30 | 耦合、多步长、阶估计和对照齐全 |
| 弱误差与不确定性 | 15 | 标准误、样本量和表述边界正确 |
| 数值稳定性 | 20 | 边界推导、失败保留和原因分析完整 |
| 复现 | 10 | 参数、种子、环境和命令可复核 |

## 通过条件

总分至少 80，且 GBM 强误差模块不得低于 60%。硬失败包括：独立路径冒充强误差、单步长结论、删除异常、把 EM 输出当解析真值。

## 引导自检

- 先写解析解或解析矩，再开始模拟。
- 检查每个步长是否复用了同一最细 Brownian 增量。
- 将强误差、弱误差、标准误和最大路径值分别列出，不用一个“总误差”掩盖问题。
