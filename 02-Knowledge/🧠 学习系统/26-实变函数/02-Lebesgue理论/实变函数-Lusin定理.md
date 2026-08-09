---
type: study
topic: "Lusin 定理"
course: "实变函数"
created: 2026-08-09
updated: 2026-08-09
status: completed
learn_status: not_started
stage_moc: "[[🧭 阶段2-Lebesgue理论]]"
flow: knowledge
kind: theorem
difficulty: advanced
concept: ["Lusin 定理", "可测函数", "近似连续", "闭集"]
upstream: ["[[实变函数-可测函数]]", "[[实变函数-简单函数]]"]
related: ["[[实变函数-Egorov定理]]", "[[实变函数-Riesz依测度收敛子列]]"]
source: "Stein & Shakarchi, Real Analysis (2005), Ch.1/2"
source_url: "https://press.princeton.edu/books/hardcover/9780691113869/real-analysis"
accessed: 2026-08-09
license: "Copyright (c) Princeton University Press; 仅作参考，不复制正文"
tags: [学习, 实变函数, Lebesgue理论]
---

# 实变函数-Lusin 定理

## 为什么学

连续函数是分析学里最好用的对象。Lusin 定理说:有限测度集上的可测函数"几乎"是连续的——你可以扔掉一个任意小的集合,在剩下的(闭)集上函数连续。这把"可测性"解释成"连续性的微小扰动",是连接可测函数与连续函数的桥梁,也是证明很多关于可测函数结论的利器(先对连续函数证,再用它逼近)。

## 定理陈述

设 $E$ 可测且 $\mu(E)<\infty$,$f:E\to\mathbb{R}$ 可测(可取有限值)。则对任意 $\varepsilon>0$,存在闭集 $F\subset E$ 使 $\mu(E\setminus F)<\varepsilon$,且 $f|_F$ 连续。

> 等价表述:$f$ 在 $E$ 上"近似连续"(continuous on a closed subset of arbitrarily large measure)。

## 证明主线(逐步展开)

**思路:用简单函数逼近,简单函数在闭子集上连续。**

1. **简单函数情形。** 设 $\varphi=\sum_{i=1}^m a_i\mathbf{1}_{E_i}$,$E_i$ 可测两两不交,$\bigcup E_i=E$。对每个 $E_i$,由测度正则性,存在闭集 $F_i\subset E_i$ 使 $\mu(E_i\setminus F_i)<\varepsilon/m$。在 $F=\bigcup_{i=1}^m F_i$(闭,因有限并)上,$\varphi$ 在每个 $F_i$ 上为常数 $a_i$,故 $\varphi|_F$ 连续(局部常数)。且 $\mu(E\setminus F)<\varepsilon$。

2. **一般可测函数。** 取简单函数 $\varphi_k$ 使 $|f-\varphi_k|<1/k$ 对所有 $x\in E$ 成立(把值域等分构造)。由上一步,对每个 $k$ 存在闭 $F_k\subset E$,$\mu(E\setminus F_k)<\varepsilon/2^k$ 且 $\varphi_k|_{F_k}$ 连续。由 Egorov(或干脆直接用 Borel–Cantelli 式估计),存在闭 $F\subset\bigcap_k F_k$ 使 $\mu(E\setminus F)<\varepsilon$,且在 $F$ 上 $\varphi_k\to f$ **一致**;一致极限保持连续,故 $f|_F$ 连续。合并得 $\mu(E\setminus F)<\varepsilon$。∎

> 简化记忆:**简单函数 → 在闭子集上连续;可测函数 → 被简单函数一致逼近 → 极限仍连续(在更小的闭子集上)。**

## 最小例子

- Dirichlet 函数 $f=\mathbf{1}_{\mathbb{Q}\cap[0,1]}$ 在 $[0,1]$ 上可测但不连续。对任意 $\varepsilon$,取 $F=[0,1]$ 去掉所有有理点附近的总长 $<\varepsilon$ 的小开区间后所得的闭集,则 $\mu([0,1]\setminus F)<\varepsilon$,在 $F$ 上 $f\equiv0$ 连续。

## 常见误区

- **以为 $f$ 在整个 $E$ 上连续:** 只在一个去掉小测度后的**闭子集**上连续;可测函数一般处处不连续。
- **漏掉有限测度/正则性:** 证明靠"每个可测集含闭子集且差可任意小";在非正则测度空间上需额外假设。对 Lebesgue 测度总成立。
- **与 Egorov 混淆:** Egorov 处理"收敛模式转换",Lusin 处理"可测⇒近似连续",两者无关但常并称。

## 与实变函数的连接

- 桥接可测函数与连续函数([[实变函数-可测函数]])。
- 与 Egorov 并列为"可测性的两条近似定理"([[实变函数-Egorov定理]])。

## 最小自测

- [ ] 闭卷陈述 Lusin 定理(闭集 $F$、$\mu(E\setminus F)<\varepsilon$)
- [ ] 说明证明如何依赖简单函数一致逼近
- [ ] 给 Dirichlet 函数构造一个满足 Lusin 的闭集 $F$

## 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

通过标准:自测全过。下一步 [[实变函数-Riesz依测度收敛子列]]。
