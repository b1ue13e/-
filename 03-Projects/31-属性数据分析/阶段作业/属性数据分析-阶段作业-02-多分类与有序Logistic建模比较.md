---
type: project
project_type: homework
course: "属性数据分析"
assignment_id: "CDA-Stage-02"
assignment_level: stage
assignment_format: lab
stage_id: "04"
requires: ["[[属性数据分析-累积Logit模型与比例优势假设]]", "[[属性数据分析-多项Logistic回归与基准类别模型]]"]
source_type: official_assignment
status: completed
flow: project
tags: [作业, 阶段作业, 属性数据分析, 有序Logistic, 累积Logit, 多项Logit]
created: 2026-08-09
---

# 属性数据分析-阶段作业-02-多分类与有序Logistic建模比较

## 🎯 学习目标
1. 掌握有序响应变量（Ordered Categorical Response）的潜变量截断机制（Latent Variable Thresholding）；
2. 熟练运用 `statsmodels.miscmodels.ordinal_model.OrderedModel` 拟合有序累积 Logit 模型；
3. 掌握比例优势假设（Proportional Odds Assumption）的假设检验与违反诊断；
4. 对比有序累积 Logit 模型与无序多项 Baseline Logit 模型在参数有效性与可解释性方面的优劣。

---

## 🚧 任务边界与环境要求
- **适用知识范围**：有序累积 Logit 模型、比例优势假设、多项 Baseline Logit 模型、AIC/BIC 模型比较。
- **计算环境**：Python 3.10+（`statsmodels`, `scipy.stats`, `pandas`）。
- **数据集**：完整真实数据集 `03-Projects/31-属性数据分析/data/arthritis.csv`（84 例关节炎双盲临床试验数据）。

---

## 📝 详细题目与任务指引

### 实验背景
使用经典 Koch 关节炎临床试验数据集 `data/arthritis.csv`（84 例完整记录），研究治疗方案（`Treatment`: Treated vs Placebo）与患者年龄（`Age`）对关节炎改善程度（`Improved`: None < Some < Marked）的效应。

### 实验步骤
1. **数据清洗与有序编码**：
   - 加载 `arthritis.csv`，确保 `Improved` 被编码为具有严格顺序的整数 $\{0: \text{None}, 1: \text{Some}, 2: \text{Marked}\}$；
   - 绘制 Treatment 与 Improved 的分层柱状图，观察治疗组与对照组的改善等级分布差异。
2. **有序累积 Logit 模型拟合**：
   - 拟合模型：
     $$
     \text{logit}(P(Y \le j)) = \alpha_j - (\beta_1 \text{Treatment\_Treated} + \beta_2 \text{Age}), \quad j = 0, 1
     $$
   - 汇报切点截距 $\hat{\alpha}_0, \hat{\alpha}_1$、回归系数 $\hat{\beta}_1, \hat{\beta}_2$ 及渐近标准误；
   - 计算 Treatment_Treated 的累积几率比（Cumulative Odds Ratio） $\text{cOR} = \exp(\hat{\beta}_1)$ 及其 95% 置信区间，解释其在“病情获得更好改善”维度上的临床意义。
3. **比例优势假设检验（Brant / LRT 检验）**：
   - 分别对 $Y \le 0$ 与 $Y \le 1$ 二值化切点拟合独立的二项 Logistic 模型；
   - 对比两个二项 Logit 模型中的回归系数，判断假设 $H_0: \boldsymbol{\beta}^{(0)} = \boldsymbol{\beta}^{(1)}$ 是否成立；
   - 汇报似然比检验统计量 $\Delta D$ 与 $p$ 值。
4. **与无序多项 Baseline Logit 模型对比**：
   - 以 `None` 为基准类别，拟合无序多项 Logistic 模型（Multinomial Logit）；
   - 比较有序 Logit 与无序多项 Logit 模型的参数个数、Log-Likelihood、AIC 与 BIC；
   - 总结为什么在响应变量具有天然顺序时，忽视顺序引入过多无序参数会导致统计功率（Power）下降。

---

## 📦 提交产物与交付要求
1. **分析脚本**：包含完整有序建模、比例优势检验及多项模型对比的 Python 脚本；
2. **模型比较表**：包含有序 Logit 与多项 Logit 的系数、标准误、cOR、AIC/BIC 汇总表；
3. **临床结论报告**：200 字以内的医学临床评估报告。

---

## 💡 引导与自检清单
- [ ] 有序累积 Logit 模型中的回归系数前是否有负号定义约定（`statsmodels` 的 `OrderedModel` 参数符号定义）？
- [ ] 治疗组 Treated 的 cOR（约 4.74~5.72）是否说明治疗能显著提高获得更好改善的累积几率？
- [ ] Brant/LRT 检验 $p > 0.05$ 是否验证了关节炎数据满足比例优势假设？

---

## 💯 综合验收标准 (Rubric)
| 评分项 | 分值 | 合格标准 |
| :--- | :---: | :--- |
| **有序编码与模型拟合** | 30 | 编码无误，`OrderedModel` 拟合正确，切点与系数汇报规范 |
| **累积 OR 临床解释** | 25 | cOR 及其 95% CI 计算无误，临床医学解释精准 |
| **比例优势检验与多项对比**| 30 | 比例优势假设检验步骤完整，与多项 Logit 的 AIC/BIC 对比深入 |
| **代码规范与报告** | 15 | 脚本可流畅运行，结论报告逻辑严密 |
