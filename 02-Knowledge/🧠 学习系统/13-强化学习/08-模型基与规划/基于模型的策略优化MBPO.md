---
created: 2026-08-07
type: study
course: "强化学习"
title: "基于模型的策略优化 MBPO (Model-Based Policy Optimization)"
topic: "基于模型的策略优化 MBPO (Model-Based Policy Optimization)"
stage_moc: "[[🧭 阶段8-模型基与规划]]"
flow: knowledge
kind: algorithm
status: learning
importance: "A"
tags: [学习, 强化学习, 模型基, 策略优化]
upstream: ["[[复合误差与模型偏差]]", "[[概率集成模型与PETS]]", "[[SAC软Actor-Critic]]"]
concept: ["MBPO", "短 horizon", "模型 rollout", "策略优化"]
sources:
  - "Janner et al. 2019 (MBPO)"
---
# 基于模型的策略优化 MBPO (Model-Based Policy Optimization)

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 对应阶段：[[🧭 阶段8-模型基与规划|返回阶段页]]

## 动机
纯模型基方法（Dyna 类）在长 horizon 下被复合误差拖垮。MBPO 的洞见：**用模型只做"短" rollout 来造更多训练数据，但策略/值函数的更新仍走无模型的 SAC 框架**。模型只负责"扩充经验"，不负责"远程规划"，从而把误差控制在几步之内。

## 正式定义 / 公式
1. 用真实数据 D_real 训练一个**概率集成动力学模型** p_θ(s'|s,a)（见「概率集成模型与PETS」）。
2. 从 D_real 采真实状态 s，用集成模型 rollout 出短轨迹（horizon H，通常 1~5 步），把 (s,a,r,s') 加进模型缓冲区 D_model。
3. 用 D_real ∪ D_model 训练 SAC 的 Actor/Critic（标准无模型更新）。
4. 真实环境交互所得新数据回流到 D_real，重新训模型，循环。

关键：价值估计来自真实+短幻象数据，且 horizon 短 → 复合误差上界小（Ω(εH)，H 小）。

## 最小手算例子
设 H=1：每次从真实状态 s 用模型预测一步得到 (r̂, ŝ)，生成一条"真实(s)→幻象(ŝ)"的转移供 SAC 训练。相比只靠真实数据，样本效率提升数倍；若把 H 提到 20，则 ŝ 已漂移到 OOD 区，SAC 学到利用模型漏洞的坏策略——所以 MBPO 坚持短 H。

## 对比与常见错误
- 与 Dyna-Q：MBPO 不做长程背景规划，而是"造数据 + 无模型优化"，对模型误差更鲁棒。
- 与 PETS：PETS 用模型做在线 CEM 控制；MBPO 用模型造数据喂策略优化。
- **常见错误**：horizon H 设太大（复合误差爆炸）；只用单模型而非集成（无不确定度，OOD 不自知）。

## 闭卷自测
1. MBPO 中模型承担什么角色？值函数靠什么更新？
2. 为什么 MBPO 要把 rollout horizon 设得很短？

## 学完后可以完成

```dataview
LIST FROM "03-Projects" WHERE contains(requires, this.file.link)
```

## 相关下游知识

```dataview
LIST FROM "02-Knowledge/🧠 学习系统" WHERE contains(upstream, this.file.link)
```
