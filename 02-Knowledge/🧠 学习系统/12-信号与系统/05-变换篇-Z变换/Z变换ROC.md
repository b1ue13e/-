---
type: study
topic: "Z变换ROC"
created: 2026-04-18
updated: 2026-08-06
status: completed
difficulty: beginner
concept: ["Z变换ROC"]
prerequisites: []
related: []
tags: ["学习", "信号与系统"]
course: "信号与系统"
flow: knowledge
stage_moc: "[[🔢 第五阶段：Z变换]]"
kind: concept
sources:
  - "Think DSP Ch.10-12：Z Transform / digital filters"
  - "MIT 6.003 Lec 20-22：Z Transform"
  - "Oppenheim §10.1-10.3：The Z-Transform"
upstream:
  - "[[拉普拉斯定义]]"
  - "[[Z平面]]"
---

# Z变换ROC

> 所属路径：[[🗺️ 信号与系统学习路径|信号与系统学习路径]]
> 所属阶段：[[🔢 第五阶段：Z变换]]
> 教材入口：[[📚 教材挂载索引|教材挂载索引]]

## 学习定位
- 模块：Z 变换
- 这张卡要回答的问题：Z 变换的收敛域（ROC）是什么？它如何决定因果性与稳定性？
- 阶段目标：掌握离散域 ROC 与极点、因果/稳定的对应，类比拉氏 ROC。

## 对应教材（真实出处）
- Think DSP Ch.10-12：Z Transform / digital filters
- MIT 6.003 Lec 20-22：Z Transform
- Oppenheim §10.1-10.3：The Z-Transform

## 一句话定义
> $X(z)=\sum x[n]z^{-n}$（z 复变）；ROC 是使级数收敛的 z 平面环形区域，由极点界定：因果序列 ROC 在最外极点之外（|z|>r_max）。

## 从学习内容上要抓什么
- ROC 为圆环 $r_1<|z|<r_2$，绝不跨过极点。
- 因果 ⇔ ROC 在最外极点外侧；稳定 ⇔ ROC 含单位圆。
- 同 X(z) 不同 ROC 对应不同序列（类比拉氏）。

## 核心内容
### 1. 基本定义与直觉
Z 变换把离散序列映射到复平面；ROC 是“能收敛的甜点区”，被极点像围栏一样围住。因果序列的甜点区在最外极点外面，稳定还要求这个区把单位圆包进去。

### 2. 公式 / 机制 / 流程
$$X(z)=\sum_{n=-\infty}^{\infty}x[n]z^{-n},\quad \text{ROC: }r_1<|z|<r_2$$

### 3. 一个最小例子
例：$x[n]=a^n u[n]$ → $X(z)=1/(1-az^{-1})$，ROC $|z|>|a|$（因果）；若改为 $-a^n u[-n-1]$ 则 ROC $|z|<|a|$（反因果）。

### 4. 常见误区
- 忘记 ROC 才使 Z 变换唯一确定序列。
- 混淆因果（ROC 在外）与稳定（含单位圆）的条件。

## 和其他笔记的关系
- 前置：[[拉普拉斯定义]]、[[ROC定义]]、[[离散信号]]
- 相关：[[单边Z变换]]、[[离散系统函数]]、[[Z与DTFT]]

## 最小自测
> **检索练习 / 通过标准**：合上笔记，能独立复述本节定义、写出核心公式（LaTeX）、指出至少一处常见误区，并独立完成上面的自测题，即视为掌握。

- [ ] 写出 Z 变换定义并说明 ROC 的含义。
- [ ] 说明因果序列与稳定序列的 ROC 分别满足什么。
- [ ] 对比同一 X(z) 的因果与反因果 ROC。

*创建于：2026-04-18 · 更新于：2026-08-06*

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/12-信号与系统"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
