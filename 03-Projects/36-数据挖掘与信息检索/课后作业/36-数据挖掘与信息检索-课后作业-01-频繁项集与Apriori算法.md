---
type: project
project_type: homework
course: "数据挖掘与信息检索"
assignment_id: "36-HW-01"
assignment_level: lesson
assignment_format: lab
stage_id: "01"
requires: ["[[关联规则挖掘]]", "[[FP-Growth频繁项集挖掘]]", "[[DGIM算法与流数据计数]]", "[[Flajolet-Martin算法与基数估计]]", "[[数据挖掘概述]]", "[[模式挖掘评估指标]]"]
source_type: official_assignment
source_url: "https://web.stanford.edu/class/cs246/"
created: 2026-08-07
status: completed
flow: project
tags: [作业, 数据挖掘, Stanford-CS246]
---

# 36-数据挖掘与信息检索 - 课后作业 01：频繁项集挖掘、关联规则与流数据估计

> **名校开源出处**：[Stanford CS246: Mining Massive Data Sets - Homework 1](https://web.stanford.edu/class/cs246/)

---

## 🎯 学习目标

1. 手写实现基于先验剪枝原理的 **Apriori 算法** 与基于前缀树压缩的 **FP-Growth 算法**；
2. 准确推导并计算关联规则的 **Support（支持度）**、**Confidence（置信度）** 与 **Lift（提升度）**；
3. 在流数据场景下掌握滑动窗口 **DGIM 算法**（指数桶合并）与 **Flajolet-Martin 算法**（哈希尾随零基数估计）。

---

## 🔒 任务边界与环境约束

- **技术约束**：纯 Python 3 / NumPy 实现，严禁直接调用第三方黑盒库 `mlxtend`；
- **输入数据**：`data/retail_transactions.json` 零售交易事务记录；
- **自动化验收**：必须通过 `pytest tests/test_frequent_itemsets.py` 与 `pytest tests/test_stream_estimation.py`。

---

## 📝 题目详细内容

### 任务 1：Apriori 算法候选生成与先验剪枝（Join & Prune）
给定事务集合 $T$，实现 $L_{k-1} \to C_k \to L_k$ 迭代：
1. **Join 步**：连接两个共享前 $k-2$ 个项的频繁 $(k-1)$-项集；
2. **Prune 步**：验证候选项集的所有 $(k-1)$ 子集是否均在 $L_{k-1}$ 中，剔除非频繁子集；
3. **规则导出**：导出所有满足 $\text{Confidence}(A \to B) \ge \text{min\_conf}$ 且 $\text{Lift}(A \to B) > 1.0$ 的强关联规则。

### 任务 2：FP-Tree 递归条件模式基挖掘
1. 扫描事务两次建立带有项头表（Header Table）与节点链表（Node-Links）的 FP-Tree；
2. 自底向上对每个项提取条件模式基（Conditional Pattern Bases），递归挖掘条件 FP-Tree。

### 任务 3：流数据滑窗统计（DGIM 与 FM 算法）
1. **DGIM**：维护大小为 $2^k$ 的指数桶，任意大小相同的桶数量不得超过 2 个，在超出窗口 $N$ 时弹出过期桶；
2. **Flajolet-Martin**：对流元素应用随机哈希函数，记录二进制尾随零的最大长度 $R = \max \rho(h(x))$，估算基数 $2^R / 0.77351$。

---

## 💻 Starter Code 骨架

```python
from collections import defaultdict
from typing import List, Set, Dict, Tuple, Optional

class FPNode:
    def __init__(self, item: str, count: int, parent: Optional['FPNode']):
        self.item = item
        self.count = count
        self.parent = parent
        self.children: Dict[str, 'FPNode'] = {}
        self.node_link: Optional['FPNode'] = None

class AprioriMiner:
    def __init__(self, transactions: List[Set[str]], min_support_count: int):
        self.transactions = transactions
        self.min_sup = min_support_count
        self.item_counts = defaultdict(int)

    def find_frequent_1_itemsets(self) -> Dict[Tuple[str, ...], int]:
        for t in self.transactions:
            for item in t:
                self.item_counts[(item,)] += 1
        return {k: v for k, v in self.item_counts.items() if v >= self.min_sup}

    def generate_candidate_k(self, l_prev: List[Tuple[str, ...]], k: int) -> List[Tuple[str, ...]]:
        """实现 Join 与 Prune 步"""
        candidates = []
        n = len(l_prev)
        for i in range(n):
            for j in range(i + 1, n):
                t1, t2 = l_prev[i], l_prev[j]
                if t1[:k-2] == t2[:k-2]:
                    c = tuple(sorted(set(t1) | set(t2)))
                    subsets = [c[:idx] + c[idx+1:] for idx in range(len(c))]
                    if all(sub in l_prev for sub in subsets):
                        candidates.append(c)
        return candidates
```

---

## 📐 评分标准 (Rubric)

- **[35%] 核心算法逻辑**：Apriori 剪枝与 FP-Growth 条件模式基构建无 bug；
- **[25%] 规则指标计算**：Support, Confidence, Lift 公式计算精确无误；
- **[25%] 流式估计算法**：DGIM 桶合并逻辑与 Flajolet-Martin 尾随零计算符合理论边界；
- **[15%] 代码规范与测试**：代码模块化，100% 通过 Pytest 单元测试。

---

## 📦 提交产物

1. 源码实现：`hw1_frequent_patterns.py`；
2. 单元测试通过日志：`pytest tests/test_frequent_itemsets.py` 与 `test_stream_estimation.py`。

---

## 💡 引导与自检

- **思考 1**：为什么 FP-Growth 只需要扫描两次数据库？第二次扫描时事务中的项必须按什么顺序插入树？
- **思考 2**：DGIM 在最坏情况下每个时间戳最多触发几次桶合并？时间复杂度是多少？
- **自检**：运行 `pytest tests/test_frequent_itemsets.py` 验证边界用例。
