---
type: study
topic: "DFT时域周期"
created: 2026-04-18
updated: 2026-08-06
status: completed
difficulty: advanced
concept: ["DFT时域周期", "DFT的隐含周期性"]
prerequisites: []
related: []
tags: ["学习", "信号与系统"]
course: "信号与系统"
flow: knowledge
stage_moc: "[[💻 第七阶段：DFT与FFT|DFT与FFT]]"
sources:
  - "Think DSP Ch.7"
  - "Oppenheim §8.1：DFT"
  - "MIT 6.003 Lec 18"
kind: concept

upstream:
  - "[[DFT乘积]]"
---
# DFT时域周期

> 所属路径：[[🗺️ 信号与系统学习路径|信号与系统学习路径]]
> 所属阶段：[[💻 第七阶段：DFT与FFT|DFT与FFT]]
> 教材入口：[[📚 教材挂载索引|教材挂载索引]]

## 学习定位
- 模块：DFT 隐含周期
- 这张卡要回答的问题：为何说 DFT 隐含「时域周期延拓」？
- 阶段目标：理解 DFT 把有限长序列视为周期 N 的主值，截断即隐含周期化。

## 对应教材（真实出处）
- Think DSP Ch.7
- Oppenheim §8.1：DFT
- MIT 6.003 Lec 18

## 一句话定义
> DFT 定义在 0..N-1，但核 e^{-j2πkn/N} 周期 N，故 DFT 等效把 x[n] 当周期 N 序列处理；有限长截断⇒周期延拓（可能引起端点不连续）。

## 从学习内容上要抓什么
- DFT 不区分主值与周期延拓。
- 非整周期截断⇒周期延拓出现跳变⇒频谱泄漏。
- 圆周运算皆源于此周期性。

## 核心内容
### 1. 基本定义与直觉
DFT 像把一段录音头尾黏成环：它默认这段会无限重复，所以端点不连续会被当成「每周期都跳一下」。

### 2. 公式 / 机制 / 流程
$$x_p[n]=\sum_r x[n+rN]\quad(\text{周期延拓}),\quad X[k]=\sum_{n=0}^{N-1}x[n]W_N^{kn}$$

### 3. 一个最小例子
截断正弦若非整周期，黏环处跳变⇒泄漏。

### 4. 常见误区
- 忽略隐含周期导致误解圆周卷积/泄漏。
- 把 DFT 当「真正有限长」变换。

## 和其他笔记的关系
- 前置：[[DFT频域周期]]
- 前置：[[频谱泄漏原因]]
- 相关：[[循环卷积定义]]
- 相关：[[加窗]]
- 相关：[[栅栏效应原因]]
- 返回阶段索引：[[💻 第七阶段：DFT与FFT|DFT与FFT]]

## 最小自测
> **检索练习 / 通过标准**：合上笔记，能独立复述本节定义、写出核心公式（LaTeX）、指出至少一处常见误区，并独立完成上面的自测题，即视为掌握。

- [ ] 说明 DFT 隐含时域周期。
- [ ] 这与泄漏有何关系？
- [ ] 写出 DFT 公式。

*创建于：2026-04-18 · 更新于：2026-08-06*

## 学完后可以完成

> 暂无直接依赖本卡的知识点作业（可结合「相关」卡或阶段作业做综合训练）。

```dataview
LIST
FROM "03-Projects/12-信号与系统"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
