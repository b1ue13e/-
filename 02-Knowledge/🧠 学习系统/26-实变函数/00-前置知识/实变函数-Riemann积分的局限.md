---
type: study
topic: "Riemann积分的局限"
course: "实变函数"
created: 2026-08-09
status: completed
stage_moc: "[[🧭 实变函数-前置知识]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["Riemann积分", "Lebesgue积分", "极限交换"]
upstream: ["[[实变函数-数学分析桥接-一致收敛与极限交换]]"]
related: ["[[实变函数-Lebesgue积分与可积函数]]"]
source: "Jirka RA I, Ch.6 & II, Ch.1"
source_url: "https://www.jirka.org/ra/"
accessed: 2026-08-09
license: "CC BY-SA 4.0"
tags: [学习, 实变函数, 前置]
---

# 实变函数-Riemann积分的局限

## 为什么学

这门课叫"实变函数",本质是回答一个问题:**Riemann 积分哪里不够用?** 先把病灶看清,阶段 2 的 Lebesgue 积分才有方向。记住:实变函数不是"更难",而是"修 Riemann 积分的三个洞"。

## Riemann 积分的三个洞

1. **可积函数太少**:有界函数 $f$ 在 $[a,b]$ 上 Riemann 可积 ⟺ 间断点集是零测集(在 Jordan 意义下"小")。因此高度振荡的有界函数(Dirichlet 函数 $D(x)=\mathbf{1}_{\mathbb{Q}}$)不可积——它在每点都间断。
2. **极限交换要强条件**:$f_n\to f$ 一致 ⟹ $\int f_n\to\int f$。但逐点/几乎处处收敛时,交换 $\lim\int=\int\lim$ 需要额外条件(控制收敛),Riemann 框架没有系统处理。
3. **积分与微分是"残缺"的互逆**:FTC 对 Riemann 积分只在 $f'$ Riemann 可积时成立;而对"处处连续但处处不可导"的 Weierstrass 函数,以及后来要构造的 Cantor 函数(连续、几乎处处导数为 0、不恒为常数),Riemann 框架的 FTC 直接失效。

## 为什么 Dirichlet 函数不可积(证明主线)

Darboux 上/下和:$D$ 在任意子区间上,上确界 = 1、下确界 = 0,所以任意划分的上和 = 1、下和 = 0;$\overline{\int}D=1\neq0=\underline{\int}D$,不可积。**Lebesgue 的修法:不再按"纵轴分划"($\sum f(\xi_k)\Delta x_k$),而是按"横轴测度分层"($\int = \sum y_k\cdot m(f^{-1}([y_k,y_{k+1}]))$),Dirichlet 函数的分层只有 0 和 1 两层,立刻可积且 $\int D=0$。**

## 最小例子

$f_n(x)=n\mathbf{1}_{(0,1/n)}(x)$ 在 $[0,1]$ 上:逐点收敛到 $f\equiv0$,但 $\int_0^1 f_n=1$ 不趋于 $\int f=0$。**逐点收敛 + Riemann 积分,极限交换失败。** 这个例子在 Lebesgue 框架下依旧提醒我们:没有控制条件,交换就是错的(控制收敛定理的"控制函数"正是为此而生)。

## 常见误区

- **以为"可积函数少"是缺点**:恰恰相反,少才是问题——极限会逃出可积函数集(见下)。
- **以为 Lebesgue 积分 = "更难算"**:对分段常函数/指示函数,Lebesgue 积分经常更简单;病态函数才显威力。
- **混淆"不可测"与"不可积"**:$V$ 不可测是定义域问题;Dirichlet 可测但 Riemann 不可积是积分框架问题。两者不同。

## 与实变函数的连接

- 阶段 2 主线:外测度 → 可测集 → 可测函数 → Lebesgue 积分 → 三大收敛定理,每一步都在修这三个洞。
- 阶段 3 的 [[实变函数-绝对连续与微积分基本定理]] 是 FTC 的 Lebesgue 版本:$f$ 绝对连续 ⟺ $f(x)-f(a)=\int_a^x f'$。

## 最小自测

- [ ] 闭卷说清 Dirichlet 函数为何 Riemann 不可积(上下和论证)
- [ ] 举出"逐点收敛但积分不收敛"的例子
- [ ] 用自己的话解释:为什么 Lebesgue 积分按"横轴分层"就能积 Dirichlet 函数

## 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

通过标准:诊断第 6 题。通过全部诊断后进入 [[🧭 阶段1-实数与点集基础|🔍 第一阶段:实数与点集基础]]。
