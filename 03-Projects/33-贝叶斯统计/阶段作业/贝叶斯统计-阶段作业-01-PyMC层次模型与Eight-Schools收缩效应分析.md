---
type: project
project_type: homework
course: "贝叶斯统计"
assignment_id: "贝叶斯统计-阶段01"
assignment_level: stage
assignment_format: project
stage_id: "03"
requires:
  - "[[贝叶斯统计-层次模型与部分汇聚收缩机制]]"
  - "[[贝叶斯统计-PyMC概率编程工作流与参数推断]]"
source_type: open_textbook_exercise
created: 2026-08-08
status: ongoing
flow: project
tags: [作业, 阶段作业, 贝叶斯统计, 层次模型, Eight-Schools, PyMC]
---

# 贝叶斯统计-阶段作业-01-PyMC层次模型与Eight-Schools收缩效应分析

> 所属阶段：[[03-层次模型与回归/🧭 阶段3-层次模型与回归|阶段3：层次模型与回归]]

---

## 1. 学习目标与任务定位
1. **完整复现经典 Eight-Schools 层次模型**，掌握部分汇聚（Partial Pooling）的自适应收缩机制；
2. **在实际数据上诊断 Neal's Funnel**，对比中心化与非中心化参数化下的 Divergence 次数；
3. **输出收缩对比森林图与参数后验不确定性报告**。

---

## 2. 任务边界与真实数据源
- **任务规模**：阶段综合实验（`stage` 规模）；
- **数据源路径**：`03-Projects/33-贝叶斯统计/data/eight_schools.csv`；
- **核心实现代码**：`03-Projects/33-贝叶斯统计/scripts/hierarchical_shrinkage.py`；
- **自动化测试代码**：`03-Projects/33-贝叶斯统计/tests/test_hierarchical_shrinkage.py`。

---

## 3. 综合实验任务清单

### 任务 1：解析收缩因子计算
加载 `data/eight_schools.csv`，在给定先验超参数 $\mu = 8.0, \tau = 5.0$ 下：
1. 计算各学校的收缩因子 $B_j = \frac{\sigma_j^2}{\sigma_j^2 + \tau^2}$；
2. 验证测量误差最大的学校 C 与测量误差最小的学校 E 的收缩强度差异。

### 任务 2：中心化 vs 非中心化 MCMC 采样与 Divergence 分析
1. 实现非中心化参数化：$\theta_j = \mu + \tau \cdot \tilde{\theta}_j, \quad \tilde{\theta}_j \sim \mathcal{N}(0, 1)$；
2. 运行 4 条独立链，每条链采样 3000 次；
3. 统计全参数的 $\hat{R}$、Bulk-ESS 与 Divergence 警告次数，证明非中心化能彻底消灭漏斗颈部的采样分歧。

### 任务 3：后验森林图与汇聚效应可视化
1. 绘制各学校原始估计值 $y_j \pm 1\sigma_j$ 与层次后验均值 $\mathbb{E}[\theta_j \mid y] \pm \text{HDI}_{95\%}$ 的对照森林图；
2. 撰写一段给 ETS 考试决策者的统计解释，阐明为什么不能根据原始数据盲目认定学校 A 的辅导效果最顶尖。

---

## 4. 提交产物与代码规范
1. `scripts/hierarchical_shrinkage.py` 中完整的数据加载、解析计算与 MCMC 推断模块；
2. `tests/test_hierarchical_shrinkage.py` 自动化测试通过证据；
3. 包含收缩因子分析与 Divergence 对比的数据科学报告。

---

## 5. 验收标准与 Rubric
- **优秀 (18–20分)**：收缩机理解释深刻，非中心化实现精准，测试全部通过，有效样本量充足且零分歧；
- **合格 (16–17分)**：完成数据读取、收缩计算与基本采样；
- **需改进 (<16分)**：未理解 Neal's Funnel 的几何成因，采样出现严重分歧未作处理。

---

## 6. 引导与自检
- [ ] 检查 `data/eight_schools.csv` 是否成功读取 8 行有效记录；
- [ ] 验证收缩因子 $B_j$ 是否严格在 $(0, 1)$ 之间，且随 $\sigma_j^2$ 增大而单调增大；
- [ ] 运行测试确认：`python -m unittest 03-Projects/33-贝叶斯统计/tests/test_hierarchical_shrinkage.py`。
