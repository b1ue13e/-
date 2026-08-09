---
type: study
topic: "乘积测度与Fubini"
course: "25-测度论"
created: 2026-08-09
status: planned
stage_moc: "[[🧭 阶段2-Lebesgue积分与收敛]]"
flow: knowledge
kind: derivation
upstream: ["[[测度论-单调收敛定理与积分收敛]]", "[[测度论-可测函数与简单函数]]"]
difficulty: intermediate
source: "Axler, Measure, Integration & Real Analysis, Ch.5A–5B"
source_url: "https://measure.axler.net/MIRA.pdf"
accessed: 2026-08-09
license: "CC BY-NC 4.0"
tags: [学习, 测度论, Fubini]
---

# 测度论-乘积测度与Fubini

## 动机与先修激活

二重积分常被写成两次一重积分，但这不是符号习惯。必须先回答三件事：二维集合如何测量、截面是否可测、交换积分次序需要非负还是绝对可积。

开始前闭卷回答：MCT 为什么允许把递增极限移出积分？`∫|f|<∞` 与“某个累次积分存在”有什么差别？

## 1. 乘积 `σ` 代数、截面与乘积测度

设 `(X,Σ,μ)`、`(Y,T,ν)` 是 `σ`-有限测度空间。所有可测矩形 `A×B` 生成乘积 `σ` 代数

$$
\Sigma\otimes\mathcal T=\sigma\{A\times B:A\in\Sigma,B\in\mathcal T\}.
$$

存在唯一测度 `μ×ν` 满足

$$
(\mu\times\nu)(A\times B)=\mu(A)\nu(B).
$$

对 `E⊆X×Y`，在 `x` 处的纵截面是 `E_x={y:(x,y)∈E}`，在 `y` 处的横截面是 `E^y={x:(x,y)∈E}`。若 `E∈Σ⊗T`，则所有截面可测。对可测函数 `f`，固定一个变量所得的截面函数也可测。

乘积测度的技术证明从矩形出发，借助单调类定理扩张到 `Σ⊗T`。本卡要求理解扩张接口，不要求重证单调类定理。

## 2. Tonelli：非负函数可以先积分

若 `f:X×Y→[0,∞]` 对 `Σ⊗T` 可测，则

$$
\int_{X\times Y}f\,d(\mu\times\nu)
=\int_X\left(\int_Yf(x,y)\,d\nu(y)\right)d\mu(x)
=\int_Y\left(\int_Xf(x,y)\,d\mu(x)\right)d\nu(y).
$$

三者允许等于 `∞`。Tonelli 的价值是：非负性排除了正负无穷抵消，所以可以先计算任一方向，再判断结果是否有限。

特别地，对可测集 `E` 应用 `f=1_E` 得

$$
(\mu\times\nu)(E)=\int_X\nu(E_x)\,d\mu(x)
=\int_Y\mu(E^y)\,d\nu(y).
$$

## 3. Fubini：绝对可积保证交换

若 `f∈L^1(μ×ν)`，即

$$
\int_{X\times Y}|f|\,d(\mu\times\nu)<\infty,
$$

则：

1. 对 `μ`-a.e. `x`，截面 `f(x,·)` 属于 `L^1(ν)`；
2. 对 `ν`-a.e. `y`，截面 `f(·,y)` 属于 `L^1(μ)`；
3. 两个累次积分都是有限的，并等于二重积分。

证明接口是先对 `|f|` 用 Tonelli，得到绝大多数截面绝对可积，再对 `f^+`、`f^-` 分别使用 Tonelli 后相减。没有 `L^1` 条件时，这个相减可能变成 `∞-∞`。

## 4. 证明阶梯

Tonelli 的核心推广顺序是：

1. 对矩形指示函数 `1_{A×B}` 直接验证；
2. 对非负简单函数用有限线性组合；
3. 对一般非负可测函数取简单函数 `s_n↑f`；
4. 对三处积分分别使用 MCT，得到相同极限。

这条阶梯解释了为什么 [[测度论-可测函数与简单函数]] 与 [[测度论-单调收敛定理与积分收敛]] 是直接前置，而不是形式上的章节顺序。

## Worked example：三角区域的面积

令 `E={(x,y)∈[0,1]^2:x<y}`。对固定 `x`，纵截面长度为 `1-x`；对固定 `y`，横截面长度为 `y`。由 Tonelli，

$$
(m\times m)(E)=\int_0^1(1-x)\,dx
=\int_0^1y\,dy=\frac12.
$$

决策点不是“区域看起来像三角形”，而是 `1_E≥0` 且可测，因此即使尚不知道面积有限，也可先用 Tonelli。

## 5. 反例：两个累次积分存在但不相等

在 $[0,1]^2\setminus\{(0,0)\}$ 上令

$$
f(x,y)=\frac{x^2-y^2}{(x^2+y^2)^2},
$$

并任意定义 `f(0,0)=0`。对 `y>0`，

$$
\int_0^1f(x,y)\,dx
=-\left[\frac{x}{x^2+y^2}\right]_{0}^{1}
=-\frac1{1+y^2},
$$

所以先对 `x` 积分得到 `-π/4`。对 `x>0`，

$$
\int_0^1f(x,y)\,dy
=\left[\frac{y}{x^2+y^2}\right]_{0}^{1}
=\frac1{1+x^2},
$$

所以反向得到 `π/4`。这不矛盾，因为 `f` 在原点附近不绝对可积，Fubini 的假设失败。单独看到两个累次积分存在，不能倒推 `f∈L^1`。

## Completion problem：选择定理

对下面三种信息分别决定能否交换积分，并补全理由：

1. `f≥0` 且可测，但不知道积分是否有限；
2. `∫|f|<∞`；
3. 只知道对每个 `x`，`∫f(x,y)dν(y)` 存在。

<details>
<summary>检查点</summary>

前两种分别使用 Tonelli 与 Fubini。第三种信息不足：它既不保证外层函数可积，也不保证另一方向的截面可积。

</details>

## 独立检索练习与通过标准

1. 用两种次序计算 `∫_[0,1]^2(x+y)d(x,y)`，并写出绝对可积依据。
2. 对三角区域 `x+y≤1` 写出两种截面并计算面积。
3. 闭卷陈述 Tonelli 与 Fubini 的假设、结论及是否允许无穷值。
4. 重建上述 `±π/4` 反例的两个原函数，并指出 Fubini 在哪一步失效。

通过标准：第 3 题无条件混淆；第 4 题能明确说出“非绝对可积”，不能只说“函数有奇点”。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 常见错误与反馈

- **“连续所以能交换”**：连续只在紧集上自动给出有界与可积；一般空间仍要检查 `L^1`。
- **只验证一个累次积分**：改为先计算 `∫|f|`，或在非负情形明确调用 Tonelli。
- **把 Tonelli 的结论写成有限数**：Tonelli 允许三边同为 `∞`；有限性需要额外判断。
- **忽略 a.e. 截面限定**：Fubini 只保证几乎处处截面可积，零测参数集合上的截面可能失效。

