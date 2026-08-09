---
created: 2026-08-07
type: study
course: "强化学习"
title: "课程学习 (Curriculum Learning)"
topic: "课程学习 (Curriculum Learning)"
stage_moc: "[[🧭 阶段9-模仿学习与探索]]"
flow: knowledge
kind: concept
status: learning
importance: "B"
tags: [学习, 强化学习, 训练技巧, 课程]
upstream: ["[[探索与利用基础]]", "[[后见之明经验回放HER]]"]
concept: ["课程学习", "任务调度", "自步", "难度递增"]
sources:
  - "Bengio et al. 2009 (curriculum); Florensa et al. 2017 (reverse curriculum)"
---
# 课程学习 (Curriculum Learning)

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 对应阶段：[[🧭 阶段9-模仿学习与探索|返回阶段页]]

## 动机
让智能体一上来就解最难任务，往往因奖励稀疏/初始随机而寸步难行。课程学习借鉴 human 学习：先易后难，逐步把任务难度调上去，让策略在每个阶段都有可学信号。它常与 HER、探索策略配合，是稀疏/难任务的有效训练技巧。

## 正式定义 / 公式
维护一个**任务分布** p(τ | 难度 λ)，随训练推进增大 λ（更难）：
- 手动课程：人设难度阶梯（先短距抓取，后长距）。
- **自步课程（self-paced）**：按"当前能学会"的标准自动选样本难度。
- **反向课程（reverse curriculum）**：从目标附近随机初始化起点，逐步拉远，保证每步都有非零奖励可学（避免从全随机初始态开始一片 0 奖励）。

## 最小手算例子
推箱子到 (5,5)。反向课程：先让起点在 (4,5)（一步可达，立刻有正信号），学会后再放到 (3,5)、(0,0)… 每个阶段都有可学梯度，比"从 (0,0) 死磕 0 奖励"快得多。配合 HER 更是如虎添翼。

## 对比与常见错误
- 与 HER：都在对抗稀疏奖励；课程调"起点/任务难度"，HER 调"目标重标"。
- 与探索策略：课程降低探索难度，内在奖励提高探索效率，二者正交可叠加。
- **常见错误**：难度跨度太大→跳级失败；课程调度过快→策略没稳住就加压。

## 闭卷自测
1. 反向课程（reverse curriculum）为何从"目标附近"开始而非从易任务开始？
2. 课程学习与 HER 在解决稀疏奖励上的分工有何不同？

## 学完后可以完成

```dataview
LIST FROM "03-Projects" WHERE contains(requires, this.file.link)
```

## 相关下游知识

```dataview
LIST FROM "02-Knowledge/🧠 学习系统" WHERE contains(upstream, this.file.link)
```
