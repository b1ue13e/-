---
type: study
topic: "TD-0"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段4-Q-Learning]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["TD-0", "TD(0) 更新规则"]
upstream: ["[[贝尔曼-V期望]]", "[[蒙特卡洛方法]]"]
tags: [学习, 强化学习]
---

# TD-0

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段4-Q-Learning|返回阶段页]]

## 动机
蒙特卡洛（MC）要等一整幕结束才能更新，太慢；动态规划（DP）要知道模型。TD(0) 折中：每走一步就用"下一步的估计"更新当前估计——边走边学，且不需要环境模型。

## 正式定义 / 公式
TD(0) 对状态价值 V 的更新：
V(s_t) ← V(s_t) + α [ r_{t+1} + γ V(s_{t+1}) − V(s_t) ]
其中方括号里就是 TD 误差 δ_t，α 为步长。

## 最小手算例子
2 状态链 s1→(step)→s2（终止），R=+1，γ=0.9，α=0.5，V 初值 0。
在 s1 走 step 到 s2：δ = 1 + 0.9·V(s2) − V(s1) = 1 + 0 − 0 = 1。
V(s1) ← 0 + 0.5·1 = 0.5。

## 对比与常见错误
- 与 MC：MC 用整幕回报 G_t 更新；TD(0) 只用一步 + 自举估计。
- 常见错误：把 γV(s_{t+1}) 写成 γV(s_t)——自举用的是"下一状态"的估计，不是当前状态。

## 闭卷自测
1. 写出 TD(0) 更新式。
2. TD(0) 与 MC 在"何时更新"上的区别？
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
