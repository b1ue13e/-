---
title: "数据结构与算法-树形DP与状压DP"
type: study
topic: "树形DP与状压DP"
course: "数据结构与算法"
created: 2026-08-06
updated: 2026-08-07
status: completed
upstream:
  - "[[数据结构与算法-动态规划基础与背包问题]]"
stage_moc: "[[🧭 阶段5-算法思想进阶]]"
flow: knowledge
kind: concept
difficulty: advanced
sources:
  - title: "MIT 6.006 Introduction to Algorithms (Spring 2020)"
    url: "https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/"
    locator: "Advanced DP: Tree DP and Bitmask DP"
    source_type: "open-textbook"
    verified_at: "2026-08-07"
concept:
  - "树形DP"
  - "状压DP"
  - "状态压缩"
tags:
  - 学习
  - 数据结构与算法
  - 高级DP
---

# 数据结构与算法-树形DP与状压DP

> **所属课程**：数据结构与算法  
> **所属阶段**：[[🧭 阶段5-算法思想进阶]]  
> **前置知识**：[[数据结构与算法-动态规划基础与背包问题]]

---

## 💡 问题动机与直观解析

当 DP 问题的拓扑结构超越简单的线性或二维网格时，衍生出两大高阶动态规划分支：
1. **树形 DP (Tree DP)**：以树形结构为决策拓扑，通常结合 DFS 后序遍历，在子树解汇总的基础上求解根节点解（如树的最大独立集、树的直径、打家劫舍 III）。
2. **状压 DP (Bitmask DP)**：当集合选择状态较小（通常 $n \le 20$）时，将一个包含 $n$ 个元素的选中/不选中布尔集合打包压缩为一个**二进制整数 $mask \in [0, 2^n - 1]$**，利用极快的高性能位运算实现状态转移（如旅行商问题 TSP、蒙德里安的梦想）。

---

## 📐 状压 DP 位运算常用技巧

设二进制整数 $mask$ 代表当前状态：
- **检查第 $i$ 位是否为 1**：`(mask >> i) & 1`
- **将第 $i$ 位置为 1**：`mask | (1 << i)`
- **将第 $i$ 位置为 0**：`mask & ~(1 << i)`
- **反转第 $i$ 位**：`mask ^ (1 << i)`
- **枚举 $mask$ 的所有子集**：
  ```python
  sub = mask
  while sub > 0:
      # 处理子集 sub
      sub = (sub - 1) & mask
  ```

---

## 💻 经典代码实现 (状压 DP 解决 TSP 问题 $\mathcal{O}(n^2 2^n)$)

求解经过 $n$ 个城市且每个城市恰好访问一次的最短回路（起始点为城市 0）。

```python
def tsp(graph: list[list[int]]) -> int:
    n = len(graph)
    # dp[mask][u]: 已经访问过的城市集合为 mask，且当前位于城市 u 的最小开销
    INF = float('inf')
    dp = [[INF] * n for _ in range(1 << n)]
    dp[1][0] = 0 # 初始起点：城市 0，mask = 000...001
    
    for mask in range(1 << n):
        for u in range(n):
            if dp[mask][u] == INF:
                continue
            if not (mask & (1 << u)):
                continue
                
            # 尝试前往下一个未访问城市 v
            for v in range(n):
                if not (mask & (1 << v)):
                    next_mask = mask | (1 << v)
                    dp[next_mask][v] = min(dp[next_mask][v], dp[mask][u] + graph[u][v])
                    
    # 最终回到城市 0
    full_mask = (1 << n) - 1
    res = min(dp[full_mask][u] + graph[u][0] for u in range(1, n))
    return res
```

---

## 📝 检索练习与自测题

1. **思考题**：在树形 DP 中，为什么通常选用 **DFS 后序遍历**？（后序遍历保证在处理当前节点 $u$ 的 DP 状态前，其所有子树节点的 DP 状态均已被计算完毕）。

---

## 🃏 Anki 卡片

- Q: 状压 DP 中如何优雅高效地枚举二进制掩码 `mask` 的所有非空子集？
- A: 使用位运算循环：`sub = mask; while sub > 0: sub = (sub - 1) & mask`。

---

## 🔗 学完后可以完成

### 🎯 对应实战作业 (点击直达)

```dataview
LIST FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
