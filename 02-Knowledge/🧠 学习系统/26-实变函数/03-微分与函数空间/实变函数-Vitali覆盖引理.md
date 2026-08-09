---
type: study
topic: "Vitali 覆盖引理"
course: "实变函数"
created: 2026-08-09
updated: 2026-08-09
status: completed
learn_status: not_started
stage_moc: "[[🧭 阶段3-微分与函数空间]]"
flow: knowledge
kind: theorem
difficulty: advanced
concept: ["Vitali 覆盖", "贪心选取", "微分定理", "测度覆盖"]
upstream: ["[[实变函数-外测度]]"]
related: ["[[实变函数-单调函数几乎处处可微]]", "[[实变函数-绝对连续与微积分基本定理]]"]
source: "Stein & Shakarchi, Real Analysis (2005), Ch.3"
source_url: "https://press.princeton.edu/books/hardcover/9780691113869/real-analysis"
accessed: 2026-08-09
license: "Copyright (c) Princeton University Press; 仅作参考，不复制正文"
tags: [学习, 实变函数, 微分]
---

# 实变函数-Vitali 覆盖引理

## 为什么学

要研究"函数在一点的局部平均",需要把所有点用各种大小的区间/球盖住,再从中挑出**互不相交**的一小撮,保证它们"几乎"盖住整片区域。Vitali 覆盖引理就是这件事的精确形式——它是 Lebesgue 密度定理、积分微分定理($\frac{d}{dx}\int_a^x f=f(x)$ a.e.)、以及单调函数 a.e. 可微的**核心工具**。

## 定理陈述(Vitali 覆盖引理,区间/球版)

设 $E\subset\mathbb{R}^n$,$\mathcal{V}$ 是 $E$ 的一个 **Vitali 覆盖**:$\mathcal{V}$ 由闭球(或闭区间)$B$ 组成,且对每个 $x\in E$ 和每个 $r>0$,存在 $B\in\mathcal{V}$ 含 $x$ 且半径 $<r$。

则存在**可数**互不相交的子族 $\{B_j\}\subset\mathcal{V}$,使得
$$E\subset\bigcup_{j=1}^\infty 5B_j$$
(其中 $5B_j$ 表示以同中心、半径放大 5 倍的球;在 $\mathbb{R}$ 上区间版常用 3 倍或 5 倍)。

## 证明主线(逐步展开)

**贪心选取(greedy selection)。**

1. 若 $\mathcal{V}$ 中所有球半径有统一上界(否则先限制在有限大球内、再并起来),开始选取。

2. 选 $B_1\in\mathcal{V}$ 使半径 $r_1$ 尽可能大(在有限截断内取最大;无限情形取一个半径 ≥ 某值)。令 $U_1=B_1$。

3. 归纳:假设已选互不相交的 $B_1,\dots,B_k$。令
   $$R_k=\sup\big\{r(B): B\in\mathcal{V},\ B\cap\bigcup_{i=1}^k B_i=\emptyset\big\}.$$
   若 $R_k=0$ 则停止。否则取 $B_{k+1}\in\mathcal{V}$ 与前面不交且 $r(B_{k+1})>\frac12 R_k$。令 $U_{k+1}=\bigcup_{i=1}^{k+1}B_i$。

4. **论证覆盖:** 任取 $B\in\mathcal{V}$。若 $B$ 与某个已选 $B_i$ 相交且 $r(B_i)\ge r(B)$,则因两球相交、中心距 $\le r(B_i)+r(B)\le2r(B_i)$,$B$ 任一点到 $B_i$ 中心距离 $\le r(B)+r(B_i)\le3r(B_i)$,故 $B\subset 5B_i$(取 5 为安全常数)。若对所有相交的 $B_i$ 都有 $r(B_i)<r(B)$,则由选择规则 $r(B_{k+1})>\frac12R_k\ge\frac12r(B)$,一旦 $B$ 与前面都不交且半径够大就早该被选入,矛盾于它未被选——故它必与某个 $B_j$ 相交且 $r(B)<2r(B_j)$,同样归入 $5B_j$。于是 $E\subset\bigcup 5B_j$。∎

> 注:严格证明中常数取 5 可保证每个未入选的 $B$ 落于某个 $5B_j$ 内;$\mathbb{R}^1$ 区间版常取 3。

## 最小例子

- 取 $E=[0,1]$,$\mathcal{V}=$ 所有中心在 $E$ 内、半径 $<1$ 的开区间。Vitali 引理保证能挑出可数不交子族使其 5 倍覆盖 $E$。直观:贪心先选大区间,缝隙用更小的填,放大 5 倍后缝隙被吞掉。

## 常见误区

- **以为不交子族直接覆盖 $E$:** 不,$B_j$ 互不相交且**不**覆盖 $E$;覆盖的是它们的 5 倍放大版。这是"packing → covering"的转化。
- **混淆 Vitali 覆盖与任意覆盖:** Vitali 覆盖要求"任意小半径都找得到",普通开覆盖无此要求。
- **常数 5 是本质的:** 改成 1 一般不成立。

## 与实变函数的连接

- 是单调函数 a.e. 可微的证明引擎([[实变函数-单调函数几乎处处可微]])。
- 用于 Lebesgue 微分定理与极大函数估计([[实变函数-绝对连续与微积分基本定理]])。

## 最小自测

- [ ] 陈述 Vitali 覆盖的定义与引理结论(5 倍覆盖)
- [ ] 解释贪心选取中 $r(B_{k+1})>\frac12R_k$ 的作用
- [ ] 说明为什么不交子族本身不覆盖 $E$ 反而其放大版覆盖

## 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

通过标准:自测全过。下一步 [[实变函数-单调函数几乎处处可微]]。
