---
type: project
project_type: homework
course: "非参数统计"
assignment_id: "非参数统计-阶段-01"
assignment_level: stage
assignment_format: lab
stage_id: "04"
requires: ["[[非参数统计-置换检验Permutation-Test]]", "[[非参数统计-Bootstrap重采样与置信区间]]"]
source_type: open_source_project_task
created: 2026-08-08
status: active
flow: project
tags: [作业, 阶段作业, 非参数统计, 置换检验, Bootstrap, 仿真实验]
---

# 非参数统计-阶段作业-01-置换检验与Bootstrap置信区间对比

---

## 🎯 学习目标

- 掌握两独立样本 Monte Carlo 置换检验算法实现与精确条件分布构建。
- 掌握 Bootstrap 四类置信区间（标准正态、基本、百分位、BCa）的算法实现。
- 定量对比在长尾偏态与异常值污染下，BCa 区间如何纠正估计偏倚与方差不对称。

---

## 🚧 任务边界

- **输入数据**：生成受离群点污染的对数正态双样本。
- **重抽样次数**：置换检验 $B \ge 5000$，Bootstrap 重采样 $B \ge 2000$。
- **评价指标**：检验 $p$ 值、置信区间覆盖率与区间不对称度。

---

## 📝 详细题目

### 步骤 1：生成厚尾受污染实验数据
设定真实数据生成机制：
- 组 A ($n_1=25$): $X \sim \text{LogNormal}(\mu=0, \sigma=1)$
- 组 B ($n_2=25$): $Y \sim \text{LogNormal}(\mu=0.5, \sigma=1) + \text{污染项}$（$10\%$ 概率混入 $+50$ 的离群值）

### 步骤 2：执行假设检验全面对比
1. 运行 Student's t 检验，记录 $p$ 值与均值差置信区间。
2. 运行 Mann-Whitney U 检验，记录 $p$ 值与中位数差估计。
3. 实现 Monte Carlo 置换检验，记录置换分布直方图与置换 $p$ 值。

### 步骤 3：Bootstrap 置信区间精度评估 ($B=5000$)
对组间中位数差 $\Delta = \text{median}(B) - \text{median}(A)$：
1. 计算 Bootstrap 标准误 $\\widehat{\text{SE}}_{\text{boot}}$；
2. 构造 Normal, Basic, Percentile, BCa 4 种 $95\%$ 置信区间；
3. 对比分析为什么在偏态厚尾下 BCa 区间能够纠正左偏/右偏的覆盖偏差。

---

## 📦 提交产物

1. **实验控制台输出与图表**：包含两样本检验 $p$ 值对比表与置换直方图。
2. **算法代码**：在 `scripts/run_nonparam_experiments.py` 中实现的 `permutation_test_mean` 与 `bootstrap_bca_ci`。

---

## 💯 验收标准 / Rubric

| 维度 | 分值 | 验收要求 |
|:---|---:|:---|
| 数据生成与离群点注入 | 20 | 数据随机种子固定，离群点污染清晰可复现 |
| 置换检验与 Monte Carlo 实现 | 30 | 无偏随机洗牌，准确计算分子加 1 修正 $p$ 值 |
| BCa 留一法与偏倚参数推导 | 30 | 正确计算 $z_0$ 与留一法加速度参数 $a$ |
| 结果对比与实证总结 | 20 | 深入剖析 t 检验在离群点下的失效机制与非参数优越性 |

---

## 🧭 引导自检

- [ ] 我的置换检验是否加上了 $(1 + \text{count}) / (1 + B)$ 的无偏修正？
- [ ] BCa 算法中的 Jackknife 是否正确计算了三阶中心矩偏度？
- [ ] 运行脚本是否能一键输出全部置信区间？

---

## 🔗 来源与后续

- 来源：Efron & Tibshirani, *An Introduction to the Bootstrap* Chapter 12 & 14.
- 后续：[[非参数统计-大作业-非参数推断与平滑方法全景实证研究]]
