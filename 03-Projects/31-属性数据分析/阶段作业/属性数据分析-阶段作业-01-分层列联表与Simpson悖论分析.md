---
type: project
project_type: homework
course: "属性数据分析"
assignment_id: "CDA-Stage-01"
assignment_level: stage
assignment_format: lab
stage_id: "01"
requires: ["[[属性数据分析-分层列联表与CMH检验]]", "[[属性数据分析-独立性与拟合优度检验]]"]
source_type: official_assignment
status: completed
flow: project
tags: [作业, 阶段作业, 属性数据分析, Simpson悖论, CMH检验, 分层分析]
created: 2026-08-09
---

# 属性数据分析-阶段作业-01-分层列联表与Simpson悖论分析

## 🎯 学习目标
1. 深入理解 Simpson 悖论在分层列联表中的几何与代数成因；
2. 熟练运用 `statsmodels.stats.contingency_tables.StratifiedTable` 进行 $2 \times 2 \times K$ 分层分析；
3. 掌握 Cochran-Mantel-Haenszel (CMH) 汇总几率比 $OR_{\text{MH}}$ 统计量推导与假设立检验；
4. 掌握 Breslow-Day 几率比同质性检验（Homogeneity of Odds Ratios），评估层间是否存在显著交互效应。

---

## 🚧 任务边界与环境要求
- **适用知识范围**：分层列联表、条件独立性、边际独立性、Simpson 悖论、CMH 检验与 Breslow-Day 同质性检验。
- **计算环境**：Python 3.10+（`statsmodels`, `scipy.stats`, `pandas`）。
- **数据集**：完整真实数据集 `03-Projects/31-属性数据分析/data/ucb_admissions.csv`（加州大学伯克利分校 6 院系 4526 人次录取频数数据）。

---

## 📝 详细题目与任务指引

### 实验背景
1973 年加州大学伯克利分校（UCB）研究生录取数据是统计学史上最著名的 Simpson 悖论案例。边际汇总数据呈现出显著的性别偏向（男性录取率高于女性），但按院系（Dept A-F）分层后，各院系内部的录取率差异几乎消失甚至微弱偏向女性。

### 实验步骤
1. **边际关联分析**：
   - 汇总 6 个院系数据，构建 $2 \times 2$ 边际列联表（性别 $\times$ 录取状态）；
   - 计算边际优势比 $\widehat{\text{OR}}_{\text{marginal}}$、Pearson $X^2$ 统计量及 $p$ 值，给出边际结论。
2. **分层关联分析与 Simpson 悖论剖析**：
   - 分别对 A, B, C, D, E, F 六个院系构建 $2 \times 2$ 条件列联表；
   - 计算每个院系内部的条件优势比 $\widehat{\text{OR}}_k$ 及其 95% 置信区间；
   - 分析混杂变量（院系申请难易度与性别申请比例）的联合分布，解释为什么边际 OR 产生了严重反转（Simpson 悖论）。
3. **CMH 汇总检验与 Breslow-Day 同质性检验**：
   - 构造 $(2, 2, 6)$ 维度频数张量，拟合 `StratifiedTable`；
   - 计算 Mantel-Haenszel 汇总优势比 $\widehat{\text{OR}}_{\text{MH}}$ 及其 95% 置信区间；
   - 汇报 CMH 检验统计量与 $p$ 值，判定在控制院系混杂后，性别与录取率是否存在条件独立性；
   - 执行 Breslow-Day 检验，评估 6 个院系的条件优势比是否满足同质性假设。

---

## 📦 提交产物与交付要求
1. **分析脚本**：完整可执行的 Python 脚本，输出边际 OR、各层条件 OR、CMH 统计量与 Breslow-Day 结果；
2. **分层分析结果表**：包含 6 个院系的申请数、录取率、条件 OR 及同质性检验汇总表格；
3. **因果推断与机制报告**：绘制混杂路径图（DAG），撰写不少于 300 字的 Simpson 悖论机制分析报告。

---

## 💡 引导与自检清单
- [ ] 边际 OR（约 1.84）与 CMH 汇总 OR（约 0.90）方向是否完全相反？
- [ ] Breslow-Day 检验的 $p$ 值是否显著（伯克利数据中 A 院系女性录取率极高导致存在同质性违背）？
- [ ] 能否从“女性集中申请竞争最激烈的 C/D 院系，男性集中申请录取率高的 A/B 院系”这一结构性分布解释悖论？

---

## 💯 综合验收标准 (Rubric)
| 评分项 | 分值 | 合格标准 |
| :--- | :---: | :--- |
| **边际与条件分析** | 25 | 边际 OR 与 6 个分层条件 OR 计算完全准确 |
| **Simpson 悖论机制剖析** | 30 | 能清晰指出混杂变量 Dept 的双重相关性（与 Gender、Admit 均相关） |
| **CMH 与 Breslow-Day 检验** | 30 | $OR_{\text{MH}}$、CMH 统计量与 Breslow-Day 检验结果无误且解释精准 |
| **报告质量与 DAG 图** | 15 | 分析报告逻辑严密，因果路径图绘制规范 |
