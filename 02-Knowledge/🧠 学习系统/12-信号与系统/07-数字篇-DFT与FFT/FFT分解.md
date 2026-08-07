---
type: study
topic: "FFT分解"
created: 2026-04-18
updated: 2026-08-06
status: completed
difficulty: beginner
concept: ["FFT分解"]
prerequisites: []
related: []
tags: ["学习", "信号与系统"]
course: "信号与系统"
flow: knowledge
stage_moc: "[[💻 第七阶段：DFT与FFT|DFT与FFT]]"
kind: concept
sources:
  - "Think DSP Ch.8：Fast Convolution / FFT"
  - "MIT 6.003 Lec 20：FFT"
  - "Oppenheim §9.1-9.2：Efficient DFT"
---

# FFT分解

> 所属路径：[[🗺️ 信号与系统学习路径|信号与系统学习路径]]
> 所属阶段：[[💻 第七阶段：DFT与FFT|DFT与FFT]]
> 教材入口：[[📚 教材挂载索引|教材挂载索引]]

## 学习定位
- 模块：DFT 与 FFT
- 这张卡要回答的问题：FFT 为什么能把 DFT 从 O(N²) 降到 O(N log N)？
- 阶段目标：理解 FFT 的分治思想，为高效频谱计算与卷积打基础。

## 对应教材（真实出处）
- Think DSP Ch.8：Fast Convolution / FFT
- MIT 6.003 Lec 20：FFT
- Oppenheim §9.1-9.2：Efficient DFT

## 一句话定义
> FFT（以 Cooley-Tukey 为代表）利用旋转因子 $W_N^{kn}$ 的周期性与对称性，把长度 N 的 DFT 递归分解为更小 DFT，复杂度由 N² 降至 N log₂N。

## 从学习内容上要抓什么
- 分治：N=N1·N2 时把 DFT 拆成 N1 个 N2 点 DFT 组合。
- radix-2 要求 N 为 2 的幂，最常用。
- 实际提速巨大：N=1024 时约快 100 倍。

## 核心内容
### 1. 基本定义与直觉
DFT 里大量计算是重复的“旋转因子”乘法。FFT 发现这些旋转因子有对称和周期规律，于是把大任务拆成小任务、复用中间结果——像分治法排序一样，把平方级降到线性对数级。

### 2. 公式 / 机制 / 流程
$W_N=e^{-j2\pi/N}$；$\mathrm{DFT}_N$ 分解为 $\mathrm{DFT}_{N/2}$（偶/奇）组合，蝶形运算。

### 3. 一个最小例子
例：N=8 的 radix-2 FFT 只需 12 次复乘（vs 直接 DFT 64 次），按蝶形图三级完成。

### 4. 常见误区
- 以为 FFT 是另一种变换；它只是 DFT 的快速算法。
- 忽略 N 为 2 的幂时 radix-2 最方便，非 2 幂可用混合基。

## 和其他笔记的关系
- 前置：[[DFT乘积]]
- 相关：[[Cooley-Tukey]]、[[循环卷积]]、[[NumPy信号]]

## 最小自测
> **检索练习 / 通过标准**：合上笔记，能独立复述本节定义、写出核心公式（LaTeX）、指出至少一处常见误区，并独立完成上面的自测题，即视为掌握。

- [ ] 说明 FFT 相比直接 DFT 的复杂度提升。
- [ ] 解释 FFT 的分治基本思想。
- [ ] 指出 radix-2 FFT 对长度 N 的要求。

*创建于：2026-04-18 · 更新于：2026-08-06*

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/12-信号与系统"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
