---
type: study
topic: "多元可微与Taylor公式"
course: "28-数学分析"
created: 2026-08-09
status: planned
stage_moc: "[[🧭 阶段5-多元分析]]"
flow: knowledge
kind: derivation
difficulty: advanced
concept: [Fréchet可微, Jacobian, Hessian]
upstream: ["[[数学分析-导数中值定理与Taylor公式]]", "[[数学分析-紧致性与一致连续]]"]
source: "Jiří Lebl, Basic Analysis II, v6.3, Chapter 8"
source_url: "https://www.jirka.org/ra/html/pd_chapter.html"
accessed: 2026-08-09
license: "CC BY-NC-SA 4.0 / CC BY-SA 4.0"
tags: [学习, 数学分析, 多元微分]
---

# 数学分析-多元可微与Taylor公式

## 多元极限与连续

对 $f:D\subseteq\mathbb R^n\to\mathbb R^m$，定义
$$\lim_{x\to a}f(x)=L$$
是指对任意 $\varepsilon>0$，存在 $\delta>0$，使 $x\in D$ 且 $0<\|x-a\|<\delta$ 时都有 $\|f(x)-L\|<\varepsilon$。Heine 判据仍成立：对每个 $x_k\to a$、$x_k\ne a$，都应有 $f(x_k)\to L$。

沿不同路径得到不同极限足以否定多元极限；沿若干条直线得到同一极限不能证明极限存在，因为趋近路径有无穷多种。例如
$$f(x,y)=\frac{x^2y}{x^4+y^2}$$
沿每条直线 $y=mx$ 都趋于 0，但沿抛物线 $y=x^2$ 恒为 $1/2$，故原点极限不存在。

## 多元可微的定义

设 $f:\mathbb R^n\to\mathbb R^m$。若存在线性映射 $A:\mathbb R^n\to\mathbb R^m$ 使
$$\lim_{h\to0}\frac{\|f(a+h)-f(a)-Ah\|}{\|h\|}=0,$$
则称 $f$ 在 $a$ Fréchet 可微，记 $Df(a)=A$。在标准基下，$A$ 的矩阵是 Jacobian。

定义要求同一个线性映射同时控制所有方向。偏导数只检查坐标方向，因此“所有偏导存在”不推出可微。

若各一阶偏导在 $a$ 的邻域存在并在 $a$ 连续，则 $f$ 在 $a$ 可微。这是常用充分条件，不是必要条件。

## 链式法则与二阶结构

若 $f$ 在 $a$ 可微、$g$ 在 $f(a)$ 可微，则
$$D(g\circ f)(a)=Dg(f(a))\,Df(a).$$

标量函数 $f:\mathbb R^n\to\mathbb R$ 的导数由梯度表示：
$$Df(a)h=\nabla f(a)^\top h.$$

若 $f\in C^2$，二阶 Taylor 展开为
$$f(a+h)=f(a)+\nabla f(a)^\top h+\frac12 h^\top H_f(a)h+o(\|h\|^2).$$

Hessian 的正定性给出严格局部极小的充分条件；半正定时不能直接下结论。

## 证明接口：连续偏导推出可微

对 $h=(h_1,\dots,h_n)$，沿坐标逐次改变变量，把
$$f(a+h)-f(a)$$
写成 n 个单变量差分之和。每一项用单变量中值定理，得到某个中间点处的偏导乘 $h_i$。再减去 $\sum_i\partial_i f(a)h_i$；偏导在 a 连续，使余项除以 $\|h\|$ 后趋于 0。

关键转念：多元增量先沿坐标折线拆分，再把单变量 MVT 复用到每一段。

## Worked example

对 $f(x,y)=x^2+xy+y^2$，
$$\nabla f=(2x+y,x+2y),\qquad H_f=\begin{pmatrix}2&1\\1&2\end{pmatrix}.$$
Hessian 特征值为 1、3，正定；唯一临界点 $(0,0)$ 是严格全局最小点。

## 反例：偏导存在但不可微

定义
$$f(x,y)=\begin{cases}\dfrac{x^2y}{x^4+y^2},&(x,y)\ne(0,0),\\0,&(0,0).\end{cases}$$
两条坐标轴上的函数恒为 0，所以原点偏导存在且为 0；沿 $y=x^2$，$f(x,x^2)=1/2$，函数甚至不连续，因此不可微。

## Completion problem

证明 $f(x,y)=\sqrt{x^2+y^2}$ 在原点不可微。若可微，因坐标偏导都为 0，候选线性映射只能是 0；但沿 $h=(t,0)$，商
$$\frac{|f(h)-0|}{\|h\|}=\underline{\qquad}$$
不趋于 0。

## 闭卷通过标准

1. 写出 Fréchet 可微定义并说明线性映射的类型。
2. 解释偏导、方向导数和可微之间的非等价关系。
3. 重建连续偏导推出可微的坐标折线证明。
4. 用一个反例展示偏导存在仍不可微。

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
