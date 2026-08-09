---
type: study
topic: "导数、中值定理与Taylor公式"
course: "28-数学分析"
created: 2026-08-09
status: planned
stage_moc: "[[🧭 阶段3-微分与Riemann积分]]"
flow: knowledge
kind: derivation
difficulty: intermediate
concept: [导数, 中值定理, Taylor公式]
upstream: ["[[数学分析-紧致性与一致连续]]"]
source: "Jiří Lebl, Basic Analysis I, v6.3, Chapter 4"
source_url: "https://www.jirka.org/ra/html/der_chapter.html"
accessed: 2026-08-09
license: "CC BY-NC-SA 4.0 / CC BY-SA 4.0"
tags: [学习, 数学分析, 微分]
---

# 数学分析-导数中值定理与Taylor公式

## 定义与局部线性化

$f$ 在 $a$ 可导，若极限
$$f'(a)=\lim_{h\to0}\frac{f(a+h)-f(a)}h$$
存在。等价地，存在数 $A$ 使
$$f(a+h)=f(a)+Ah+o(h),\qquad h\to0,$$
此时 $A=f'(a)$。第二种形式强调导数是最佳一阶线性近似，而不只是切线斜率。

可导必连续，反之不成立；$|x|$ 在 0 连续但不可导。

## 定理链

### Rolle 定理

若 $f$ 在 $[a,b]$ 连续、在 $(a,b)$ 可导且 $f(a)=f(b)$，则存在 $c\in(a,b)$ 使 $f'(c)=0$。

证明依赖极值定理：若函数非常数，内部取得最大或最小值；内部极值点的导数为零。

### Lagrange 中值定理

在相同连续/可导条件下，存在 $c\in(a,b)$ 使
$$f'(c)=\frac{f(b)-f(a)}{b-a}.$$

对 $g(x)=f(x)-\frac{f(b)-f(a)}{b-a}(x-a)$ 使用 Rolle 定理即可。关键转念是减去连接端点的割线，把端点函数值变成相等。

### Taylor 定理（Lagrange 余项）

若 $f$ 在包含 $a,x$ 的区间有 $n+1$ 阶导数，并满足适用的连续性条件，则存在 $\xi$ 位于 $a,x$ 之间，使
$$f(x)=\sum_{k=0}^{n}\frac{f^{(k)}(a)}{k!}(x-a)^k+
\frac{f^{(n+1)}(\xi)}{(n+1)!}(x-a)^{n+1}.$$

余项是误差控制，不等于“Taylor 级数必收敛到函数”。

## Worked example：$\log(1+x)\le x$

令 $g(x)=x-\log(1+x)$，定义域 $x>-1$。$g(0)=0$，且
$$g'(x)=1-\frac1{1+x}=\frac{x}{1+x}.$$
当 $x\ge0$ 时 $g'\ge0$，所以 $g(x)\ge0$。也可对 $\log$ 在 $[0,x]$ 用 MVT：$\log(1+x)=x/(1+c)\le x$。

## Completion problem：Lipschitz 控制

设 $|f'(x)|\le M$ 于区间 $I$。对任意 $x,y\in I$，由 MVT 存在 c 使
$$f(x)-f(y)=\underline{\qquad}.$$
因此 $|f(x)-f(y)|\le\underline{\qquad}$，从而 $f$ 一致连续。

## 反例与条件边界

- $f(x)=|x|$ 连续但在 0 不可导。
- 导数存在不保证导数连续，例如 $x^2\sin(1/x^2)$ 在 0 的适当延拓。
- $f'(x)=0$ 处处推出区间上常数；若定义域不是区间，结论可失败。
- 光滑函数的 Taylor 级数不一定等于函数；$e^{-1/x^2}$ 在 0 的所有阶导数为 0，却在 $x\ne0$ 时为正。

## 检索练习与通过标准

1. 从 Rolle 定理构造 MVT 证明中的辅助函数。
2. 用 MVT 证明导数有界推出 Lipschitz。
3. 写出二阶 Taylor 公式和余项条件。
4. 解释“Taylor 多项式逼近”与“函数等于 Taylor 级数”的差别。

## 下游知识

```dataview
LIST
FROM "02-Knowledge/🧠 学习系统/28-数学分析"
WHERE contains(upstream, this.file.link)
SORT file.name ASC
```

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/28-数学分析"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

