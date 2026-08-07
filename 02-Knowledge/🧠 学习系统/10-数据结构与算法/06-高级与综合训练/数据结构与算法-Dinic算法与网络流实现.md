---
type: study
topic: "Dinic算法与网络流实现"
course: "数据结构与算法"
created: 2026-08-07
status: completed
stage_moc: "[[🧭 阶段6-高级与综合训练]]"
flow: knowledge
kind: concept
---

# 数据结构与算法-Dinic算法与网络流实现

> **摘要**：网络流（Network Flow）是图论中的经典问题。Dinic 算法通过构造**分层图（Level Graph）**与**多路增广（Multi-way Augmentation）**结合**当前弧优化（Current-Arc Optimization）**，将最大流的时间复杂度优化至 $O(V^2 E)$，在二分图最大匹配网络中复杂度可达 $O(E \sqrt{V})$。

---

## 1. 💡 核心原理与算法机制

### 1.1 最大流最小割定理 (Max-Flow Min-Cut Theorem)
在一个容量网络 $G=(V, E)$ 中，从源点 $S$ 到汇点 $T$ 的**最大可行流的值严格等于将 $S$ 与 $T$ 分离的最小割的容量和**。

### 1.2 Dinic 算法的三大优化机制
1. **BFS 构造分层图**：从源点 $S$ 运行 BFS，计算每个节点的深度 $\text{level}[u]$。只允许流量沿着 $\text{level}[v] = \text{level}[u] + 1$ 的边推送，防止环路死循环。
2. **DFS 多路增广**：一次 DFS 寻找多条可行增广路，充分利用剩余容量。
3. **当前弧优化 (Current-Arc Optimization)**：记录每个节点当前遍历到的邻接边位置 `cur[u]`，避免重复尝试已经满流或无法推送的边。

---

## 2. 💻 Python 核心实现

```python
from collections import deque

class Edge:
    def __init__(self, to: int, cap: int, flow: int, rev: int):
        self.to = to
        self.cap = cap
        self.flow = flow
        self.rev = rev  # 反向边在邻接表中的索引

class Dinic:
    def __init__(self, n: int):
        self.n = n
        self.graph = [[] for _ in range(n)]
        self.level = [-1] * n
        self.cur = [0] * n

    def add_edge(self, fr: int, to: int, cap: int):
        forward = Edge(to, cap, 0, len(self.graph[to]))
        backward = Edge(fr, 0, 0, len(self.graph[fr]))
        self.graph[fr].append(forward)
        self.graph[to].append(backward)

    def bfs(self, s: int, t: int) -> bool:
        self.level = [-1] * self.n
        self.level[s] = 0
        queue = deque([s])
        
        while queue:
            u = queue.popleft()
            for edge in self.graph[u]:
                if edge.cap - edge.flow > 0 and self.level[edge.to] == -1:
                    self.level[edge.to] = self.level[u] + 1
                    queue.append(edge.to)
                    
        return self.level[t] != -1

    def dfs(self, u: int, t: int, pushed: int) -> int:
        if pushed == 0 or u == t:
            return pushed

        for i in range(self.cur[u], len(self.graph[u])):
            self.cur[u] = i
            edge = self.graph[u][i]
            v = edge.to
            
            if self.level[v] == self.level[u] + 1 and edge.cap - edge.flow > 0:
                tr = self.dfs(v, t, min(pushed, edge.cap - edge.flow))
                if tr == 0:
                    continue
                edge.flow += tr
                self.graph[v][edge.rev].flow -= tr
                return tr

        return 0

    def max_flow(self, s: int, t: int) -> int:
        flow = 0
        while self.bfs(s, t):
            self.cur = [0] * self.n
            while True:
                pushed = self.dfs(s, t, float('inf'))
                if pushed == 0:
                    break
                flow += pushed
        return flow
```

---

## 3. 🃏 Anki 闭卷自测点

- **Q1**: Dinic 算法中反向边（Residual Edge）的作用是什么？为什么反向容量初始值为 0？
- **Q2**: 为什么使用当前弧优化 `cur[u]` 可以大幅度降低 DFS 增广阶段的时间损耗？

---

## 4. 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```


## 🚨 常见误区与边界条件

1. **当前弧优化 (Current Arc Optimization) 遗漏**：DFS 找增广路时，若不使用 `cur[u]` 记录当前遍历到的边，DFS 会重复遍历已经榨干流量的边，导致复杂度退化为 $O(V^2 E)$。
2. **反向边初始流量与索引配对**：网络流建图必须成对添加正向边与反向边，正向边初始容量为 $C$，反向边初始容量为 $0$。边编号必须满足 `edge ^ 1` 为反向边（如 0/1, 2/3）。
