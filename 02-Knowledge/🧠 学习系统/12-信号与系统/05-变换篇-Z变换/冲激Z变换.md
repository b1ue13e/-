---
type: study
topic: "冲激Z变换"
created: 2026-04-18
updated: 2026-08-06
status: completed
difficulty: intermediate
concept: ["冲激Z变换", "常见序列的Z变换"]
prerequisites: []
related: []
tags: ["学习", "信号与系统"]
course: "信号与系统"
flow: knowledge
stage_moc: "[[🔢 第五阶段：Z变换]]"
sources:
  - "Think DSP Ch.10"
  - "Oppenheim §10.1"
  - "MIT 6.003 Lec 20"
kind: concept

---
# 冲激Z变换

> 所属路径：[[🗺️ 信号与系统学习路径|信号与系统学习路径]]
> 所属阶段：[[🔢 第五阶段：Z变换]]
> 教材入口：[[📚 教材挂载索引|教材挂载索引]]

## 学习定位
- 模块：典型序列ZT
- 这张卡要回答的问题：单位冲激 δ[n] 与移位冲激的 Z 变换？
- 阶段目标：掌握 Z{δ[n]}=1，Z{δ[n-n0]}=z^{-n0}，是最简基准。

## 对应教材（真实出处）
- Think DSP Ch.10
- Oppenheim §10.1
- MIT 6.003 Lec 20

## 一句话定义
> δ[n] 的 ZT=1（全平面 ROC）；移位 δ[n-n0] 的 ZT=z^{-n0}，对应 z 平面的纯相位/延时。

## 从学习内容上要抓什么
- δ[n] 含所有离散频率等强（类比连续）。
- z^{-1} = 单位延时算子。
- 是 Z 域「1」与「延时」的基准。

## 核心内容
### 1. 基本定义与直觉
单位冲激的 ZT 是平的 1，就像它的 DTFT 也是 1；z^{-1} 就是「推后一格」的记号。

### 2. 公式 / 机制 / 流程
$$\mathcal{Z}\{\delta[n]\}=1,\quad \mathcal{Z}\{\delta[n-n_0]\}=z^{-n_0}$$

### 3. 一个最小例子
延时系统 H(z)=z^{-1} ⇒ 输出 y[n]=x[n-1]。

### 4. 常见误区
- 把 δ[n] 的 ZT 写成含 z 的式子（实为常数 1）。
- 忽略 z^{-1} 即单位延时的意义。

## 和其他笔记的关系
- 前置：[[离散信号]]
- 前置：[[筛选性质]]
- 相关：[[阶跃Z变换]]
- 相关：[[指数Z变换]]
- 相关：[[离散卷积]]
- 返回阶段索引：[[🔢 第五阶段：Z变换]]

## 最小自测
> **检索练习 / 通过标准**：合上笔记，能独立复述本节定义、写出核心公式（LaTeX）、指出至少一处常见误区，并独立完成上面的自测题，即视为掌握。

- [ ] 写出 δ[n] 的 ZT。
- [ ] 写出 δ[n-1] 的 ZT。
- [ ] z^{-1} 的物理意义？

*创建于：2026-04-18 · 更新于：2026-08-06*

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/12-信号与系统"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
