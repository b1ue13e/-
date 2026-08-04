---
title: "HW12 - CPCV 与 PBO 过拟合审计正式作业说明书"
date: 2026-07-24
updated: 2026-07-31
type: homework
course: "量化金融"
status: active
difficulty: "Advanced (4-Tier)"
homework_id: "HW12"
stage: "第三阶段：金融 ML、因子与回测"
tags: [实战作业, 量化金融, 正式作业说明书, 老师版]
prerequisites:
  - '[[Purged Group TimeSeries Cross-Validation 净化交叉验证 (Purged Group K-Fold CV)]]'
  - '[[Meta-labeling 二级标签与元标注 (Meta-labeling in Financial ML)]]'
  - '[[组合过拟合概率 PBO (Probability of Backtest Overfitting & CPCV in AFML)]]'
---

# 🎓 HW12 - CPCV 与 PBO 过拟合审计正式作业说明书

> **说明书定位**：教师正式发布版  
> **关联主干笔记**：[[组合过拟合概率 PBO (Probability of Backtest Overfitting & CPCV in AFML)]]  
> **教师视角总设计**：[[🧑‍🏫 量化金融老师视角教学设计与作业节奏]]

---

## 1. 布置时机

在学生已经做过至少一种策略、配置或金融 ML 研究，并学完 Purged CV 与 PBO 后布置。建议放在 U11 结束后，作为第三阶段压舱石作业。

**教师布置理由：**
只有当学生亲眼见过‘看起来很漂亮的回测结果’后，才会真正理解为什么过拟合审计是硬门槛。

---

## 2. 前置知识

学生在开启本作业前，至少应完成以下知识卡与课上最小示例：

- [[Purged Group TimeSeries Cross-Validation 净化交叉验证 (Purged Group K-Fold CV)]]
- [[Meta-labeling 二级标签与元标注 (Meta-labeling in Financial ML)]]
- [[组合过拟合概率 PBO (Probability of Backtest Overfitting & CPCV in AFML)]]

**开作业前的教师检查点：**
学生应能解释 leakage、purging、embargo 和普通随机 CV 为什么不适合金融时间序列。

---

## 3. 教学目标

1. 理解 CPCV、purging、embargo 和 PBO 的作用。
2. 会对策略或模型进行过拟合审计，而不是只看收益。
3. 能设计公平的样本外与参数对照。
4. 形成‘先审计，再汇报收益’的研究纪律。

---

## 4. 作业任务

### 4.1 核心任务

选择一份已有策略或模型结果，使用 CPCV / purging / embargo 做过拟合审计，并估计 PBO 或其他稳健性指标。

### 4.2 分层要求

- 🟢 Simple：构造基本时间块并理解 purging/embargo 规则。
- 🟡 Medium：在一个已有策略上完成 CPCV 验证流程。
- 🔴 Strong：估计 PBO 或相关过拟合风险指标，并解释结果。
- 🟣 Boss：比较多组参数或多模型，提出可执行的准入规则。

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

重点看验证方案是否严谨、参数比较是否公平、审计结果是否真正改变了研究结论。

---

## 6. 交付格式

建议按如下结构提交：

~~~text
hw12/
  README.md
  data/                # 原始数据说明或下载脚本，不提交受限原始大文件
  src/ 或 notebooks/    # 主要实现
  tests/               # 至少 1 个 smoke test
  results/             # 指标表、导出结果、关键中间产物
  figures/             # 图表
  report.md            # 正式分析报告
~~~

**必交内容：**
- README.md：说明被审计策略、时间切分和验证框架。
- src/ 或 notebook：实现 CPCV、purging/embargo 与风险估计。
- tests/：至少 1 个 smoke test，验证切分和隔离逻辑。
- report.md：说明审计结论、失败参数和研究准入建议。

---

## 7. 教师备注

这份作业是进入 Qlib 或更大 Capstone 前的研究纪律门槛。
