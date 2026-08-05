---
title: "数据结构与算法 4-Tier 阶梯作业全景规范说明书"
type: project
topic: "数据结构与算法 4-Tier 阶梯作业规范"
course: "数据结构与算法"
created: 2026-08-02
updated: 2026-08-02
status: active
flow: project
kind: moc
tags: [数据结构与算法, 4Tier作业, 阶梯作业, 编程实战, PyTest, MIT6006]
---

# 🌲 数据结构与算法 4-Tier 阶梯作业全景规范说明书 (MIT 6.006 & CLRS 范式)

> 本说明书为 **10-数据结构与算法** 路径（基于 OpenDSA 与 MIT 6.006 / CLRS）提供严格的 **4-Tier Baseline** 划分标准与测试校验 Harness 规范。

---

## 🧭 4-Tier Baseline 梯队划分原则

```
🟢 L1 - Simple Baseline   │ LeetCode Easy/Medium 题目求解 / 调用 Python dict/list/heapq 跑通算例
🟡 L2 - Medium Baseline   │ 复杂度分析 (Big-O / Big-Omega) / 递归树主定理 / 可视化数据结构追踪
🔴 L3 - Strong Baseline   │ [核心] 不调用高级数据结构，纯 Python/C++ 从零手撕 AVL树 / 最小堆 / 并查集 / 图算法
👑 L4 - Boss Baseline     │ 摊还分析 (Amortized Analysis) 势能法证明 / 动态规划高级优化 (斜率优化/四边形不等式)
```

---

## 🎯 数据结构与算法阶梯作业 4-Tier 细化规格清单

### 1. HW01 - 动态数组与摊还分析 (Dynamic Arrays & Amortized Analysis)
- **开源溯源**：MIT 6.006 Lecture 2 / CLRS Ch 17
- 🟢 **L1**: 使用 Python `list` 实现动态数组的增删改查。
- 🟡 **L2**: 计算翻倍扩容 (Doubling) 的平均时间复杂度。
- 🔴 **L3 (手撕核心)**：**从零手撕带缩容 (Halving & Resizing) 的 Dynamic Array 结构，确保单次操作摊还时间 $O(1)$ 且无空间浪费陷阱**。
- 👑 **L4**: 使用势能法 (Potential Method $\Phi(D_i) = |2Num - Size|$) 给出严格的摊还复杂度证明。

### 2. HW02 - 树形结构与平衡树 (AVL Tree & Red-Black Tree)
- **开源溯源**：MIT 6.006 Lecture 6 / CLRS Ch 13
- 🟢 **L1**: 实现二叉搜索树 (BST) 的前序、中序、后序遍历。
- 🟡 **L2**: 实现 BST 的节点插入、查找与删除算法。
- 🔴 **L3 (手撕核心)**：**从零手撕自平衡 AVL 树（包含单旋 Left-Rotate / Right-Rotate 与双旋 LR-Rotate / RL-Rotate 及树高平衡因子维护）**。
- 👑 **L4**: 实现红黑树 (Red-Black Tree) 插入修复 (Fixup) 逻辑。

### 3. HW03 - 优先队列与二叉堆 (Min-Heap & Priority Queue)
- **开源溯源**：MIT 6.006 Lecture 4 / CLRS Ch 6
- 🟢 **L1**: 使用 Python `heapq` 求解前 K 个高频元素。
- 🟡 **L2**: 实现 $O(N)$ 建堆算法 (Build-Min-Heap)。
- 🔴 **L3 (手撕核心)**：**从零手撕 MinHeap 算法（包含 `heapify_up`, `heapify_down`, `extract_min` 与任意节点 `decrease_key`）**。
- 👑 **L4**: 实现 斐波那契堆 (Fibonacci Heap) 的 $O(1)$ 摊还 `decrease_key`。

### 4. HW04 - 图算法：最短路径与最小生成树 (Shortest Path & MST)
- **开源溯源**：MIT 6.006 Lecture 9-12 / CLRS Ch 23 & 24
- 🟢 **L1**: 使用 NetworkX 跑通 BFS / DFS 遍历与 Dijkstra 最短路径。
- 🟡 **L2**: 实现 Bellman-Ford 负权边最短路径算法与负环 (Negative Cycle) 判定。
- 🔴 **L3 (手撕核心)**：**手撕带路径压缩 (Path Compression) 与按秩合并 (Union-by-Rank) 的并查集 (Disjoint Set) 及 Kruskal / Prim 最小生成树算法**。
- 👑 **L4**: 实现 Dynamic All-Pairs Shortest Path (Floyd-Warshall 矩乘优化)。

### 5. HW05 - 动态规划与记忆化搜索 (Dynamic Programming)
- **开源溯源**：MIT 6.006 Lecture 15-18 / CLRS Ch 15
- 🟢 **L1**: 求解最长公共子序列 (LCS) 与 0-1 背包问题。
- 🟡 **L2**: 画出 DP 状态转移 DAG 图，比较自顶向下记忆化搜索与自底向上 DP 表。
- 🔴 **L3 (手撕核心)**：**手撕编辑距离 (Edit Distance / Levenshtein Distance) 与最长递增子序列 (LIS) $O(N \log N)$ 二分优化算法**。
- 👑 **L4**: 实现斜率优化 DP (Convex Hull Trick / Monotone Queue Optimization)。

---

## 🧪 测试校验 Harness 规范 (`pytest`)

在 `03-Projects/projects-dsa/tests/` 目录下运行单元测试：

```bash
pytest 03-Projects/projects-dsa/tests/test_hw02_avl.py
pytest 03-Projects/projects-dsa/tests/test_hw03_heap.py
pytest 03-Projects/projects-dsa/tests/test_hw04_mst.py
```
