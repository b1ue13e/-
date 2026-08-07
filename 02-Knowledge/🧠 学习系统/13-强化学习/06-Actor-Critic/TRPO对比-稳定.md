---
type: study
topic: "TRPO对比-稳定"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段6-Actor-Critic]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["TRPO对比-稳定", "TRPO 对比：训练稳定性"]
upstream: ["[[TRPO家族]]", "[[REINFORCE-不稳定]]"]
tags: [学习, 强化学习]
---

# TRPO对比-稳定

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段6-Actor-Critic|返回阶段页]]

## 动机
TRPO 的稳定性来自信任域约束，这是它相对原始 PG 的最大优势。

## 正式定义 / 公式
KL 约束限制单步策略突变，避免「REINFORCE-不稳定」式的崩溃；
PPO 的 clip 也提供类似稳定（近似约束）。

## 最小手算例子
<!-- NUMEX2 -->稳定性：二者都比 vanilla 策略梯度稳；TRPO 理论保证单调改进（近似），PPO 实践中同样稳且对超参更鲁棒。

长训练里 TRPO/PPO 曲线平滑，原 PG 易震荡——信任域从机制上保稳定。

## 对比与常见错误
- 常见错误：朴素 PG 加小学习率就能等同 TRPO——小 LR 不限分布变化，仍可能塌缩。

## 闭卷自测
1. TRPO 稳定性来源？
2. 小学习率能否替代信任域？
## 学完后可以完成

```dataview
TABLE assignment_level, source_type FROM "03-Projects"
WHERE contains(requires, this.file.link)
```

## 相关下游知识

```dataview
LIST FROM "02-Knowledge/🧠 学习系统"
WHERE contains(upstream, this.file.link)
```
