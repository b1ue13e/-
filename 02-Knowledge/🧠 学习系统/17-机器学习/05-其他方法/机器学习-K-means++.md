---

type: study

topic: "K-means++ (初始化改进)"

course: "机器学习"

created: 2026-08-06

status: ongoing

stage_moc: "[[🧭 阶段5-其他方法]]"

flow: knowledge

kind: concept

upstream: ["[[机器学习-K-means]]"]

source: "周志华《机器学习》第6–10、13–16章"
source_url: "https://book.douban.com/subject/26708119/"
accessed: 2026-08-07
license: "[待验证]"

---



# K-means++



## 为什么学



标准 [[机器学习-K-means]] 随机初始化质心，容易把多个质心放到同一个密集簇里，导致收敛到很差的局部最优、结果对初始化敏感。**K-means++ 用「离已选质心越远越可能被选中」的初始化**，显著提升稳定性与最终聚类质量，且几乎不增加计算成本。



## 算法



1. 随机均匀选第一个质心 `c₁`。

2. 对每个样本 `x`，计算到**最近已选质心**的距离平方 `D(x)² = min_{c∈C} ||x−c||²`。

3. 以概率 `P(x) = D(x)² / Σ_{x'} D(x')²` 选下一个质心。

4. 重复 2–3 直到选满 `k` 个质心。

5. 之后照常执行标准 Lloyd 迭代（分配→更新）。



## 直觉



质心尽量「铺开」——已经覆盖的区域附近不再重复放质心，未覆盖的稀疏/远离区域更可能被选中，从而更接近真实簇分布。



## 最小例子



二维点云有两团：左团密、右团长条。随机初始化可能两个质心都落左团；K-means++ 因右团离左团质心远，会以高概率把第二个质心放到右团长条，初始化即更接近真实结构。



## 常见错误



- 误以为 K-means++ 改变了「分配步骤」或「更新步骤」——它**只改初始化**，后续仍是标准 Lloyd。

- 把 `D(x)²` 当作已选质心数量平均——概率正比于距离平方，不是平均分配。

- 在特征量纲不一致时直接用欧氏距离初始化 → 应先标准化。



## 前后连接



- 前置：[[机器学习-K-means]]（标准 Lloyd 迭代）、[[机器学习-线性代数基础]]（向量距离）

- 对比：[[机器学习-高斯混合模型]]（软分配、可建模椭圆/重叠簇）

- 返回：[[🧭 阶段1-基础概念]]







## 可执行示例（Python）



```python

import numpy as np

from sklearn.cluster import KMeans



rng = np.random.default_rng(0)

A = rng.normal([-2, 0], 0.3, (50, 2))

B = rng.normal([2, 1], 0.3, (50, 2))

X = np.vstack([A, B])



km = KMeans(n_clusters=2, init="k-means++", n_init=5, random_state=0).fit(X)

print("质心:\n", km.cluster_centers_.round(2))

print("前两样本标签:", km.labels_[:2])

```

> 运行环境：Python 3.11+、numpy、scikit-learn；`random_state=0` 保证可复现。观察 K-means++ 初始化即把两个质心分别放到左右两团。



## 检索练习（闭卷自检）



- 用自己的话复述 **K-means++ (初始化改进)** 要解决的问题，并举一個它适用的真实场景。

- 对比 **K-means++ (初始化改进)** 与最相近的概念（如 [[机器学习-K-means]]）的异同，说清各自的适用边界与失败模式。

- 闭卷写出 **K-means++ (初始化改进)** 的关键步骤 / 公式 / 算法要点，再回卡核对；把错处记入 [[机器学习-错题整理]]。

- （可选）用一份玩具数据集把 **K-means++ (初始化改进)** 的核心方法跑通，并记录与 Spine（周志华 / Hands-on ML / MML）结果的差异。

## 学完后可以完成



> 下面由作业 `requires` 自动反查：学完本卡后可完成的课后作业、阶段作业与大作业（单一事实源，不手动维护）。



```dataview

LIST

FROM "03-Projects"

WHERE type = "project" AND contains(map(requires, (r) => r.path), this.file.name)

SORT assignment_level ASC, file.name ASC

```

