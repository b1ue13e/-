---
title: "HW05 - Black-Scholes 定价与动态 Delta 对冲正式作业说明书"
date: 2026-07-24
updated: 2026-07-31
type: homework
course: "量化金融"
status: active
difficulty: "Advanced (4-Tier)"
homework_id: "HW05"
stage: "第二阶段：时间序列、期权与风控"
tags: [实战作业, 量化金融, 正式作业说明书, 老师版]
prerequisites:
  - '[[远期、期货与期权的区别]]'
  - '[[二叉树期权定价模型 (Binomial Option Pricing Model)]]'
  - '[[Black-Scholes 期权定价模型 (Black-Scholes Option Pricing Model)]]'
  - '[[期权希腊字母 (Option Greeks_ Delta, Gamma, Theta, Vega, Rho)]]'
---

# 🎓 HW05 - Black-Scholes 定价与动态 Delta 对冲正式作业说明书

> **说明书定位**：教师正式发布版  
> **关联主干笔记**：[[Black-Scholes 期权定价模型 (Black-Scholes Option Pricing Model)]]  
> **教师视角总设计**：[[🧑‍🏫 量化金融老师视角教学设计与作业节奏]]

---

## 1. 布置时机

在完成期权 payoff、BSM 闭式和 Greeks 基础后布置。建议放在 U06 结束后。

**教师布置理由：**
学生此时第一次真正同时面对「定价 + 风险暴露 + 对冲误差」，正是理解衍生品课程核心语言的最好时点。

---

## 2. 前置知识

学生在开启本作业前，至少应完成以下知识卡与课上最小示例：

- [[远期、期货与期权的区别]]
- [[二叉树期权定价模型 (Binomial Option Pricing Model)]]
- [[Black-Scholes 期权定价模型 (Black-Scholes Option Pricing Model)]]
- [[期权希腊字母 (Option Greeks_ Delta, Gamma, Theta, Vega, Rho)]]

**开作业前的教师检查点：**
学生应能解释 call/put payoff、Delta 的方向意义，以及连续对冲与离散对冲为何不同。

---

## 3. 教学目标

1. 掌握 BSM 定价和 Greeks 的基础实现。
2. 理解 Delta 对冲的直觉与局限。
3. 能分析离散调仓、波动率误设和摩擦成本带来的误差。
4. 建立「模型价格不等于无风险套利机会」的意识。

---

## 4. 作业任务

### 4.1 核心任务

实现一个标准的 BSM 定价器，并在历史或模拟路径上做离散 Delta 对冲，分析 PnL、对冲误差和调仓频率。

### 4.2 分层要求

- 🟢 Simple：完成 BSM 闭式定价与基本 Greeks 计算。
- 🟡 Medium：在模拟路径上实现离散 Delta 对冲。
- 🔴 Strong：分析波动率误设、调仓频率与对冲损耗。
- 🟣 Boss：扩展到 Delta-Vega 或更复杂风险暴露讨论。

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

重点看定价与对冲逻辑是否一致、误差分析是否到位，不以单次 PnL 漂亮作为高分依据。

---

## 6. 交付格式

建议按如下结构提交：

~~~text
hw05/
  README.md
  data/                # 原始数据说明或下载脚本，不提交受限原始大文件
  src/ 或 notebooks/    # 主要实现
  tests/               # 至少 1 个 smoke test
  results/             # 指标表、导出结果、关键中间产物
  figures/             # 图表
  report.md            # 正式分析报告
~~~

**必交内容：**
- README.md：说明模型假设、路径生成方式与运行方法。
- src/pricing.py 与 src/hedge.py 或 notebook：完成定价和对冲实验。
- tests/：至少 1 个 smoke test，验证 BSM 基本公式与边界情况。
- report.md：解释误差来源、对冲效果和方法边界。

---

## 7. 教师备注

批改时要看学生是否真的理解误差从哪来，而不是只把公式抄出来。
