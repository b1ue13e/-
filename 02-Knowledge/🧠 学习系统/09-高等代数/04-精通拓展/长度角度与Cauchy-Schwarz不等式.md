---
type: study
topic: "长度、角度与Cauchy-Schwarz不等式"
course: "高等代数"
created: 2026-08-06
status: ongoing
difficulty: intermediate
concept: ["范数", "夹角", "Cauchy-Schwarz不等式", "三角不等式"]
stage_moc: "[[🚀 第四阶段：内积空间与谱理论]]"
upstream: ["[[内积的定义与性质]]"]
flow: knowledge
kind: concept
source: "Hefferon Linear Algebra Ch.6 §6.1 + MIT 18.06SC Lec 14；参考高等代数（第5版）"
source_url: "https://hefferon.net/linearalgebra/"
accessed: 2026-08-06
license: "CC BY-SA 4.0（Hefferon）；MIT OCW（18.06SC）"
tags: [高等代数, 线性代数, 范数, Cauchy-Schwarz]
---

# 长度、角度与 Cauchy-Schwarz 不等式

> **核心问题**：内积给出了哪些几何量？最重要的不等式是什么？——范数、夹角、C-S 不等式。

## 0. 学习边界

| 分类 | 评估 |
|:--|:--|
| 价值等级 | **A** — Cauchy-Schwarz 是内积空间最重要不等式，贯穿整个数学分析 |
| 理由 | 三角不等式、夹角定义、投影公式全部依赖 C-S；它的证明技巧（判别式）极具代表性 |
| 投入建议 | 必须能独立证明 C-S（两种方法）、定义范数与夹角，并验证范数三公理 |

## 1. 这个知识点解决什么问题？

内积（4.1）定义了配对运算，本卡把它"翻译"成几何语言：**范数**（长度）$\lVert\mathbf{u}\rVert=\sqrt{\langle\mathbf{u},\mathbf{u}\rangle}$ 与**夹角** $\cos\theta=\langle\mathbf{u},\mathbf{v}\rangle/(\lVert\mathbf{u}\rVert\lVert\mathbf{v}\rVert)$。夹角公式有意义的**前提**是 $|\cos\theta|\le1$——这正是 **Cauchy-Schwarz 不等式**：$|\langle\mathbf{u},\mathbf{v}\rangle|\le\lVert\mathbf{u}\rVert\lVert\mathbf{v}\rVert$。

## 2. 它为什么重要？它有什么用？

- **三角不等式**：$\lVert\mathbf{u}+\mathbf{v}\rVert\le\lVert\mathbf{u}\rVert+\lVert\mathbf{v}\rVert$（C-S 的推论）——度量空间公理。
- **夹角定义合法化**：$\cos\theta$ 有界 ⟹ 角度有意义。
- **投影公式**：$\operatorname{proj}_\mathbf{v}\mathbf{u}=\frac{\langle\mathbf{u},\mathbf{v}\rangle}{\lVert\mathbf{v}\rVert^2}\mathbf{v}$（4.4）。
- **应用**：相关系数（$|\rho|\le1$）、Holder/Minkowski 不等式（$L^p$ 空间）、机器学习相似度。

## 3. 学它之前需要哪些前置知识？

1. [[内积的定义与性质|内积的定义与性质]]：公理与性质。
2. [[向量空间与子空间|向量空间与子空间]]（阶段 I）：线性相关。

## 4. 定义复述

### 4.1 范数（由内积诱导）

$$\lVert\mathbf{u}\rVert=\sqrt{\langle\mathbf{u},\mathbf{u}\rangle}$$

**范数三公理**：非负性（$\lVert\mathbf{u}\rVert\ge0$，等号 ⟺ $\mathbf{u}=0$）、正齐性（$\lVert k\mathbf{u}\rVert=|k|\lVert\mathbf{u}\rVert$）、三角不等式。

### 4.2 夹角

$$\cos\theta=\frac{\langle\mathbf{u},\mathbf{v}\rangle}{\lVert\mathbf{u}\rVert\,\lVert\mathbf{v}\rVert}\qquad(\mathbf{u},\mathbf{v}\neq\mathbf{0})$$

### 4.3 Cauchy-Schwarz 不等式

$$|\langle\mathbf{u},\mathbf{v}\rangle|\le\lVert\mathbf{u}\rVert\,\lVert\mathbf{v}\rVert$$

等号成立 ⟺ $\mathbf{u},\mathbf{v}$ 线性相关。

### 4.4 常用范数（$\mathbb{R}^n$）

$\lVert\mathbf{x}\rVert_2=\sqrt{\sum x_i^2}$（Euclid）；$\lVert\mathbf{x}\rVert_1=\sum|x_i|$；$\lVert\mathbf{x}\rVert_\infty=\max|x_i|$。只有 $\lVert\cdot\rVert_2$ 由标准内积诱导。

## 5. 直觉与图像

- 范数 = "尺子"；夹角 = "量角器"；C-S = "相似度不会超过两个长度之积"。
- C-S 的几何意义：$\mathbf{u}$ 在 $\mathbf{v}$ 方向投影长度 $\le$ $\mathbf{u}$ 的长度（斜边 ≥ 直角边）。
- 三角不等式 = "抄近路不绕远"。

> **一句话本质**：C-S 说"内积的有界性"——任何两个向量的"相似度"不可能超过两者长度之积，这是整个度量几何的地基。

## 6. 定理陈述与证明重建

### 定理：Cauchy-Schwarz 不等式

**前提**：内积空间 $V$，$\mathbf{u},\mathbf{v}\in V$；**结论**：$|\langle\mathbf{u},\mathbf{v}\rangle|\le\lVert\mathbf{u}\rVert\lVert\mathbf{v}\rVert$。

**证明主线（判别式法）**：设 $\mathbf{v}\neq\mathbf{0}$，考虑 $f(t)=\lVert\mathbf{u}+t\mathbf{v}\rVert^2=\lVert\mathbf{u}\rVert^2+2t\langle\mathbf{u},\mathbf{v}\rangle+t^2\lVert\mathbf{v}\rVert^2\ge0$（正定性）。这是 $t$ 的二次多项式且恒非负 ⟹ 判别式 $\Delta=4\langle\mathbf{u},\mathbf{v}\rangle^2-4\lVert\mathbf{u}\rVert^2\lVert\mathbf{v}\rVert^2\le0$，移项即得。$\square$

**关键"转念"**：把"长度平方恒非负"翻译成"二次多项式判别式非正"——**不等式证明的判别式技巧**。

**证明主线（投影法，更几何）**：设 $\mathbf{w}=\mathbf{u}-\frac{\langle\mathbf{u},\mathbf{v}\rangle}{\lVert\mathbf{v}\rVert^2}\mathbf{v}$（正交于 $\mathbf{v}$ 的残差），则 $\lVert\mathbf{u}\rVert^2=\lVert\mathbf{w}\rVert^2+\frac{\langle\mathbf{u},\mathbf{v}\rangle^2}{\lVert\mathbf{v}\rVert^2}\ge\frac{\langle\mathbf{u},\mathbf{v}\rangle^2}{\lVert\mathbf{v}\rVert^2}$（勾股）。$\square$

### 推论：三角不等式

**证明主线**：$\lVert\mathbf{u}+\mathbf{v}\rVert^2=\lVert\mathbf{u}\rVert^2+2\langle\mathbf{u},\mathbf{v}\rangle+\lVert\mathbf{v}\rVert^2\le\lVert\mathbf{u}\rVert^2+2\lVert\mathbf{u}\rVert\lVert\mathbf{v}\rVert+\lVert\mathbf{v}\rVert^2=(\lVert\mathbf{u}\rVert+\lVert\mathbf{v}\rVert)^2$（用 C-S）。$\square$

## 7. 经典反例库

### 反例 1：$l^1$ 范数不满足平行四边形恒等式

$\lVert(1,0)\rVert_1+\lVert(0,1)\rVert_1$ 检验平行四边形失败 ⟹ 无内积诱导（4.1 反例 1 回看）。

### 反例 2：C-S 等号在相关时取到

$\mathbf{u}=(1,2)$，$\mathbf{v}=(2,4)=2\mathbf{u}$：$|\langle\mathbf{u},\mathbf{v}\rangle|=10=\lVert\mathbf{u}\rVert\lVert\mathbf{v}\rVert=\sqrt5\cdot\sqrt{20}$——线性相关取等号。

### 反例 3：$\lVert\cdot\rVert_\infty$ 的三角不等式成立但不是内积范数

$\lVert(x,y)\rVert_\infty=\max(|x|,|y|)$ 满足范数公理但无内积（平行四边形失败）——"范数 ≠ 内积范数"。

## 8. 条件变式

| 变式方向 | 具体变化 | 影响 |
|:--|:--|:--|
| 弱化：半正定形式 | C-S 仍成立（弱形式） | 半内积空间 |
| 加强：线性相关 | 等号成立 | 夹角 0° 或 180° |
| 换空间：$L^2$ | $\lvert\int fg\rvert\le\lVert f\rVert_2\lVert g\rVert_2$ | 分析学核心 |
| 换视角：相关系数 | $\rho=\cos\theta$（中心化后） | 统计 |
| 推广：Holder | $p\neq2$ 的推广 | $L^p$ 空间 |

## 9. 相关知识点与 Obsidian 双链建议

- [[内积的定义与性质|内积的定义与性质]] — 上游
- [[正交与正交补|正交与正交补]] — 下游：夹角 90° 特例
- [[正交投影与正交分解|正交投影与正交分解]] — 下游：投影公式
- [[正交矩阵与正交变换|正交矩阵]] — 横向：保内积的变换
- 矩阵范数（数值补充）— 横向：范数的矩阵版本

## 10. 闭卷验收（数学模式）

- [ ] **定义默写**：范数、夹角、C-S 不等式。
- [ ] **证明**：C-S（判别式法与投影法）；三角不等式。
- [ ] **计算**：给向量算长度、夹角、投影长度。
- [ ] **反例**：非内积范数；等号条件。

## 11. 分级习题

| 等级 | 题目 | 来源 |
|:--|:--|:--|
| ★ | 求 $\mathbf{u}=(1,2,2)$ 的范数与 $\mathbf{u},(1,0,0)$ 的夹角 | Hefferon §6.1 |
| ★★ | 证明 $\lvert\langle\mathbf{u},\mathbf{v}\rangle\rvert^2\le\langle\mathbf{u},\mathbf{u}\rangle\langle\mathbf{v},\mathbf{v}\rangle$（展开 $\lVert\mathbf{u}+t\mathbf{v}\rVert^2\ge0$） | MIT 18.06 Lec 14 |
| ★★★ | 证明三角不等式并说明等号条件（共线同向） | 高等代数（第5版） |
| ★★★★ | 证明极化恒等式并由此说明 $l^1$ 无内积 | Hefferon §6.1 |

## 12. 我的主动回忆区

> 不看上文：写 C-S 与两种证明；三角不等式；夹角公式；举非内积范数。

## 13. 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

---
*创建于：2026-08-06 | 来源：Hefferon Ch.6 §6.1 + MIT 18.06SC Lec 14 + 高等代数（第5版）；旧空壳（长度与角度）于 2026-08-06 重写*

