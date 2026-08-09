---
type: project
project_type: homework
course: "22-概率论与数理统计"
assignment_id: "Stat-Capstone"
assignment_level: capstone
assignment_format: project
stage_id: "04"
requires: ["[[概率统计-连续随机变量与核心分布族]]", "[[概率统计-点估计方法：矩估计与极大似然估计]]", "[[概率统计-参数区间估计与枢轴量法]]", "[[概率统计-非参数Bootstrap重抽样与置信区间]]", "[[概率统计-一元与多元线性回归的推断基础]]"]
source_type: local_integration_task
created: 2026-08-09
status: completed
flow: project
tags: [作业, 概率论与数理统计, 大作业, Capstone, Bootstrap, 真实数据建模]
---

# 概率统计-大作业-真实世界不确定性建模与Bootstrap稳健推断系统

## 来源与改编说明

- **source_type**：`local_integration_task` —— 跨阶段综合任务，由本课程本地设计，整合连续分布、点估计、区间估计、Bootstrap 与回归推断。
- **数据集来源**：文中「真实世界」数据集（金融延迟 / 厚尾样本）的精确出处与许可证 [待验证]；若无法核验，默认按合成/示例数据对待，不冒充公开数据集成果。
- **本地化适配**：问题定义、数据处理、方法选择、实现、评价与错误分析链路均为本课程本地设计，用于跨阶段综合验收。

## 🎯 学习目标

面向具有显著右偏与厚尾特征的真实世界业务数据集（`data/financial_loss_or_delay_data.csv`，记录 $n=1000$ 笔系统服务延迟与负载特征），构建端到端的数理统计建模与推断系统。涵盖探索性数据分析（EDA）、候选多参数分布族拟合与 AIC/BIC 优选、非参数 BCa Bootstrap 稳健区间估计、多元线性回归 OLS 矩阵推断与残差诊断，输出严谨的统计科学研究报告。

---

## 1. 任务背景与数据集说明

- **数据集路径**：`03-Projects/22-概率论与数理统计/data/financial_loss_or_delay_data.csv`
- **样本容量**：$n = 1000$ 条真实/高保真业务记录
- **变量字典**：
  - `latency_ms`：核心响应变量（服务响应延迟，单位：毫秒，呈现典型右偏厚尾形态）；
  - `request_volume`：每秒并发请求量；
  - `server_load`：服务器 CPU 负载百分比（$0 \sim 100\%$）；
  - `system_tier`：系统部署层级（$1, 2, 3$）；
  - `is_peak_hour`：是否为高峰时段（$0$ 或 $1$）。

---

## 2. 五大核心任务规范

```
真实数据 (data/financial_loss_or_delay_data.csv)
                      │
                      ▼
[模块 1: EDA 与偏态诊断] ──► 均值/方差/偏度/超额峰度、eCDF 与正态 QQ 图
                      │
                      ▼
[模块 2: 多分布 MLE 拟合] ──► 正态 vs 对数正态 vs Gamma (极大似然、AIC/BIC 排序)
                      │
                      ▼
[模块 3: BCa Bootstrap 推断] ──► 95% 极端分位数 (VaR) 置信区间与标准误
                      │
                      ▼
[模块 4: 多元线性回归推断] ──► OLS 系数显著性 t 检验、整体 F 检验与共线性 VIF
                      │
                      ▼
[模块 5: 残差诊断与科学报告] ──► 异方差散点图、JB 正态性检验与统计结论
```

### 任务 1：探索性数据分析（EDA）与非正态性诊断
1. 统计 `latency_ms` 的四阶样本矩（均值、标准差、偏度 Skewness、超额峰度 Kurtosis）；
2. 绘制经验累积分布函数（eCDF）与标准正态 QQ 图；
3. 执行 Shapiro-Wilk 或 Jarque-Bera 正态性假设检验，给出是否拒绝正态总体的统计学判断。

### 任务 2：多候选分布族拟合与信息准则优选
1. 选取正态分布 $\mathcal{N}(\mu, \sigma^2)$、对数正态分布 $\text{Lognormal}(\mu, \sigma^2)$ 与 Gamma 分布 $\text{Gamma}(\alpha, \beta)$ 作为候选分布族；
2. 基于 `scripts/stats_solver.py` 中的 `MLEFitter` 求解各分布的极大似然参数估计；
3. 计算各模型的最大对数似然 $\ell$、赤池信息准则 $\text{AIC} = 2k - 2\ell$ 与贝叶斯信息准则 $\text{BIC} = k\ln n - 2\ell$；
4. 给出最优拟合模型并解释为什么厚尾/偏态模型显著优于经典正态假定。

### 任务 3：非参数 BCa Bootstrap 稳健区间估计
1. 针对服务质量与风控最关注的 **95% 分位数（$95\text{th}$ Percentile / 风险价值 VaR）** 统计量；
2. 实施 $B = 2,000$ 次有放回重抽样，计算百分位数 Bootstrap 置信区间与偏差校正加速（BCa）Bootstrap $95\%$ 置信区间；
3. 比较非参数 Bootstrap 与传统正态参数法（$\bar{X} + 1.645 S$）估计极端分位数的偏差，分析厚尾数据下参数法低估极端风险的机理。

### 任务 4：多元线性回归建模与显著性推断
1. 构建以对数延迟 $\ln(\text{latency})$ 为因变量、以 `request_volume`、`server_load`、`system_tier`、`is_peak_hour` 为自变量的多元回归模型：
   $$\ln(\text{Latency}_i) = \beta_0 + \beta_1 \text{Vol}_i + \beta_2 \text{Load}_i + \beta_3 \text{Tier}_i + \beta_4 \text{Peak}_i + \epsilon_i$$
2. 基于 OLS 解析解求解系数向量 $\hat{\boldsymbol{\beta}}$、标准误 $\text{SE}(\hat{\boldsymbol{\beta}})$、$t$ 统计量及 $p$ 值；
3. 输出判定系数 $R^2$、调整 $R^2$ 与整体模型 $F$ 检验显著性。

### 任务 5：残差诊断与端到端科研报告
1. 绘制残差散点图（Residuals vs Fitted），检查同方差性假定；
2. 计算方差膨胀因子（VIF），检验自变量间是否存在多重共线性；
3. 撰写结构严谨、图文并茂的最终 Markdown 统计分析报告。

---

## 3. 提交产物清单

1. **大作业研究报告**（Markdown 格式，含完整 EDA 结论、多模型 AIC 对比表、Bootstrap 区间与回归解释）；
2. **端到端执行脚本**（Python 源码，调用 `stats_solver.py` 并通过自动化测试）；
3. **图表集**（eCDF 对比图、多分布拟合概率密度曲线、残差诊断散点图）。

---

## 4. 课程大作业 Rubric 评分标准

| 维度 | 分值 | 评审标准 |
| :--- | :---: | :--- |
| **EDA 画像与非正态诊断** | 20 | 完整计算四阶矩、绘制 eCDF 与 QQ 图，严谨执行正态性假设检验 |
| **分布拟合与 AIC/BIC 优选** | 25 | 正确求解多模型对数似然与 Hessian 信息矩阵，利用 AIC/BIC 科学决策 |
| **BCa Bootstrap 稳健推断** | 25 | 重抽样算法正确，准确求解 95% 分位数 BCa 区间，深刻对比参数法缺陷 |
| **多元回归与残差诊断** | 20 | OLS 估计与假设检验完整，残差诊断深入，解释统计学与业务意义 |
| **科学报告与工程交付** | 10 | 代码模块化、具备 100% 通过的 PyTest 用例与专业格式研究报告 |

---

## 5. 引导自检与检查点

- [ ] 真实数据路径配置正确，无硬编码绝对路径导致的跨机器加载失败；
- [ ] 极大似然求解中所有正数参数已设置下界数值保护；
- [ ] 运行 `pytest` 确保 `test_real_world_capstone_dataset_pipeline` 测试用例 100% 通过；
- [ ] 结合业务实际解释各回归自变量系数符号的经济学/工程学意义。

## 6. 关联与导航

- 前置卡片：[[概率统计-连续随机变量与核心分布族]]、[[概率统计-点估计方法：矩估计与极大似然估计]]、[[概率统计-非参数Bootstrap重抽样与置信区间]]、[[概率统计-一元与多元线性回归的推断基础]]
- 返回作业索引：[[🧭 课程作业总索引]]
