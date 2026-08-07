---
type: project
project_type: homework
course: "时间序列分析"
assignment_id: "时间序列分析-02"
assignment_level: lesson
assignment_format: lab
stage_id: "02"
requires: ["[[L02-ACF-PACF与白噪声]]", "[[自相关函数ACF]]", "[[PACF（深挖笔记）]]", "[[白噪声]]"]
source_type: local_integration_task
source: "本地原创题目，概念顺序参考 FPP3 Sections 2.8-2.9"
source_url: "https://otexts.com/fpp3/acf.html; https://otexts.com/fpp3/wn.html"
source_version: "FPP3 3e online, accessed 2026-08-06"
license: "本地原创任务；外部教材仅 link-only，不复制教材答案。"
created: 2026-08-02
updated: 2026-08-06
status: planned
flow: project
tags: [作业, 时间序列分析, ACF, PACF, 白噪声]
---

# 时间序列分析｜课后作业 02：ACF、PACF 与白噪声

## 学习目标

手算短序列相关、预测理论 ACF/PACF 形状、量化有限样本误报，并用季节残差峰提出可证伪诊断。

## 任务边界与环境

- Python 3、`numpy`、`statsmodels`、`matplotlib`；记录版本。
- 固定随机种子 `2026`；白噪声长度 50、200、2000，各重复 100 次。
- 运行前提交图形预期；禁止把单根越界柱当整体白噪声检验。
- 普通 CPU 预计少于 3 分钟。

## 题目

### 1. 手算（20 分）

对 `2, 4, 3, 5, 6` 计算均值、离差与课程分母口径下的 $r_1$，解释符号和短样本限制。

### 2. 图形预测（20 分）

先画白噪声、AR(1) $\phi=0.8$、AR(1) $\phi=-0.8$、MA(1) $\theta=0.8$ 的 ACF/PACF 草图，再模拟并解释偏差。

### 3. 样本量实验（30 分）

记录前 20 阶 ACF 至少一根越过单滞后 95% 参考带的重复比例，比较三种样本量，并解释“至少一根越界”为何不应按 5% 理解。

### 4. 诊断与费曼解释（30 分）

1. 某残差 ACF 在 lag 12、24 明显为正，说明可能遗漏什么？下一步检查哪些图、模型和基线？
2. 用“共同朋友/中间人”类比，在 120 字内区分 ACF 与 PACF。

## 提交产物

`answer.md`、`acf_pacf_experiment.py`、预期草图、模拟图、100 次重复汇总 CSV、环境版本与运行命令。

## Rubric

| 维度 | 分值 | 通过证据 |
| :--- | ---: | :--- |
| 手算 | 20 | 对齐表、离差与分母口径完整 |
| 先验预测 | 20 | 运行前保存，形状与机制可解释 |
| 重复实验 | 30 | 三个样本量、100 次重复、汇总而非挑图 |
| 诊断与表达 | 30 | 不把相关当因果/唯一选阶证据，季节故障映射合理 |

硬失败：没有重复实验、删除不符合预期的结果、把 PACF 当因果效应。通过线 80/100。

## 自检与后续

检查代码是否固定种子、柱图和整体检验是否分开解释、季节周期是否有频率与机制证据。通过后进入[[时间序列分析-课后作业-03-AR模型与均值回归]]。

提交前还要核对重复次数、样本量标签和 CSV 行数，确认没有只保留“符合预期”的模拟结果。
