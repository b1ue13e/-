---
type: project
project_type: homework
course: "16-多元统计"
assignment_id: "多元统计-HW01"
assignment_level: lesson
assignment_format: lab
stage_id: "01"
requires: ["[[多元统计-多元正态分布与性质]]", "[[多元统计-均值向量与协方差矩阵估计]]", "[[多元统计-Hotelling T² 检验]]"]
source_type: official_assignment
created: 2026-08-09
status: completed
flow: project
tags: [作业, 课后作业, 多元正态, Hotelling, 瑞士钞票]
---

# 多元统计-课后作业-01-多元正态推断与Hotelling T²

---

## 1. 学习目标

完成本项课后作业后，你将能够：
1. 严格运用矩阵代数推导多元样本均值向量、离差阵与合并样本协方差矩阵；
2. 掌握单样本与两样本 Hotelling $T^2$ 统计量的构造与精确 $F$ 分布自由度转换；
3. 熟练调用 `mva_toolkit.py` 与 `load_data.py`，对真实瑞士钞票数据（Flury & Riedwyl 1988）进行 Mardia 正态性诊断与两样本 $T^2$ 均值向量检验。

---

## 2. 任务背景与真实数据

- **数据集路径**：`03-Projects/16-多元统计/data/swiss_banknotes.csv`（可调用 `scripts/load_data.py` 加载）。
- **样本信息**：瑞士中央银行 200 张钞票（100 张真钞 vs 100 张伪钞），包含 6 个几何尺寸指标：
  - `Length`（长度）、`Left`（左边宽）、`Right`（右边宽）、`Bottom`（下边距）、`Top`（上边距）、`Diagonal`（对角线长度）。
- **任务边界**：
  - 题目 1：小样本理论推断与手算验证；
  - 题目 2：基于 Python 加载真实 `swiss_banknotes.csv` 进行完整的假设检验与报告撰写。

---

## 3. 详细题目与实验内容

### 题目 1：小样本理论推导与手算 (30分)
设有两组 2 维连续数据：
- 组 1 ($n_1 = 3$)：$\mathbf{x}_{11} = (1, 2)^T, \mathbf{x}_{12} = (2, 3)^T, \mathbf{x}_{13} = (3, 4)^T$
- 组 2 ($n_2 = 3$)：$\mathbf{x}_{21} = (4, 5)^T, \mathbf{x}_{22} = (5, 6)^T, \mathbf{x}_{23} = (6, 7)^T$

1. 手算两组样本均值向量 $\bar{\mathbf{x}}_1, \bar{\mathbf{x}}_2$ 及无偏样本协方差矩阵 $\mathbf{S}_1, \mathbf{S}_2$；
2. 计算合并样本协方差矩阵 $\mathbf{S}_{pooled}$ 及其逆矩阵 $\mathbf{S}_{pooled}^{-1}$；
3. 计算两样本 Hotelling $T^2$ 统计量及转换后的 $F$ 统计量与自由度。

### 题目 2：真实瑞士钞票数据集假设检验实战 (50分)
编写 Python 脚本调用 `load_data.py` 和 `mva_toolkit.py`：
1. **正态性诊断**：对真钞 100 张样本进行 Mardia 偏度与峰度检验；
2. **两样本 Hotelling $T^2$ 检验**：检验真钞与伪钞在 6 个维度上的总体均值向量是否完全相同（$H_0: \boldsymbol{\mu}_{gen} = \boldsymbol{\mu}_{fake}$）；
3. **同时置信区间**：输出 95% 显著性水平下 6 个指标的 Bonferroni 与 Hotelling 同步置信区间，并分析哪个几何指标对识别假钞最具贡献。

### 题目 3：高维病态协方差矩阵崩溃与 Cholesky 正则化对比实验 (20分)
1. 构造一个近共线性的 $p=6, n=10$ 小样本数据矩阵 $\mathbf{X}$（条件数 $\kappa(\mathbf{S}) > 10^5$）；
2. 对比原生 `np.linalg.inv` 直接求逆与 `mva_toolkit.py` 内部基于 Cholesky 岭正则化求逆算出的 Hotelling $T^2$ 统计量；
3. 分析当特征维度接近或大于样本量时，标准样本协方差矩阵崩塌的第一性原理原因，并说明为什么 Cholesky 分解加正则化是工程与科研的最佳实践。

---

## 4. 环境与依赖说明

- **Python 环境**：$\ge 3.10$
- **依赖库**：`numpy`, `scipy`, `pandas`
- **数据加载接口**：
  ```python
  from load_data import load_swiss_banknotes
  from mva_toolkit import mardia_test, hotelling_t2_two_sample
  df_bank = load_swiss_banknotes()
  ```

---

## 5. 提交产物清单

1. 包含题目 1 完整手算推导步骤的手稿或 Markdown 文档；
2. 包含 Mardia 正态检验、两样本 Hotelling $T^2$ 检验与 6 维同时置信区间的 Python 运行脚本；
3. 瑞士真伪钞票几何尺寸差异辨析分析报告。

---

## 6. 评判标准 (Rubric)

| 评分项 | 满分 | 达标要求 |
| :--- | :--- | :--- |
| **理论推导严谨性** | 30分 | 均值、协方差、$\mathbf{S}_{pooled}^{-1}$ 与 $T^2$ 手算步骤准确无误 |
| **代码与真实数据分析** | 40分 | 正确加载 `swiss_banknotes.csv`，Mardia 检验与两样本 $T^2$ 运行无误 |
| **统计结论与特征分析** | 30分 | 准确指出 `Diagonal` 和 `Bottom` 边距是区分真假钞票的核心几何指标 |

---

## 7. 引导提示与提交自检

- **提示**：两样本 $T^2$ 假定真伪钞票总体的协方差矩阵相等，运行前可以先调用 `box_m_test` 检查协方差齐性。
- **自检项**：
  - [ ] `swiss_banknotes.csv` 路径载入无误；
  - [ ] 两样本 $T^2$ 转换后的 $F$ 统计量自由度为 $df_1 = 6, df_2 = 193$；
  - [ ] 同步置信区间中 Hotelling 边界比 Bonferroni 边界更加宽松（包络包含更多向量方向）。

---

## 8. 规格验证记录（GOV-6, spec_verified）

- **验证脚本**：`scripts/hw01_verify.py`。
- **运行日期**：2026-08-10；**关键数值**：swiss 两样本 Hotelling T²=1351.36、F=219.54、df₁=6、df₂=193、p≈0（与题面自检一致）；Mardia 偏度 p=0.325、峰度 p=0.740（真钞近似多元正态）。
- **规格注意（待作者决定）**：题目 1 玩具数据 (1,2)/(2,3)/(3,4) 与 (4,5)/(5,6)/(6,7) 完全共线，导致合并协方差 S_pooled 奇异、S_pooled⁻¹ 不存在；mva_toolkit 经岭正则化给出 T²≈13.5。建议扰动玩具数据或显式改用广义逆。
- 本记录仅证明规格可执行与题面数值一致；学习者真实执行仍待补齐。
