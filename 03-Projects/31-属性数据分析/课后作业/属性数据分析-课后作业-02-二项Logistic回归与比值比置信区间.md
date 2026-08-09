---
type: project
project_type: homework
course: "属性数据分析"
assignment_id: "CDA-HW-02"
assignment_level: lesson
assignment_format: lab
stage_id: "02"
requires: ["[[属性数据分析-二项Logistic回归模型与参数解释]]", "[[属性数据分析-Logistic模型参数估计与Fisher得分算法]]"]
source_type: official_assignment
status: completed
flow: project
tags: [作业, 属性数据分析, Logistic回归, GLM]
created: 2026-08-09
---

# 属性数据分析-课后作业-02-二项Logistic回归与比值比置信区间

## 🎯 学习目标
1. 掌握二分类响应变量的构造与 Logistic 模型的规范形式；
2. 熟练使用 `statsmodels` 拟合单变量与多变量二项 Logistic 回归模型，提取对数似然值、Deviance 与协方差矩阵；
3. 掌握连续协变量（甲壳宽度、体重）与多分类因子（甲壳颜色）在几率比（Odds Ratio）维度的严谨统计学解释；
4. 运用 Divide-by-4 经验法则估算自变量的最大边际概率效应，并与模型在特定点处的精确偏导数对比；
5. 在 173 条完整真实马蹄蟹数据上完成参数估计、Wald 检验与似然比检验（LRT）的比较。

---

## 🚧 任务边界与环境要求
- **适用知识范围**：二项 Logistic 回归模型、Logit 变换、几率比解释、IRLS 估计理论与渐近推断三大检验。
- **计算环境**：Python 3.10+（依赖 `pandas`, `numpy`, `statsmodels`, `scipy.stats`, `matplotlib`）。
- **数据集**：完整真实数据集 `03-Projects/31-属性数据分析/data/crabs.csv`（173 只雌马蹄蟹记录）。

---

## 📝 详细题目与任务指引

### 实验背景
使用经典 Agresti 马蹄蟹数据集 `data/crabs.csv`（173 条完整记录），研究雌蟹形态特征（甲壳宽度 `Width` cm、体重 `Weight` kg、甲壳颜色 `Color`）对其是否吸引到至少一只卫星公蟹伴侣（`Has_Satellites = (Satellites > 0)`）的影响。

### 实验步骤
1. **数据预处理与探索**：
   - 加载 `crabs.csv`，验证样本量为 173；
   - 构造二值响应变量 $y_i = \mathbb{I}(\text{Satellites}_i > 0)$，统计伴侣存在率 $P(y=1)$；
   - 绘制甲壳宽度与伴侣存在率的散点平滑拟合曲线（Lowess 平滑）。
2. **单变量 Logistic 回归与参数解释**：
   - 拟合模型 $\text{logit}(P(y=1)) = \alpha + \beta \cdot \text{Width}$；
   - 汇报 $\hat{\alpha}, \hat{\beta}$、渐近标准误 $\text{SE}(\hat{\beta})$、Wald $z$ 统计量及 $p$ 值；
   - 计算甲壳宽度每增加 1cm 对应的优势比 $\widehat{\text{OR}} = \exp(\hat{\beta})$ 及其 95% profile likelihood 与 Wald 置信区间；
   - 利用 Divide-by-4 规则估算甲壳宽度增加 1cm 带来的最大概率增量 $\Delta \hat{\pi}_{\max} \approx \hat{\beta}/4$，并计算在样本均值 $\overline{\text{Width}}$ 处的精确概率增量。
3. **多变量扩展与混杂控制**：
   - 将分类变量 `Color` 进行哑变量编码（以 Color=1 为基准），构建全模型：
     $$
     \text{logit}(P(y=1)) = \beta_0 + \beta_1 \text{Width} + \beta_2 \text{Weight} + \sum_{k=2}^4 \gamma_k \mathbb{I}(\text{Color}=k)
     $$
   - 比较单变量与多变量模型中 Width 系数的变化，分析 Weight 与 Width 的多重共线性对各自 Wald 显著性的影响；
   - 使用似然比检验（LRT）联合检验 `Color` 的所有哑变量系数是否显著为 0（$\Delta D \sim \chi^2_3$）。
4. **模型预测与置信带可视化**：
   - 在宽度区间 $[20, 32]$ 范围内生成网格点，计算预测概率 $\hat{\pi}(x)$ 及其线性预测器 $\hat{\eta}(x) \pm 1.96 \cdot \text{SE}(\hat{\eta})$ 反变换得到的 95% 置信带；
   - 绘制预测概率曲线图并导出保存为 `output/crab_logit_curve.png`。

---

## 📦 提交产物与交付要求
1. **分析脚本**：完整可执行的 Python 脚本（含数据清洗、模型拟合、LRT 检验与可视化输出）；
2. **结果对比表**：包含单变量与多变量模型的参数估计、标准误、Wald $p$ 值、调整优势比（aOR）及 95% CI；
3. **可视化图表**：包含置信区间的预测概率曲线图；
4. **统计报告**：针对生态学研究人员撰写的结论报告（不少于 300 字），回答“甲壳宽度是否是决定伴侣吸引力的关键因素”。

---

## 💡 引导与自检清单
- [ ] 数据集是否确认包含了全部 173 只马蹄蟹，而非切片数据？
- [ ] 连续变量的优势比解释是否明确说明了“在控制其他协变量不变的前提下”？
- [ ] 在解释 $\exp(\hat{\beta})$ 时，是否准确区分了“几率（Odds）增加了 $(e^\beta - 1) \times 100\%$”与“概率（Probability）增加了多少”？
- [ ] LRT 检验统计量计算式 $\Delta D = -2(\ell_{\text{reduced}} - \ell_{\text{full}})$ 是否正确？

---

## 💯 综合验收标准 (Rubric)
| 评分项 | 分值 | 优异标准 | 合格标准 |
| :--- | :---: | :--- | :--- |
| **数据清洗与单变量模型** | 25 | 数据转换无误，单变量 Logit 参数估计与标准误精确，Divide-by-4 解释到位 | 模型拟合成功，完成基础单变量参数汇报 |
| **参数解释与置信区间** | 30 | Log-odds 与 OR 解释规范，Wald 与 Profile 似然置信区间推导无误 | OR 计算正确，给出基础 Wald 区间 |
| **多变量扩展与 LRT 检验** | 25 | 哑变量编码无误，共线性分析深入，LRT 统计量与自由度计算准确 | 多变量模型拟合成功，完成基础方差分析 |
| **可视化与结论报告** | 20 | 曲线图带反变换置信带，生态学结论严谨，无概念混淆 | 图表清晰，报告结构完整 |
