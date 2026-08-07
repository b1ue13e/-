---
type: study
topic: "DP方法"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段4-Q-Learning]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["DP方法", "动态规划"]
upstream: ["[[贝尔曼-算子]]", "[[策略迭代]]", "[[值迭代]]"]
tags: [学习, 强化学习]
---

# DP方法

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段4-Q-Learning|返回阶段页]]

## 动机
动态规划（DP）在"已知环境模型（P、R）"时，用贝尔曼方程迭代求解价值函数。它是 TD/MC 的理论对照。

## 正式定义 / 公式
在已知 P(s'|s,a)、R 下，用贝尔曼期望/最优算子迭代：
- 策略评估：V ← T^π V
- 策略迭代：评估 + 贪心改进
- 值迭代：V ← T* V
（详见阶段2/阶段3 对应卡片。）

## 最小手算例子
2 状态链已知 P：s1 step→s2 概率1，R=+1。T* V(s1)=max(1+0.9·0)=1 → V*(s1)=1。与 TD/MC 终值一致。

## 对比与常见错误
- 与 TD/MC：DP 需模型、可离线、确定收敛；TD/MC 模型无关但需采样。
- 常见错误：在未知环境直接套 DP——没有 P、R 就不能用 DP。

## 闭卷自测
1. DP 与 TD/MC 的根本区别？
2. DP 为什么需要环境模型？
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
