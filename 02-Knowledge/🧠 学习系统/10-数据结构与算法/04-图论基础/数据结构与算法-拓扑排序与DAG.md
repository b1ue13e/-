---
title: "数据结构与算法-拓扑排序与DAG"
type: study
topic: "拓扑排序与DAG"
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
    locator: "Lecture 12: Topological Sort and DAGs"
    source_type: "open-textbook"
    verified_at: "2026-08-07"
concept:
  - "拓扑排序"
  - "DAG 有向无环图"
  - "Kahn算法"
  - "入度"
tags:
  - 学习
  - 数据结构与算法
  - 拓扑排序
---

# 数据结构与算法-拓扑排序与DAG

> **所属课程**：数据结构与算法  
> **所属阶段**：[[🧭 阶段4-图论基础]]  
> **前置知识**：[[数据结构与算法-内存指针与数据结构底层形态]]

---

## 💡 问题动机与直观解析

在现实世界中，许多任务之间存在明确的**先修依赖关系**（如大学课程选修顺序、编译器 Makefile/CMake 编译依赖、前端 npm 包依赖打包顺序）。

这类带依赖方向且不存在循环死锁的问题，在图论中抽象为**有向无环图 (DAG, Directed Acyclic Graph)**。

**拓扑排序 (Topological Sort)** 是对 DAG 所有顶点进行线性排序，使得对图中任意有向边 $(u, v)$，$u$ 在序列中均出现在 $v$ 之前。

---

## 📐 算法原理与 Kahn 算法 (基于入度)

### Kahn 算法步骤

1. 统计图中所有顶点的**入度 (Indegree)**。
2. 将所有入度为 `0` 的节点压入**队列**（入度为 0 意味着没有前置依赖，可直接执行）。
3. 循环弹出队头节点 $u$ 加入拓扑序列，并将其所有邻接节点 $v$ 的入度减 1。
4. 若 $v$ 的入度减至 `0`，将其压入队列。
5. 最终若生成的拓扑序列长度等于总节点数 $|V|$，则拓扑排序成功；否则图中**必存在有向环路**！

---

## 💻 Kahn 算法 Python 代码实现

```python
from collections import deque

def topological_sort(n: int, edges: list[tuple[int, int]]) -> list[int]:
    in_degree = [0] * n
    graph = [[] for _ in range(n)]
    
    for u, v in edges:
        graph[u].append(v)
        in_degree[v] += 1
        
    queue = deque([i for i in range(n) if in_degree[i] == 0])
    topo_order = []
    
    while queue:
        u = queue.popleft()
        topo_order.append(u)
        
        for v in graph[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)
                
    if len(topo_order) == n:
        return topo_order
    return [] # 存在有向环，拓扑排序失败
```

---

## 📝 检索练习与自测题

1. **思考题**：DFS 后序遍历的逆序也可以生成拓扑序列。如果图中存在环路，DFS 法如何发现环？（通过访问在当前递归栈上的节点，即灰色节点）。

---

## 🃏 Anki 卡片

- Q: Kahn 算法如何检测有向图中是否存在环路？
- A: 比较最终生成的拓扑序列节点数与图中总节点数 $|V|$。若序列节点数 $< |V|$，说明环上的节点入度永远无法降至 0，存在有向环。

---

## 🔗 学完后可以完成

### 🎯 对应实战作业 (点击直达)

```dataview
LIST FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
