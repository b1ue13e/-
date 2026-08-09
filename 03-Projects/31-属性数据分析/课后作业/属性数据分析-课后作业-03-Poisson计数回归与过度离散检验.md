---
type: project
project_type: homework
course: "属性数据分析"
assignment_id: "CDA-HW-03"
assignment_level: lesson
assignment_format: lab
stage_id: "03"
requires: ["[[属性数据分析-Poisson回归模型与暴露量率模型]]", "[[属性数据分析-过度离散诊断与负二项扩展]]"]
source_type: official_assignment
status: completed
flow: project
tags: [作业, 属性数据分析, Poisson回归, 过度离散, 负二项回归]
created: 2026-08-09
---

# 属性数据分析-课后作业-03-Poisson计数回归与过度离散检验

## 🎯 学习目标
1. 掌握计数响应变量（Count Data）的 Poisson 概率分布特性与 Log 链接函数建模；
2. 理解发生率比（Incidence Rate Ratio, IRR）的物理意义与参数解释；
3. 掌握 Pearson 残差分散参数 $\hat{\phi} = \frac{X^2}{\text{df}_{\text{resid}}}$ 的过度离散（Overdispersion）定量诊断；
4. 掌握使用负二项回归模型（Negative Binomial, NB2）修正过度离散并估计二次方差参数 $\alpha$。

---

## 🚧 任务边界与环境要求
- **适用知识范围**：Poisson 回归模型、Log 链接函数、暴露量（Offset）设定、过度离散检验与 NB2 模型。
- **计算环境**：Python 3.10+（`statsmodels`, `scipy.stats`, `pandas`）。
- **数据集**：完整真实数据集 `03-Projects/31-属性数据分析/data/crabs.csv`（173 只雌马蹄蟹伴侣计数）。

---

## 📝 详细题目与任务指引

### 实验背景
在马蹄蟹伴侣研究中，响应变量为雌蟹吸引到的卫星公蟹数量（`Satellites`），取值为非负整数 $\{0, 1, 2, \dots, 15\}$。探索甲壳宽度 `Width` 与体重 `Weight` 对伴侣数量的计数效应。

### 实验步骤
1. **探索性计数分析**：
   - 加载 `crabs.csv`，计算 `Satellites` 的样本均值 $\bar{y}$ 与样本方差 $s^2$；
   - 比较均值与方差，初步判断是否存在方差显著大于均值的过度离散现象（Overdispersion）。
2. **Poisson 计数回归**：
   - 拟合 Poisson 模型 $\ln(\mu_i) = \beta_0 + \beta_1 \text{Width}_i + \beta_2 \text{Weight}_i$；
   - 汇报系数 $\hat{\beta}_1, \hat{\beta}_2$、标准误、Wald $z$ 值及发生率比 $\text{IRR} = \exp(\hat{\beta})$；
   - 计算 Pearson 卡方统计量 $X^2 = \sum \frac{(y_i - \hat{\mu}_i)^2}{\hat{\mu}_i}$ 与残差自由度 $\text{df} = n - p = 170$；
   - 计算分散参数估计值 $\hat{\phi} = \frac{X^2}{170}$，评估模型的过度离散程度。
3. **负二项回归 (NB2) 修正**：
   - 拟合方差结构为 $\text{Var}(Y) = \mu + \alpha \mu^2$ 的负二项回归模型；
   - 比较 Poisson 与 NB2 模型的参数估计值、标准误变化及 AIC/BIC；
   - 解释为什么在过度离散存在时，Poisson 回归的标准误会被严重低估，导致虚假的显著性。

---

## 📦 提交产物与交付要求
1. **分析脚本**：包含完整数据加载、Poisson 与 NB2 模型拟合及 $\hat{\phi}$ 诊断的 Python 脚本；
2. **模型对比表**：包含 Poisson 与 NB2 模型下的系数、标准误、IRR、Log-Likelihood 及 AIC 表格；
3. **诊断报告**：150 字以内的过度离散诊断与选型建议。

---

## 💡 引导与自检清单
- [ ] 样本均值与方差相差多少？$\hat{\phi}$ 是否显著大于 1（马蹄蟹数据通常在 3.0 以上）？
- [ ] 从 Poisson 切换到 NB2 后，自变量系数的标准误是否放大了？这说明了什么？
- [ ] IRR 的解释是否规范说明了“自变量增加 1 单位，预期事件频数变为原来的 $\exp(\hat{\beta})$ 倍”？

---

## 💯 综合验收标准 (Rubric)
| 评分项 | 分值 | 合格标准 |
| :--- | :---: | :--- |
| **数据清洗与 Poisson 拟合** | 30 | 数据读取正确，Poisson 模型拟合成功，参数与 IRR 解释准确 |
| **过度离散诊断** | 35 | 准确计算 Pearson $X^2$ 与 $\hat{\phi}$，对过散现象成因分析深入 |
| **NB2 修正与对比** | 35 | NB2 模型拟合无误，准确对比标准误扩大的统计学影响，模型选型论据充分 |
