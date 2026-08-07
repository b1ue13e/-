---
type: study
topic: "指数Z变换"
created: 2026-04-18
updated: 2026-08-06
status: completed
difficulty: intermediate
concept: ["指数Z变换", "常见序列的Z变换"]
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

upstream:
  - "[[Z变换ROC]]"
  - "[[复指数信号]]"
---
# 指数Z变换

> 所属路径：[[🗺️ 信号与系统学习路径|信号与系统学习路径]]
> 所属阶段：[[🔢 第五阶段：Z变换]]
> 教材入口：[[📚 教材挂载索引|教材挂载索引]]

## 学习定位
- 模块：典型序列ZT
- 这张卡要回答的问题：指数序列 a^n u[n] 的 Z 变换是什么？
- 阶段目标：掌握 Z{a^n u[n]}=1/(1-az^{-1})，ROC |z|>|a|，理解 |a| 与稳定。

## 对应教材（真实出处）
- Think DSP Ch.10
- Oppenheim §10.1
- MIT 6.003 Lec 20

## 一句话定义
> a^n u[n] 的 ZT = 1/(1-a z^{-1})，ROC |z|>|a|；|a|<1 稳定（极点圆内），|a|≥1 不稳定。

## 从学习内容上要抓什么
- 极点 z=a，位置决定稳定。
- |a|<1 衰减，=1 临界，>1 增长。
- 是离散一阶系统的基本模态。

## 核心内容
### 1. 基本定义与直觉
离散指数像每步乘 a：|a|<1 逐拍缩小（稳），>1 逐拍放大（炸）。

### 2. 公式 / 机制 / 流程
$$\mathcal{Z}\{a^n u[n]\}=\frac{1}{1-a z^{-1}},\quad |z|>|a|$$

### 3. 一个最小例子
a=0.5 ⇒ 极点 0.5 圆内稳；a=1.2 ⇒ 圆外不稳。

### 4. 常见误区
- ROC 边界写成 |z|>a（应 |a|）。
- 忽略 a 复值时极点在圆上引起振荡。

## 和其他笔记的关系
- 前置：[[阶跃Z变换]]
- 前置：[[Z域极点]]
- 相关：[[冲激Z变换]]
- 相关：[[离散系统函数]]
- 相关：[[因果化]]
- 返回阶段索引：[[🔢 第五阶段：Z变换]]

## 最小自测
> **检索练习 / 通过标准**：合上笔记，能独立复述本节定义、写出核心公式（LaTeX）、指出至少一处常见误区，并独立完成上面的自测题，即视为掌握。

- [ ] 写出 a^n u[n] 的 ZT。
- [ ] ROC 是什么？
- [ ] a 取何值稳定？

*创建于：2026-04-18 · 更新于：2026-08-06*

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/12-信号与系统"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
