---
type: project
project_type: homework
course: "泛函分析"
assignment_id: "泛函分析-HW03"
assignment_level: lesson
assignment_format: problem-set
stage_id: "02"
requires: ["[[泛函分析-Hilbert空间与正交投影定理]]", "[[泛函分析-Riesz表示定理与Lax-Milgram引理]]"]
source_type: official_assignment
created: 2026-08-09
status: active
flow: project
tags: [作业, 泛函分析, Hilbert空间, 正交投影, Riesz表示定理]
---

# 泛函分析-课后作业-03-Hilbert空间投影与Riesz表示

> 对应知识点：[[泛函分析-Hilbert空间与正交投影定理]]、[[泛函分析-Riesz表示定理与Lax-Milgram引理]]
> 官方来源基准：MIT 18.102 Problem Set 4 & 5 (Hilbert Spaces, Orthogonality, and Riesz Representation)

---

## 🎯 学习目标与任务背景

### 1. 学习目标
1. 熟练运用平行四边形律判定内积空间，并掌握极化恒等式的代数展开。
2. 掌握 Hilbert 空间闭子空间上的正交分解计算与最小二乘最佳逼近问题。
3. 熟练应用 Riesz 表示定理寻找连续泛函的代表元，并运用 Lax-Milgram 引理分析简单微分方程弱解。

### 2. 任务背景与边界
本作业涵盖 Hilbert 空间的几何特征、正交投影最佳逼近计算、Riesz 对偶代表元求解以及一维变分弱解的 Lax-Milgram 求解。要求给出解析解的显式积分表达式与双线性型不等式界。

---

## 📝 作业题目清单 (满分 100 分)

### 题 1：Jordan-von Neumann 平行四边形律判定 (25 分)
在连续函数空间 $X = C[0, 1]$ 上分别考虑以下两个范数：
1. 范数 $\|f\|_1 = \left( \int_0^1 |f(t)|^2 dt \right)^{1/2}$；
2. 范数 $\|f\|_2 = \max_{t \in [0,1]} |f(t)|$。
请判断并证明：哪一个范数是由内积诱导的？哪一个范数绝不可能由任何内积诱导？(25 分)

---

### 题 2：$L^2[0, 1]$ 上的多项式正交投影与最佳逼近 (25 分)
在实 Hilbert 空间 $H = L^2[0, 1]$（内积 $\langle f, g \rangle = \int_0^1 f(t)g(t) dt$）中，设 $M = \operatorname{span}\{1, t\}$ 为所有一次多项式构成的二维子空间。
设目标函数 $f(t) = t^2$。
1. 计算 $M$ 的标准正交基 $\{e_1(t), e_2(t)\}$（利用 Gram-Schmidt 正交化）。(10 分)
2. 计算 $f(t) = t^2$ 在子空间 $M$ 上的正交投影函数 $P_M f(t)$。(10 分)
3. 计算点到子空间的最短距离 $\operatorname{dist}(t^2, M) = \|t^2 - P_M(t^2)\|_{L^2}$。(5 分)

---

### 题 3：Riesz 表示定理构造代表元 (25 分)
在实 Hilbert 空间 $H = L^2[0, 1]$ 上定义泛函：
$$F(g) = \int_0^1 \left( \int_0^t g(s) ds \right) dt$$
1. 证明 $F: L^2[0, 1] \to \mathbb{R}$ 是连续线性泛函，并估计其范数上界 $\|F\|_{H^*}$。(10 分)
2. 显式寻找唯一的函数 $y(t) \in L^2[0, 1]$，使得 $F(g) = \int_0^1 g(t) y(t) dt \ (\forall g \in L^2[0,1])$，并精确计算 $\|F\|_{H^*}$。(15 分)

---

### 题 4：一维 Dirichlet 边值问题的 Lax-Milgram 求解 (25 分)
考虑一维边值问题：
$$-u^{\prime\prime}(x) + c(x) u(x) = f(x), \quad x \in (0, 1), \quad u(0) = u(1) = 0$$
其中 $c(x) \ge 0$ 是 $[0,1]$ 上的连续非负函数，$f \in L^2(0,1)$。
设实 Hilbert 空间为 Sobolev 空间 $H_0^1(0, 1)$，内积定义为 $\langle u, v \rangle_{H_0^1} = \int_0^1 u^\prime(x) v^\prime(x) dx$。
1. 将该微分方程转化为等价的弱形式变分方程：求 $u \in H_0^1(0,1)$ 使得 $a(u, v) = \int_0^1 f(x)v(x)dx \ (\forall v \in H_0^1)$。(10 分)
2. 验证双线性型 $a(u, v) = \int_0^1 [u^\prime v^\prime + c(x) u v] dx$ 在 $H_0^1(0,1)$ 上满足**连续性**与**矫顽性**。(10 分)
3. 应用 Lax-Milgram 引理证明该问题存在唯一的弱解 $u \in H_0^1(0,1)$。(5 分)

---

## 📦 提交产物与格式规范

1. 包含 4 道题完整证明与具体数值/函数解析解的推导报告。
2. 包含 Gram-Schmidt 正交化中间过程与 Fubini 积分交换的具体步骤。

---

## 📊 100 分 Rubric 验收标准

| 评分维度 | 权重 | 评分标准 |
| :--- | :---: | :--- |
| **几何计算与正交化** | 30% | Gram-Schmidt 正交化、投影积分与最短距离计算无算术与微积分错误。 |
| **Fubini 交换与代表元求解** | 30% | 准确利用 Fubini 定理交换积分次序，代表元函数 $y(t)$ 形式无误。 |
| **Lax-Milgram 变分验证** | 30% | 弱形式分部积分推导规范，连续常数 $C$ 与矫顽常数 $\alpha$ 估计清晰。 |
| **定理与格式规范** | 10% | 正确引用 Poincaré 不等式或内积公理。 |

---

## 🔍 引导自检与检查点

- 💡 **自检 1**：在题 3 中，交换积分次序 $\int_0^1 dt \int_0^t g(s)ds = \int_0^1 g(s) ds \int_s^1 dt = \int_0^1 (1-s) g(s) ds$，因此代表元为 $y(t) = 1 - t$！
- 💡 **自检 2**：在题 4 矫顽性证明中，$a(u, u) = \int_0^1 (u^\prime)^2 dx + \int_0^1 c(x) u^2 dx \ge \int_0^1 (u^\prime)^2 dx = \|u\|_{H_0^1}^2$（因为 $c(x) \ge 0$），矫顽常数直接可取 $\alpha = 1$！
