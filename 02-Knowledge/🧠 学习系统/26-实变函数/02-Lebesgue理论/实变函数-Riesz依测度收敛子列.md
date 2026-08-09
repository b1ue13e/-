---
type: study
topic: "Riesz 依测度收敛子列定理"
course: "实变函数"
created: 2026-08-09
updated: 2026-08-09
status: completed
learn_status: not_started
stage_moc: "[[🧭 阶段2-Lebesgue理论]]"
flow: knowledge
kind: theorem
difficulty: advanced
concept: ["依测度收敛", "Riesz 定理", "子列原理", "Borel-Cantelli"]
upstream: ["[[实变函数-收敛关系]]", "[[实变函数-可测函数]]"]
related: ["[[实变函数-Egorov定理]]", "[[实变函数-Lusin定理]]"]
source: "Stein & Shakarchi, Real Analysis (2005), Ch.2"
source_url: "https://press.princeton.edu/books/hardcover/9780691113869/real-analysis"
accessed: 2026-08-09
license: "Copyright (c) Princeton University Press; 仅作参考，不复制正文"
tags: [学习, 实变函数, Lebesgue理论]
---

# 实变函数-Riesz 依测度收敛子列

## 为什么学

"依测度收敛"比 a.e. 收敛更弱、更便于运算(在有限测度空间上是度量化的)。但它有个反直觉之处:a.e. 收敛 ⇒ 依测度收敛,反过来**不成立**。Riesz 定理补上了这个缺口:依测度收敛的序列,**必含一个 a.e. 收敛的子列**。这是把依测度结论"升级"回 a.e. 结论的标准技巧。

## 定理陈述(Riesz 子列原理)

设 $\mu(E)<\infty$,$f_n\to f$ 依测度于 $E$。则存在子列 $\{f_{n_k}\}$ 使 $f_{n_k}\to f$ a.e. 于 $E$。

(逆:若 $f_n\to f$ 依测度且某子列 a.e. 收敛到 $g$,则 $f=g$ a.e.——因为该子列也依测度→$f$。)

## 证明主线(逐步展开)

1. 由依测度收敛,对每个 $k$,存在 $n_k$(取 $n_k\uparrow\infty$)使
   $$\mu\Big(\big\{x:|f_{n_k}(x)-f(x)|>1/k\big\}\Big)<\frac{1}{2^k}.$$

2. 令 $A_k=\big\{x:|f_{n_k}(x)-f(x)|>1/k\big\}$,则 $\sum_k\mu(A_k)<\infty$。

3. 由 Borel–Cantelli 引理(测度版):对 a.e. $x$,$x$ 只属于有限多个 $A_k$。即存在 $K(x)$ 使对所有 $k\ge K(x)$,$|f_{n_k}(x)-f(x)|\le1/k$。

4. 于是 $f_{n_k}(x)\to f(x)$ 对所有这样的 $x$ 成立,而例外集 $\bigcap_m\bigcup_{k\ge m}A_k$ 测度为 0。∎

> 关键转念:$1/k$ 的精度 + $1/2^k$ 的尾部概率,使"无限多个大误差"的概率为 0。

## 最小例子(反例:依测度收敛但不 a.e. 收敛)

**打字机序列(typewriter sequence):** 在 $[0,1]$ 上,把 $[0,1]$ 按 $2^m$ 等分,第 $m$ 组排 $2^m$ 个指标:
$$f_n=\mathbf{1}_{\big[\frac{j-1}{2^m},\frac{j}{2^m}\big]},\quad n=2^m+j,\ 0\le j<2^m.$$
则对每个 $x$,$f_n(x)=1$ 在无穷多个 $n$ 成立、$=0$ 也在无穷多个 $n$ 成立,故 **不 a.e. 收敛**。但 $m(f_n>\varepsilon)=2^{-m}\to0$,所以 $f_n\to0$ **依测度**。Riesz 告诉我们:总能从中挑出 a.e.→0 的子列(例如取足够稀疏、区间互不重叠且长度→0 的子列)。

## 常见误区

- **以为依测度收敛 ⇒ 整体 a.e. 收敛:** 错,打字机序列是标准反例。"子列"二字不能省。
- **混淆两种"子列":** Riesz 给的是 a.e. 收敛子列;Egorov 给的是去掉小测度集后一致收敛。
- **在无限测度集上直接套:** Borel–Cantelli 的"a.e. 只有限次"需要 $\sum\mu(A_k)<\infty$,有限测度只是让依测度收敛定义良好;证明本身对任意满足 $\sum\mu(A_k)<\infty$ 的空间都成立。

## 与实变函数的连接

- 依赖依测度收敛定义与 Borel–Cantelli([[实变函数-收敛关系]])。
- 与 Egorov 互补:一个把 a.e. 升一致,一个把依测度提 a.e.([[实变函数-Egorov定理]])。

## 最小自测

- [ ] 闭卷陈述 Riesz 子列定理并写出 $n_k$ 的选取与 Borel–Cantelli 论证
- [ ] 构造打字机序列并验证它依测度→0 但不 a.e. 收敛
- [ ] 说明"依测度收敛 ⇒ 含 a.e. 收敛子列"中"含子列"为何不能去掉

## 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

通过标准:自测全过。下一步 [[实变函数-Lusin定理]]。
