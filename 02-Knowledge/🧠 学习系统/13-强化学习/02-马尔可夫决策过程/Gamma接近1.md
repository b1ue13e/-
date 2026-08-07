---
type: study
topic: "Gamma接近1"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段2-马尔可夫决策过程]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["折扣", "Gamma接近1"]
upstream: ["[[MDP-折扣因子]]"]
tags: [学习, 强化学习]
---

# Gamma接近1

> 所属模块：[[🧭 阶段2-马尔可夫决策过程]] · 主线：折扣因子 γ
> 前置：[[MDP-折扣因子]]

## 动机

$\gamma\to1$ 用于战略/长程任务；理解其收益与代价，避免"调高就好"的误区。

## 正式定义 / 公式

- $\gamma$ 接近 1（如 0.999）：极重视长远，适合决策后果跨数千步的任务。
- 代价：回报方差剧增、$Q$ 估计噪声大、需更大批量与更稳目标（如目标网络）。

## 最小手算例子

围棋（终局才评分）需要大 $\gamma$ 把终局胜负回溯到早先落子；但训练用目标网络/蒙特卡洛树来稳。


权重衰减：γ=0.99 时第 k 步奖励权重 0.99^k；k=10 为 0.904，k=100 为 0.366，k=460 才衰减到约 0.01。即约 460 步外的奖励仍保留 1% 影响——长程但方差大、相邻步相关系数高。
## 对比与常见错误

- **无脑拉满**：方差与相关性导致发散，而非更好。
- **忽视配套技术**：大 $\gamma$ 需 TD-λ、目标网络、优势归一化等配合。

## 闭卷自测
- 何时需要 $\gamma$ 接近 1？
- 它的主要训练代价是什么？

## 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 相关下游知识

```dataview
LIST
FROM "02-Knowledge/🧠 学习系统"
WHERE contains(upstream, this.file.link)
SORT file.name ASC
```
