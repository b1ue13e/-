---
type: study
topic: "Fourier级数"
course: "实变函数"
created: 2026-08-09
status: completed
learn_status: not_started
stage_moc: "[[🧭 阶段4-Fourier与应用]]"
flow: knowledge
kind: concept
difficulty: advanced
concept: ["Fourier系数", "三角级数", "收敛类型"]
upstream: ["[[实变函数-收敛关系]]"]
related: ["[[实变函数-Fourier级数与L2收敛]]"]
source: "Stein & Shakarchi, Real Analysis (2005), Ch.5"
source_url: "https://press.princeton.edu/books/hardcover/9780691113869/real-analysis"
accessed: 2026-08-09
license: "Copyright (c) Princeton University Press; 仅作参考，不复制正文"
tags: [学习, 实变函数, Fourier]
---

# 实变函数-Fourier级数

## 为什么学

Fourier 级数是"用正弦余弦分解周期函数"的系统。在 Riemann 时代就有(Dirichlet 收敛定理),但真正干净的理论在 $L^2$ 框架下:$L^2$ 正交基使收敛变得无条件。本卡给出系数定义、正交性、点态收敛的 Dirichlet 条件。

## 核心定义

- 对 $f\in L^1([-\pi,\pi])$ 周期延拓,Fourier 系数
  $$\hat f(n)=\frac{1}{2\pi}\int_{-\pi}^{\pi}f(x)e^{-inx}\,dx.$$
- 部分和 $S_N(f)(x)=\sum_{n=-N}^{N}\hat f(n)e^{inx}=\frac{1}{2\pi}\int_{-\pi}^{\pi}f(x-t)D_N(t)\,dt$,
  其中 $D_N(t)=\frac{\sin((N+1/2)t)}{\sin(t/2)}$ 为 **Dirichlet 核**。

## 证明主线(逐步展开)

### 1. 正交性

$\frac{1}{2\pi}\int_{-\pi}^{\pi}e^{int}e^{-imt}\,dt=\delta_{nm}$。由此系数唯一,且投影公式成立。

### 2. Dirichlet 核与部分和

改写 $S_N$ 为与 $D_N$ 的卷积(上式)。$D_N$ 满足 $\frac{1}{2\pi}\int D_N=1$,但 $\|D_N\|_1\sim\log N$ 无界——这是 Fourier 级数点态收敛比 $L^2$ 更微妙的根源(有界核才能保证逐点收敛)。

### 3. 点态收敛(Dirichlet 条件)

若 $f$ 在 $x$ 处满足单边导数存在(或局部 Lipschitz),则 $S_N(f)(x)\to f(x)$。
**证明**:把 $D_N$ 代入后分部积分,将 $f(x-t)-f(x)$ 与有界核 $K_N$ 配对,再用 Lebesgue 微分定理得极限为 0。

## 最小例子

- $f(x)=x$ 在 $(-\pi,\pi)$:$S_N\to x$,但在端点跳跃处收敛到 0,并出现 **Gibbs 现象**(overshoot 约 9%)。
- 方波:其 Fourier 级数在间断点处振荡不止。

## 常见误区

- 以为 $L^1$ 函数的 Fourier 级数处处收敛。错:存在 $L^1$ 函数其 Fourier 级数处处发散;Carleson 定理只对 $L^2$ 保证 a.e. 收敛。
- 混淆 $D_N$(部分和核)与 Fejér 核(Cesàro 平均核,恒收敛)。
- 把 Fourier 级数(周期/离散谱)与 Fourier 变换(非周期/连续谱)混为一谈。

## 与实变函数的连接

- 建立在收敛关系上([[实变函数-收敛关系]])。
- $L^2$ 收敛与 Parseval 见 [[实变函数-Fourier级数与L2收敛]]。
- 与变换衔接 [[实变函数-Fourier变换]]。

## 最小自测

- [ ] 写出 Fourier 系数与 Dirichlet 核
- [ ] 证明三角函数正交性
- [ ] 说明 Dirichlet 条件如何推出点态收敛

## 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

通过标准:自测全过。下一步 [[实变函数-Fourier级数与L2收敛]]。
