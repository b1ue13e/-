---
type: study
topic: "Fourier应用专题"
course: "实变函数"
created: 2026-08-09
status: completed
learn_status: not_started
stage_moc: "[[🧭 阶段4-Fourier与应用]]"
flow: knowledge
kind: concept
difficulty: advanced
concept: ["热方程", "波动方程", "滤波", "频谱"]
upstream: ["[[实变函数-mollifier与正则化]]"]
related: ["[[实变函数-卷积定理]]"]
source: "Stein & Shakarchi, Real Analysis (2005), Ch.5"
source_url: "https://press.princeton.edu/books/hardcover/9780691113869/real-analysis"
accessed: 2026-08-09
license: "Copyright (c) Princeton University Press; 仅作参考，不复制正文"
tags: [学习, 实变函数, Fourier应用]
---

# 实变函数-Fourier应用专题

## 为什么学

Fourier 方法不只在课本里:热方程、波动方程、滤波、频谱分析都靠它。本卡串起几个标准应用,展示"把微分变乘法"的威力,并点出实变函数提供的严格基础(收敛、积分换序、$L^2$ 框架)。

## 核心应用

### 1. 热方程

$\partial_t u=\Delta u$,初值 $u(0,x)=f(x)$。Fourier 域:$\widehat{u_t}=-4\pi^2|\xi|^2\hat u$,解得 $\hat u(t,\xi)=e^{-4\pi^2|\xi|^2t}\hat f(\xi)$,反演得 $u=f*K_t$,$K_t$ 为热核。严格性由 $L^2$ 框架 + Plancherel 保证。

### 2. 波动方程与采样

一维波动方程经 Fourier 变为两个一阶方程;采样定理(Nyquist)由频带受限函数的 Fourier 反演给出——连接信号处理。

### 3. 滤波与频谱

低通滤波 = 乘一个频域指示函数,再反变换 = 与 sinc 卷积。Gibbs 现象(见 [[实变函数-Fourier级数]])说明理想滤波有振铃。

### 4. 概率与特征函数

独立随机变量和的特征函数是特征函数之积——即 Fourier 变换域的卷积定理。中心极限定理的标准证明经特征函数完成。

## 证明主线(以热方程为例)

1. 对方程两边取 Fourier 变换(对空间变量),利用 $\widehat{\Delta u}=-4\pi^2|\xi|^2\hat u$。
2. 化为 ODE $\partial_t\hat u=-4\pi^2|\xi|^2\hat u$,解指数。
3. 反演 + 卷积定理得 $u=f*K_t$。
全程依赖 [[实变函数-卷积定理]] 与 [[实变函数-Fourier变换]] 的严格基础。

## 最小例子

- 初值为 $\mathbf 1_{[-a,a]}$ 的热方程解,随 $t$ 扩散为 Gauss 型。
- 两独立均匀变量之和(卷积例)的分布是三角核。

## 常见误区

- 以为"Fourier 能解一切 PDE"。错:非线性、复杂边界需其他方法。
- 忽略收敛条件就做反演。
- 把离散 FFT 与连续变换的数学前提混淆。

## 与实变函数的连接

- 全部依赖前几张卡([[实变函数-Fourier变换]]、[[实变函数-卷积定理]]、[[实变函数-mollifier与正则化]]、[[实变函数-Fourier级数]])。
- 概率应用连回 [[实变函数-L2空间与完备性]] 的 $L^2$ 框架。

## 最小自测

- [ ] 用 Fourier 法推导热方程解的形式
- [ ] 说明低通滤波 = 频域乘法 = 与 sinc 卷积
- [ ] 举一个 Fourier 在概率中的应用(特征函数)

## 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

通过标准:自测全过。本课程核心卡完结。
