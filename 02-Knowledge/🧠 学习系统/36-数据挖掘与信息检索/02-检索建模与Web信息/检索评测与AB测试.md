---
type: study
topic: "检索评测与AB测试"
course: "数据挖掘与信息检索"
created: 2026-08-07
status: completed
stage_moc: "[[🧭 阶段2-检索建模与Web信息]]"
flow: knowledge
kind: concept
upstream: ["[[分类任务与评估]]", "[[TF-IDF与BM25]]"]
tags: [学习, 数据挖掘与信息检索]
---
## 💡 直觉与动机

在信息检索系统中，"结果好不好"必须量化。**离线评测**告诉我们模型在标注测试集上的质量；**在线 A/B 测试**告诉我们在真实用户流量中的商业价值变化。两者缺一不可：离线指标高但上线 CTR 下降的案例在工业界屡见不鲜。

本卡覆盖检索评测的完整体系：从单查询指标（Precision@K）到系统级指标（MAP、NDCG），再到工业界 A/B 实验统计显著性检验。

---

## 📐 正式定义与关键公式

### 基础概念

对于查询 $q$，检索系统返回排序结果 $[d_1, d_2, \ldots, d_K]$，其中每个文档有**相关性标注** $\text{rel}(d_i) \in \{0, 1\}$（二元）或 $\in \{0, 1, 2, 3\}$（多级）。

### Precision@K 与 Recall@K

$$P@K = \frac{|\{d \in \text{Top-K} : \text{rel}(d) = 1\}|}{K}$$

$$R@K = \frac{|\{d \in \text{Top-K} : \text{rel}(d) = 1\}|}{|\{d : \text{rel}(d) = 1\}|}$$

### 平均精度（AP）与均值平均精度（MAP）

对单个查询 $q$，设相关文档在结果中的位置为 $r_1 < r_2 < \cdots < r_m$：

$$\text{AP}(q) = \frac{1}{|\text{relevant}|} \sum_{k=1}^{m} P@r_k$$

对所有查询取均值：

$$\text{MAP} = \frac{1}{|Q|} \sum_{q \in Q} \text{AP}(q)$$

### 归一化折扣累积增益（NDCG@K）

$$\text{DCG@K} = \sum_{i=1}^{K} \frac{2^{\text{rel}(d_i)} - 1}{\log_2(i+1)}$$

$$\text{NDCG@K} = \frac{\text{DCG@K}}{\text{IDCG@K}}$$

其中 IDCG@K 是理想排序（所有相关文档排在前面）的 DCG 值，NDCG $\in [0, 1]$。

### MRR（Mean Reciprocal Rank）

$$\text{MRR} = \frac{1}{|Q|} \sum_{q \in Q} \frac{1}{\text{rank}_q}$$

$\text{rank}_q$ 是第一个相关文档的位置，适用于问答类场景（只关心第一个正确答案）。

### 在线 A/B 测试显著性检验

对照组（Control，用旧模型）和实验组（Treatment，用新模型）各取 $n$ 个用户，观测指标 $\mu_C$ 和 $\mu_T$：

$$z = \frac{\hat{\mu}_T - \hat{\mu}_C}{\sqrt{\hat{\sigma}^2_C/n_C + \hat{\sigma}^2_T/n_T}}$$

当 $p\text{-value} < 0.05$（即 $|z| > 1.96$），认为实验效果在 95% 置信水平下显著。

---

## 💻 最小 Python 实现

```python
import numpy as np
from scipy import stats

def ndcg_at_k(relevances: list[int], k: int) -> float:
    """计算 NDCG@K（多级相关性标注版本）"""
    r = np.array(relevances[:k], dtype=float)
    discounts = np.log2(np.arange(2, len(r) + 2))  # log2(2), log2(3), ...
    dcg = np.sum((2**r - 1) / discounts)

    # IDCG：将 relevances 降序排列（理想情况）
    ideal_r = np.array(sorted(relevances, reverse=True)[:k], dtype=float)
    idcg = np.sum((2**ideal_r - 1) / discounts[:len(ideal_r)])

    return float(dcg / idcg) if idcg > 0 else 0.0

def average_precision(relevances: list[int]) -> float:
    """计算 AP（二元相关性）"""
    hits, ap = 0, 0.0
    for i, r in enumerate(relevances, 1):
        if r == 1:
            hits += 1
            ap += hits / i
    total_relevant = sum(relevances)
    return ap / total_relevant if total_relevant > 0 else 0.0

def ab_test_significance(control: list, treatment: list, alpha: float = 0.05) -> dict:
    """双样本 t 检验，检验 A/B 实验显著性"""
    t_stat, p_value = stats.ttest_ind(treatment, control)
    return {
        "control_mean": np.mean(control),
        "treatment_mean": np.mean(treatment),
        "relative_lift": (np.mean(treatment) - np.mean(control)) / np.mean(control),
        "p_value": p_value,
        "significant": p_value < alpha
    }

# 示例
relevances = [1, 0, 1, 0, 0, 1, 0, 0, 0, 1]  # 搜索结果 Top-10 的相关性
print(f"NDCG@5:  {ndcg_at_k(relevances, 5):.4f}")
print(f"NDCG@10: {ndcg_at_k(relevances, 10):.4f}")
print(f"AP:      {average_precision(relevances):.4f}")

# A/B 测试显著性
np.random.seed(42)
control   = np.random.normal(0.30, 0.05, 10000).tolist()  # 旧模型 CTR
treatment = np.random.normal(0.32, 0.05, 10000).tolist()  # 新模型 CTR
result = ab_test_significance(control, treatment)
print(f"\nA/B Test: lift={result['relative_lift']:.2%}, p={result['p_value']:.4f}, significant={result['significant']}")
```

---

## ⚠️ 常见误区与避坑指南

1. **MAP 和 NDCG 的适用场景不同**：MAP 要求二元相关性，适用于 TREC 风格的精确信息需求；NDCG 支持多级相关性（0/1/2/3），更适合推荐和商业搜索（用户满意度有不同程度）。

2. **NDCG 的折扣参数选择**：$\log_2(i+1)$ 的折扣会让排名第 10 和第 11 的文档影响差异很小（$\log_2 11 \approx \log_2 12$）。若业务只关心 Top-3，应使用更陡峭的折扣或直接看 NDCG@3。

3. **A/B 测试样本量不够就"结束"**：需要提前计算最小样本量（基于期望 MDE、显著性水平和统计功效 Power=0.8），实验在达到样本量前不应提前终止（Peeking Problem）。

4. **多重检验问题**：同时测试 5 个指标，每个 $\alpha=0.05$，至少一个显著的概率 $= 1 - 0.95^5 \approx 23\%$。应使用 Bonferroni 校正：将 $\alpha$ 除以检验数量。

5. **忽略网络效应（Spillover Effect）**：在推荐场景中，处理组用户的行为会影响对照组（如创作者发现流量下降会改变创作），导致 A/B 结论失效。需要按用户集群（Cluster Randomization）而非个人随机分组。

---

---

## 🔗 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```