---
type: study
topic: "mollifier与正则化"
course: "实变函数"
created: 2026-08-09
status: completed
learn_status: not_started
stage_moc: "[[🧭 阶段4-Fourier与应用]]"
flow: knowledge
kind: concept
difficulty: advanced
concept: ["mollifier", "正则化", "光滑逼近"]
upstream: ["[[实变函数-卷积定理]]"]
related: ["[[实变函数-Fourier应用专题]]"]
source: "Stein & Shakarchi, Real Analysis (2005), Ch.3/Ch.5"
source_url: "https://press.princeton.edu/books/hardcover/9780691113869/real-analysis"
accessed: 2026-08-09
license: "Copyright (c) Princeton University Press; 仅作参考，不复制正文"
tags: [学习, 实变函数, Fourier]
---

# 实变函数-mollifier与正则化

## 为什么学

很多存在性证明需要"先用光滑函数逼近,再取极限"。mollifier(光滑近似恒等)提供了一套标准工具:对任意局部可积 $f$,$f*\eta_\varepsilon$ 是 $C^\infty$ 且当 $\varepsilon\to0$ 时回到 $f$(在连续点 / $L^p$ 意义)。它是连接"粗糙函数"与"光滑函数"的桥梁,也是证明 Lebesgue 微分定理与弱解正则性的基础。

## 核心定义

- 取 $\eta\in C_c^\infty(B_1)$,$\eta\ge0$,$\int\eta=1$;令 $\eta_\varepsilon(x)=\varepsilon^{-n}\eta(x/\varepsilon)$。
- **正则化**:$f_\varepsilon=f*\eta_\varepsilon$。

## 证明主线(逐步展开)

### 1. 光滑性

$\eta_\varepsilon\in C^\infty$,卷积保持光滑性,故 $f_\varepsilon\in C^\infty$。

### 2. 逼近性质

- 若 $f$ 在 $x$ 连续,则 $f_\varepsilon(x)=\int f(x-y)\eta_\varepsilon(y)\,dy\to f(x)$(因 $\eta_\varepsilon$ 质量集中在原点附近的近似恒等性质)。
- 若 $f\in L^p_{loc}$,则 $f_\varepsilon\to f$ 于 $L^p_{loc}$(由积分的绝对连续性 + 平移连续性)。

### 3. 用于 Lebesgue 微分定理(概要)

用 $f_\varepsilon$ 逼近,把"差商"转化为对光滑函数的微分,再取极限——这是证明单调函数 a.e. 可微的标准路线之一(配合 Vitali 覆盖引理)。

## 最小例子

- 取 $f=\mathbf 1_{[0,\infty)}$(Heaviside),则 $f_\varepsilon$ 是光滑过渡函数,在 0 附近平滑上升。
- 任意 $L^1$ 函数可被 $C_c^\infty$ 在 $L^1$ 中逼近——这是测试函数稠密性的基础。

## 常见误区

- 以为 mollifier 改变函数的本质信息。错:它是逼近,极限还原原函数。
- 忘记 $\eta$ 需紧支光滑且积分 1。
- 混淆正则化(卷积)与插值。

## 与实变函数的连接

- 依赖卷积运算([[实变函数-卷积定理]])。
- 用于证明微分定理与弱解正则性。
- 应用见 [[实变函数-Fourier应用专题]]。

## 最小自测

- [ ] 定义 mollifier 并说明为何 $\int\eta_\varepsilon=1$
- [ ] 证 $f*\eta_\varepsilon\in C^\infty$
- [ ] 说明 $f_\varepsilon\to f$ 在连续点成立

## 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

通过标准:自测全过。下一步 [[实变函数-Fourier应用专题]]。
