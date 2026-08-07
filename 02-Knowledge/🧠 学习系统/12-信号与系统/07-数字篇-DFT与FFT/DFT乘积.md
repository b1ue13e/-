---
type: study
topic: "DFT乘积"
created: 2026-04-18
updated: 2026-08-06
status: completed
difficulty: beginner
concept: ["DFT乘积"]
prerequisites: []
related: []
tags: ["学习", "信号与系统"]
course: "信号与系统"
flow: knowledge
stage_moc: "[[💻 第七阶段：DFT与FFT|DFT与FFT]]"
kind: concept
sources:
  - "Think DSP Ch.7：The Discrete Fourier Transform"
  - "MIT 6.003 Lec 17-18：DFT"
  - "Oppenheim §8.1-8.2：Discrete Fourier Transform"
upstream:
  - "[[傅里叶变换定义]]"
  - "[[卷积定理]]"
---

# DFT乘积

> 所属路径：[[🗺️ 信号与系统学习路径|信号与系统学习路径]]
> 所属阶段：[[💻 第七阶段：DFT与FFT|DFT与FFT]]
> 教材入口：[[📚 教材挂载索引|教材挂载索引]]

## 学习定位
- 模块：DFT 与 FFT
- 这张卡要回答的问题：离散傅里叶变换（DFT）如何定义？它和连续傅里叶变换是什么关系？
- 阶段目标：掌握有限长序列的频域表示，为 FFT 与数字滤波奠基。

## 对应教材（真实出处）
- Think DSP Ch.7：The Discrete Fourier Transform
- MIT 6.003 Lec 17-18：DFT
- Oppenheim §8.1-8.2：Discrete Fourier Transform

## 一句话定义
> 对长度为 N 的序列，$X[k]=\sum_{n=0}^{N-1}x[n]e^{-j2\pi kn/N}$（k=0..N-1），逆变换 $x[n]=\frac{1}{N}\sum X[k]e^{j2\pi kn/N}$。DFT 是连续 FT 在等间隔频点的采样。

## 从学习内容上要抓什么
- DFT 输入输出都是有限长、离散的（时域与频域都离散）。
- 频点 k 对应频率 k·(fs/N)；隐含周期性（模 N）。
- 与 DTFT 不同：DTFT 连续频谱，DFT 是其 N 点采样。

## 核心内容
### 1. 基本定义与直觉
DFT 把一段有限长的离散信号，投影到 N 个等间隔的“旋转基”上——相当于在连续频谱上只取 N 个采样点来看。它是连接离散信号与频域计算（尤其是 FFT）的桥梁。

### 2. 公式 / 机制 / 流程
$$X[k]=\sum_{n=0}^{N-1}x[n]e^{-j2\pi kn/N},\quad x[n]=\frac{1}{N}\sum_{k=0}^{N-1}X[k]e^{j2\pi kn/N}$$

### 3. 一个最小例子
例：x=[1,0,−1,0]，手算 4 点 DFT 得 X=[0,2,0,2]（仅偶次频率有分量）。

### 4. 常见误区
- 忘记逆变换的 1/N 因子。
- 混淆 DFT（有限离散）与 DTFT（连续频谱）的适用范围。

## 和其他笔记的关系
- 前置：[[傅里叶变换定义]]、[[离散信号]]
- 相关：[[循环卷积]]、[[FFT分解]]、[[Cooley-Tukey]]、[[乘积定理]]

## 最小自测
> **检索练习 / 通过标准**：合上笔记，能独立复述本节定义、写出核心公式（LaTeX）、指出至少一处常见误区，并独立完成上面的自测题，即视为掌握。

- [ ] 写出 DFT 正变换公式并说明 k 对应什么频率。
- [ ] 写出 IDFT 并指出 1/N 因子的位置。
- [ ] 手算一个 4 点序列的 DFT。

*创建于：2026-04-18 · 更新于：2026-08-06*

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/12-信号与系统"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
