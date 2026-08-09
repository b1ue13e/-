---
type: project
project_type: homework
course: "量化金融"
assignment_id: "QF-L09"
assignment_level: lesson
assignment_format: lab
stage_id: "02"
requires: ["[[量化金融-随机过程-伊藤引理与随机微分方程]]", "[[量化金融-期权定价-Greeks与动态对冲]]"]
source_type: local_integration_task
source_url: "https://ocw.mit.edu/courses/18-s096-topics-in-mathematics-with-applications-in-finance-fall-2013/resources/mit18_s096f13_pset9/"
source_locator: "Problem Set 9: Stochastic Differential Equations；本地必做为 GBM Euler–Maruyama 与离散 delta hedge"
official_assignment_url: "https://ocw.mit.edu/courses/18-s096-topics-in-mathematics-with-applications-in-finance-fall-2013/resources/mit18_s096f13_pset9/"
official_assignment_scope: "MIT 原题的 Vasicek 与 SDE 验证为独立加练；本地不要求短利率模型"
accessed: 2026-08-07
answer_policy: "link-only; independent; 不复制官方答案"
license: "本地原创；MIT OCW 原题链接按其页面许可单独使用"
estimated_hours: "4-5"
fixture_path: "scripts/assignments/lesson_fixtures.py::qf_l09_fixture"
created: 2026-08-07
updated: 2026-08-07
status: planned
flow: project
tags: [作业, 量化金融]
---
# 量化金融-课后作业-09-SDE与动态对冲

## 作业定位

这是随机微积分阶段的收束 lesson：先比较 GBM 的精确离散式和 Euler–Maruyama，再用同一欧式 call 做少量频率/成本情景的 delta hedge。Vasicek、随机利率和模型校准不属于本地必做。

## 学习目标

你将把 SDE 公式落实到可复现路径，区分强路径误差与均值误差，并用逐笔台账验证库存、现金、期末结算和交易成本守恒。

## 任务边界

- 使用 fixture 冻结初始价格、漂移、波动率、到期日、路径数、步数、成本率和种子。
- 只做欧式 call 的离散 delta hedge；不做 gamma hedge、最优再平衡或随机利率。
- 两个步数与两个成本率是最小比较矩阵；不得扩展成全参数网格。

## 固定输入

```python
from scripts.assignments.lesson_fixtures import qf_l09_fixture

data = qf_l09_fixture()
```

`gbm`、`euler`、`hedge` 下的路径/步数/成本和种子由 fixture 统一维护；题面只定义计算规则。

## 题目细化

### Q1 精确 GBM 与 Euler–Maruyama（25 分）

1. 写出 GBM 的 exact step 与 Euler–Maruyama step。
2. 对 fixture 的两个步数，用同一组标准正态增量生成两种路径。
3. 报告终值均值、均方误差和最小价格；解释 Euler 在大步长下可能产生负价格。

### Q2 收敛与随机种子（20 分）

1. 重复两次同一种子实验，逐项比较结果。
2. 画步数与终值均方误差关系；区分强误差（路径配对）与弱误差（均值/分布矩）。
3. 不把两种方法使用不同噪声造成的差异归因于离散格式。

### Q3 离散 delta hedge（30 分）

用 fixture 的两个再平衡频率与两个成本率逐路径维护 `stock_position`、`cash`、`option_value`、`trade` 和 `cost`。

1. 初始现金由 call 价格和 delta 头寸确定。
2. 每次再平衡先按上一时点信息计算 delta，再执行交易并扣成本。
3. 到期用 call payoff 结算，输出每个情景的 hedging error 均值、标准差和成本均值。

### Q4 台账守恒与边界（25 分）

1. 对一条路径逐期检查库存守恒、现金变动恒等式和期末结算。
2. 让成本率变为负数，测试必须拒绝输入。
3. 说明更高频率可能降低离散误差但增加成本；该结论不等于真实市场最优执行。

## 提交产物

```text
QF-L09/
├── solution.md
├── sde_hedge.py
├── artifacts/
│   ├── convergence.csv
│   └── hedge_summary.csv
└── tests/
    └── test_sde_hedge.py
```

## 公开验收断言

```python
import numpy as np

assert np.all(np.isfinite(exact_terminal))
assert euler_summary["paths"] == exact_summary["paths"]
assert np.all(hedge_table["inventory_residual"].abs() < 1e-10)
assert np.all(hedge_table["cost"] >= 0)
assert np.allclose(hedge_table["cash_change"], hedge_table["trade_cash"] - hedge_table["cost"])
assert np.allclose(hedge_table["terminal_error"], hedge_table["portfolio_value"] - payoff)
assert negative_cost_rejected is True
```

## 引导自检

- [ ] exact step 是否使用指数项和同一 Brownian increment？
- [ ] Euler 与 exact 是否用配对噪声？
- [ ] delta 是否只使用当前或上一时点信息？
- [ ] 每笔交易的现金、库存和成本是否能在台账中逐行复算？

## 失败诊断

| 现象 | 优先检查 |
| :--- | :--- |
| Euler 误差不随步数下降 | 检查是否配对 Brownian 增量及步长缩放 |
| 交易成本为负 | 检查成交量绝对值、成本率校验和买卖方向 |
| 期末误差恒等于零 | 检查是否误把期权 payoff 写进 hedge 组合初值 |

## 验收标准

exact/Euler 的输入、配对噪声和误差定义明确；四个对冲情景均有完整台账；库存、现金、成本和期末结算不变量通过；复现实验结果一致。

## 失败条件

- 把 Vasicek 或随机利率作为隐藏必做；
- 对冲时读取未来价格或未来波动率；
- 只给最终 P&L、没有逐笔台账；
- 以合成路径结果宣称实盘对冲能力。

## 评分量表

| 维度 | 分值 | 判据 |
| :--- | ---: | :--- |
| Q1 离散化 | 25 | exact/Euler 公式、配对路径和误差正确 |
| Q2 收敛 | 20 | 强弱误差、种子和图表可复现 |
| Q3 对冲 | 30 | 四情景、信息时序、成本和误差齐全 |
| Q4 守恒 | 25 | 逐笔不变量、负成本负例和边界完整 |

## 官方原题加练

完成本地题后，可独立进入 [MIT 18.S096 Problem Set 9: Stochastic Differential Equations](https://ocw.mit.edu/courses/18-s096-topics-in-mathematics-with-applications-in-finance-fall-2013/resources/mit18_s096f13_pset9/) 加练 SDE 验证和 Vasicek。Vasicek 不是本地作业的隐藏前置。

## 来源与答案边界

MIT 18.S096 Problem Set 9 提供 SDE 官方题集入口；Euler–Maruyama 与 delta hedge 任务为本地原创综合。fixture 只冻结配置和输入，不包含学生解答。
