---
type: study
topic: "RLHF-PPO"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段7-PPO]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["RLHF-PPO", "PPO 做 RLHF"]
upstream: ["[[PPO近端策略优化]]", "[[RLHF-奖励模型]]"]
tags: [学习, 强化学习]
---

# RLHF-PPO

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段7-PPO|返回阶段页]]

## 动机
RLHF 的 RL 阶段为什么几乎都用 PPO。

## 正式定义 / 公式
用 PPO 优化语言策略：rollout 生成回答，RM 给 r_φ，组合 KL 惩罚得总奖励，用 GAE 估计优势，按裁剪目标更新策略与价值网络 K 个 epoch。

## 最小手算例子
<!-- NUMEX2 -->RLHF-PPO：以 RM 为奖励并加 KL(π‖π_ref) 惩罚防偏离。例 KL 系数 β=0.05，奖励 r=R_free−β·KL，PPO 优化该目标。

一批 prompt → 生成回答 → 算 r_φ−β·KL → PPO 更新 → 重复。

## 对比与常见错误
- 与 PPOClip-目标：RLHF 只是把奖励换成 RM+KL。
- 常见错误：忽略价值网络——PPO 仍需 V 来估计 GAE。

## 闭卷自测
1. RLHF 的 PPO 阶段流程是什么？
2. 它和标准 PPO 的区别在哪？
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
