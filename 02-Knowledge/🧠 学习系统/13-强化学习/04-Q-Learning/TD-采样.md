---
type: study
topic: "TD-采样"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段4-Q-Learning]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["TD-采样", "TD sampling"]
upstream: ["[[TD-0]]", "[[蒙特卡洛方法]]"]
tags: [学习, 强化学习]
---

# TD-采样

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段4-Q-Learning|返回阶段页]]

## 动机
TD 是"采样"的：只需与环境交互得到 (s,a,r,s') 一步样本，不必知道转移模型，也不必跑完整幕。

## 正式定义 / 公式
TD 从真实交互采样单步转移 (s_t, a_t, r_{t+1}, s_{t+1}) 更新；
DP 需要已知 P(s'|s,a)、R；MC 需要采样整幕轨迹直到终止。

## 最小手算例子
智能体在 s1 实际走了一步得到 (s1, step, +1, s2)，立刻更新 V(s1)——无需知道 P 也无需等到幕末。

## 对比与常见错误
- 常见错误：把"采样"与"自举"对立——TD 同时具备"采样"（不需模型）和"自举"（不需幕末）。

## 闭卷自测
1. TD 在"模型需求"和"更新时机"上与 DP、MC 有何不同？
2. TD 是否同时采样且自举？
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
