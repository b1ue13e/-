---
type: project
project_type: homework
course: "复变函数"
assignment_id: "37-复变函数-HW01"
assignment_level: lesson
assignment_format: problem-set
stage_id: "01"
requires: ["[[解析函数与 Cauchy-Riemann 方程]]", "[[复数运算与复平面]]", "[[复变函数-前置-实分析与多元微积分]]"]
source_type: open_textbook_exercise
created: 2026-08-07
status: completed
flow: project
tags: [复变函数, 作业, Cauchy-Riemann]
---

# 37-复变函数-课后作业-01-Cauchy-Riemann方程与解析性

## 学习目标

1. 深入理解复数的代数表示（\(z = x+iy\)）、三角表示与指数表示（Euler 公式 \(e^{i\theta}\)），掌握复平面的拓扑概念（邻域、区域、单连通性）。
2. 熟练运用 Cauchy-Riemann (C-R) 条件判定复函数的解析性，深刻理解复可导与实可微的本质区别。
3. 掌握由调和函数求调和共轭函数的方法，构造完整的复解析函数。

## 任务边界

本作业专注于第一阶段复微分学的核心计算与理论证明：
- 严格验证复导数定义极限的不依赖路径特性。
- 求解 Cauchy-Riemann 偏微分方程组。
- 利用线积分法或偏微分积分法构造调和共轭函数。

可以使用 Python 的 `sympy` 符号运算模块协助验证偏导数与共轭函数，但提交产物中必须保留完整的推导细节与求解步骤。

## 详细题目

### 题目 1 (复导数与解析性证明 [MIT 18.04 Spring 2018 PS1 Problem 3])
设 \( f(z) = u(x,y) + i v(x,y) \) 在开区域 \( D \subset \mathbb{C} \) 内解析。
1. 试利用 Cauchy-Riemann 方程证明：若 \( f'(z) = 0 \) 在 \( D \) 内恒成立，则 \( f(z) \) 在 \( D \) 内必为常数。
2. 若 \( |f(z)| \) 在 \( D \) 内为常数 \( C \)，证明 \( f(z) \) 在 \( D \) 内亦必为常数。（提示：区分 \( C=0 \) 与 \( C>0 \) 两种情形，利用 \( u^2 + v^2 = C^2 \) 对 \( x, y \) 求偏导并结合 C-R 条件分析方程组的系数行列式）。

### 题目 2 (调和共轭与解析函数构造 [MIT 18.04 Spring 2018 PS2 Problem 1])
已知实二元函数 \( u(x,y) = x^3 - 3xy^2 + 2x \)：
1. 计算 \( u(x,y) \) 的 Laplacian \(\Delta u = \frac{\partial^2 u}{\partial x^2} + \frac{\partial^2 u}{\partial y^2}\)，验证其在全平面 \(\mathbb{R}^2\) 上为调和函数。
2. 求 \( u(x,y) \) 的调和共轭函数 \( v(x,y) \)，使得 \( f(z) = u(x,y) + i v(x,y) \) 满足 Cauchy-Riemann 方程且满足初始条件 \( f(0) = 0 \)。
3. 将求得的 \( f(z) \) 显式表示为复变量 \( z \) 的多项式形式。

---

## 提交产物

- Markdown 或 LaTeX 格式的详细推导解答文档。
- （可选）Python SymPy 验证代码及运行结果输出截图。

## 验收标准 (Rubric)

| 评分维度 | 满分 | 得分标准 |
| :--- | :--- | :--- |
| **C-R 方程推导与逻辑** | 40% | 偏导数求解准确，C-R 方程引用无误，证明过程推导严密 |
| **调和函数与共轭构造** | 30% | 调和性证明完整，调和共轭积分路径或方程求解无误 |
| **复变量多项式表示** | 30% | 正确将 \( u+iv \) 归纳重构为 \( z \) 的解析表达式，无残留 \(\bar{z}\) |

## 引导与自检

- **常见错误**: 遗漏一阶偏导数连续的充要条件；C-R 方程正负号记错（正确为 \( u_x = v_y \), \( u_y = -v_x \)）。
- **自检点**: 构造出的 \( f(z) \) 必须能完全表达为 \( z \) 的函数，如果化简后包含 \(\bar{z}\) 或 \(|z|\) 等非解析成分，说明共轭函数计算有误。
