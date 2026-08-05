---
title: "多元统计 4-Tier 阶梯作业全景规范说明书"
type: project
topic: "多元统计 4-Tier 阶梯作业规范"
course: "多元统计"
created: 2026-08-02
updated: 2026-08-02
status: active
flow: project
kind: moc
tags: [多元统计, 4Tier作业, 阶梯作业, 编程实战, PyTest, STAT505, Johnson]
---

# 📊 多元统计 4-Tier 阶梯作业全景规范说明书 (Penn State STAT 505 & Johnson 范式)

> 本说明书为 **16-多元统计** 路径（基于 Penn State STAT 505 与 Johnson & Wichern《Applied Multivariate Statistical Analysis》）提供严格的 **4-Tier Baseline** 划分标准与测试校验 Harness 规范。

---

## 🧭 4-Tier Baseline 梯队划分原则

```
🟢 L1 - Simple Baseline   │ Scikit-Learn / SciPy / Statsmodels 调包 / 基础描述性统计量与相关矩阵
🟡 L2 - Medium Baseline   │ 多元正态性检验 (Mardia's Test) / 假设检验 (Hotelling's T-squared)
🔴 L3 - Strong Baseline   │ [核心] 不调用高级统计库，从零手撕 主成分分析 (PCA 协方差特征分解) / 典型相关分析 (CCA) / 判别分析 (LDA)
👑 L4 - Boss Baseline     │ 高维统计 (High-Dimensional Statistics) 稀疏协方差估计 / 广义估计方程 (GEE)
```

---

## 🎯 多元统计阶梯作业 4-Tier 细化规格清单

### 1. HW01 - 多元正态分布与推断 (Multivariate Normal & Inference)
- **开源溯源**：Johnson Ch 4-5 / STAT 505 Lec 4-5
- 🟢 **L1**: 生成并可视化二元正态分布的 3D 曲面与等高线 (Contour)。
- 🟡 **L2**: 计算样本均值向量 $\bar{x}$ 与样本协方差矩阵 $S$，验证马哈拉诺比斯距离 (Mahalanobis Distance)。
- 🔴 **L3 (手撕核心)**：**手撕 单样本与双样本 Hotelling's $T^2$ 检验统计量计算，并将其转换为 $F$ 分布求 $p$ 值**。
- 👑 **L4**: 实现稳健协方差估计 (Robust Covariance Estimation, 例如 Minimum Covariance Determinant, MCD)。

### 2. HW02 - 主成分分析与因子分析 (PCA & Factor Analysis)
- **开源溯源**：Johnson Ch 8-9 / STAT 505 Lec 11-12
- 🟢 **L1**: 调用 `sklearn.decomposition.PCA` 提取前两主成分，画出散点图。
- 🟡 **L2**: 绘制碎石图 (Scree Plot) 确定保留的主成分数量，计算方差贡献率。
- 🔴 **L3 (手撕核心)**：**从零手撕 数据中心化、协方差矩阵求解、特征值分解 (Eigendecomposition) 实现的 PCA 降维与逆重构**。
- 👑 **L4**: 实现主成分因子分析 (Principal Component Factor Analysis) 并引入方差最大旋转 (Varimax Rotation)。

### 3. HW03 - 典型相关分析与判别分析 (CCA & Discriminant Analysis)
- **开源溯源**：Johnson Ch 10-11 / STAT 505 Lec 13-14
- 🟢 **L1**: 使用 `sklearn.discriminant_analysis` 运行 LDA 与 QDA 分类。
- 🟡 **L2**: 验证费舍尔线性判别式 (Fisher's Linear Discriminant) 将组间方差与组内方差之比最大化的准则。
- 🔴 **L3 (手撕核心)**：**手撕 典型相关分析 (Canonical Correlation Analysis, CCA) 提取最大化两组变量相关性的线性组合权重向量**。
- 👑 **L4**: 实现带正则化的高维惩罚判别分析 (Penalized LDA)。

### 4. HW04 - 聚类分析与多维尺度分析 (Clustering & MDS)
- **开源溯源**：Johnson Ch 12 / STAT 505 Lec 15
- 🟢 **L1**: 调用 K-Means 进行快速聚类并计算轮廓系数 (Silhouette Score)。
- 🟡 **L2**: 使用 SciPy 构建层次聚类 (Hierarchical Clustering) 的树状图 (Dendrogram)。
- 🔴 **L3 (手撕核心)**：**基于距离矩阵 (Distance Matrix) 从零手撕 经典多维尺度分析 (Classical Multidimensional Scaling, MDS) 恢复相对坐标**。
- 👑 **L4**: 实现非度量多维尺度分析 (Non-metric MDS) 处理序数等级差异度。

---

## 🧪 测试校验 Harness 规范 (`pytest`)

在 `03-Projects/projects-stats/tests/` 目录下运行单元测试：

```bash
pytest 03-Projects/projects-stats/tests/test_hw01_hotelling.py
pytest 03-Projects/projects-stats/tests/test_hw02_pca.py
pytest 03-Projects/projects-stats/tests/test_hw03_cca.py
```
