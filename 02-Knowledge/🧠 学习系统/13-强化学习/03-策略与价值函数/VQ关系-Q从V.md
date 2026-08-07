---
type: study
topic: "VQ关系-Q从V"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段3-策略与价值函数]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["VQ关系-Q从V", "Q^π(s,a)=E[R+γV^π(S')]"]
upstream: ["[[V函数-定义]]", "[[Q函数-定义]]"]
tags: [学习, 强化学习]
---

# VQ关系-Q从V

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段3-策略与价值函数|返回阶段页]]

## 动机
反向：已知状态价值 V，如何得到动作价值 Q？需要"走一步"看转移。

## 正式定义 / 公式
Q^π(s,a) = Σ_{s'} P(s'|s,a) · [ R(s,a,s') + γ V^π(s') ]
即在 s 做 a 后，对下一状态 s' 求"奖励 + 折扣 V"的期望。

## 最小手算例子
2 状态 MDP：s1 做 step 必到 s2，R=+1，V(s2)=0，γ=0.9：
Q(s1,step)=1·[1+0.9·0]=1=V(s1)。✓

## 对比与常见错误
- 常见错误：漏掉期望号 Σ_{s'}——若转移随机，必须对所有可能 s' 加权。

## 闭卷自测
1. 由 V 求 Q 的公式？
2. 为什么这里有对 s' 的期望？
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
