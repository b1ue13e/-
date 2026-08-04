---
title: "主线-概率统计与数据建模"
type: moc
kind: moc
flow: knowledge
track: "概率统计与数据建模"
status: active
created: 2026-07-30
updated: 2026-07-30
tags:
  - MOC
  - 主线
  - 概率统计
  - 数据建模
  - 知识网络
---

# 🎲 主线：概率统计与数据建模 (Probability, Statistics & Data Modeling Track)

> 🧭 **主线宗旨**：构建从概率论基础、随机过程到多元统计、回归分析与贝叶斯推断的完整统计建模体系。消除统计推断与数据分析中的概念冗余，为机器学习、数据挖掘与量化建模提供坚实的概率不确定性推断底座。

---

## 🗺️ 7 门子线路径逻辑递进图

```mermaid
flowchart TD
    subgraph 概率与随机过程基石
        P0["[[🗺️ 概率论与数理统计学习路径\|22-概率论与数理统计]]<br/>(随机变量, 大数定律, 中心极限定理)"]
        P0 --> P1["[[🗺️ 随机过程学习路径\|24-随机过程]]<br/>(Markov 链, Poisson 过程, 鞅)"]
    end

    subgraph 经典统计建模
        P0 --> S1["[[🗺️ 应用回归分析学习路径\|30-应用回归分析]]<br/>(OLS, 诊断, 多重共线性, GLM)"]
        S1 --> S2["[[🗺️ 多元统计学习路径|16-多元统计]]<br/>(PCA, 因子分析, MANOVA, 聚类)"]
        S1 --> S3["[[🗺️ 属性数据分析学习路径\|31-属性数据分析]]<br/>(Logistic 回归, 列联表, Poisson 回归)"]
    end

    subgraph 现代扩展与贝叶斯推断
        P0 --> E1["[[🗺️ 非参数统计学习路径\|32-非参数统计]]<br/>(Wilcoxon 检验, 核密度估计, Bootstrap)"]
        P0 & P1 --> E2["[[🗺️ 贝叶斯统计学习路径\|33-贝叶斯统计]]<br/>(先验/后验, MCMC, Gibbs 采样, Variational)"]
    end
```

---

## 🔑 全库唯一 Master 概念卡

所有概率定理、参数估计与检验方法统一收拢至基础统计路径中的 Master 主卡：

1. **极大似然估计与 Log-Likelihood**：[[极大似然估计MLE]] ($\hat{\theta}_{\text{MLE}} = \arg\max_\theta \sum \log p(x_i | \theta)$)
2. **中心极限定理与渐近正态性**：[[中心极限定理CLT]] ($\sqrt{n}(\bar{X}_n - \mu) \xrightarrow{d} \mathcal{N}(0, \sigma^2)$)
3. **马尔可夫链平稳分布**：[[Markov链与平稳分布]] ($\boldsymbol{\pi} \mathbf{P} = \boldsymbol{\pi}$)
4. **主成分分析与特征分解**：[[主成分分析PCA]] ($\mathbf{\Sigma} \mathbf{v}_i = \lambda_i \mathbf{v}_i$)
5. **贝叶斯定理与共轭先验**：[[贝叶斯定理与后验分布]] ($p(\theta | x) \propto p(x | \theta) p(\theta)$)

---

## 📊 包含子路径看板 (Dataview)

```dataview
TABLE course AS "课程名称", status AS "状态", importance AS "优先级", updated AS "最近更新"
FROM "02-Knowledge/🧠 学习系统"
WHERE type = "index" AND track = "概率统计与数据建模"
SORT file.name ASC
```

---

*主线更新时间：2026-07-30 | 状态：active*
