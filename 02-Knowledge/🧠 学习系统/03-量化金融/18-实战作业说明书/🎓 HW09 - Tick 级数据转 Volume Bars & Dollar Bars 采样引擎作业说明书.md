---
title: "HW09 - Volume Bars 与 Dollar Bars 采样正式作业说明书"
date: 2026-07-24
updated: 2026-07-31
type: homework
course: "量化金融"
status: active
difficulty: "Advanced (4-Tier)"
homework_id: "HW09"
stage: "第三阶段：金融 ML、因子与回测"
tags: [实战作业, 量化金融, 正式作业说明书, 老师版]
prerequisites:
  - '[[OHLCV字段清洗与复权]]'
  - '[[限价订单簿数据与 L1_L2_L3 盘口重建 (Limit Order Book Data & Reconstructing L1_L2_L3)]]'
  - '[[金融微观结构采样棒 (Financial Data Bars_ Volume, Dollar & Imbalance Bars in AFML)]]'
---

# 🎓 HW09 - Volume Bars 与 Dollar Bars 采样正式作业说明书

> **说明书定位**：教师正式发布版  
> **关联主干笔记**：[[金融微观结构采样棒 (Financial Data Bars_ Volume, Dollar & Imbalance Bars in AFML)]]  
> **教师视角总设计**：[[🧑‍🏫 量化金融老师视角教学设计与作业节奏]]

---

## 1. 布置时机

在学生已经做过日频收益序列分析，并理解采样方式会改变统计性质后布置。建议放在 U09 结束后。

**教师布置理由：**
课程从这里开始进入研究工程层，学生必须意识到‘数据怎么切’本身就是研究设计的一部分。

---

## 2. 前置知识

学生在开启本作业前，至少应完成以下知识卡与课上最小示例：

- [[OHLCV字段清洗与复权]]
- [[限价订单簿数据与 L1_L2_L3 盘口重建 (Limit Order Book Data & Reconstructing L1_L2_L3)]]
- [[金融微观结构采样棒 (Financial Data Bars_ Volume, Dollar & Imbalance Bars in AFML)]]

**开作业前的教师检查点：**
学生应能解释时间 bars 与成交量 bars 的区别，并理解不同采样方式会影响序列分布特征。

---

## 3. 教学目标

1. 理解为什么金融数据采样不是中性的。
2. 会从 tick 或成交数据构造 volume bars / dollar bars。
3. 能比较不同采样方式下的统计性质差异。
4. 开始建立金融 ML 之前的数据工程意识。

---

## 4. 作业任务

### 4.1 核心任务

从更细粒度成交数据出发，实现 volume bars 与 dollar bars 采样流程，并比较不同 bars 下收益分布、峰度或稳定性差异。

### 4.2 分层要求

- 🟢 Simple：实现 volume bars 基本切分。
- 🟡 Medium：实现 dollar bars，并输出对照统计结果。
- 🔴 Strong：分析采样方式对分布、波动率或标签质量的影响。
- 🟣 Boss：扩展到 imbalance bars 或流式采样。

**统一硬门槛：**
- 必须写清楚数据来源、时间区间、切分方式和成本口径。
- 必须提供最小可运行示例或 smoke test，证明流程能从头到尾跑通。
- 必须说明失败案例、异常结果或方法边界，不能只汇报最好结果。

---

## 5. 评分标准

### 5.1 一票否决项

- 使用未来数据、前视偏差或未说明的数据泄漏处理方式。
- 没有 baseline 或没有与朴素方案做公平对照。
- 代码无法运行，或没有最小复现步骤。
- 报告只给结论，不解释方法、限制和失败案例。

### 5.2 评分维度

| 维度 | 分值 | 评分说明 |
|:---|:---:|:---|
| 问题理解与方法正确性 | 25 | 是否真正理解本作业的金融问题，方法是否与题目匹配 |
| 数据处理与实验设计 | 20 | 数据口径、时间切分、无泄漏设计是否清楚可靠 |
| Baseline 与结果对照 | 20 | 是否有朴素基线、公平对照和合理比较 |
| 分析解释与边界意识 | 20 | 是否能解释结果，是否报告失败案例与局限 |
| 工程质量与复现性 | 15 | 目录结构、脚本可运行性、文档完整性是否达标 |

### 5.3 本作业特别强调

重点看采样规则是否清晰、对照是否公平、统计差异是否有解释，不只是把原始数据切成几段。

---

## 6. 交付格式

建议按如下结构提交：

~~~text
hw09/
  README.md
  data/                # 原始数据说明或下载脚本，不提交受限原始大文件
  src/ 或 notebooks/    # 主要实现
  tests/               # 至少 1 个 smoke test
  results/             # 指标表、导出结果、关键中间产物
  figures/             # 图表
  report.md            # 正式分析报告
~~~

**必交内容：**
- README.md：说明原始数据结构、采样规则和运行步骤。
- src/ 或 notebook：实现 bars 构建和统计对照分析。
- tests/：至少 1 个 smoke test，验证小样本切分结果正确。
- report.md：说明采样方式如何影响后续研究结论。

---

## 7. 教师备注

这份作业是进入金融 ML 前的数据观念转折点，讲评时值得花时间。
