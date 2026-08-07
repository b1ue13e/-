---
type: project
project_type: homework
topic: "VAE与主题模型"
course: "14-概率图模型"
assignment_id: "概率图模型-课后作业-06"
assignment_level: lesson
assignment_format: problem-set
stage_id: "6"
requires:
  - "[[概率图模型-变分自编码器]]"
  - "[[概率图模型-主题模型]]"
  - "[[概率图模型-变分推断与ELBO]]"
  - "[[概率图模型-深度生成模型]]"
source_type: open_textbook_exercise
created: 2026-08-07
updated: 2026-08-07
status: planned
flow: project
kind: project
difficulty: advanced
tags: [作业, 14-概率图模型, VAE, LDA]
---

# 概率图模型 - 课后作业 06：VAE 与主题模型

> 本作业验证阶段 6 的**深度生成模型**紧密知识点：VAE 的 ELBO 与重参数化、LDA 生成过程与变分 EM。以**推导 + 最小实现**为主。

---

## 0. 学习目标

完成后能够证明：

1. 推导 VAE 的 ELBO（重构项 + KL 项）并解释两项作用；
2. 手算高斯 KL 闭式与重参数化采样；
3. 写出 LDA 的生成过程与变分 E 步更新；
4. 说明 VAE/LDA 与阶段 2 变分推断的联系。

---

## 1. 任务背景与边界

- 推导为主，允许最小 Python（numpy）。
- 不要求完整训练 VAE（时间/算力），只需正确推导与手算小例；完整训练属于阶段作业-02 的可选挑战。
- 每题给出推导过程。

---

## 2. 详细题目

### 题 1（VAE 的 ELBO，25 分）

1. 写出 VAE 的 ELBO：$\mathcal{L} = \mathbb{E}_{q_\phi(\mathbf{z}\mid\mathbf{x})}[\log p_\theta(\mathbf{x}\mid\mathbf{z})] - \text{KL}(q_\phi(\mathbf{z}\mid\mathbf{x}) \parallel p(\mathbf{z}))$；
2. 从 $\log p_\theta(\mathbf{x})$ 出发推导该下界（写出关键不等式与 KL 项）；
3. 解释：重构项与 KL 项各起什么作用（生成质量 vs 正则）；
4. 说明：为什么最大化 ELBO 等价于最小化 $\text{KL}(q_\phi \parallel p(\mathbf{z}\mid\mathbf{x}))$。

### 题 2（高斯 KL 与重参数化，25 分）

1. 推导 $\text{KL}(\mathcal{N}(\mu,\sigma^2)\parallel\mathcal{N}(0,1)) = \frac{1}{2}(\mu^2 + \sigma^2 - 1 - \log\sigma^2)$；
2. 手算：$\mu = (0.5, 1.0)$，$\sigma^2 = (2.0, 1.0)$ 的 KL（二维，独立分解）；
3. 重参数化：$\mu=1.0$，$\sigma=0.5$，$\epsilon=0.8$ 时 $\mathbf{z}$ 的值；
4. 解释：为什么重参数化让 ELBO 可对 $\phi$ 求梯度（对比评分函数估计的方差）。

### 题 3（LDA 生成过程，25 分）

1. 写出 LDA 的生成过程（$K$ 主题、$\alpha,\eta$ 先验、每文档/每词步骤）；
2. 写出联合分布 $P(\mathbf{w},\mathbf{z},\theta,\beta\mid\alpha,\eta)$；
3. 说明：为什么后验 $P(\theta,\mathbf{z},\beta\mid\mathbf{w})$ 不可解（词-主题耦合）；
4. 解释：Dirichlet 先验相对 pLDA（无先验）的作用（缓解过拟合）。

### 题 4（LDA 变分 EM，25 分）

1. 写出平均场近似 $q(\theta,\mathbf{z},\beta) = \prod_d q(\theta_d)\prod_{dn}q(z_{dn})\prod_k q(\beta_k)$；
2. 写出变分 E 步的 $\phi_{dnk}$ 更新公式（词-主题责任）；
3. 写出 M 步的 $\beta_{kv}$ 更新（软计数）；
4. 说明：LDA 求解为何是 [[概率图模型-变分EM]] 的实例（E 步变分、M 步全局参数）。

---

## 3. 环境与复现

- **Python**：3.11+；依赖仅 `numpy`；
- 题 2 数值可验证；题 1/3/4 推导；
- 无需随机种子。

---

## 4. 提交产物

1. `answers.md`：4 题推导；
2. `verify.py`（可选）：题 2 的 KL 计算（约 15 行）；
3. 一句"卡点/收获"。

---

## 5. 验收标准与 Rubric

| 维度 | 分值 | 通过要求 |
|:---|---:|:---|
| 题 1 ELBO 推导 | 25 | 下界推导完整（Jensen/分解）、两项解释合理 |
| 题 2 KL + 重参数化 | 25 | KL 闭式推导正确、$\text{KL}=1.279$、重参数化值正确 |
| 题 3 LDA 生成 | 25 | 生成过程/联合分布正确、后验不可解理由合理 |
| 题 4 LDA 变分 EM | 25 | $\phi$ 与 $\beta$ 更新公式正确、与变分 EM 关联清晰 |
| **总计** | **100** | **≥ 75 且题 1 不低于 20** |

---

## 6. 引导与自检

- **检查点 1**：题 1——用 $p(\mathbf{x},\mathbf{z}) = p(\mathbf{z}\mid\mathbf{x})p(\mathbf{x})$ 展开，KL 非负得下界；不要跳过 Jensen 步骤；
- **检查点 2**：题 2——KL 二维 = 两维独立求和；$\log 2 = 0.693$，核对数值；
- **检查点 3**：题 3——后验不可解是因为 $\theta$ 与 $\beta$ 通过 $z$ 耦合（观测词同时依赖两者）；
- **常见错误**：ELBO 把 KL 方向写反（应为 $q\parallel p$）；重参数化把 $\epsilon$ 当参数；LDA 变分 E 步与 M 步混淆；忘记 Dirichlet 先验的作用。
- **提交前清单**：每题有推导；KL 数值核对；$\phi$ 归一化（$\sum_k\phi_{dnk}=1$）。

---

## 7. 知识依赖与后续

- 所需知识见 frontmatter `requires`（阶段 6 VAE/LDA 卡 + 阶段 2 变分推断）；
- 完成后可衔接阶段作业-02 的可选挑战（VAE 实现）与课程 Capstone（若选生成部分）；
- VAE/LDA 的变分推断是阶段 2 [[概率图模型-变分推断算法]] 的落地应用。

---

## 8. 来源

- Kingma & Welling (2014). Auto-encoding variational Bayes. *ICLR* 习题改编。
- Blei, Ng & Jordan (2003). Latent Dirichlet allocation. *JMLR* 习题改编。
- 课程内部整理题（`open_textbook_exercise`）。访问日期：2026-08-07。
