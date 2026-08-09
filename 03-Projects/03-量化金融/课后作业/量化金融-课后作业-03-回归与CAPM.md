---
type: project
project_type: homework
course: "量化金融"
assignment_id: "QF-L03"
assignment_level: lesson
assignment_format: lab
stage_id: "02"
requires: ["[[收益率与对数收益率]]", "[[CAPM 资本资产定价模型]]"]
source_type: local_integration_task
source_url: "https://ocw.mit.edu/courses/18-s096-topics-in-mathematics-with-applications-in-finance-fall-2013/resources/mit18_s096f13_pset3/"
source_locator: "Problem Set 3: Regression Analysis；本地只取一元 OLS 与 CAPM 解释"
official_assignment_url: "https://ocw.mit.edu/courses/18-s096-topics-in-mathematics-with-applications-in-finance-fall-2013/resources/mit18_s096f13_pset3/"
official_assignment_scope: "MIT 原题为独立加练；投影矩阵、leverage 与 Cook 距离不属于本地必做"
accessed: 2026-08-07
answer_policy: "link-only; independent; 不复制官方答案"
license: "本地原创；MIT OCW 原题链接按其页面许可单独使用"
estimated_hours: "3-4"
fixture_path: "scripts/assignments/lesson_fixtures.py::qf_l03_fixture"
created: 2026-08-07
updated: 2026-08-07
status: planned
flow: project
tags: [作业, 量化金融]
---
# 量化金融-课后作业-03-回归与CAPM

## 作业定位

本作业把 CAPM 卡中的协方差定义、带截距 OLS 和经济解释连成一个最小实验。投影矩阵、杠杆值、Cook 距离和多因子模型留给后续，不作为完成条件。

## 学习目标

你将手算并程序估计 alpha/beta，检查 OLS 的基本残差不变量，报告置信区间，并用单位变换与单点扰动区分“代数恒等性”和“样本敏感性”。

## 任务边界

- 使用带截距的 `asset_excess = alpha + beta * market_excess + residual`。
- 允许：`numpy`、`statsmodels.api.OLS`。
- 不要求：矩阵投影证明、多元回归、稳健协方差、Cook 距离或因果解释。

## 固定输入

```python
from scripts.assignments.lesson_fixtures import qf_l03_fixture

data = qf_l03_fixture()
```

fixture 提供同期市场和资产超额收益，以及一个用于敏感性检查的追加观测；不得改数据追求显著性。

## 题目细化

### Q1 手算 alpha 与 beta（20 分）

1. 用样本协方差除以市场样本方差计算 beta。
2. 用样本均值计算 alpha。
3. 写出收益单位，并与带截距 OLS 的输出核对。

### Q2 OLS 拟合与不变量（30 分）

1. 用 `statsmodels` 拟合 CAPM，输出 alpha、beta、标准误和 95% 置信区间。
2. 保存 fitted value 与 residual。
3. 检查带截距回归的残差和近似为零，且残差与市场超额收益的样本内积近似为零。
4. 不用显著性替代经济含义：分别解释 alpha 和 beta。

### Q3 单位变换负例（20 分）

把两列收益同时从小数改为百分数后重新拟合。

1. 预测 beta 如何变化，再验证。
2. 预测 alpha 和其标准误如何变化，再验证。
3. 若结论与预测不符，定位是单位、截距还是数据对齐错误。

### Q4 单点敏感性与结论边界（30 分）

把 fixture 的追加观测加入样本并重新估计。

1. 比较 alpha、beta 和置信区间的变化。
2. 不删除该点；解释“小样本系数对单点敏感”与“该点一定错误”的区别。
3. 写出进入真实数据前必须补充的三项协议，例如频率、无风险利率口径和样本期。

## 提交产物

```text
QF-L03/
├── solution.md
├── capm.py
├── artifacts/
│   ├── coefficients.csv
│   └── residuals.csv
└── tests/
    └── test_capm.py
```

## 公开验收断言

```python
import numpy as np

assert np.isclose(beta_hand, beta_ols, atol=1e-12)
assert abs(residuals.sum()) < 1e-10
assert abs(np.dot(market_excess, residuals)) < 1e-10
assert np.isclose(beta_percent, beta_ols, atol=1e-12)
assert np.isclose(alpha_percent, 100 * alpha_ols, atol=1e-10)
assert confidence_interval[0] <= beta_ols <= confidence_interval[1]
```

## 引导自检

- [ ] 是否把市场放在解释变量、资产放在被解释变量？
- [ ] 是否显式加入截距？
- [ ] 手算和库函数是否使用相同的自由度口径？
- [ ] 是否保留追加观测，而不是按结果删点？

## 失败诊断

| 现象 | 优先检查 |
| :--- | :--- |
| 手算 beta 与 OLS 不同 | 检查变量方向、截距和协方差/方差的 `ddof` |
| 残差和明显不为零 | 检查是否给 OLS 加常数列 |
| 换成百分数后 beta 放大 100 倍 | 是否只缩放了一列收益 |

## 验收标准

手算与 OLS 一致；残差两个基本不变量通过；单位负例的预测与结果一致；单点敏感性被量化且没有被误写成异常点判决。

## 失败条件

- 使用原始收益替代超额收益却仍称为 CAPM；
- 把相关系数当 beta；
- 只贴回归摘要，不解释单位和经济含义；
- 删除不利观测或把统计关系写成因果关系。

## 评分量表

| 维度 | 分值 | 判据 |
| :--- | ---: | :--- |
| Q1 手算 | 20 | alpha/beta、单位与程序结果一致 |
| Q2 OLS | 30 | 区间、残差产物和两个不变量完整 |
| Q3 单位负例 | 20 | 先预测后验证，缩放关系正确 |
| Q4 敏感性 | 30 | 不删点，量化变化并声明外推边界 |

## 官方原题加练

完成本地题后，可独立进入 [MIT 18.S096 Problem Set 3: Regression Analysis](https://ocw.mit.edu/courses/18-s096-topics-in-mathematics-with-applications-in-finance-fall-2013/resources/mit18_s096f13_pset3/) 加练投影矩阵和回归诊断。那些内容比本地 CAPM 形成性任务更广，不计入本地通过条件。

## 来源与答案边界

MIT 18.S096 Problem Set 3 是官方开放题集入口。本地作业只映射一元回归能力，并使用原创数据与验收；不复制官方题面、代码或答案。
