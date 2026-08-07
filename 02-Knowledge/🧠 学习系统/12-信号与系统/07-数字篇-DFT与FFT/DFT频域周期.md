---
type: study
topic: "DFT频域周期"
created: 2026-04-18
updated: 2026-08-06
status: completed
difficulty: advanced
concept: ["DFT频域周期", "DFT的隐含周期性"]
prerequisites: []
related: []
tags: ["学习", "信号与系统"]
course: "信号与系统"
flow: knowledge
stage_moc: "[[💻 第七阶段：DFT与FFT|DFT与FFT]]"
sources:
  - "Think DSP Ch.7"
  - "Oppenheim §8.1"
  - "MIT 6.003 Lec 18"
kind: concept

upstream:
  - "[[DFT时域周期]]"
  - "[[DTFT周期性]]"
---
# DFT频域周期

> 所属路径：[[🗺️ 信号与系统学习路径|信号与系统学习路径]]
> 所属阶段：[[💻 第七阶段：DFT与FFT|DFT与FFT]]
> 教材入口：[[📚 教材挂载索引|教材挂载索引]]

## 学习定位
- 模块：DFT 隐含周期
- 这张卡要回答的问题：DFT 的频域为何也是周期的？
- 阶段目标：掌握 X[k] 以 N 为周期，k 与 k+N 等价（对应折叠频率）。

## 对应教材（真实出处）
- Think DSP Ch.7
- Oppenheim §8.1
- MIT 6.003 Lec 18

## 一句话定义
> X[k+N]=X[k]：DFT 频域只有 N 个独立值，k 与 k+N 表示同一频率（k 超 N/2 即负频率折叠）。

## 从学习内容上要抓什么
- 只有 N 个独立频点（含 0 与折叠）。
- k>N/2 对应负频率（按 fftshift 理解）。
- 与 DTFT 的 2π 周期一致（抽样）。

## 核心内容
### 1. 基本定义与直觉
DFT 频域像把圆分成 N 格，转一圈回到原点；后半格其实是「负频率那半圈」。

### 2. 公式 / 机制 / 流程
$$X[k+N]=X[k],\quad k\in\mathbb{Z}$$

### 3. 一个最小例子
N=8：X[5] 对应负频率（等价于 X[-3]）。

### 4. 常见误区
- 把 k>N/2 当「更高正频」（实为折叠负频）。
- 忽略 fftshift 的必要性。

## 和其他笔记的关系
- 前置：[[DFT时域周期]]
- 前置：[[DTFT周期性]]
- 相关：[[栅栏效应原因]]
- 相关：[[补零]]
- 相关：[[卷积关系]]
- 返回阶段索引：[[💻 第七阶段：DFT与FFT|DFT与FFT]]

## 最小自测
> **检索练习 / 通过标准**：合上笔记，能独立复述本节定义、写出核心公式（LaTeX）、指出至少一处常见误区，并独立完成上面的自测题，即视为掌握。

- [ ] 说明 X[k] 的周期性。
- [ ] k>N/2 表示什么？
- [ ] 与 DTFT 周期的关系？

*创建于：2026-04-18 · 更新于：2026-08-06*

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/12-信号与系统"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
