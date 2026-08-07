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
source_locator: "Problem Set 3: Regression Analysis；projection matrix, leverage and case influence"
license: "本地原创题面；仅映射 MIT OCW 回归能力目标，不复制官方解答"
estimated_hours: "4-5"
fixture_path: "scripts/assignments/lesson_fixtures.py::qf_l03_fixture"
starter_path: "scripts/assignments/QF-L03/hw01_capm_alpha_beta/"
created: 2026-08-07
updated: 2026-08-07
status: planned
flow: project
tags: [作业, 量化金融]
---
# 量化金融-课后作业-03-回归与 CAPM

## 作业定位

目标不是生成一张回归表，而是证明自己理解回归表从哪里来、一个高杠杆样本如何改变结论，以及 CAPM 的统计估计为何不等于因果结论。

## 学习目标

- 从投影矩阵和正规方程推导 OLS，并验证投影不变量。
- 估计 CAPM 的 alpha、beta、标准误和残差，而不是只报告 $R^2$。
- 使用 leverage 与 Cook's distance 识别影响点，并执行事先规定的敏感性分析。

## 任务边界

- 主任务只使用题面给定的 12 期超额收益，不下载市场数据。
- CAPM 回归固定为 $r_{i,t}-r_{f,t}=\alpha+\beta(r_{m,t}-r_{f,t})+\epsilon_t$。
- 影响点只能在敏感性分析中剔除；主结果必须保留全样本。
- 不把显著 alpha 写成技能、因果关系或未来收益保证。

## 固定输入

以下数值均为月度小数超额收益：

| t | `market_excess` | `asset_excess` |
| ---: | ---: | ---: |
| 1 | 0.020 | 0.031 |
| 2 | -0.010 | -0.012 |
| 3 | 0.015 | 0.021 |
| 4 | 0.030 | 0.043 |
| 5 | -0.020 | -0.027 |
| 6 | 0.005 | 0.009 |
| 7 | 0.012 | 0.016 |
| 8 | -0.015 | -0.019 |
| 9 | 0.025 | 0.035 |
| 10 | -0.005 | -0.006 |
| 11 | 0.018 | 0.025 |
| 12 | 0.008 | 0.012 |

影响点实验额外加入第 13 期：`market_excess=0.080`、`asset_excess=-0.040`。

## 题目细化

### Q1 OLS 与投影矩阵（25 分）

1. 构造含截距的设计矩阵 $X=[\mathbf 1,x]$，写出其形状与满列秩条件。
2. 从最小化残差平方和推导正规方程和 $\hat\beta=(X^TX)^{-1}X^Ty$。
3. 构造 $H=X(X^TX)^{-1}X^T$，数值验证 $H^T=H$、$H^2=H$ 与 $X^T\hat\epsilon=0$。
4. 解释 $h_{ii}$ 的含义，并验证 $\sum_i h_{ii}=p$，其中 `p=2`。

### Q2 CAPM 基准回归（30 分）

1. 用闭式协方差/方差公式手算 beta，再用 `numpy.linalg.lstsq` 复核 alpha 与 beta。
2. 计算残差、残差方差、参数协方差矩阵、alpha/beta 标准误与 95% 置信区间。
3. 输出每期 `fitted` 与 `residual`，验证残差和及 $X^T\hat\epsilon$ 在容差内为 0。
4. 分别用“每月小数”和线性年化 `12*alpha*100%` 陈述 alpha；说明单位改变不会改变 t 值，但会改变系数展示，且线性年化不是复利收益预测。

### Q3 杠杆与影响点（30 分）

1. 加入第 13 期后重新拟合，报告 alpha、beta、最大 leverage 与最大 Cook's distance 的样本编号。
2. 使用
   $$
   D_i=\frac{\hat\epsilon_i^2}{p\hat\sigma^2}\frac{h_{ii}}{(1-h_{ii})^2}
   $$
   计算 Cook's distance。
3. 按预先规则 `D_i > 4/n` 标记影响点。不得因为系数变得“不好看”而另设阈值。
4. 提交全样本与删除影响点后的敏感性表；主结论仍以全样本为准。

### Q4 解释边界（15 分）

回答以下问题，每题不超过 120 字：

1. 相关系数为什么不等于 beta？
2. beta 估计显著为什么不证明市场收益导致资产收益？
3. 12 期样本为什么不足以支持稳定 alpha 的强结论？

## 提交产物

```text
submissions/QF-L03/
├── report.md              # 推导、回归表、影响点表与边界回答
├── capm.py                # fit_ols/hat_matrix/cooks_distance
├── test_capm.py           # 至少 8 个测试
├── baseline_rows.csv      # 12 期 fitted/residual/leverage
├── influence_rows.csv     # 13 期 fitted/residual/leverage/CookD
└── evidence/
    └── pytest.txt
```

可复用 starter 位于 `scripts/assignments/QF-L03/hw01_capm_alpha_beta/`；允许重写实现，但不得删除输入检查。

## 公开验收断言

```python
assert X.shape == (12, 2)
assert np.allclose(H, H.T, atol=1e-10)
assert np.allclose(H @ H, H, atol=1e-10)
assert np.allclose(X.T @ residuals, 0.0, atol=1e-10)
assert abs(np.trace(H) - 2.0) < 1e-10
assert beta_closed_form == pytest.approx(beta_lstsq, abs=1e-12)
```

## 引导自检

- [ ] 超额收益位于等式两侧，且频率与单位一致。
- [ ] 参数数 `p` 包含截距，残差自由度使用 `n-p`。
- [ ] 全样本结果和敏感性结果没有互相覆盖。
- [ ] 影响点阈值在看结果前已固定。
- [ ] 报告同时给出估计值、不确定性和解释边界。

## 失败诊断

| 现象 | 优先检查 |
| :--- | :--- |
| alpha 明显异常 | 是否把市场总收益与资产超额收益混用 |
| `trace(H)` 不等于 2 | 是否遗漏截距或设计矩阵不满秩 |
| 残差与解释变量相关 | 正规方程、转置或列顺序是否写错 |
| Cook's distance 全为 0 | 是否误用原始收益而非残差，或整数除法 |
| 删除样本后主表也改变 | 是否在原数组上就地修改 |

## 验收标准

- 闭式 beta、`lstsq` 和投影矩阵三条证据一致。
- 回归表包含系数、标准误、置信区间、样本量和频率。
- 影响点有公开阈值、全样本主结果和敏感性结果。
- 至少包含“遗漏截距”与“混用总收益/超额收益”两个负例测试。

## 失败条件

- 只粘贴库函数摘要，没有投影矩阵与闭式复核。
- 仅保留删除影响点后的结果。
- 把显著性、相关性或 beta 解释为因果效应。
- 未说明频率、单位、自由度或无风险收益口径。

## 评分量表

| 项目 | 分值 | 满分证据 |
| :--- | ---: | :--- |
| Q1 OLS 与投影 | 25 | 推导和四项投影不变量完整 |
| Q2 CAPM 基准 | 30 | 系数、标准误、区间、残差与单位解释完整 |
| Q3 影响点 | 30 | leverage、CookD、固定阈值和敏感性表完整 |
| Q4 边界 | 15 | 三类常见误解均被准确拆开 |

总分 `>= 75`，且 Q2、Q3 均不低于 `18` 分才通过。

## 来源与答案边界

- 来源入口：[MIT 18.S096 Problem Set 3: Regression Analysis](https://ocw.mit.edu/courses/18-s096-topics-in-mathematics-with-applications-in-finance-fall-2013/resources/mit18_s096f13_pset3/)。
- 官方 Problem Set 3 覆盖投影矩阵、leverage 和 case influence；本题的 CAPM 数据、输出契约和评分规则为本地原创。
- 禁止提交官方或第三方解答；允许在完成后对照课程讲义复盘定义。
