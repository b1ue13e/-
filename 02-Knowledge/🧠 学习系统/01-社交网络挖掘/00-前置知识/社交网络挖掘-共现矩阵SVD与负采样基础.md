---
type: study
topic: "共现矩阵、SVD 与负采样基础"
course: "社交网络挖掘"
created: 2026-08-07
status: planned
difficulty: intermediate
concept: [共现矩阵, 截断SVD, 负采样]
prerequisites: [矩阵乘法, 概率抽样, Python数组]
flow: knowledge
kind: derivation
stage_moc: "[[🧭 社交网络挖掘-前置知识]]"
upstream: ["[[社交网络挖掘-线性代数与矩阵传播基础]]", "[[社交网络挖掘-概率抽样与随机实验基础]]", "[[社交网络挖掘-Python图数据处理基础]]"]
source: "Local bridge for Hamilton GRL Chapter 3"
source_url: "https://www.cs.mcgill.ca/~wlh/grl_book/"
accessed: 2026-08-07
license: "本地原创桥接卡；GRL 预出版稿仅作章节定位，link-only"
tags: [学习, 社交网络挖掘, 前置知识, SVD, 负采样]
---

# 社交网络挖掘：共现矩阵、SVD 与负采样基础

## 要解决的问题

DeepWalk 和 Node2Vec 会先产生随机游走序列，但“有了序列”还没有得到节点向量。本卡补齐两条最低实现路径：用共现矩阵加截断 SVD 得到可检查的基线，或用正负样本训练 Skip-gram 目标。

本卡只讲到能完成本课程的节点表示实验，不展开完整矩阵分解理论、自然语言处理或大规模优化。

## 从游走窗口到共现矩阵

对节点序列 $(v_1,\ldots,v_T)$ 和窗口半径 $w$，若 $0<\lvert i-j\rvert\le w$，就给共现矩阵增加一次计数：

$$
C_{v_i,v_j}\leftarrow C_{v_i,v_j}+1.
$$

例如序列 `0, 1, 2, 1`、窗口半径 1 会产生有向上下文对 $(0,1),(1,0),(1,2),(2,1),(2,1),(1,2)$。实现时必须说明是否保留方向、是否对称化以及是否对高频节点降权。

## 截断 SVD 基线

对非负共现矩阵 $C\in\mathbb R^{n\times n}$ 做奇异值分解：

$$
C=U\Sigma V^T.
$$

保留最大的 $d$ 个奇异值，节点表示可取

$$
Z=U_{[:,1:d]}\Sigma_{1:d,1:d}^{1/2}.
$$

这是低秩共现基线，不等同于完整 DeepWalk 训练。它的价值是：规模小、确定性强、容易用重构误差和形状断言检查。

## Skip-gram 与负采样

对正上下文对 $(u,v)$，Skip-gram 希望内积 $z_u^Tz'_v$ 较大。负采样再从噪声分布抽取 $K$ 个节点 $n_k$，最小目标可写为

$$
\log\sigma(z_u^Tz'_v)+\sum_{k=1}^{K}\log\sigma(-z_u^Tz'_{n_k}).
$$

- 正样本来自真实游走窗口。
- 负样本不得是同一个窗口里的正上下文。
- 噪声分布、$K$、随机种子和重复样本处理必须写入实验 manifest。
- 测试边必须在生成游走之前从图中移除，否则上下文已经编码答案。

## 可运行最小例

```python
import numpy as np

walks = [[0, 1, 2, 1], [2, 1, 0]]
node_count = 3
window = 1
cooccurrence = np.zeros((node_count, node_count), dtype=float)

for walk in walks:
    for center_index, center in enumerate(walk):
        left = max(0, center_index - window)
        right = min(len(walk), center_index + window + 1)
        for context_index in range(left, right):
            if context_index != center_index:
                cooccurrence[center, walk[context_index]] += 1

u, singular_values, _ = np.linalg.svd(cooccurrence, full_matrices=False)
dimension = 2
embedding = u[:, :dimension] * np.sqrt(singular_values[:dimension])

assert cooccurrence.shape == (3, 3)
assert embedding.shape == (3, 2)
assert np.isfinite(embedding).all()
print(cooccurrence)
print(np.round(embedding, 3))
```

## 常见错误

1. **把节点 ID 当作连续行号。** 先建立稳定的 `node_to_index` 映射。
2. **在完整图上生成游走再切分。** 这会产生结构泄漏。
3. **把 SVD 基线称为 Node2Vec。** Node2Vec 还需要二阶有偏游走；SVD 只负责把共现压缩成低维表示。
4. **负样本中混入正上下文。** 训练目标会同时拉近和推远同一对节点。
5. **只报告最好种子。** 游走和负采样都有随机性，必须保留全部种子。

## 与课程的连接

- [[图表示学习-DeepWalk与Node2Vec]] 使用本卡完成“游走序列到节点向量”的缺口。
- [[链接预测与无泄漏评估]] 决定哪些边可以进入游走图。
- 阶段 6 先跑共现加 SVD，再把 Node2Vec 作为有偏游走改进，避免一上来依赖黑盒库。

## 检索练习与通过标准

1. 给定一条长度 5 的游走，手算窗口半径 1 的全部上下文对。
2. 解释 $U_d\Sigma_d^{1/2}$ 的形状和每一行代表什么。
3. 写出一个正样本、两个负样本的训练目标。
4. 解释为什么切边必须发生在生成游走之前。
5. 修改代码使用窗口半径 2，并断言共现总数增加。

前四项能闭卷完成，并能独立运行修改后的代码，才算通过。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/01-社交网络挖掘"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

