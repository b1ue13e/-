---
title: "实变函数-Fourier级数与L2收敛"
topic: "实变函数-Fourier级数与L2收敛"
date: "2026-08-03"
updated: 2026-08-09
type: study
course: "实变函数"
importance: "A"
tags: [学习, 实变函数]
stage_moc: "[[🧭 阶段4-Fourier与应用]]"
flow: knowledge
kind: concept
upstream: ["[[实变函数-Fourier级数]]", "[[实变函数-L2空间与完备性]]"]
status: completed
learn_status: not_started
difficulty: advanced
concept: ["Fourier 级数", "正交基", "Parseval 等式"]
prerequisites: ["L2空间", "Lebesgue积分", "三角级数"]
related: ["[[实变函数-Fourier变换]]"]
source: "Stein & Shakarchi, Real Analysis (2005), Ch.5"
source_url: "https://press.princeton.edu/books/hardcover/9780691113869/real-analysis"
accessed: 2026-08-09
license: "Copyright (c) Princeton University Press; 仅作参考，不复制正文"
created: 2026-08-03
---

# 实变函数-Fourier级数与L2收敛

## 为什么学

在 $L^2([-\pi,\pi])$ 中,$\{e^{int}/\sqrt{2\pi}\}_{n\in\mathbb Z}$ 是完备正交系,因此每个 $f\in L^2$ 的 Fourier 级数在 $L^2$ 中收敛到 $f$,且 Parseval 等式成立。这是 Hilbert 空间理论的第一个重大应用,也是"用正交基展开"的范本。

## 核心定义

- 内积 $\langle f,g\rangle=\frac{1}{2\pi}\int f\bar g$;$\{e_n=e^{int}/\sqrt{2\pi}\}_{n\in\mathbb Z}$ 正交归一。
- **完备正交系**:其有限线性组合的闭包 = 全空间。

## 证明主线(逐步展开)

### 1. 正交基与最佳逼近

对固定 $N$,$\sum_{|n|\le N}\hat f(n)e^{int}$ 是 $f$ 在 $N$ 维子空间上的 $L^2$ 投影,最小化 $\|f-\sum c_ne^{int}\|_2$。故误差随 $N$ 单调下降。

### 2. 完备性 ⇒ $L^2$ 收敛

需证有限三角多项式在 $L^2$ 中稠密。用 Fejér 平均
$$\sigma_N(f)=\sum_{|n|\le N}\Big(1-\frac{|n|}{N+1}\Big)\hat f(n)e^{int},$$
它是有界算子且对连续函数一致收敛到 $f$;连续函数在 $L^2$ 稠密,故三角多项式稠密。于是 $S_N(f)\to f$ 于 $L^2$。∎

### 3. Parseval 等式

由内积连续性:
$$\frac{1}{2\pi}\int_{-\pi}^{\pi}|f|^2\,dx=\sum_{n\in\mathbb Z}|\hat f(n)|^2.$$
这是能量守恒:$L^2$ 范数 = 谱系数的 $\ell^2$ 范数。

## 最小例子

- $f(x)=x$ 在 $(-\pi,\pi)$:$\hat f(n)=(-1)^{n+1}/(in)$,Parseval 给出 $\sum_{n\ge1}1/n^2=\pi^2/6$ 的推导。
- 方波的 Parseval 直接给出其 $\ell^2$ 系数和。

## 常见误区

- $L^2$ 收敛不保逐点(见 [[实变函数-L2空间与完备性]])。
- 完备性需证明稠密性,不能默认。
- Parseval 是内积空间中勾股定理的无穷维版本。

## 与实变函数的连接

- 依赖 $L^2$ 完备性与内积([[实变函数-L2空间与完备性]])。
- 点态收敛见 [[实变函数-Fourier级数]]。
- 推广到变换 [[实变函数-Fourier变换]]。

## 最小自测

- [ ] 证 $\{e^{int}\}$ 是 $L^2$ 正交系
- [ ] 用 Fejér 平均证完备性 ⇒ $L^2$ 收敛
- [ ] 写 Parseval 等式并举一应用

## 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

通过标准:自测全过。下一步 [[实变函数-Fourier变换]]。
