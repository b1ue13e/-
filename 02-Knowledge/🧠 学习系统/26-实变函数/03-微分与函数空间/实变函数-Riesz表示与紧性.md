---
type: study
topic: "Riesz表示与紧性"
course: "实变函数"
created: 2026-08-09
status: completed
learn_status: not_started
stage_moc: "[[🧭 阶段3-微分与函数空间]]"
flow: knowledge
kind: concept
difficulty: advanced
concept: ["Riesz表示定理", "弱紧性", "对偶空间"]
upstream: ["[[实变函数-L2空间与完备性]]"]
related: ["[[实变函数-Lp空间与不等式]]"]
source: "Stein & Shakarchi, Real Analysis (2005), Ch.4 (Hilbert); Radon-Nikodym 见 Ch.6"
source_url: "https://press.princeton.edu/books/hardcover/9780691113869/real-analysis"
accessed: 2026-08-09
license: "Copyright (c) Princeton University Press; 仅作参考，不复制正文"
tags: [学习, 实变函数, Lp空间]
---

# 实变函数-Riesz表示与紧性

## 为什么学

Hilbert 空间最重要的结构定理:Riesz 表示定理说 $L^2$ 上的连续线性泛函都来自内积($T(f)=\langle f,g\rangle$)。这让"对偶"变得具体。弱紧性(有界序列有弱收敛子列)是证明存在性的利器(变分、最优控制、逼近论)。

## 核心定义

- 连续线性泛函 $T:L^2\to\mathbb R$,$\|T\|=\sup_{\|f\|=1}|T(f)|$。
- **弱收敛** $f_n\rightharpoonup f$:对所有 $g$,$\langle f_n,g\rangle\to\langle f,g\rangle$。

## 证明主线(逐步展开)

### 1. Riesz 表示定理($L^2$)

设 $T$ 连续线性。若 $T=0$ 取 $g=0$。否则 $\ker T$ 是闭子空间且非零正交补存在。取 $h\perp\ker T$,$h\ne0$。对任意 $f$,分解 $f=f_0+\lambda h$($f_0\in\ker T$),则 $T(f)=\lambda T(h)$。而
$$\lambda=\frac{\langle f,h\rangle}{\|h\|_2^2},$$
故 $T(f)=\langle f,\ \overline{T(h)}h/\|h\|_2^2\rangle$。取 $g=\overline{T(h)}h/\|h\|_2^2$,则 $T(f)=\langle f,g\rangle$,且 $\|T\|=\|g\|_2$。∎

### 2. 有界序列有弱收敛子列

在可分 Hilbert 空间中,单位球弱紧:取有界列,对可数稠密集逐点取子列(对角线法),再用有界性 + 稠密性推广到全空间弱收敛。这是 Banach-Alaoglu 在 Hilbert 空间的体现。

### 3. Radon-Nikodym(概要,Ch.6)

若 $\nu\ll\mu$ 为 $\sigma$-有限测度,则存在 $f=d\nu/d\mu$ 使 $\nu(A)=\int_A f\,d\mu$。证明用 Hahn 分解 + $L^2$ 上泛函对应密度(由 Riesz 表示)。

## 最小例子

- $T(f)=\int_0^1 f(x)\,x\,dx$ 是 $L^2[0,1]$ 上泛函,对应 $g(x)=x$。直接验证 $\langle f,g\rangle=T(f)$。

## 常见误区

- Riesz 表示在一般 Banach 空间不都"漂亮"(需要具体对偶空间);在 Hilbert 空间才简洁。
- 弱收敛不保范数:$\|f_n\|\not\to\|f\|$ 一般;只保弱下半连续 $\|f\|\le\liminf\|f_n\|$。
- 混淆弱收敛与强($L^2$)收敛。

## 与实变函数的连接

- 依赖 $L^2$ 内积与完备性([[实变函数-L2空间与完备性]])。
- Radon-Nikodym 是测度论核心,延伸自 [[实变函数-外测度]]。

## 最小自测

- [ ] 陈述并证明 $L^2$ 的 Riesz 表示定理
- [ ] 说明弱收敛不保范数(举例)
- [ ] 写出 Radon-Nikodym 定理的陈述

## 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

通过标准:自测全过。下一步 [[实变函数-收敛关系]]。
