---
title: "数据结构与算法-图的存储与BFS-DFS遍历"
type: study
topic: "图的存储与BFS-DFS遍历"
course: "数据结构与算法"
created: 2026-08-06
updated: 2026-08-07
status: completed
upstream:
  - "[[数据结构与算法-内存指针与数据结构底层形态]]"
stage_moc: "[[🧭 阶段4-图论基础]]"
flow: knowledge
kind: concept
difficulty: intermediate
sources:
  - title: "MIT 6.006 Introduction to Algorithms (Spring 2020)"
    url: "https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/"
    locator: "Lecture 11, 12: Breadth-First Search and Depth-First Search"
    source_type: "open-textbook"
    verified_at: "2026-08-07"
concept:
  - "图的表示"
  - "BFS"
  - "DFS"
tags:
  - 学习
  - 数据结构与算法
  - 图论
---

# 数据结构与算法-图的存储与BFS-DFS遍历

> **所属课程**：数据结构与算法  
> **所属阶段**：[[🧭 阶段4-图论基础]]  
> **前置知识**：[[数据结构与算法-内存指针与数据结构底层形态]]

---

## 💡 问题动机与直观解析

图 (Graph) $G = (V, E)$ 是刻画非线性复杂关联关系的最强抽象载体。其中 $V$ 为顶点集，$E$ 为边集。

根据存储结构不同，图主要有两大存在形态：
1. **邻接矩阵 (Adjacency Matrix)**：二维数组 $M[u][v]$。优点是判定边是否存在只需 $\mathcal{O}(1)$；缺点是空间开销为 $\mathcal{O}(|V|^2)$，在稀疏图下空间浪费极其严重。
2. **邻接表 (Adjacency List)**：为每个顶点维护一个相邻节点的列表/向量。空间开销优化至 $\mathcal{O}(|V| + |E|)$，是工程实践中的默认实现。

---

## 📐 两大图遍历范式对比

### 1. 广度优先搜索 (Breadth-First Search, BFS)

使用**队列 (Queue)** 按水波纹层级向外扩散：
- **核心定理**：在所有**无权图 (Unweighted Graph)** 中，BFS 首次到达某个节点时所经过的边数，必为源点到该节点的最短路径！
- 时间复杂度：$\mathcal{O}(|V| + |E|)$。空间复杂度：$\mathcal{O}(|V|)$。

---

### 2. 深度优先搜索 (Depth-First Search, DFS)

使用**递归栈**深入探寻直至尽头再回溯：
- **时间戳与边分类**：DFS 树为图赋予树边 (Tree Edge)、后向边 (Back Edge，指示环路存在)、前向边与横跨边。
- 时间复杂度：$\mathcal{O}(|V| + |E|)$。空间复杂度：$\mathcal{O}(|V|)$。

---

## 💻 经典代码实现 (邻接表 + BFS 最短路)

```python
from collections import deque

def bfs_shortest_path(graph: dict[int, list[int]], start: int, target: int) -> int:
    visited = {start}
    queue = deque([(start, 0)]) # (node, distance)
    
    while queue:
        curr, dist = queue.popleft()
        if curr == target:
            return dist
            
        for neighbor in graph.get(curr, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))
                
    return -1 # 不可达
```

---

## 📝 检索练习与自测题

1. **思考题**：在无向图中，如何利用 DFS 检测是否存在环路？在有向图中，单凭“节点已被访问 `visited[u] == True`”能否证明存在环路？（不能，有向图需记录当前递归调用栈上的 `in_stack` / 节点颜色：白-未访、灰-在栈中、黑-已完成）。

---

## 🃏 Anki 卡片

- Q: 为什么在无权图上 BFS 找到的路径必然是最短路径？
- A: 因为队列保证了按距离递增的层级顺序探索节点，首次入队时记录的距离即为源点到该节点的最短边步数。

---

## 🔗 学完后可以完成

### 🎯 对应实战作业 (点击直达)

```dataview
LIST FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
