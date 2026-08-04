---
title: "数据挖掘与信息检索-题型-LSH近邻查找与FP-Growth阶梯作业"
type: problem-type
kind: problem-type
flow: knowledge
topic: "数据挖掘与信息检索作业"
course: "36-数据挖掘与信息检索"
created: 2026-07-29
updated: 2026-07-29
date: 2026-07-29
status: learning
difficulty: advanced
importance: A
concept: ["数据挖掘", "BM25", "LSH", "FP-Growth"]
prerequisites: ["[[02-Knowledge/🧠 学习系统/10-数据结构与算法/🗺️ 数据结构与算法学习路径|数据结构]]"]
related: ["[[社交网络挖掘-题型-PageRank与Louvain社区发现阶梯作业]]"]
upstream: ["[[36-数据挖掘与信息检索/🗺️ 横向知识地图|数据挖掘与信息检索学习路径]]"]
downstream: []
tags: [学习, 36-数据挖掘与信息检索, 作业, 实战, 阶梯作业]
aliases: ["CS246-HW01-LSH与FPGrowth作业"]
---

# 数据挖掘与信息检索 - HW01：LSH 近邻查找与 FP-Growth 阶梯作业

> 🎯 **作业目标**：手写倒排索引与 BM25 计算、实现 MinHash + 局部敏感哈希 (LSH)，以及 FP-Growth 频繁项集挖掘算法。

---

## 1. ⚙️ 环境与 Starter Code 准备
- **Starter Code 路径**：`03-Projects/projects-ir/hw01_lsh_fpgrowth.ipynb`
- **开源标杆仓库**：[Stanford CS246 Mining Massive Datasets](https://web.stanford.edu/class/cs246/)
- **核心依赖**：`pyspark`, `numpy`, `scikit-learn`, `pytest`

---

## 2. 🎯 阶梯式 Baseline / 难度设计 (4-Tier Difficulty)

| 梯度级别 | 目标 / 验证标准 | 关键实现细节与要求 |
| :--- | :--- | :--- |
| 🟢 **L1 - Simple Baseline** | BM25 检索得分正确 | 手写文本分词与倒排索引构建，计算词频与 BM25 检索得分。 |
| 🟡 **L2 - Medium Baseline** | 查全率 Recall ≥ 85% | **实现 MinHash 签名矩阵与 LSH (局部敏感哈希)** 分桶算法，解决海量文本近邻查找。 |
| 🔴 **L3 - Strong Baseline** | 无需候选生成 | **手撕 FP-Growth 算法**：构建 FP-Tree 树结构与递归频繁模式挖掘。 |
| 👑 **L4 - Boss Baseline** | 分布式运行通过 | 在 PySpark 上构建支持分布式 MapReduce 计算的海量文档搜索引擎索引与检索管道。 |

---

## 3. 🧪 自动化测试 Harness (PyTest Validation)

```python
import pytest
import numpy as np

def test_minhash_jaccard_estimation():
    from ir_solvers import minhash_jaccard
    # 两集合交集 50, 并集 100 => 真实 Jaccard 相似度 0.5
    set1 = set(range(50)) | set(range(50, 100))
    set2 = set(range(50)) | set(range(100, 150))
    
    est_jaccard = minhash_jaccard(set1, set2, num_hashes=200)
    assert np.isclose(est_jaccard, 0.5, atol=0.08), "MinHash 估算出的 Jaccard 相似度必须接近真值 0.5"
```

---

## 🃏 Anki 卡片

- Q: 局部敏感哈希 (LSH) 中为何要将 MinHash 签名矩阵划分为 $b$ 个 Band、每个 Band 包含 $r$ 行？其 S 曲线 (S-curve) 过滤概率公式是什么？
- A: 分组技术可以将相似度比较从全量对比转为分桶对比。两个 Jaccard 相似度为 $s$ 的文档在至少一个 Band 中完全相同的概率为 $P = 1 - (1 - s^r)^b$。该 S 曲线能够将高相似度文档以极高概率分入同一桶，同时过滤低相似度文档。
