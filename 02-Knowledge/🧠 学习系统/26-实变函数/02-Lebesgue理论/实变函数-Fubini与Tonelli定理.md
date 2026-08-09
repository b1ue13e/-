---
type: study
topic: "Fubini 与 Tonelli 定理"
course: "实变函数"
created: 2026-08-09
updated: 2026-08-09
status: completed
learn_status: not_started
stage_moc: "[[🧭 阶段2-Lebesgue理论]]"
flow: knowledge
kind: theorem
difficulty: advanced
concept: ["Fubini 定理", "Tonelli 定理", "乘积测度", "累次积分"]
upstream: ["[[实变函数-外测度]]", "[[实变函数-三大收敛定理]]"]
related: ["[[实变函数-卷积定理]]", "[[实变函数-Lebesgue积分与可积函数]]"]
source: "Stein & Shakarchi, Real Analysis (2005), Ch.6"
source_url: "https://press.princeton.edu/books/hardcover/9780691113869/real-analysis"
accessed: 2026-08-09
license: "Copyright (c) Princeton University Press; 仅作参考，不复制正文"
tags: [学习, 实变函数, Lebesgue理论]
---

# 实变函数-Fubini 与 Tonelli 定理

## 为什么学

重积分要能"先对 y 积、再对 x 积"(或反过来)。Riemann 框架下这要函数连续或分段好;Lebesgue 框架下 Fubini/Tonelli 把条件降到"非负"或"绝对可积"。这是多重积分、概率(联合分布)、卷积、Fourier 变换计算的基石。

## 定理陈述

设 $(X,\mathcal{M},\mu)$、$(Y,\mathcal{N},\nu)$ 为 σ-有限测度空间,乘积测度 $\mu\times\nu$ 在 $\mathcal{M}\otimes\mathcal{N}$ 上唯一确定。

1. **Tonelli 定理(非负):** 若 $f:X\times Y\to[0,\infty]$ 可测,则
   $$x\mapsto\int_Y f(x,y)\,d\nu(y)\ \text{可测},\quad y\mapsto\int_X f(x,y)\,d\mu(x)\ \text{可测},$$
   且
   $$\int_{X\times Y}f\,d(\mu\times\nu)=\int_X\Big(\int_Y f(x,y)\,d\nu(y)\Big)d\mu(x)=\int_Y\Big(\int_X f(x,y)\,d\mu(x)\Big)d\nu(y).$$
   (三数均存在,可能 $=+\infty$。)

2. **Fubini 定理(可积):** 若 $f$ 可测且
   $$\int_{X\times Y}|f|\,d(\mu\times\nu)<\infty$$
   (即 $f\in L^1(\mu\times\nu)$),则对 a.e. $x$,$f(x,\cdot)\in L^1(\nu)$;对 a.e. $y$,$f(\cdot,y)\in L^1(\mu)$;且两个累次积分相等并等于 $\int_{X\times Y}f\,d(\mu\times\nu)$。

## 证明主线(逐步展开)

1. **Tonelli 对示性/简单函数:** 若 $f=\mathbf{1}_{A\times B}$,直接验证 $\int_Y\mathbf{1}_{A\times B}(x,y)d\nu=\nu(B)\mathbf{1}_A(x)$,积分得 $\mu(A)\nu(B)=(\mu\times\nu)(A\times B)$,两边相等。线性推广到简单函数。

2. **Tonelli 对一般非负:** 用非负简单函数 $0\le s_n\uparrow f$。由 MCT,
   $$\int_{X\times Y}f=\lim\int s_n=\lim\int_X\Big(\int_Y s_n\Big)d\mu\overset{\text{MCT}}{=}\int_X\Big(\int_Y f\Big)d\mu.$$
   交换合法因逐项非负(单调收敛允许取极限穿过积分)。

3. **Fubini 由 Tonelli:** 把 $f$ 拆 $f=f^+-f^-$。因 $|f|\in L^1$,$f^+,f^-\in L^1$,对两者用 Tonelli 得累次积分有限且等于 $\int f^\pm$;相减即得 Fubini。∎

## 最小例子(Fubini 失败的经典反例)

在 $[0,1]\times[0,1]$ 上定义
$$f(x,y)=\frac{x^2-y^2}{(x^2+y^2)^2}\quad((x,y)\neq(0,0)),\ f(0,0)=0.$$

- 固定 $x>0$,$\int_0^1 f(x,y)dy=\frac{1}{x^2+1}$(计算用换元 $y=xt$)。故
  $$\int_0^1\Big(\int_0^1 f(x,y)dy\Big)dx=\int_0^1\frac{1}{x^2+1}dx=\frac{\pi}{4}.$$

- 由对称性,先对 $x$ 积分得 $-\frac{\pi}{4}$。

- 两累次积分**不相等**,所以 $f\notin L^1$(事实上 $\int\int|f|=\infty$)。这正是 Fubini 要求 $|f|$ 可积的原因——少了这个条件,交换次序毫无保证。

## 常见误区

- **未验证 $|f|$ 可积就交换积分次序:** 必须先用 Tonelli 算 $\int|f|$ 或确认非负。非负用 Tonelli,绝对可积用 Fubini。
- **漏掉 σ-有限性:** 乘积测度唯一性与定理都依赖 σ-有限;在计数测度 × 非 σ-有限等病态空间可能失效。
- **以为累次积分存在且相等就推出 $\int|f|<\infty$:** 反例(如上)两累次积分都存在(±π/4)但 $f\notin L^1$,Fubini 不适用。

## 与实变函数的连接

- 建立在乘积可测空间与 Carathéodory 构造上([[实变函数-外测度]])。
- 配合 MCT/Fatou([[实变函数-三大收敛定理]])完成证明。
- 是卷积与 Fourier 变换计算的基础([[实变函数-卷积定理]])。

## 最小自测

- [ ] 闭卷陈述 Tonelli 与 Fubini 的差异(非负 vs 绝对可积)
- [ ] 复述 Fubini 由 Tonelli 拆分 $f^\pm$ 的证明思路
- [ ] 给出"累次积分存在但不相等"的反例并说明它为何不违 Fubini

## 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

通过标准:自测全过。下一步 [[实变函数-卷积定理]]。
