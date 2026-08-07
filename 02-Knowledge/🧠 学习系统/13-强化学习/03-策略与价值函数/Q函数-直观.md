---
type: study
topic: "Q函数-直观"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段3-策略与价值函数]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["Q函数-直观", "Q^π(s,a) 的直觉"]
upstream: ["[[Q函数-定义]]"]
tags: [学习, 强化学习]
---

# Q函数-直观

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段3-策略与价值函数|返回阶段页]]

## 动机
Q 的直觉：它是"在某状态试某动作"的性价比评分。

## 正式定义 / 公式
- Q^π(s,a) 高 → 在 s 做 a 是个好选择。
- 最优 Q*：Q*(s,a)=max_π Q^π(s,a)；取 a*=argmax_a Q*(s,a) 即得最优动作。
- 很多算法（Q-learning、DQN）学的就是 Q*，再贪心出策略。

## 最小手算例子
两动作 s1：动作 step 给 +1，动作 stay 给 0。Q*(s1,step)=1 > Q*(s1,stay)=0，最优动作=step。

## 对比与常见错误
- 常见错误：把 Q(s,a) 解读为"做完 a 之后的总价值"——它包含第一步奖励 + 后续价值。

## 闭卷自测
1. 怎么用直觉解释 Q^π(s,a)？
2. 如何由 Q* 得到最优动作？
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
