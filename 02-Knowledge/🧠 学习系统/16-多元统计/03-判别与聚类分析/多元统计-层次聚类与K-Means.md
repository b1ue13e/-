---
type: study
topic: "层次聚类与 K-Means"
course: "16-多元统计"
created: 2026-08-09
status: completed
stage_moc: "[[🧭 阶段3-判别与聚类分析]]"
upstream: ["[[多元统计-前置-正定矩阵与谱分解]]"]
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["K-Means", "层次聚类", "Ward方法", "轮廓系数", "距离度量", "硬聚类"]
tags: [学习, 多元统计, 聚类, 无监督学习, 距离度量]
---

# 多元统计-层次聚类与K-Means

## 1. 为什么无监督聚类是探索高维流形的第一步？

当数据缺乏先验类别标签时，聚类的核心目标是将 $n$ 个多维观测划分为 $K$ 个不同的簇 (Clusters)，使得**簇内相似度（距离小）最大化、簇间差异度（距离大）极大化**。

本卡对比两类经典非参数聚类范式：
1. **层次聚类 (Hierarchical Clustering)**：基于自底向上的凝聚 (Agglomerative) 树状图，无需预先指定 $K$；
2. **K-Means 迭代划分聚类**：基于中心点交替优化的局部极大化方法。

---

## 2. 距离度量与聚类准则

### 2.1 簇间距离连元准则

设簇 $A$ 与簇 $B$：
- **最短距离法 (Single Linkage)**：$d(A, B) = \min_{\mathbf{x}_i \in A, \mathbf{x}_j \in B} \|\mathbf{x}_i - \mathbf{x}_j\|$
- **最长距离法 (Complete Linkage)**：$d(A, B) = \max_{\mathbf{x}_i \in A, \mathbf{x}_j \in B} \|\mathbf{x}_i - \mathbf{x}_j\|$
- **类平均法 (Average Linkage)**：$d(A, B) = \frac{1}{|A||B|} \sum_{\mathbf{x}_i \in A} \sum_{\mathbf{x}_j \in B} \|\mathbf{x}_i - \mathbf{x}_j\|$
- **Ward 最小方差法 (Ward's Minimum Variance Method)**：合并使得簇内平方和增加量 $\Delta \text{SSE}$ 最小的两个簇：
  $$\Delta \operatorname{SSE}(A, B) = \frac{|A||B|}{|A| + |B|} \|\bar{\mathbf{x}}_A - \bar{\mathbf{x}}_B\|^2$$

### 2.2 轮廓系数 (Silhouette Coefficient)

评估划分质量的标准指标：对样本 $i$，设 $a(i)$ 为其到同簇内其他点的平均距离（簇内凝聚度），$b(i)$ 为其到最近异簇点的平均距离（簇间分离度）：
$$s(i) = \frac{b(i) - a(i)}{\max(a(i), b(i))} \in [-1, 1]$$
- $s(i) \approx 1$：划分合理；
- $s(i) \approx 0$：处于边界模糊区；
- $s(i) < 0$：错划入邻簇。

---

## 3. Python 实战代码：UCI 葡萄酒数据集 K-Means 与轮廓系数

```python
import sys
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

sys.path.insert(0, r"f:\-\03-Projects\16-多元统计\scripts")
from load_data import load_wine_data

# 1. 加载葡萄酒数据
df_wine = load_wine_data()
X = df_wine.drop(columns=['Cultivar']).values
# 标准化
X_scaled = (X - np.mean(X, axis=0)) / np.std(X, axis=0)

# 2. 运行 K-Means (K=3)
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
labels = kmeans.fit_predict(X_scaled)

score = silhouette_score(X_scaled, labels)
print("=== UCI 葡萄酒数据集 K-Means (K=3) 聚类评估 ===")
print(f"轮廓系数 (Silhouette Score): {score:.4f}")

assert score > 0.25
print("✅ K-Means 聚类与轮廓系数计算通过！")
```

---

## 4. 检索自测练习

1. 证明 Ward 离差平方和增加量公式 $\Delta \operatorname{SSE}(A, B) = \frac{|A||B|}{|A| + |B|} \|\bar{\mathbf{x}}_A - \bar{\mathbf{x}}_B\|^2$。
2. 比较最短距离法与最长距离法在处理长条形/网状流形簇时的优缺点（如链式效应）。

---

## 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
