---
type: study
topic: "A3C-全局"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段6-Actor-Critic]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["A3C-全局", "A3C 全局网络"]
upstream: ["[[A3C家族]]"]
tags: [学习, 强化学习]
---

# A3C-全局

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段6-Actor-Critic|返回阶段页]]

## 动机
A3C 的中心是"全局网络"，所有 worker 围绕它读写参数。

## 正式定义 / 公式
全局网络 θ_g, φ_g 存最新参数；worker i 拷贝到局部 (θ_i,φ_i)，交互算梯度后异步更新全局。
局部网络仅用于本 worker 推演。

## 最小手算例子
worker 1 拉取全局参数→跑 20 步→算梯度→异步写回全局；worker 2 同时进行。

## 对比与常见错误
- 与同步 A2C：无中心 barrier，worker 各自为政。
- 常见错误：把全局网络当"会等待"——A3C 故意不等待。

## 闭卷自测
1. A3C 全局网络的作用？
2. 局部网络做什么？
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
