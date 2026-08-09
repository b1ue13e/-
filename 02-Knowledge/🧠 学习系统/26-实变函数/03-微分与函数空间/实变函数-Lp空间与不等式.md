---
type: study
topic: "Lp空间与不等式"
course: "实变函数"
created: 2026-08-09
status: completed
learn_status: not_started
stage_moc: "[[🧭 阶段3-微分与函数空间]]"
flow: knowledge
kind: concept
difficulty: advanced
concept: ["Lp空间", "Hölder不等式", "Minkowski不等式"]
upstream: ["[[实变函数-Lebesgue积分与可积函数]]"]
related: ["[[实变函数-L2空间与完备性]]", "[[实变函数-收敛关系]]"]
source: "Stein & Shakarchi, Real Analysis (2005), Ch.4"
source_url: "https://press.princeton.edu/books/hardcover/9780691113869/real-analysis"
accessed: 2026-08-09
license: "Copyright (c) Princeton University Press; 仅作参考，不复制正文"
tags: [学习, 实变函数, Lp空间]
---

# 实变函数-Lp空间与不等式

## 为什么学

$L^p$ 是 Lebesgue 可积函数按不同"积分幂次"分类的统一框架。$p=1$ 是绝对可积,$p=2$ 是 Hilbert,$p=\infty$ 是有界。Hölder 与 Minkowski 不等式是 $L^p$ 内的三角不等式与对偶配对基础,几乎所有 $L^p$ 估计都靠它们。

## 核心定义

- $\|f\|_p=(\int|f|^p)^{1/p}$,$1\le p<\infty$;$\|f\|_\infty=\operatorname{ess\,sup}|f|$。
- $L^p=\{f:\|f\|_p<\infty\}$(a.e. 等同)。

## 证明主线(逐步展开)

### 1. Hölder 不等式

若 $1/p+1/q=1$,则 $\int|fg|\le\|f\|_p\|g\|_q$。
**证明**:用 Young 不等式 $ab\le a^p/p+b^q/q$(对 $a,b\ge0$)。令归一化 $A=|f|/\|f\|_p$,$B=|g|/\|g\|_q$,则
$$\int AB\le\int\Big(\frac{A^p}{p}+\frac{B^q}{q}\Big)=\frac1p+\frac1q=1,$$
乘回即得。等号当且仅当 $|f|^p$ 与 $|g|^q$ 成比例。

### 2. Minkowski 不等式(三角不等式)

$\|f+g\|_p\le\|f\|_p+\|g\|_p$($p\ge1$)。
**证明**:对 $p>1$,写 $\int|f+g|^p=\int|f+g|\cdot|f+g|^{p-1}$,对第二项用 Hölder(配 $q=p/(p-1)$)得
$$\le(\|f\|_p+\|g\|_p)\|f+g\|_p^{p-1},$$
约去 $\|f+g\|_p^{p-1}$。$p=1$ 平凡。

### 3. 对偶 $(L^p)^*=L^q$

对 $1\le p<\infty$,每个有界线性泛函 $T$ 形如 $T(f)=\int fg$,其中 $g\in L^q$。($p=\infty$ 需额外正则性条件。)

## 最小例子

- 在 $[0,1]$ 上,$\|x^{-a}\|_p<\infty\iff ap<1$。用来判断一个函数在哪个 $L^p$ 中。
- $f\equiv1$ 在 $\mathbb R$ 上不属于任何 $L^p$,但在有限测度集上属于所有 $L^p$(因 $p\ge1$ 时 $\|f\|_p\le\|f\|_1^{1/p}\mu(E)^{1-1/p}$)。

## 常见误区

- Hölder 要求共轭指数 $1/p+1/q=1$;取错 $q$ 直接错。
- $p<1$ 时 $\|\cdot\|_p$ 不是范数(三角不等式失效)。
- $\|f\|_\infty$ 是本质 supremum,允许零测集上任意大。

## 与实变函数的连接

- 建立在 Lebesgue 积分上([[实变函数-Lebesgue积分与可积函数]])。
- $L^2$ 是其 Hilbert 特例([[实变函数-L2空间与完备性]])。
- 控制收敛在 $L^p$ 中的版本见 [[实变函数-收敛关系]]。

## 最小自测

- [ ] 用 Young 不等式证 Hölder
- [ ] 证 Minkowski(三角不等式)
- [ ] 判断 $x^{-a}$ 在 $[0,1]$ 属于哪些 $L^p$

## 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

通过标准:自测全过。下一步 [[实变函数-L2空间与完备性]]。
