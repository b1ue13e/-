---
type: index
topic: "Qlib 项目执行入口"
created: 2026-07-31
updated: 2026-08-01
status: active
flow: sprint
kind: moc
course: 量化金融
sprint_id: 2026-S01-quant
tags: [学习, 量化金融, Qlib, 项目入口, 掌握学习]
anki_deck: "量化金融::Qlib"
anki_tags: [quant, K23, qlib_workflow]
---

# 🚀 Qlib 项目执行入口

> 这是当前量化金融 Sprint 的唯一行动入口。一次只处理一个 K；“运行成功”不等于“知识通过”。

## 🎯 当前唯一行动

| 字段 | 当前值 |
|:---|:---|
| 当前知识点 | **[[01-夯实基础/收益率与对数收益率|K01 收益率与对数收益率]]** |
| 当前阶段 | **第一关：数据与时间协议** |
| 当前作业 | **[[A01-数据协议与无泄漏审计]]** |
| 当前状态 | `learning` |
| 解锁下一个 | K01 闭卷、手算、代码、边界和证据全部通过后，解锁 K02 |

### 今天只做这四件事

1. 不看笔记，写出简单收益率与对数收益率公式。
2. 手算价格 `100 → 102 → 101 → 105 → 103` 的两种收益率。
3. 用代码复核，并解释多期简单收益为什么不能直接相加。
4. 把证据写入 [[A01-数据协议与无泄漏审计#K01 证据登记|A01 的 K01 证据登记]]。

## 🧭 唯一执行链

`[[🚀 Active Sprint]]` → `本页当前 K` → `[[🧩 Qlib 项目知识点—作业—验收路线图]]` → `对应 A 作业` → `[[00-Qlib项目总看板]]`

- 逐知识点路线：[[🧩 Qlib 项目知识点—作业—验收路线图]]
- 项目总看板：[[00-Qlib项目总看板]]
- PoW：[[Quant-Factor-And-Arbitrage-Engine]]
- 最终规格：[[18-实战作业说明书/HW17-Qlib因子研究与成本敏感回测作业说明书|HW17 作业说明书]]
- 可运行作业包：`F:\-\03-Projects\金融与时序\03-量化金融\real_assignment_packages\hw17_qlib_factor_research\`

## ⛔ 防止提前跳关

- 当前 Sprint 只要求 K01–K06 与 A01。
- K07–K28、A02–A06 保留在六周路线中，不在本 Sprint 追赶。
- 只在 E0/E1 通过闸门后调 LightGBM。
- 不以漂亮收益曲线替代时间协议、成本和无泄漏证据。

## ✅ 完成一个 K 的硬条件

- [ ] 能闭卷解释它解决什么问题
- [ ] 手算或最小代码可复核
- [ ] 证据写入对应 A 作业
- [ ] 能指出至少一个错误或失效边界
- [ ] 制作 1–3 张高价值 Anki 卡
- [ ] 没有用测试集反复调参

## 🧩 后续阶段

| 阶段 | K | 作业 | 目标 |
|:---|:---:|:---|:---|
| 数据与时间协议 | K01–K06 | [[A01-数据协议与无泄漏审计|A01]] | 数据可信、时间可交易、无泄漏 |
| E0 组合基准 | K07–K10 | [[A02-E0等权与指数基线|A02]] | 建立无模型基准 |
| E1 简单因子 | K11–K17 | [[A03-E1简单连续因子|A03]] | 可解释信号与因子评价 |
| E2 Qlib/LightGBM | K18–K23 | [[A04-E2-Qlib-LightGBM|A04]] | 公平比较复杂模型增量 |
| 稳健性审计 | K24–K28 | [[A05-成本与稳健性审计|A05]] | 成本、偏差、消融和失败案例 |
| 复现与答辩 | A01–A05 | [[A06-复现报告与答辩|A06]] | 新环境可重跑、结论边界清楚 |

## 🃏 Anki 卡片

- K23｜Qlib 最小研究链的六段是什么？ :: provider → dataset → model → record → strategy → backtest。
- K23｜为什么 qrun 退出码为 0 不等于研究完成？ :: 它只证明配置与工具链可运行，不能证明知识掌握、时间无泄漏、基线公平或结论稳健。

<!-- quant-route-quality-v2 -->
## K23 来源、边界与独立复核

### 定义、假设、机制与边界

Qlib项目执行入口对应的核心机制是 provider 到 dataset、model、recorder、strategy、executor 与 backtest 的证据链。每一层都应保存配置和产物，避免“qrun 成功”被误当成研究结论。假设官方示例能运行只证明环境与接口基本可用；数据许可、复权、交易日历和样本外设计仍需独立审计。反例是只保存最终图表而丢失预测分数和配置哈希。验证要从回测结果反向定位模型与数据版本。

### 可定位来源

1. Microsoft Qlib Introduction, Section Framework layers: https://qlib.readthedocs.io/en/stable/introduction/introduction.html
2. Microsoft Qlib Quick Start, Section qrun workflow: https://qlib.readthedocs.io/en/stable/introduction/quick.html
3. Microsoft Qlib Recorder, Section experiment management: https://qlib.readthedocs.io/en/stable/component/recorder.html

### 可复现示例与验证

```python
artifacts = {"config": True, "prediction": True, "metrics": True, "portfolio": True}
assert all(artifacts.values())
pipeline = ["provider", "dataset", "model", "record", "strategy", "backtest"]
assert pipeline.index("dataset") < pipeline.index("model") < pipeline.index("backtest")
```

该最小实验只验证 K23 的定义、符号或时间边界，不等价于策略有效。正式结论还必须保存输入版本、期望输出、实际结果和失败案例。

### 知识连接

- [[03-策略开发与实战/量化预测]]
- [[03-策略开发与实战/回测偏差五层审计]]
- [[🧩 Qlib 项目知识点—作业—验收路线图]]
- [[🚀 Qlib项目执行入口]]
