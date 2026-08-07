---
type: study
topic: "DFT线性"
created: 2026-04-18
updated: 2026-08-06
status: completed
difficulty: advanced
concept: ["DFT线性", "线性"]
prerequisites: []
related: []
tags: ["学习", "信号与系统"]
course: "信号与系统"
flow: knowledge
stage_moc: "[[💻 第七阶段：DFT与FFT|DFT与FFT]]"
sources:
  - "Think DSP Ch.7：DFT"
  - "Oppenheim §8.2：Properties"
  - "MIT 6.003 Lec 18"
kind: concept

upstream:
  - "[[DFT时域周期]]"
  - "[[DFT频域周期]]"
  - "[[线性性质]]"
---
# DFT线性

> 所属路径：[[🗺️ 信号与系统学习路径|信号与系统学习路径]]
> 所属阶段：[[💻 第七阶段：DFT与FFT|DFT与FFT]]
> 教材入口：[[📚 教材挂载索引|教材挂载索引]]

## 学习定位
- 模块：DFT 性质
- 这张卡要回答的问题：DFT 的线性性质如何表述？
- 阶段目标：掌握 DFT 是线性变换：DFT{a x + b y}=a·DFT{x}+b·DFT{y}。

## 对应教材（真实出处）
- Think DSP Ch.7：DFT
- Oppenheim §8.2：Properties
- MIT 6.003 Lec 18

## 一句话定义
> DFT 是线性算子：两序列加权之和的 DFT = 各自 DFT 加权之和；前提是同一长度 N（不足补零）。

## 从学习内容上要抓什么
- 源于求和线性。
- 用于把信号拆分量分别求谱再相加。
- 与连续 FT 线性一致。

## 核心内容
### 1. 基本定义与直觉
DFT 像调色盘：两束光的频谱分别算再按比例混，等于先混再算。

### 2. 公式 / 机制 / 流程
$$\mathrm{DFT}\{a x[n]+b y[n]\}=aX[k]+bY[k]$$

### 3. 一个最小例子
x+噪声：DFT 后信号谱与噪声谱线性叠加。

### 4. 常见误区
- 忽略长度 N 需一致（否则要对齐补零）。
- 系数漏带进频域。

## 和其他笔记的关系
- 前置：[[DFT频域周期]]
- 前置：[[线性性质]]
- 相关：[[DFT时域周期]]
- 相关：[[卷积关系]]
- 相关：[[补零]]
- 返回阶段索引：[[💻 第七阶段：DFT与FFT|DFT与FFT]]

## 最小自测
> **检索练习 / 通过标准**：合上笔记，能独立复述本节定义、写出核心公式（LaTeX）、指出至少一处常见误区，并独立完成上面的自测题，即视为掌握。

- [ ] 写出 DFT 线性。
- [ ] 为何要求同长度 N？
- [ ] 举一个应用。

*创建于：2026-04-18 · 更新于：2026-08-06*

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/12-信号与系统"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
