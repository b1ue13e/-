---
type: study
topic: "A2C-批量"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段6-Actor-Critic]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["A2C-批量", "A2C 批量优势估计"]
upstream: ["[[A2C-同步]]", "[[优势-GAE]]"]
tags: [学习, 强化学习]
---

# A2C-批量

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段6-Actor-Critic|返回阶段页]]

## 动机
A2C 的优势估计常在"一批轨迹"上做（常用 GAE），更稳定。

## 正式定义 / 公式
对一批 (s,a,r,s') 用 GAE 算优势 A_t^{GAE}，再批量做 actor/critic 更新（MSE + 策略梯度）。
批量降低单样本噪声。

## 最小手算例子
收集 4 worker × 20 步=80 Transition，GAE 得 80 个优势，批量反向传播。

## 对比与常见错误
- 与逐样本更新：批量估计优势方差更低、GPU 利用率高。
- 常见错误：批次过大拖慢反馈——需调批量与回报周期。

## 闭卷自测
1. A2C 如何批量估计优势？
2. 批量的好处？
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
