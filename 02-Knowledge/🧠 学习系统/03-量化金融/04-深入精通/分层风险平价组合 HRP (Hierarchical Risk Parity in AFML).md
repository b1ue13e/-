---
title: 分层风险平价组合 HRP (Hierarchical Risk Parity in AFML)
type: concept
topic: 分层风险平价组合
created: '{date}'
status: ongoing
difficulty: advanced
course: 量化金融
importance: A
tags: 
concept: []
prerequisites: []
related: []
upstream: 
downstream: 
date: 2026-07-23
---

# 分层风险平价组合 HRP (Hierarchical Risk Parity in AFML)

---

## 0. 先判断它值不值得深挖

**分类：A 类（核心概念，必须深挖）**

**理由：**
分层风险平价算法（Hierarchical Risk Parity, HRP，由 Marcos López de Prado 2016 年发表于 *Journal of Portfolio Management* 并在 AFML 第 16 章系统阐述）被称为现代资产配置领域“对马科维茨均值-方差模型 MPT 的终极超越”。传统的 MPT 和 Risk Parity 需要对高维样本协方差矩阵进行直接求逆（$\Sigma^{-1}$），当资产数量较多或资产间存在强烈相关性时，矩阵会极易陷入病态（Ill-conditioned），导致极度不稳健的权重配置。HRP 结合图论与层次聚类（Hierarchical Clustering），**完全无需对协方差矩阵求逆**，实现了超高稳健性与顶级的实盘 Out-of-Sample 表现。

---

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦：**

假设你正在为一家基金管理包含 100 只股票和债券的资产组合。
你使用传统的马科维茨均值-方差模型或标准风险平价（Risk Parity）计算权重：
当科技板块内部有 10 只股票彼此相关系数高达 0.95 时，协方差矩阵 $\Sigma$ 接近奇异矩阵（Singular Matrix）。
如果你对 $\Sigma$ 强行求逆 $\Sigma^{-1}$，求解器会给出极其荒谬的答案——**要求你给某股票分配 $+500\%$ 的杠杆做多，给相邻股票分配 $-400\%$ 的做空**！当下一期市场稍有波动时，你的组合收益率会直接崩盘。

**以前的方法在哪里卡住：**
1. **强制要求协方差矩阵求逆**：对输入数据微小噪声极其敏感（Error Maximizer）。
2. **忽略资产的分层层级结构 (Hierarchical Structure)**：把“苹果股票”与“微软股票”的关系，和“苹果股票”与“美国国债”的关系同等平铺看待，忽视了资产天然聚类成组的层级关系。

**为什么必须引入分层风险平价 (HRP)：**
使用图论与层次聚类（Single/Complex Linkage），根据协方差矩阵构造距离矩阵，递归生成二叉层次树树状图（Dendrogram），并在树状图的分支上递归施加平滑的逆方差风险分配（Recursive Bisection）。

**它到底解决了哪类问题：**
解决了**高维资产配置中免除矩阵求逆、消除共线性冲击、实现全局顶级样本外风险分散**的问题。

---

## 2. 为什么它重要？它有什么用？

- **体系与大图景**：金融机器学习与资产配置（第三阶段）的顶尖算法，连接数据聚类分析、图论树状图与组合风险管理。
- **量化与实战应用**：
  1. **多资产全能配置 (Multi-Asset Allocation)**：在全球股票、国债、商品、加密货币跨大类资产配置中，HRP 的样本外夏普比率和最大撤回普遍显著击败 MPT 和传统 Risk Parity。
  2. **高维股票池权重分配**：对 500 只成分股进行无求逆稳健权重分配。

---

## 3. 学它之前需要哪些前置知识？

1. **[[相关系数、协方差与资产组合分散化 (Covariance, Correlation & Diversification)|马科维茨均值-方差模型]]**：理解传统均值-方差模型依赖 $\Sigma^{-1}$ 求逆的致命缺点。
2. **[[相关系数、协方差与资产组合分散化 (Covariance, Correlation & Diversification)|相关系数、协方差与分散化]]**：理解相关系数矩阵 $R$ 与协方差矩阵 $\Sigma$。
3. **最小必要背景（欧氏距离矩阵与层次聚类）**：
   > 两个资产 $i$ 和 $j$ 的相关系数为 $\rho_{ij}$，其相关性距离定义为：
   > $$d_{ij} = \sqrt{\frac{1}{2} (1 - \rho_{ij})}$$
   > 若 $\rho_{ij} = 1$，距离 $d_{ij} = 0$（完全相同）；若 $\rho_{ij} = -1$，距离 $d_{ij} = 1$（完全相反）。

---

## 4. 用直觉语言解释它

### 生活类比：大型家族遗产的分层分家产

- 假设一个大家族要分遗产（分配资金权重 $w_i$）：
  - **传统 MPT (马科维茨)** 就像：把全家族 100 个子孙后代全部叫到一个房间里，让他们同时相互辩论争抢财产。如果其中有两个双胞胎兄弟（高度相关资产）吵得不可开交，整个房间直接炸锅失控！
  - **分层风险平价 (HRP)** 就像：**按家族树状图（宗族表）分层递进分家**：
    1. **第一步（大支脉分类）**：先把家产按 50% vs 50% 平分给“大儿子房”和“二儿子房”；
    2. **第二步（小支脉分类）**：大儿子房拿到 50% 后，再在内部按 25% vs 25% 平分给大儿子的两个孩子；
    3. **第三步（逐级递归）**：层层向下递进，直到最底层的每个人。

**HRP 的直觉本质**：
不搞全员混战，先根据亲疏远近画出资产“家族树状图”，然后在树枝节点上层层对半分配风险资本。

«“HRP 就是先把资产按相似度画出一棵二叉树，然后从树根开始向树枝层层递归分配资金。”»

---

## 5. 正式定义、核心公式、符号解释

### 核心定义
**分层风险平价 (Hierarchical Risk Parity, HRP)**：一种基于机器学习无监督聚类的资产配置算法。该算法包含三大步骤：
1. **树状图聚类 (Tree Clustering)**：根据资产相关性距离进行层次聚类，生成资产结构树；
2. **准对角线化 (Quasi-Diagonalization)**：重新排列协方差矩阵的行和列，使相近资产集中在对角线附近；
3. **递归二分分配 (Recursive Bisection)**：在树的每个分支上按逆方差风险平价递归分配权重。

### 核心公式与三大计算步骤

#### 步骤一：构建相关性距离与欧氏距离矩阵
对于相关系数矩阵 $\mathbf{R}$ 中的元素 $\rho_{ij}$，转换距离：
$$d_{ij} = \sqrt{\frac{1}{2}(1 - \rho_{ij})}$$
计算任意两资产向量之间的相对欧氏距离 $\tilde{d}_{ij}$：
$$\tilde{d}_{ij} = \sqrt{\sum_{k=1}^N (d_{ki} - d_{kj})^2}$$
利用层次聚类算法构建树状二叉树。

#### 步骤二：准对角线化 (Quasi-Diagonalization)
将树状图中的叶子节点重新排序，得到新的资产序列 $S = (a_1, a_2, \dots, a_N)$，使相似资产在协方差矩阵中紧密靠拢。

#### 3. 步骤三：递归二分分配 (Recursive Bisection)
对于当前资产子集 $W$，将其等分为左子集 $L$ 与右子集 $R$。
分别计算左右子集的对角化方差 $V_L$ 与 $V_R$：
对于子集 $K \in \{L, R\}$，定义其内部逆方差权重：
$$w_K = \frac{\text{diag}(\boldsymbol{\Sigma}_K)^{-1}}{\text{trace}(\boldsymbol{\Sigma}_K^{-1})}$$
子集整体方差为：
$$V_K = w_K^T \boldsymbol{\Sigma}_K w_K$$
计算分配给左子集的比例系数 $\alpha_L$：

$$\alpha_L = 1 - \frac{V_L}{V_L + V_R} = \frac{V_R}{V_L + V_R}$$

更新权重：$\mathbf{w}_L \leftarrow \mathbf{w}_L \cdot \alpha_L$，$\mathbf{w}_R \leftarrow \mathbf{w}_R \cdot (1 - \alpha_L)$。递归至单个资产。

### 符号解释表

| 符号 | 含义 | 维度/量纲 | 备注 |
| :--- | :--- | :--- | :--- |
| $\mathbf{R}$ | 资产相关系数矩阵 | $N \times N$ | 范围 $[-1, 1]$ |
| $d_{ij}$ | 资产 $i$ 与 $j$ 的相关性距离 | $[0, 1]$ | $\rho=1 \implies d=0$ |
| $V_L, V_R$ | 递归二分中左/右子集的方差 | 标量 | 用于确定两分支分配比例 |
| $\alpha_L$ | 分配给左分支的资金系数 | $[0, 1]$ | **方差越大，分配系数 $\alpha_L$ 越小** |

---

## 6. 推导思路和思想来源

### 为什么 HRP 算法完全不需要对协方差矩阵求逆（$\boldsymbol{\Sigma}^{-1}$）？
1. **求逆的魔咒**：求逆矩阵需要解方程 $\boldsymbol{\Sigma} \mathbf{x} = \mathbf{1}$。只要特征值中存在微小的近零特征值（代表两资产高度相关），其倒数就会变成成千上万，导致权重剧烈震荡。
2. **转念（自顶向下的风险分割）**：
   HRP 在子集内部使用极简的**对角线逆方差权重**（即只取对角线上的单资产方差 $\frac{1}{\sigma_i^2}$），完全忽略了子集内部复杂的非对角协方差求逆！
3. **子集间的协方差由二分保证**：子集与子集之间的相关性已经在第一步通过层次聚类隔离开了。
4. **结果**：HRP 彻底绕过了高维求逆，使得计算复杂度降低为 $O(N \log N)$，运行速度与稳健性无与伦比！

---

## 7. 例子：基础 → 中等 → 实际应用

### 例子 1：基础手算例题（两子集 HRP 递归分配）

**题目**：
假设资产池经聚类切分为两个大类：
- **左子集 $L$（股票类）**：算得子集方差 $V_L = 0.04$
- **右子集 $R$（国债类）**：算得子集方差 $V_R = 0.01$

计算分配给股票类子集 $L$ 与 国债类子集 $R$ 的 HRP 权重比例 $\alpha_L$ 与 $\alpha_R$。

**解答过程**：
1. 计算分配给左子集（股票类）的系数：
   $$\alpha_L = \frac{V_R}{V_L + V_R} = \frac{0.01}{0.04 + 0.01} = \frac{0.01}{0.05} = 0.20 \quad (20\%)$$
2. 计算分配给右子集（国债类）的系数：
   $$\alpha_R = 1 - \alpha_L = 1 - 0.20 = 0.80 \quad (80\%)$$
3. **结论**：由于股票类方差是国债类的 4 倍，HRP 自动给股票类分配 20% 资金，向低风险的国债类分配 80% 资金，完美实现了跨子集的风险平价！

---

### 例子 2：中等例题（三资产 HRP 树状结构递推）

**题目**：
已知 3 只资产：股票 A、股票 B、国债 C。
聚类树结构为：`( (A, B), C )`（即 A 和 B 先聚为左分支，C 为右分支）。
子集方差分别为：$V_A = 0.09, V_B = 0.09$，A 和 B 组合后左分支方差 $V_{AB} = 0.08$；右分支国债 $V_C = 0.02$。
求三只资产最终的 HRP 权重 $w_A, w_B, w_C$。

**解答过程**：
1. **第一层递归（(AB) 与 C）**：
   $$\alpha_{AB} = \frac{V_C}{V_{AB} + V_C} = \frac{0.02}{0.08 + 0.02} = \frac{0.02}{0.10} = 0.20$$
   $$\alpha_C = 1 - 0.20 = 0.80 \implies w_C = 0.80 \quad (80\%)$$
2. **第二层递归（在 AB 内部分配 20% 资金）**：
   A 与 B 方差相等（$0.09$），故在内部按 50% : 50% 对半分配：
   $$w_A = \alpha_{AB} \times 0.50 = 0.20 \times 0.50 = 0.10 \quad (10\%)$$
   $$w_B = \alpha_{AB} \times 0.50 = 0.20 \times 0.50 = 0.10 \quad (10\%)$$
3. **最终权重向量**：$w = [w_A, w_B, w_C] = [10\%, 10\%, 80\%]$。

---

### 例子 3：实际应用（Python 实现 AFML 标准 HRP 分层风险平价算法）

```python
import numpy as np
import pandas as pd
import scipy.cluster.hierarchy as sch

def get_hrp_weights(cov, corr):
    # 1. 步骤一：距离矩阵与层次聚类 (Single Linkage)
    dist = np.sqrt(0.5 * (1 - corr))
    link = sch.linkage(dist, 'single')
    
    # 2. 步骤二：准对角线排序 (Quasi-Diagonalization)
    def get_quasi_diag(link):
        link = link.astype(int)
        sort_idx = pd.Series([link[-1, 0], link[-1, 1]])
        num_items = link[-1, 3]
        while sort_idx.max() >= num_items:
            sort_idx.index = range(0, sort_idx.shape[0] * 2, 2)
            df0 = sort_idx[sort_idx >= num_items]
            i = df0.index
            j = df0.values - num_items
            sort_idx[i] = link[j, 0]
            df1 = pd.Series(link[j, 1], index=i + 1)
            sort_idx = pd.concat([sort_idx, df1]).sort_index()
            sort_idx.index = range(sort_idx.shape[0])
        return sort_idx.tolist()
        
    sort_idx = get_quasi_diag(link)
    sorted_items = cov.columns[sort_idx].tolist()
    
    # 3. 步骤三：递归二分权重分配 (Recursive Bisection)
    def get_cluster_var(cov, items):
        cov_slice = cov.loc[items, items]
        ivp = 1.0 / np.diag(cov_slice)
        ivp /= ivp.sum()
        return np.dot(np.dot(ivp, cov_slice), ivp)

    weights = pd.Series(1.0, index=sorted_items)
    clusters = [sorted_items]
    
    while len(clusters) > 0:
        clusters = [c[i:j] for c in clusters for i, j in ((0, len(c) // 2), (len(c) // 2, len(c))) if len(c) > 1]
        for i in range(0, len(clusters), 2):
            c_left = clusters[i]
            c_right = clusters[i + 1]
            v_left = get_cluster_var(cov, c_left)
            v_right = get_cluster_var(cov, c_right)
            alpha = 1.0 - v_left / (v_left + v_right)
            weights[c_left] *= alpha
            weights[c_right] *= (1.0 - alpha)
            
    return weights

# 模拟 5 只资产
np.random.seed(42)
returns = pd.DataFrame(np.random.normal(0, 0.02, (250, 5)), columns=['Eq1', 'Eq2', 'Bnd1', 'Bnd2', 'Cmd1'])
cov = returns.cov()
corr = returns.corr()

hrp_w = get_hrp_weights(cov, corr)
print("=== HRP 分层风险平价实战分配权重 ===")
print(hrp_w.round(4))
```

---

## 7.5 💥 课本挂载与工业级实战模块 (Textbook Mapping & Production Lab)

### 7.5.1 📚 经典课本章节锚定
- **教材挂载 1**：Marcos López de Prado *《Advances in Financial Machine Learning (AFML)》* 第 16 章 "Asset Allocation" Section 16.4 "Hierarchical Risk Parity (HRP)"。
  - **课本必读重点**：Quasi-Diagonalization 拟对角线化证明、Recursive Bisection 递推公式、与 MPT 样本外 Sharpe 比率对比。
  - **推荐课后代码 Lab**：AFML Chapter 16 Snippet 16.1 ~ 16.4（完整 Python HRP 模块构建）。
- **教材挂载 2**：Marcos López de Prado *《Machine Learning for Asset Manager》* 第 6 章 "Hierarchical Clustering Applications"。
  - **实战挂载重点**：构建 Dendrogram（树状图）可视化资产关联网络。

### 7.5.2 ⚙️ 工业级 Python 最小可运行实战脚手架
（见上方 例子 3 完整代码）

### 7.5.3 ⚠️ 实盘落地“踩坑指南”与回测陷阱
1. **层次聚类 Linkage 方法的选择**：
   层次聚类有 Single Linkage, Complete Linkage, Ward Linkage 等。单联动 (Single Linkage) 容易产生链状结构 (Chaining Effect)。工业界在资产数量极大（如 500 只股票）时，推荐使用 **Ward 或 Ward.D2 聚类** 保持树枝均衡。
2. **忽视绝对方差极小资产的权重暴增**：
   若子集中包含货币市场基金等波动率极接近 0 的资产，$1/V_K$ 会导致其分到 99% 的资金。需要设置**单资产最大权重上限约束 (Max Weight Cap)**。

### 7.5.4 📊 实战性能评估指标体系
- **Out-of-Sample 夏普比率 (OOS Sharpe)**：评估非平稳测试集上的抗风险能力。
- **最大历史撤回 (Max Drawdown)**：评估尾部风险防守。
- **权重条件数 (Condition Number)**：相比求逆模型，HRP 权重条件数降低几个数量级。

### 7.5.5
> 🔓 **作业解锁前置条件**：学完 [[相关系数、协方差与资产组合分散化 (Covariance, Correlation & Diversification)|马科维茨均值-方差模型]] + [[相关系数、协方差与资产组合分散化 (Covariance, Correlation & Diversification)|相关系数、协方差与分散化]] + [[分层风险平价组合 HRP (Hierarchical Risk Parity in AFML)|分层风险平价组合]] 即可正式解锁本 Challenge 实战！
> 💡 **解锁指引**：理解 MPT 协方差矩阵求逆炸裂问题后即可解锁层次聚类树状图递归分配。

 🧪 拓展实验与李宏毅式实战 Challenge 题 (HW10-HRP 层次聚类与免求逆资产配置算法)

本作业参考 **李宏毅 (Hung-yi Lee) 教授 ML 课程作业架构** 设计，设置四个渐进式难度基线 (Baselines)：

- 🟢 **简单基线 (Simple Baseline)**：
  - **任务要求**：根据相关系数矩阵 $\mathbf{R}$ 计算相关性距离矩阵 $d_{ij} = \sqrt{\frac{1}{2}(1 - \rho_{ij})}$。
  - **达标标准**：代码无 Error 跑通，输出基础结果。

- 🟡 **中等基线 (Medium Baseline)**：
  - **任务要求**：使用 `scipy.cluster.hierarchy` 实现 Single Linkage 层次聚类、Quasi-Diagonalization 准对角线排序与 Recursive Bisection 递归分配。
  - **达标标准**：完成核心算法的向量化与参数校准，模型表现达到基线水平。

- 🔴 **强基线 (Strong Baseline)**：
  - **任务要求**：绘制 50 只股票的层次聚类树状图 (Dendrogram)，对比 HRP 与马科维茨 MPT 的样本外 (OOS) 夏普比率与矩阵条件数。
- **达标标准**：使用预先固定的数据、时间切分、基准与成本口径完成样本外比较；改进必须同时报告效应大小、风险变化和失败案例，不设跨数据集通用收益阈值。

- 🟣 **Boss 基线 (Kaggle / 实盘级基线)**：
  - **任务要求**：在固定版本的大类资产池上实现带 Ward.D2 聚类与单资产上限约束的 HRP；与 1/N、MPT 比较样本外收益、回撤、换手、条件数和参数敏感性，不设置跨资产池通用回撤门槛。
- **达标标准**：完成预先注册的过拟合、样本外与压力测试；报告 PBO 的切分方案、不确定性和阈值敏感性，不把单一候选阈值当作跨市场通用上线标准。


## 8. 常见误区和易混概念

### 误区 1：分层风险平价 (HRP) 和传统的风险平价 (Risk Parity) 是同一种东西

错误直觉：“都是风险平价，名字差不多，算法应该也差不多。”  
为什么错：传统 Risk Parity（如 Bridgewater 全天候策略）依然需要解非线性方程求逆协方差矩阵，极易受共线性破坏。HRP 是基于机器学习聚类树的完全无求逆算法。  
正确理解：**HRP 是加入了无监督机器学习树状图的升级版风险平价。**

### 概念对比：马科维茨 MPT vs 传统 Risk Parity vs HRP 分层风险平价

| 维度 | 马科维茨 MPT | 传统 Risk Parity (风险平价) | HRP 分层风险平价 |
| :--- | :--- | :--- | :--- |
| **是否依赖求逆 $\Sigma^{-1}$** | **是**（极不稳定） | **是**（解非线性方程组） | **否（绝对不需要求逆！）** |
| **考虑资产层级结构** | 否（平铺盲目求逆） | 否（平铺相等风险贡献） | **是（建立二叉树分层分配）** |
| **对协方差噪声敏感度** | 极度敏感 (Error Maximizer) | 中等敏感 | **极低（工业级稳健）** |
| **计算复杂度** | $O(N^3)$ | $O(N^2)$ | **$O(N \log N)$（极快）** |

---

## 9. 相关知识点与 Obsidian 双链建议

请帮我建立知识网络。

注意：不要只列链接。每个链接后面必须用一句话说明“为什么要链接”。

上游依赖

- [[相关系数、协方差与资产组合分散化 (Covariance, Correlation & Diversification)|马科维茨均值-方差模型]]：提供基础概念与理论推导支撑。
- [[相关系数、协方差与资产组合分散化 (Covariance, Correlation & Diversification)|相关系数、协方差与分散化]]：提供基础概念与理论推导支撑。

下游延伸

- [[协方差去噪与随机矩阵理论 RMT (Covariance Denoising & Marchenko-Pastur Law in AFML)|协方差去噪与随机矩阵理论]]：进一步延伸拓展该知识点的应用场景与模型构建。
- [[止损与仓位]]：进一步延伸拓展该知识点的应用场景与模型构建。

横向关联

- [[收益率与对数收益率]]：衡量资产收益特性的基础量纲。
- [[实盘风控]]：风险控制与投资组合保护。

应用场景

- [[实盘风控]]：工业级量化策略风控与组合风险度量。


## 10. 闭卷复现任务

1. [ ] 默写 HRP 算法的三大步骤（树状图聚类、准对角线化、递归二分）。
2. [ ] 用“大家族按宗族树状图分遗产”解释 HRP 的直觉。
3. [ ] 写出相关性距离的计算公式 $d_{ij} = \sqrt{\frac{1}{2}(1 - \rho_{ij})}$。
4. [ ] 解释为什么 HRP 算法完全不需要对协方差矩阵求逆（$\Sigma^{-1}$）。
5. [ ] 比较马科维茨 MPT、传统 Risk Parity 与 HRP 的核心差异。

---

## 11. 自测题：5 道

| 题号 | 类型 | 难度 | 考查点 |
| :--- | :--- | :--- | :--- |
| 1 | 概念辨析 | 基础 | HRP 免求逆特性 |
| 2 | 公式运用 | 基础 | 给出左右子集方差 $V_L=0.03, V_R=0.01$ 手算 $\alpha_L$ |
| 3 | 条件判断 | 中等 | 两资产相关系数 $\rho = 1$ 时的距离 $d_{ij}$ |
| 4 | 变式/综合 | 中等 | HRP 准对角线化的几何含义 |
| 5 | 开放/建模 | 较难 | 在包含 500 只股票的高维组合中验证 HRP 相比 MPT 的 OOS 夏普提升 |

---

### 第 1 题：概念辨析（基础）
**题目**：分层风险平价 (HRP) 算法相比传统均值-方差模型 (MPT) 最关键的数学优势是什么？

> [!question]- 答案解析
> **答案**：HRP 完全不需要对协方差矩阵进行求逆操作（$\boldsymbol{\Sigma}^{-1}$），彻底消除了因矩阵病态（Ill-conditioned）导致的最优化求解器数值崩溃与参数敏感性。  
> **Obsidian 标签**：`#自测题/HRP优势`

---

### 第 2 题：公式运用（基础）
**题目**：在递归二分分配中，左子集方差 $V_L = 0.06$，右子集方差 $V_R = 0.02$。求分配给左子集的比例 $\alpha_L$。

> [!question]- 答案解析
> **答案**：
> $\alpha_L = \frac{V_R}{V_L + V_R} = \frac{0.02}{0.06 + 0.02} = \frac{0.02}{0.08} = 0.25 \quad (25\%)$。  
> **Obsidian 标签**：`#自测题/HRP手算`

---

### 第 3 题：条件判断（中等）
**题目**：当资产 $A$ 与资产 $B$ 的相关系数 $\rho_{AB} = -1.0$（完全负相关）时，两者的相关性距离 $d_{AB}$ 为多少？

> [!question]- 答案解析
> **答案**：
> $d_{AB} = \sqrt{\frac{1}{2}(1 - (-1.0))} = \sqrt{\frac{1}{2} \times 2.0} = 1.0$。
> 距离达到最大值 1.0（代表两个资产处于树状图的最远对立两端）。  
> **Obsidian 标签**：`#自测题/相关性距离`

---

### 第 4 题：变式/综合（中等）
**题目**：简述 HRP 步骤二“准对角线化 (Quasi-Diagonalization)”的作用。

> [!question]- 答案解析
> **答案**：
> 准对角线化通过对协方差矩阵的行和列重新排序，使在二叉树中距离相近（相关性高）的资产在矩阵中被强行排列在相邻位置，使协方差矩阵的相似块集中在主对角线附近，便于下一步自顶向下的递归平滑分割。  
> **Obsidian 标签**：`#自测题/准对角线化`

---

### 第 5 题：开放/建模（较难）
**题目**：在实际量化对冲基金中，如何将宏观主观观点（如看好科技股）融入 HRP 纯数量化资产配置框架中？

> [!question]- 答案解析
> **解析**：
> 1. **分层叠加**：在 HRP 算出的纯数量化风险平价基础权重 $w_{HRP}$ 上，建立主观观点因子向量 $\mathbf{v}$。
> 2. **子树调整**：不直接修改底层单股票权重，而是在 HRP 的顶层子树节点（如“科技股子树节点”）上微调递归分配系数 $\alpha_{Tech} \leftarrow \alpha_{Tech} \times (1 + \delta)$。
> 3. **效果**：既保留了 HRP 在底层资产上的绝对防范求逆风险的稳健性，又成功融入了宏观战术资产配置 (TAA) 观点。  
> **Obsidian 标签**：`#自测题/HRP主观融合`

---

## 12. 我的主动回忆区

## 我的闭卷复述

> 不看上文，用自己的话解释这个知识点：

## 我的推导复现

> 不看上文，尝试写出核心公式或推导主线：

## 我的错误与卡点

- 

## 下次复习日期

- [ ] 明天
- [ ] 3 天后
- [ ] 7 天后
- [ ] 14 天后

---

## 13. 给 Obsidian 的归档建议

- **适合文件夹**：`02-Knowledge/🧠 学习系统/03-量化金融/03-策略开发与实战/`
- **建议双链**：[[相关系数、协方差与资产组合分散化 (Covariance, Correlation & Diversification)|马科维茨均值-方差模型]]、[[相关系数、协方差与资产组合分散化 (Covariance, Correlation & Diversification)|相关系数、协方差与分散化]]、[[止损与仓位]]
- **

---

<!-- quant-evidence-v3 -->
## 可定位依据与失效复核

本卡的复核对象是 **分层风险平价组合**，而不是只复述一个公式。对 **分层风险平价组合** 的独立验证重点是：对资产排序、距离定义和链接方法做扰动，检查层次聚类的小变化是否导致权重大跳变。

### 权威来源与定位

1. Markowitz (1952), *Portfolio Selection*, DOI: 10.1111/j.1540-6261.1952.tb01525.x。用于复核“对资产排序、距离定义和链接方法做扰动，检查层次聚类的小变化是否导致权重大跳变”。
2. López de Prado (2016), *Building Diversified Portfolios that Outperform Out of Sample*, DOI: 10.3905/jpm.2016.42.4.059。用于复核“对资产排序、距离定义和链接方法做扰动，检查层次聚类的小变化是否导致权重大跳变”。
3. Campbell、Lo 与 MacKinlay, *The Econometrics of Financial Markets*, Princeton University Press, ISBN 9780691043012, Chapter 5（收益协方差与组合检验）。用于复核“对资产排序、距离定义和链接方法做扰动，检查层次聚类的小变化是否导致权重大跳变”。

### 失效边界与验收协议

- **成立条件**：先写清数据时点、估计窗口、交易摩擦和分布/市场结构假设，再运行模型。
- **反例压力测试**：对资产排序、距离定义和链接方法做扰动，检查层次聚类的小变化是否导致权重大跳变。
- **最小实验**：固定随机种子或冻结原始数据快照，同时保存基线、破坏条件后的对照组、关键中间量与失败日志。
- **通过标准**：结论必须在样本外仍保持方向一致；若成本、延迟、参数扰动或结构突变使结论反转，就把该情形登记为适用边界而不是删除失败结果。
\n\n> ⚔️ **支线实战任务 (Side Quest)**：👉 点击进入 [[[支线任务] HW10-HRP层次聚类]] 刷怪通关！\n