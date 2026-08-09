---
type: study
topic: "多重积分与Green公式"
course: "28-数学分析"
created: 2026-08-09
status: planned
stage_moc: "[[🧭 阶段5-多元分析]]"
flow: knowledge
kind: derivation
difficulty: advanced
concept: [多重积分, 换元公式, Green定理]
upstream: ["[[数学分析-多元可微与Taylor公式]]", "[[数学分析-Riemann积分与微积分基本定理]]"]
source: "Jiří Lebl, Basic Analysis II, v6.3, Chapters 9-10"
source_url: "https://www.jirka.org/ra/html/mi_chapter.html"
accessed: 2026-08-09
license: "CC BY-NC-SA 4.0 / CC BY-SA 4.0"
tags: [学习, 数学分析, 多重积分]
---

# 数学分析-多重积分与Green公式

## 多重积分与换元

对矩形 $R\subset\mathbb R^n$ 上有界函数，可用小矩形分割定义 Riemann 和；连续函数在紧矩形上可积。对连续 $f$，Fubini 定理允许迭代积分：
$$\int_{[a,b]\times[c,d]}f(x,y)\,d(x,y)
=\int_a^b\left(\int_c^d f(x,y)\,dy\right)dx.$$

若 $\Phi:U\to V$ 是合适的 $C^1$ 双射且 Jacobian 不退化，则换元公式为
$$\int_V f(y)\,dy=\int_U f(\Phi(x))\,|\det D\Phi(x)|\,dx.$$

绝对值不能省；行列式符号编码定向，体积缩放取其绝对值。

## 二维 worked example：极坐标

计算单位圆盘 $D$ 上 $x^2+y^2$ 的积分。令
$$x=r\cos\theta,\quad y=r\sin\theta,\quad |\det D\Phi|=r,$$
得到
$$\int_D(x^2+y^2)\,dA
=\int_0^{2\pi}\int_0^1 r^2\,r\,dr\,d\theta=\frac\pi2.$$

遗漏额外因子 $r$ 是最常见错误。

## 路径积分与 Green 定理

对分段 $C^1$ 路径 $\gamma:[a,b]\to\mathbb R^n$ 和连续向量场 $\mathbf F$，线积分定义为
$$\int_\gamma \mathbf F\cdot d\mathbf r
=\int_a^b\mathbf F(\gamma(t))\cdot\gamma'(t)\,dt.$$

若 $\mathbf F=\nabla\varphi$，则由链式法则和一维 FTC，
$$\int_\gamma\nabla\varphi\cdot d\mathbf r
=\varphi(\gamma(b))-\varphi(\gamma(a)).$$
因此梯度场的积分只依赖端点，沿闭曲线积分为零。

### Green 定理

对平面中正向分段光滑简单闭曲线 $\partial\Omega$ 和 $C^1$ 向量场 $(P,Q)$，
$$\oint_{\partial\Omega}P\,dx+Q\,dy
=\iint_{\Omega}\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)dA.$$

## 证明主线接口

Green 定理先在矩形上用一维 FTC 分别证明 P、Q 两部分，再通过区域分割扩展；内部公共边界方向相反而抵消，只剩外边界。该“内部抵消”思想是更一般边界积分定理的入口，但三维 Stokes/Gauss 不在当前 Spine 和必修范围。

## 反例与边界

- 极坐标换元在 $r=0$ 处 Jacobian 为 0，但该单点不影响积分；不能据此把任意非单射换元都视为合法。
- 反转边界方向会使 Green 左侧变号。
- 在穿孔平面上，$\mathbf F=(-y/(x^2+y^2),x/(x^2+y^2))$ 的标量旋度为零，但沿单位圆积分为 $2\pi$；“旋度为零推出路径无关”还需要合适的区域条件。
- 向量场在区域内有奇点时不能直接套 Green 定理；必须挖去奇点并处理新增边界。
- Fubini 在本卡仅使用连续函数/紧矩形的安全版本；更一般的可积条件留给测度论。

## Completion problem

用 Green 定理计算单位圆正向边界上的 $\oint -y\,dx+x\,dy$。先求
$$\partial_x Q-\partial_y P=\underline{\qquad},$$
再乘圆盘面积，结果为 `______`。

## 闭卷通过标准

1. 写出换元公式并解释 Jacobian 绝对值。
2. 在二维例子中正确设置区域、积分次序与边界。
3. 写出路径积分基本定理和 Green 定理的对象、定向与正则性条件。
4. 解释内部边界抵消机制，并给出穿孔区域中旋度为零但非路径无关的反例。

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
