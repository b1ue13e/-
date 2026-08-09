---
type: study
topic: "Riemann积分与微积分基本定理"
course: "28-数学分析"
created: 2026-08-03
updated: 2026-08-09
status: planned
stage_moc: "[[🧭 阶段3-微分与Riemann积分]]"
flow: knowledge
kind: derivation
difficulty: intermediate
concept: [Riemann积分, Darboux和, 微积分基本定理]
upstream: ["[[数学分析-导数中值定理与Taylor公式]]", "[[数学分析-紧致性与一致连续]]"]
source: "Jiří Lebl, Basic Analysis I, v6.3, Chapter 5"
source_url: "https://www.jirka.org/ra/html/int_chapter.html"
accessed: 2026-08-09
license: "CC BY-NC-SA 4.0 / CC BY-SA 4.0"
tags: [学习, 数学分析, Riemann积分]
---

# 数学分析-Riemann积分与微积分基本定理

## 要解决的问题

“积分等于求原函数”不能作为积分定义，因为许多连续函数没有初等原函数。Riemann 积分先用有限矩形和定义累积量，再由微积分基本定理说明它何时与导数互逆。

## Darboux 定义

设 $f$ 在 $[a,b]$ 有界，分割
$$P:a=x_0<x_1<\cdots<x_n=b.$$
在 $I_i=[x_{i-1},x_i]$ 上令 $M_i=\sup_{I_i}f$、$m_i=\inf_{I_i}f$，定义
$$U(P,f)=\sum_iM_i\Delta x_i,\qquad L(P,f)=\sum_im_i\Delta x_i.$$

若
$$\inf_PU(P,f)=\sup_PL(P,f),$$
则称 $f$ Riemann 可积，公共值记作 $\int_a^bf$。

**Darboux 判据**：有界函数 $f$ 可积，当且仅当对任意 $\varepsilon>0$，存在分割 $P$ 使
$$U(P,f)-L(P,f)<\varepsilon.$$

连续函数在闭区间上一致连续；取足够细分割即可使每个小区间上的振荡统一变小，从而证明可积。

## 微积分基本定理

### FTC 第一部分

若 $f$ 在 $[a,b]$ Riemann 可积，定义
$$F(x)=\int_a^x f(t)\,dt.$$
则 $F$ 连续；若 $f$ 在 $x_0$ 连续，则 $F$ 在 $x_0$ 可导且 $F'(x_0)=f(x_0)$。

证明核心是
$$\frac{F(x_0+h)-F(x_0)}h=\frac1h\int_{x_0}^{x_0+h}f(t)\,dt,$$
即差商是短区间上的平均高度。连续性把该平均值夹到 $f(x_0)$。

### FTC 第二部分

若 $f$ 在 $[a,b]$ Riemann 可积且存在原函数 $G$，则
$$\int_a^bf(x)\,dx=G(b)-G(a).$$

令 $H(x)=\int_a^xf-G(x)$。在 $f$ 连续点可直接用第一部分；一般 Riemann 可积版本需要相应的积分中值/分割论证。课程必修证明先采用 $f$ 连续的安全版本：此时 $H'=0$，由 MVT 得 $H$ 为常数。

## Worked example

对 $f(x)=x^2$ 于 $[0,1]$，等分割的右端点和为
$$\frac1n\sum_{k=1}^n\left(\frac kn\right)^2
=\frac{n(n+1)(2n+1)}{6n^3}\to\frac13.$$
这既从 Riemann 和得到积分，也与原函数 $x^3/3$ 的端点差一致。

## 反例与条件

- Dirichlet 函数 $1_{\mathbb Q}$ 在任意子区间上上下确界分别为 1、0，故任何分割都有 $U-L=b-a$，不可积。
- 可积不推出连续；单点跳跃或有限个跳跃仍可积。
- FTC1 的“$F'(x_0)=f(x_0)$”需要 $f$ 在 $x_0$ 连续。
- 无界函数不属于本卡的有界 Riemann 积分框架；反常积分必须另行定义。

## Completion problem

证明连续函数可积。给定 ε，由一致连续性取 δ，使 $|x-y|<\delta$ 时
$$|f(x)-f(y)|<\underline{\qquad}.$$
取网格宽小于 δ 的分割，补全
$$U(P,f)-L(P,f)\le\sum_i\underline{\qquad}\,\Delta x_i<\varepsilon.$$

## 闭卷通过标准

1. 写出 Darboux 上下和和可积判据。
2. 重建连续函数可积证明。
3. 分别陈述 FTC 两部分的条件与结论。
4. 用 Dirichlet 函数解释不可积性。

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

