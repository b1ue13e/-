---
type: study
topic: "函数极限与Heine判据"
course: "28-数学分析"
created: 2026-08-09
status: planned
stage_moc: "[[🧭 阶段2-函数极限与连续]]"
flow: knowledge
kind: derivation
difficulty: intermediate
concept: [函数极限, 连续性, Heine判据]
upstream: ["[[数学分析-数列极限与Cauchy准则]]"]
source: "Jiří Lebl, Basic Analysis I, v6.3, Sections 3.1-3.2"
source_url: "https://www.jirka.org/ra/html/lim_chapter.html"
accessed: 2026-08-09
license: "CC BY-NC-SA 4.0 / CC BY-SA 4.0"
tags: [学习, 数学分析, 函数极限]
---

# 数学分析-函数极限与Heine判据

## 定义

设 $c$ 是 $D\subseteq\mathbb R$ 的聚点。称 $\lim_{x\to c}f(x)=L$，若
$$\forall\varepsilon>0\ \exists\delta>0\ \forall x\in D:
0<|x-c|<\delta\Rightarrow |f(x)-L|<\varepsilon.$$

条件 $0<|x-c|$ 排除点 $c$ 本身，因此极限与 $f(c)$ 是否定义无关。函数在 $c\in D$ 连续，要求
$$\lim_{x\to c}f(x)=f(c).$$

连续性把“去心邻域极限”与“点值”接在一起。

## Heine 判据

$$\lim_{x\to c}f(x)=L$$
当且仅当对每个满足 $x_n\in D\setminus\{c\}$ 且 $x_n\to c$ 的数列，都有 $f(x_n)\to L$。

### 证明主线

- `ε-δ ⇒ 数列`：先由 ε 取 δ，再由 $x_n\to c$ 取 $N$，把两个定义串接。
- `数列 ⇒ ε-δ`：若 ε-δ 失败，则存在 $\varepsilon_0>0$；对每个 $n$ 选 $x_n$ 满足 $0<|x_n-c|<1/n$ 且 $|f(x_n)-L|\ge\varepsilon_0$。于是 $x_n\to c$，但 $f(x_n)$ 不收敛到 $L$，矛盾。

关键转念：否定 ε-δ 后，用 $\delta=1/n$ 把每个失败点串成一个反例数列。

## Worked example：$x^2$ 在 $a$ 处连续

$$|x^2-a^2|=|x-a||x+a|.$$
先限制 $|x-a|<1$，得到 $|x|<|a|+1$，所以 $|x+a|<2|a|+1$。再取
$$\delta=\min\left\{1,\frac{\varepsilon}{2|a|+1}\right\},$$
即可推出 $|x^2-a^2|<\varepsilon$。

证明的关键是先制造一个与 $x$ 无关的界，再根据 ε 选 δ。

## 用 Heine 判据否定极限

对 $f(x)=\sin(1/x)$ 在 0，取
$$x_n=\frac{1}{\pi/2+2\pi n},\qquad y_n=\frac{1}{3\pi/2+2\pi n}.$$
两列都趋于 0，但 $f(x_n)=1$、$f(y_n)=-1$，故极限不存在。

## 反例与常见错误

- 只沿直线或一条数列检查不能证明极限存在；存在性要求所有趋近方式一致。
- 左右极限相等只适用于一维内部点；多元极限有无穷多条路径。
- 连续函数的复合连续，但需要内层函数值落在外层定义域中。
- Dirichlet 函数 $1_{\mathbb Q}$ 在每点不连续：任意邻域同时有有理数和无理数。

## Completion problem

证明若 $f(x)\to L$、$g(x)\to M$，则 $f(x)+g(x)\to L+M$。先分别把误差控制到 `______`，再使用
$$|(f+g)-(L+M)|\le |f-L|+|g-M|.$$

## 闭卷通过标准

1. 写出函数极限定义和完整否定。
2. 重建 Heine 判据的反证方向。
3. 完成 $x^2$ 连续证明并说明 `min{1,...}` 的作用。
4. 构造两条数列否定一个振荡函数的极限。

四项全部完成，才通过。

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
