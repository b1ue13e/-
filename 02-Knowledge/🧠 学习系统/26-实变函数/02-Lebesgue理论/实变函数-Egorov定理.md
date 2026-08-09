---
type: study
topic: "Egorov 定理"
course: "实变函数"
created: 2026-08-09
updated: 2026-08-09
status: completed
learn_status: not_started
stage_moc: "[[🧭 阶段2-Lebesgue理论]]"
flow: knowledge
kind: theorem
difficulty: advanced
concept: ["Egorov 定理", "几乎处处收敛", "一致收敛", "有限测度"]
upstream: ["[[实变函数-可测函数]]", "[[实变函数-三大收敛定理]]"]
related: ["[[实变函数-Lusin定理]]", "[[实变函数-Riesz依测度收敛子列]]"]
source: "Stein & Shakarchi, Real Analysis (2005), Ch.1/2"
source_url: "https://press.princeton.edu/books/hardcover/9780691113869/real-analysis"
accessed: 2026-08-09
license: "Copyright (c) Princeton University Press; 仅作参考，不复制正文"
tags: [学习, 实变函数, Lebesgue理论]
---

# 实变函数-Egorov 定理

## 为什么学

"几乎处处收敛"是 Lebesgue 理论里最常用的收敛,但它比"一致收敛"弱得多——a.e. 收敛允许在无穷多个点上乱跳。Egorov 定理说:在**有限测度**集上,a.e. 收敛"几乎"就是一致收敛——你可以扔掉一个任意小的集合,在剩下的集合上收敛是一致的。这是把 a.e. 收敛转化为一致收敛(从而能套用连续函数的好性质)的关键桥。

## 定理陈述

设 $(X,\mathcal{M},\mu)$ 为测度空间,$E\in\mathcal{M}$,$\mu(E)<\infty$。若 $f_n,f$ 在 $E$ 上有限 a.e.,且 $f_n\to f$ a.e. 于 $E$,则对任意 $\varepsilon>0$,存在可测集 $A\subset E$ 使 $\mu(E\setminus A)<\varepsilon$,且在 $A$ 上 $f_n\to f$ **一致**。

> 直觉:有限测度把"坏点"关进了一个可以任意缩小的小盒子里。

## 证明主线(逐步展开)

1. **把"不收敛得足够好"的集合量化。** 对 $k,m\in\mathbb{N}$,令
   $$E_k^{(m)}=\bigcup_{n\ge m}\Big\{x\in E:\big|f_n(x)-f(x)\big|\ge\frac1k\Big\}.$$
   $E_k^{(m)}$ 关于 $m$ 递减;记 $E_k=\bigcap_{m=1}^\infty E_k^{(m)}$。
   若 $x\notin E_k$,则存在 $m$ 使对所有 $n\ge m$,$|f_n(x)-f(x)|<1/k$——即 $f_n(x)\to f(x)$ 且误差最终小于 $1/k$。所以 $E_k$ 正是"误差永远 $\ge1/k$"的点集,由 a.e. 收敛知 $\mu(E_k)=0$。

2. **用从上连续性让尾巴任意小。** 因 $\mu(E_k^{(1)})\le\mu(E)<\infty$,且 $E_k^{(m)}\downarrow E_k$,连续性从上有
   $$\lim_{m\to\infty}\mu\big(E_k^{(m)}\big)=\mu(E_k)=0.$$
   故可取 $m_k$ 使 $\mu\big(E_k^{(m_k)}\big)<\varepsilon/2^k$。

3. **取好集 $A$。** 令 $A=E\setminus\bigcup_{k=1}^\infty E_k^{(m_k)}$。则
   $$\mu(E\setminus A)\le\sum_{k=1}^\infty\mu\big(E_k^{(m_k)}\big)<\sum_{k=1}^\infty\frac{\varepsilon}{2^k}=\varepsilon.$$

4. **在 $A$ 上验证一致收敛。** 任给 $\delta>0$,取 $k$ 使 $1/k<\delta$。对任意 $x\in A$,$x\notin E_k^{(m_k)}$,即对所有 $n\ge m_k$,$|f_n(x)-f(x)|<1/k<\delta$。$m_k$ 只依赖 $\delta$ 不依赖 $x$——这就是一致收敛。∎

## 最小例子

- 在 $(0,1)$ 上 $f_n(x)=x^n\to0$ a.e.(仅在 $x=1$ 不收敛,零测)。Egorov 保证对任意 $\varepsilon$,存在 $A\subset(0,1)$ 使 $\mu((0,1)\setminus A)<\varepsilon$ 且 $x^n\to0$ 一致于 $A$。取 $A=(0,1-\varepsilon)$ 即可(在 $A$ 上 $|x|^n\le(1-\varepsilon)^n\to0$ 一致)。

## 常见误区

- **漏掉有限测度条件:** 在无限测度空间上结论失效。例 $f_n=\mathbf{1}_{[n,n+1]}$ 在 $\mathbb{R}$ 上处处→0,但对任何有限测度的 $A$,你无法让"补集成小"同时保证一致收敛到 0(坏尾巴跑到无穷远)。Egorov 要求 $\mu(E)<\infty$。
- **以为收敛在整个 $E$ 上一致:** 只在一个去掉小测度集后一致,原集上仍可能不统一。
- **把一致收敛当成 a.e. 收敛:** 反向(一致⇒a.e.)平凡,无需 Egorov。

## 与实变函数的连接

- 是 a.e. 收敛与一致收敛之间的枢纽,常配合 Lusin 定理使用。
- 依赖可测函数与测度的从上连续性([[实变函数-可测函数]])。
- 与依测度收敛的子列原理对照([[实变函数-Riesz依测度收敛子列]])。

## 最小自测

- [ ] 闭卷写出 Egorov 定理陈述(含有限测度条件)
- [ ] 重证:取 $E_k^{(m)}$、用从上连续性选 $m_k$、构造 $A$
- [ ] 举一个没有有限测度时结论失败的例子
- [ ] 说明 Egorov 与"一致收敛⇒a.e. 收敛"的方向关系

## 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

通过标准:自测全过,且能独立重建 $A$ 的构造与一致性论证。下一步 [[实变函数-Lusin定理]]。
