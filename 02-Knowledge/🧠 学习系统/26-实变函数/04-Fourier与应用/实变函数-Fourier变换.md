---
type: study
topic: "Fourier变换"
course: "实变函数"
created: 2026-08-09
status: completed
learn_status: not_started
stage_moc: "[[🧭 阶段4-Fourier与应用]]"
flow: knowledge
kind: concept
difficulty: advanced
concept: ["Fourier变换", "平移", "缩放"]
upstream: ["[[实变函数-Fourier级数与L2收敛]]"]
related: ["[[实变函数-卷积定理]]"]
source: "Stein & Shakarchi, Real Analysis (2005), Ch.5"
source_url: "https://press.princeton.edu/books/hardcover/9780691113869/real-analysis"
accessed: 2026-08-09
license: "Copyright (c) Princeton University Press; 仅作参考，不复制正文"
tags: [学习, 实变函数, Fourier]
---

# 实变函数-Fourier变换

## 为什么学

Fourier 级数处理周期函数(离散谱);Fourier 变换处理非周期函数(连续谱)。它是偏微分方程、信号处理、概率论的核心工具。本卡给出定义、基本性质(平移/缩放/导数)和 Plancherel(变换版的 Parseval)。

## 核心定义

- $\hat f(\xi)=\int_{\mathbb R^n}f(x)e^{-2\pi i x\cdot\xi}\,dx$($f\in L^1$)。
- 反演:若 $f,\hat f\in L^1$,则 $f(x)=\int\hat f(\xi)e^{2\pi i x\cdot\xi}\,d\xi$。
- 在 $L^2$ 上经 Plancherel 延拓为酉算子。

## 证明主线(逐步展开)

### 1. 基本性质

- 平移:$\widehat{f(x-a)}(\xi)=e^{-2\pi i a\cdot\xi}\hat f(\xi)$。
- 缩放:$\widehat{f(ax)}(\xi)=|a|^{-1}\hat f(\xi/a)$。
- 导数:$\widehat{f'}(\xi)=2\pi i\xi\hat f(\xi)$(分部积分,边界项因 $f\in L^1$ 衰减消失)。

### 2. Plancherel 定理

$\int|\hat f|^2=\int|f|^2$(先对 $L^1\cap L^2$ 证,再稠密延拓到 $L^2$)。这是 $L^2$ 上 Fourier 变换为等距(酉)算子的依据。

### 3. 反演公式

取近似恒等核 $K_t$(如 Gauss),证 $(f*K_t)\to f$,且 $\widehat{f*K_t}=\hat f\cdot\hat K_t$,令 $t\to0$ 得反演。Gauss 核 $g(x)=e^{-\pi|x|^2}$ 满足 $\hat g=g$,是最干净的演示。

## 最小例子

- $\widehat{\mathbf 1_{[-a,a]}}(\xi)=\frac{\sin(2\pi a\xi)}{\pi\xi}$,展示矩形函数的 sinc 谱。
- Gauss $e^{-\pi x^2}$ 是 Fourier 变换的特征函数(变换后仍是自身)。

## 常见误区

- 变换要求 $f\in L^1$ 才有逐点定义;一般 $L^2$ 函数需 Plancherel 解释。
- 混淆频率归一化($e^{-2\pi ix\xi}$ vs $e^{-ix\xi}$)导致导数公式差 $2\pi$ 因子。
- 反演需要 $\hat f\in L^1$,否则需主值/Cauchy 意义。

## 与实变函数的连接

- 级数到变换的推广([[实变函数-Fourier级数与L2收敛]])。
- 卷积定理使变换可解微分方程([[实变函数-卷积定理]])。
- mollifier 用变换/卷积做光滑逼近([[实变函数-mollifier与正则化]])。

## 最小自测

- [ ] 证平移/缩放/导数性质
- [ ] 写 Plancherel 等式
- [ ] 计算矩形函数的 Fourier 变换

## 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

通过标准:自测全过。下一步 [[实变函数-卷积定理]]。
