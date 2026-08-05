---
title: "概率图模型 4-Tier 阶梯作业全景规范说明书"
type: project
topic: "概率图模型 4-Tier 阶梯作业规范"
course: "概率图模型"
created: 2026-08-02
updated: 2026-08-02
status: active
flow: project
kind: moc
tags: [概率图模型, 4Tier作业, 阶梯作业, 编程实战, PyTest, CS228, Koller]
---

# 🎲 概率图模型 4-Tier 阶梯作业全景规范说明书 (Stanford CS228 & Koller 范式)

> 本说明书为 **14-概率图模型** 路径（基于 Daphne Koller《Probabilistic Graphical Models》与 Stanford CS228）提供严格的 **4-Tier Baseline** 划分标准与测试校验 Harness 规范。

---

## 🧭 4-Tier Baseline 梯队划分原则

```
🟢 L1 - Simple Baseline   │ pgmpy 调包构建贝叶斯网络与马尔可夫网 / D-分离判断
🟡 L2 - Medium Baseline   │ 变量消除算法 (Variable Elimination) / 朴素贝叶斯与隐马尔可夫 (HMM) 参数学习
🔴 L3 - Strong Baseline   │ [核心] 不调用 pgmpy，从零手撕 信念传播 (Belief Propagation, 团树算法) / 吉布斯采样 (Gibbs Sampling)
👑 L4 - Boss Baseline     │ 变分推理 (Variational Inference, Mean Field) / 结构学习 (PC 算法，因果发现)
```

---

## 🎯 概率图模型阶梯作业 4-Tier 细化规格清单

### 1. HW01 - 贝叶斯网络与独立性 (Bayesian Networks & D-Separation)
- **开源溯源**：Koller Ch 2-3 / CS228 HW1
- 🟢 **L1**: 在 `pgmpy` 中定义一个医疗诊断贝叶斯网络 (如 Student Network)，并填入条件概率表 (CPD)。
- 🟡 **L2**: 编写递归算法在图中检查两组变量在给定观测变量下是否满足 D-分离 (D-Separation)。
- 🔴 **L3 (手撕核心)**：**手撕 变量消除算法 (Variable Elimination, VE)**，包括因子 (Factor) 的相乘 (Multiplication) 与边缘化 (Marginalization) 操作。
- 👑 **L4**: 实现启发式最小化诱导宽度 (Induced Width) 的消元顺序搜索算法。

### 2. HW02 - 马尔可夫随机场与精确推断 (Markov Networks & Exact Inference)
- **开源溯源**：Koller Ch 4, 9-10 / CS228 HW2
- 🟢 **L1**: 在图像去噪任务中，构建一个网格图 (Grid Graph) 的马尔可夫随机场 (Ising Model)。
- 🟡 **L2**: 实现条件随机场 (Conditional Random Field, CRF) 序列标注任务的基础特征函数设计。
- 🔴 **L3 (手撕核心)**：**从零手撕 团树 / 联结树算法 (Junction Tree Algorithm) 中的信念传播 (Belief Propagation) 消息传递机制 (Sum-Product & Max-Product 算法)**。
- 👑 **L4**: 实现 Loopy Belief Propagation (LBP) 处理带环图的近似推断。

### 3. HW03 - 采样与近似推断 (Sampling & Approximate Inference)
- **开源溯源**：Koller Ch 12 / CS228 HW3
- 🟢 **L1**: 实现前向采样 (Forward Sampling) 与拒绝采样 (Rejection Sampling) 估计后验概率。
- 🟡 **L2**: 比较似然加权采样 (Likelihood Weighting) 与重要性采样 (Importance Sampling) 在稀有事件上的方差差异。
- 🔴 **L3 (手撕核心)**：**手撕 吉布斯采样 (Gibbs Sampling) 与 Metropolis-Hastings (MCMC) 算法**，通过构建马尔可夫链稳态分布进行后验估计。
- 👑 **L4**: 实现 粒子滤波 (Particle Filtering) 解决动态非线性系统的时间序列追踪。

### 4. HW04 - 学习：参数估计与结构学习 (Learning: Parameters & Structure)
- **开源溯源**：Koller Ch 16-19 / CS228 HW4
- 🟢 **L1**: 基于完整数据集，使用最大似然估计 (MLE) 与拉普拉斯平滑计算贝叶斯网络 CPD。
- 🟡 **L2**: 在带缺失值的数据集上运行期望最大化算法 (Expectation-Maximization, EM)。
- 🔴 **L3 (手撕核心)**：**基于 Chow-Liu 算法 (最大生成树) 手撕树型结构的自动学习，以及基于互信息 (Mutual Information) 评分的贪心搜索**。
- 👑 **L4**: 手撕 PC 算法 (基于条件独立性测试 Constraint-based) 进行有向无环图 (DAG) 的因果结构发现 (Causal Discovery)。

---

## 🧪 测试校验 Harness 规范 (`pytest`)

在 `03-Projects/projects-pgm/tests/` 目录下运行单元测试：

```bash
pytest 03-Projects/projects-pgm/tests/test_hw01_variable_elimination.py
pytest 03-Projects/projects-pgm/tests/test_hw02_belief_propagation.py
pytest 03-Projects/projects-pgm/tests/test_hw03_gibbs_sampling.py
```
