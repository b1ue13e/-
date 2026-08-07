---
type: study
topic: "Cooley-Tukey正确性推导"
created: 2026-08-06
updated: 2026-08-06
status: completed
difficulty: advanced
concept: ["Cooley-Tukey正确性推导", "FFT分解证明"]
prerequisites: ["Cooley-Tukey", "FFT分解"]
related: ["Cooley-Tukey", "FFT分解", "DFT乘积", "蝶形运算", "位反转"]
tags: ["学习", "信号与系统", "推导"]
course: "信号与系统"
flow: knowledge
stage_moc: "[[💻 第七阶段：DFT与FFT]]"
kind: derivation
sources:
  - "Oppenheim §9.3：Cooley-Tukey (derivation)"
  - "Think DSP Ch.8：The Cooley-Tukey algorithm"
  - "MIT 6.003 Lec 20"
upstream:
  - "[[Cooley-Tukey]]"
  - "[[DFT乘积]]"
  - "[[卷积定理推导]]"
---

# Cooley-Tukey 正确性推导

> 所属路径：[[🗺️ 信号与系统学习路径|信号与系统学习路径]]
> 所属阶段：[[💻 第七阶段：DFT与FFT]]
> 教材入口：[[📚 教材挂载索引|教材挂载索引]]
> 配套概念卡：[[Cooley-Tukey]]、[[FFT分解]]、[[蝶形运算]]

## 学习定位
- 模块：DFT 与 FFT
- 这张卡要回答的问题：radix-2 时域抽取（DIT）的奇偶分解公式为什么精确等于完整 N 点 DFT？复杂度为何降为 $O(N\log N)$？
- 阶段目标：从 DFT 定义严格推出 $X[k]=E[k]+W_N^k O[k]$ 与下半支符号翻转，并说明蝶形结构与位反转的来源。

## 约定
- DFT：$X[k]=\sum_{n=0}^{N-1}x[n]W_N^{kn},\quad W_N=e^{-j2\pi/N},\;k=0,\dots,N-1$。
- 设 $N$ 为 2 的幂（radix-2）。偶下标 $n=2r$，奇下标 $n=2r+1$，$r=0,\dots,N/2-1$。

## 推导
将求和按奇偶拆开：
$$
\begin{aligned}
X[k]
&=\sum_{r=0}^{N/2-1}x[2r]W_N^{k(2r)}+\sum_{r=0}^{N/2-1}x[2r+1]W_N^{k(2r+1)} \\[4pt]
&=\sum_{r}x[2r]\big(W_N^{2}\big)^{kr}+W_N^{k}\sum_{r}x[2r+1]\big(W_N^{2}\big)^{kr}
\end{aligned}
$$
注意 $W_N^{2}=e^{-j2\pi\cdot 2/N}=e^{-j2\pi/(N/2)}=W_{N/2}$。于是
$$
X[k]=\underbrace{\sum_{r}x[2r]W_{N/2}^{kr}}_{E[k]\;:\;N/2\text{ 点 DFT of 偶序}}+\;W_N^{k}\underbrace{\sum_{r}x[2r+1]W_{N/2}^{kr}}_{O[k]\;:\;N/2\text{ 点 DFT of 奇序}}
$$
即 $X[k]=E[k]+W_N^{k}O[k]$。

**下半支（$k+N/2$）：** 利用 $W_N^{N/2}=e^{-j\pi}=-1$ 与 $W_{N/2}^{(k+N/2)r}=W_{N/2}^{kr}W_{N/2}^{(N/2)r}=W_{N/2}^{kr}\cdot 1$（因 $W_{N/2}^{N/2}=1$），有
$$E[k+N/2]=E[k],\qquad O[k+N/2]=O[k]$$
故
$$X[k+N/2]=E[k]+W_N^{k+N/2}O[k]=E[k]-W_N^{k}O[k]$$
合并得经典蝶形：
$$\boxed{
\begin{aligned}
X[k]&=E[k]+W_N^{k}O[k]\\
X[k+N/2]&=E[k]-W_N^{k}O[k]
\end{aligned}
}\qquad k=0,\dots,N/2-1\qquad\blacksquare$$
递归对 $E,O$ 继续拆分，即得完整 FFT。

## 复杂度
- 朴素 DFT：$N$ 个点各需 $N$ 次复乘 $\Rightarrow O(N^2)$。
- FFT：每层有 $N/2$ 个蝶形（每蝶形 1 次复乘），共 $\log_2 N$ 层 $\Rightarrow$ 复乘约 $\frac{N}{2}\log_2 N$，即 $O(N\log N)$。

## 常见误区
- **「时域抽取」是按时间下标奇偶分，不是按频率分**（DIF 才反过来）。
- **忘用旋转因子 $W_N^k$ 合成上下半支**：少了它上下支只是同值相加，得不到正确频谱。
- **下半支符号来源不清**：$X[k+N/2]$ 的差号来自 $W_N^{N/2}=-1$，这是关键。
- **位反转来源**：自然序输入经递归奇偶拆后，内存地址按位反转排列，故输出需位反转重排（见 [[位反转]]）。
- **周期误解**：$E[k],O[k]$ 是长度为 $N/2$ 的 DFT，对下标以 $N/2$ 为周期，所以 $E[k+N/2]=E[k]$ 成立。

## 和其他笔记的关系
- 前置：[[Cooley-Tukey]]、[[FFT分解]]、[[DFT乘积]]
- 配套：[[蝶形运算]]、[[位反转]]、[[循环卷积]]
- 应用：[[卷积定理推导]]（频域乘法代替长卷积）

## 最小自测
> **检索练习 / 通过标准**：能从 DFT 定义推出奇偶分解的蝶形公式，说明 $W_N^{N/2}=-1$ 如何给出下半支，并给出复杂度阶。

- [ ] 写出 $X[k]=E[k]+W_N^k O[k]$ 的拆分与 $W_N^2=W_{N/2}$ 化简。
- [ ] 推导 $X[k+N/2]=E[k]-W_N^k O[k]$，点明 $-1$ 的来源。
- [ ] 说明为何 FFT 复杂度是 $O(N\log N)$ 而非 $O(N^2)$。
- [ ] 解释位反转为何出现。

*创建于：2026-08-06 · 更新于：2026-08-06*

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/12-信号与系统"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
