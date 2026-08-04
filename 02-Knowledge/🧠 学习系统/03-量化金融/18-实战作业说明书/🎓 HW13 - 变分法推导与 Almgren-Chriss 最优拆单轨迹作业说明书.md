---
title: "HW13 - Almgren-Chriss 最优执行正式作业说明书"
date: 2026-07-24
updated: 2026-07-31
type: homework
course: "量化金融"
status: active
difficulty: "Advanced (4-Tier)"
homework_id: "HW13"
stage: "第四阶段：高频交易与强化学习"
tags: [实战作业, 量化金融, 正式作业说明书, 老师版]
prerequisites:
  - '[[买卖价差及其微观结构拆解 (Bid-Ask Spread & Microstructure Decomposition)]]'
  - '[[市场冲击成本模型与平方根法则 (Market Impact Models & Square-Root Law)]]'
  - '[[Implementation Shortfall 执行缺口与 Almgren-Chriss 最优执行模型.md]]'
  - '[[Almgren-Chriss 最优算法执行轨迹推导 (Almgren-Chriss Optimal Execution)]]'
---

# 🎓 HW13 - Almgren-Chriss 最优执行正式作业说明书

> **说明书定位**：教师正式发布版  
> **关联主干笔记**：[[Almgren-Chriss 最优算法执行轨迹推导 (Almgren-Chriss Optimal Execution)]]  
> **教师视角总设计**：[[🧑‍🏫 量化金融老师视角教学设计与作业节奏]]

---

## 1. 布置时机

在学生学完执行缺口、冲击成本和最优执行直觉后布置。建议放在 U13 开始。

**教师布置理由：**
课程此时从‘做什么策略’转入‘如何真实下单’，是进入交易工程问题的第一步。

---

## 2. 前置知识

学生在开启本作业前，至少应完成以下知识卡与课上最小示例：

- [[买卖价差及其微观结构拆解 (Bid-Ask Spread & Microstructure Decomposition)]]
- [[市场冲击成本模型与平方根法则 (Market Impact Models & Square-Root Law)]]
- [[Implementation Shortfall 执行缺口与 Almgren-Chriss 最优执行模型.md]]
- [[Almgren-Chriss 最优算法执行轨迹推导 (Almgren-Chriss Optimal Execution)]]

**开作业前的教师检查点：**
学生应能解释冲击成本、执行风险和 TWAP/VWAP 的基本区别。

---

## 3. 教学目标

1. 理解 Almgren-Chriss 的目标函数与风险-成本权衡。
2. 会计算或实现最优拆单轨迹。
3. 能比较匀速执行与最优执行的差异。
4. 开始形成执行层面的量化思维。

---

## 4. 作业任务

### 4.1 核心任务

实现或推导 Almgren-Chriss 最优执行轨迹，并在给定订单规模与风险厌恶参数下比较执行成本与风险。

### 4.2 分层要求

- 🟢 Simple：理解并实现风险中性匀速拆单。
- 🟡 Medium：求解或近似实现 AC 最优轨迹。
- 🔴 Strong：比较不同风险厌恶参数下的执行路径与成本。
- 🟣 Boss：扩展到非线性冲击或更复杂约束。

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

重点看成本-风险权衡是否真正讲清楚，不以推导写得多为唯一高分依据。

---

## 6. 交付格式

建议按如下结构提交：

~~~text
hw13/
  README.md
  data/                # 原始数据说明或下载脚本，不提交受限原始大文件
  src/ 或 notebooks/    # 主要实现
  tests/               # 至少 1 个 smoke test
  results/             # 指标表、导出结果、关键中间产物
  figures/             # 图表
  report.md            # 正式分析报告
~~~

**必交内容：**
- README.md：说明模型设定、参数含义和运行方式。
- src/ 或 notebook：完成轨迹求解与对照模拟。
- tests/：至少 1 个 smoke test，验证小规模参数输入。
- report.md：分析执行轨迹、风险偏好和工程含义。

---

## 7. 教师备注

批改时要看学生是否意识到‘最优执行’是约束条件下的最优，而不是无条件省钱。
