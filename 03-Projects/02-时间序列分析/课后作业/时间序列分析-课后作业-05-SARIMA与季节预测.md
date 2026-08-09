---
type: project
project_type: homework
course: "时间序列分析"
assignment_id: "时间序列分析-05"
assignment_level: lesson
assignment_format: lab
stage_id: "03"
requires: ["[[L06-SARIMA与季节预测]]", "[[SARIMA模型]]", "[[季节性与STL分解]]"]
source_type: local_integration_task
source: "本地原创题目；季节 ARIMA 结构参考 FPP3 Section 9.9，软件接口参考 statsmodels ARIMA"
source_url: "https://otexts.com/fpp3/seasonal-arima.html; https://www.statsmodels.org/stable/generated/statsmodels.tsa.arima.model.ARIMA.html"
source_version: "official pages accessed 2026-08-07"
license: "本地原创任务与合成数据；外部教材和文档仅 link-only。"
starter_code: "scripts/build_lesson_homework_fixtures.py"
estimated_time: "120 minutes"
created: 2026-08-02
updated: 2026-08-07
status: planned
flow: project
tags: [作业, 时间序列分析, SARIMA, 季节预测]
---

# 时间序列分析｜课后作业 05：SARIMA 与季节预测

## 作业定位

本作业用一个固定合成月度序列验证季节差分、乘法结构和 seasonal naïve 基线。自由选数据、搜索六个模型、滚动多窗口和区间校准已移回阶段作业，避免 lesson 任务膨胀。

## 学习目标

- 手算季节差分与普通差分的组合。
- 展开乘法季节算子并识别交叉滞后。
- 在冻结周期和切分下比较 seasonal naïve 与两个预注册 SARIMA。
- 保留收敛警告和季节位置失败，不靠最终结果改候选。

## 任务边界

只使用课程生成的固定月度序列、周期 12、一个训练段和一个评估段；只能拟合题面给定的两个 SARIMA。自由选数据、自动搜索和滚动回测不属于本作业。

## 起始材料与固定协议

运行：

```powershell
python scripts/build_lesson_homework_fixtures.py
```

输入为 `artifacts/homework-fixtures/hw05_monthly_series.csv`，共 144 个连续月度观测。冻结：

- 季节周期 $m=12$；
- 前 120 个观测为训练，后 24 个为一次性评估段；
- 基线：seasonal naïve；
- 候选 A：ARIMA$(0,1,1)(0,1,1)_{12}$；
- 候选 B：ARIMA$(1,0,0)(1,1,0)_{12}$；
- 两个候选均使用 `trend="n"`，不得根据评估段增删候选。

Python 3，依赖 `pandas`、`numpy`、`statsmodels`、`matplotlib`；普通 CPU 预计少于 5 分钟。

## 渐隐任务

### Q1｜差分手算（15 分）

对季度序列 `10,14,18,22,12,16,21,25` 先做 $m=4$ 季节差分，再做一次普通差分；展开：

$$
(1-B)(1-B^4)y_t.
$$

解释为什么先季节差分再普通差分更容易检查是否还需要第二步。

### Q2｜乘法结构（15 分）

展开 ARIMA$(1,0,0)(1,0,0)_4$ 的 AR 多项式，标出 lag 1、4、5 项，并解释 lag 5 系数为什么不是第三个独立参数。

### Q3｜基线先行（20 分）

先只实现 seasonal naïve，对 24 个评估月生成预测。提交 `artifacts/forecast_comparison.csv` 的前三列：

```text
timestamp,actual,seasonal_naive
```

手算前 3 个评估月的基线预测并与代码核对。

### Q4｜固定候选拟合（30 分）

拟合候选 A、B，完整保留警告。向同一 CSV 增加 `candidate_a`、`candidate_b`，并提交：

```text
model,converged,aic,mae,rmse,largest_error_month,largest_abs_error
```

不得因候选失败而删除行；失败时在指标字段写空值并在 `artifacts/failures.csv` 保留异常类型和消息。

### Q5｜季节位置误差（10 分）

按月份 `1–12` 汇总绝对误差，指出每个模型最差的季节位置。解释这一结果可能来自季节振幅、趋势、短期记忆还是单次样本波动，并给出一种可证伪检查。

### Q6｜口试稿（10 分）

在 180 字内解释 $(p,d,q)(P,D,Q)_{12}$ 六类项分别处理什么，以及为什么 SARIMA 残差较好仍可能输给 seasonal naïve。

## 必要提示

1. seasonal naïve 的第 $h$ 步预测取训练末尾对应季节的最近观测，不是训练均值。
2. 两个候选共享同一训练段、评估时间戳和真实值。
3. 本作业评估段用于形成性比较，不是最终测试；不得反复查看后调候选。

## 常见错误

- 用 12 个虚拟变量代替本题要求的季节差分，却仍声称完成 SARIMA。
- 候选与基线的预测起点错开一个月。
- 只报告总体 RMSE，不保留逐时间预测。
- 拟合失败后改变阶数却不记录原失败。

## 提交产物

`answer.md`、手算、`src/sarima_lab.py`、`artifacts/forecast_comparison.csv`、`artifacts/model_summary.csv`、`artifacts/failures.csv`、季节位置误差图和 `environment.txt`。

## Rubric

| 维度 | 分值 | 完整证据 |
| :--- | ---: | :--- |
| 差分手算 | 15 | 季节/普通差分与含义正确 |
| 乘法结构 | 15 | 交叉滞后和参数依赖解释正确 |
| 季节基线 | 20 | 24 个预测对齐且前三项手算核对 |
| 固定候选 | 30 | 同切分、警告/失败保留、指标可复算 |
| 季节误差 | 10 | 按月汇总并给出可证伪机制 |
| 口试稿 | 10 | 六类项与基线价值解释准确 |

通过线 80/100。硬失败：使用评估段调阶、无 seasonal naïve、预测时间戳错位、删除失败拟合，或只提交汇总而无逐预测 CSV。

## 提交前自检与复盘

- [ ] 训练恰好 120 行，评估恰好 24 行。
- [ ] 三个模型的 `timestamp` 与 `actual` 完全一致。
- [ ] 失败和警告保留在独立文件。
- [ ] 记录一次季节索引错位或算子展开错误及修正。

完成后进入[[时间序列分析-课后作业-06-模型识别与残差诊断]]。

## 来源说明

FPP3 §9.9 用于核对季节 ARIMA 记号与结构；statsmodels 官方 ARIMA 文档用于核对接口。题目、候选协议和合成数据为本地原创。
