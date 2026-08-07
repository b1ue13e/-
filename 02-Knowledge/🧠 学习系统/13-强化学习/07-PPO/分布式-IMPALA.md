---
type: study
topic: "分布式-IMPALA"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段7-PPO]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["分布式-IMPALA", "IMPALA"]
upstream: ["[[A3C家族]]", "[[优势-定义]]"]
tags: [学习, 强化学习]
---

# 分布式-IMPALA

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段7-PPO|返回阶段页]]

## 动机
A3C 异步但 on-policy 限制数据复用，IMPALA 想用大规模异步又保持高效。

## 正式定义 / 公式
IMPALA：多个 actor 异步生成轨迹送给 learner；因 actor 与 learner 策略有延迟偏差，用 V-trace 离策略修正把返回值校正到 learner 策略：
v_s = V(s) + Σ_l γ^l (Π_{i≤l} c_i) (r_l + γ V(s_{l+1}) − V(s_l))。

## 最小手算例子
<!-- NUMEX2 -->IMPALA：1 learner + 数百 actor 并行，用 V-trace 修正 off-policy 偏差。例 256 actor 吞吐可达百万步/秒级。

actor 用旧参数采一步，learner 用 V-trace 校正后更新，无需等同步。

## 对比与常见错误
- 与 A3C：IMPALA 是中心化 learner + 离策略修正。
- 常见错误：忽略 V-trace——直接异步会引入大 off-policy 偏差。

## 闭卷自测
1. IMPALA 用什么机制修正离策略偏差？
2. 它与 A3C 架构区别？
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
