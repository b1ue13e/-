---
type: project
project_type: homework
course: "22-概率论与数理统计"
assignment_id: "Stat-HW03"
assignment_level: lesson
assignment_format: problem-set
stage_id: "02"
requires: ["[[概率统计-充分统计量与因子分解定理]]", "[[概率统计-点估计方法：矩估计与极大似然估计]]"]
source_type: open_textbook_exercise
source_url: "https://ocw.mit.edu/courses/6-041sc-probabilistic-systems-analysis-and-applied-probability-fall-2013/"
created: 2026-08-09
status: completed
flow: project
tags: [作业, 概率论与数理统计, 课后作业, 充分统计量, MLE]
---

# 概率统计-课后作业-03-充分统计量与MLE数值求解

## 来源与改编说明

- **source_type**：`open_textbook_exercise` —— 本题依课程双理论 Spine 的习题口径融合改编，非官方原题照抄。
- **可追溯来源**：MIT 6.041SC Probabilistic Systems Analysis（Fall 2013，CC BY-NC-SA 4.0，见 `📚 教材挂载索引`）；对应 茆诗松《概率论与数理统计教程》（第3版）第 5–6 章（数理统计的基本概念、点估计与充分统计量）。
- **题号与页码**：[待验证] —— 具体教材题号/页码未逐题核对，不冒充官方原题；精确出处以对应 Spine 官方习题集为准。
- **本地化适配**：Beta/Weibull MLE 数值求解与因子分解验证为本课程本地设计，用于对齐已教授知识卡与闭卷验收。

## 🎯 学习目标

掌握 Neyman-Fisher 因子分解定理在多参数指数族下的应用；独立推导双参数连续分布（Beta 分布与 Weibull 分布）的似然方程组，并通过数值优化求解器实现参数极大似然估计（MLE）与 Fisher 观测信息量计算。

---

## 1. 详细任务说明

### 题目 1（理论手算）：双参数指数族与充分统计量证明
设 $X_1, \dots, X_n \overset{\text{i.i.d.}}{\sim} \text{Beta}(\alpha, \beta)$，其总体密度为：
$$f(x; \alpha, \beta) = \frac{1}{B(\alpha, \beta)} x^{\alpha-1} (1-x)^{\beta-1} \mathbb{I}_{(0, 1)}(x)$$
1. **指数族形式**：将联合样本密度 $f(\mathbf{x}; \alpha, \beta) = \prod_{i=1}^n f(x_i; \alpha, \beta)$ 改写为标准双参数指数族规范形式；
2. **充分统计量**：利用 Neyman-Fisher 因子分解定理，严格证明 $T(\mathbf{X}) = \left(\sum_{i=1}^n \ln X_i, \sum_{i=1}^n \ln(1 - X_i)\right)$ 是 $(\alpha, \beta)$ 的联合充分统计量；
3. **似然方程组**：写出对数似然函数 $\ell(\alpha, \beta)$，建立一阶导数方程（用 Digamma 函数 $\psi(x) = \frac{d}{dx}\ln\Gamma(x)$ 表达）。

### 题目 2（数值实现）：威布尔分布（Weibull）参数的数值极大似然估计
威布尔分布常用于工程寿命与可靠性分析，其概率密度为：
$$f(x; k, \lambda) = \frac{k}{\lambda} \left(\frac{x}{\lambda}\right)^{k-1} \exp\left(-\left(\frac{x}{\lambda}\right)^k\right) \quad (x > 0)$$
- **任务要求**：
  1. 写出样本 $x_1, \dots, x_n$ 的负对数似然函数 $\text{NLL}(k, \lambda)$ 解析式；
  2. 利用 Python（`scipy.optimize.minimize` 或自定义梯度下降）实现带参数正值约束的数值极小化求解；
  3. 对模拟寿命数据进行参数拟合，输出最优估计值 $(\hat{k}, \hat{\lambda})$ 与基于二阶数值导数（Hessian 矩阵）的参数渐近标准误 $\text{SE}(\hat{k})$ 和 $\text{SE}(\hat{\lambda})$。

---

## 2. 提交产物清单

1. 包含 Beta 分布指数族转化与充分性严密证明的 Markdown 报告；
2. 包含 Weibull MLE 数值求解模块与测试断言的 Python 源码；
3. 优化收敛轨迹日志与估计值与真实参数的偏差分析表。

---

## 3. 评分标准（Rubric）

| 评分项 | 分值 | 满分标准 |
| :--- | :---: | :--- |
| **Beta 充分性与指数族推导** | 45 | 指数族形式转换规范，因子分解定理应用严谨，充分统计量推导无误 |
| **Weibull 对数似然与数值优化** | 40 | 负对数似然表达式正确，优化算法收敛稳定，边界约束处理妥当 |
| **Hessian 与标准误分析** | 15 | 正确计算二阶导数矩阵，通过逆矩阵得到合理的渐近标准误 |

---

## 4. 引导自检与检查点

- [ ] 联合密度分解时指标函数 $\mathbb{I}_{(0, 1)}(x_i)$ 已纳入因式分解中；
- [ ] Weibull 尺度参数 $\lambda > 0$ 与形状参数 $k > 0$ 已设置正数下界保护；
- [ ] 运行 pytest 确保所有单元测试 100% 通过且无数值发散警告；
- [ ] 解释为什么 Weibull 无法直接求出封闭解析解而必须依赖数值迭代。

## 5. 关联与导航

- 前置卡片：[[概率统计-充分统计量与因子分解定理]]、[[概率统计-点估计方法：矩估计与极大似然估计]]
- 返回作业索引：[[🧭 课程作业总索引]]
