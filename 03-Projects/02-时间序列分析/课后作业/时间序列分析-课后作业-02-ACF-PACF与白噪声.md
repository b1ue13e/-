---
type: project
project_type: homework
course: "时间序列分析"
assignment_id: "时间序列分析-02"
assignment_level: lesson
assignment_format: lab
stage_id: "02"
requires: ["[[L02-ACF-PACF与白噪声]]", "[[自相关函数ACF]]", "[[时间序列分析-偏自相关函数PACF]]", "[[白噪声]]"]
source_type: local_integration_task
source: "本地原创题目；ACF 定义与白噪声边界参考 FPP3 Sections 2.8–2.9"
source_url: "https://otexts.com/fpp3/acf.html; https://otexts.com/fpp3/wn.html"
source_version: "FPP3 3e online, accessed 2026-08-07"
license: "本地原创任务；外部教材仅 link-only，不复制教材题面或答案。"
estimated_time: "90 minutes"
created: 2026-08-02
updated: 2026-08-07
status: planned
flow: project
tags: [作业, 时间序列分析, ACF, PACF, 白噪声]
---

# 时间序列分析｜课后作业 02：ACF、PACF 与白噪声

## 作业定位

本作业训练“相关图是证据，不是判决书”。你要先手算一个滞后，再通过重复模拟观察单根越界和联合诊断的差异；不要求在本作业中完成 ARIMA 选阶。

## 学习目标

- 按统一分母手算样本 ACF。
- 区分 ACF 的直接加间接关系与 PACF 的条件关系。
- 量化同时查看多个滞后产生的误报。
- 把季节残差峰转成下一步可证伪检查。

## 任务边界

只研究短序列 ACF、四种已给生成机制和白噪声误报；不执行 ARIMA 搜索，也不把相关图当作最终模型选择或因果证据。

## 环境与固定协议

使用 Python 3、`numpy`、`pandas`、`statsmodels`、`matplotlib`。固定种子 `20260807`；白噪声长度只取 `60` 和 `240`，每种长度重复 `200` 次，检查 lag 1–20。普通 CPU 预计少于 3 分钟。

运行前先保存 `artifacts/shape_predictions.csv`，禁止运行后覆盖。

## 渐隐任务

### Q1｜从对齐表到公式（20 分）

对 `2, 4, 3, 5, 6` 计算均值、离差，并按

$$
r_1=\frac{\sum_{t=2}^{T}(y_t-\bar y)(y_{t-1}-\bar y)}
{\sum_{t=1}^{T}(y_t-\bar y)^2}
$$

手算 $r_1$。必须提交 `t,y_t,y_{t-1},y_t-\bar y,y_{t-1}-\bar y,product` 对齐表，并说明短样本下结果为何不稳定。

### Q2｜形状预判与补全过程（20 分）

分别考虑四个生成机制：白噪声、$y_t=0.8y_{t-1}+\varepsilon_t$、$y_t=-0.8y_{t-1}+\varepsilon_t$、$y_t=\varepsilon_t+0.8\varepsilon_{t-1}$。

先画 ACF/PACF 草图并填写：

```text
process,acf_expected,pacf_expected,mechanism
```

再各模拟一条长度 300 的路径。只比较方向、衰减和截尾的近似特征，不因一根柱不符就改写预判。

### Q3｜多重查看实验（35 分）

对每种样本量重复 200 次白噪声模拟，记录：

1. lag 1–20 中越过 $\pm1.96/\sqrt{T}$ 的柱数；
2. 是否至少一根越界；
3. Ljung–Box 在预注册 lag 10 的 p 值是否小于 0.05。

提交 `artifacts/false_alarm_summary.csv`：

```text
sample_size,repetitions,any_spike_rate,mean_spike_count,ljung_box_reject_rate
```

解释为什么 `any_spike_rate` 通常明显高于 5%，以及这不等于 Ljung–Box 应永不拒绝。

### Q4｜故障定位（15 分）

给定残差 ACF 在 lag 12、24 持续为正，写出一个按顺序执行的检查清单：频率/周期 → 数据处理 → 季节基线 → 候选模型 → 重新诊断。每一步必须说明什么结果会推翻“遗漏季节结构”的判断。

### Q5｜费曼解释（10 分）

用“共同朋友/中间人”类比，在 120 字内区分 ACF 与 PACF；不得把 PACF 写成因果效应。

## 必要提示

1. 模拟中所有序列都使用同一随机数生成器连续派生，不要每次循环重设同一 seed。
2. `plot_acf` 的参考带是逐滞后近似，不是 20 次同时检验的家族错误率控制。
3. Ljung–Box 的原假设是到指定滞后为止无联合自相关；大 p 值不是“证明独立正态”。

## 常见错误

- 手算分子和分母使用不同均值或不同样本口径。
- 只保存一张“符合理论”的模拟图。
- 把 AR/MA 图形口诀写成唯一选阶规则。
- `any_spike_rate` 分母写成柱数而不是重复次数。

## 提交产物

`answer.md`、手算对齐表、`src/acf_pacf_lab.py`、预判 CSV、四组图、`artifacts/false_alarm_summary.csv` 和 `environment.txt`。

## Rubric

| 维度 | 分值 | 完整证据 |
| :--- | ---: | :--- |
| 手算 | 20 | 对齐表、统一分母和短样本解释正确 |
| 形状预判 | 20 | 运行前保存，机制而非口诀主导 |
| 重复实验 | 35 | 两种样本量、200 次重复和联合检验均可复算 |
| 故障定位 | 15 | 每一步均有可推翻条件 |
| 费曼解释 | 10 | 区分条件关系且不冒充因果 |

通过线 80/100。硬失败：没有重复实验、覆盖预判、删除不符合预期的路径、把单柱参考带解释成整体 5% 检验，或把 PACF 当因果。

## 提交前自检与复盘

- [ ] CSV 中 `repetitions` 对每种样本量都等于 200。
- [ ] 图和 CSV 能由一个命令重建。
- [ ] 白噪声出现越界柱时没有被删除。
- [ ] 记录一个“图形口诀差点误导我”的具体例子。

通过后进入[[时间序列分析-课后作业-03-AR模型与均值回归]]。

## 来源说明

FPP3 §2.8 用于核对 ACF 定义与趋势/季节形态，§2.9 用于核对白噪声参考带；本作业题目与模拟协议为本地原创。
