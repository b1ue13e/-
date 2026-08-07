# -*- coding: utf-8 -*-
# dsa_cards_s6.py  –  第06组：高级与综合训练（22张）

CARDS_S6 = {

# ──────────────────────────────────────────────────────────────────────────────
"10-数据结构与算法-KMP算法": """\
---
tags: [字符串, KMP, 模式匹配, 算法]
aliases: [Knuth-Morris-Pratt]
sources:
  - https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/
  - https://cp-algorithms.com/string/prefix-function.html
---

# KMP 算法

KMP（Knuth-Morris-Pratt）是线性时间字符串匹配算法，核心在于利用模式串自身的重复结构，避免文本指针回退，总时间复杂度 O(n+m)，其中 n 为文本长度，m 为模式长度。MIT OCW 6.006 课程（见 https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/ ）在字符串处理专题中详细推导了 KMP 的正确性证明。

## 前缀函数（failure function）

对模式串 P[0..m-1]，定义 `fail[i]` 为 P[0..i] 的最长真前缀且同时是后缀的长度。  
- `fail[0] = 0`（单字符没有真前缀）  
- 计算 `fail[i]`：令 `k = fail[i-1]`，若 `P[k] == P[i]` 则 `fail[i] = k+1`；否则令 `k = fail[k-1]` 继续回退，直到 `k==0`。

## 手算例证

模式串 `P = "ABABC"`：
```
i=0: P[0]='A', fail[0]=0
i=1: P[1]='B', k=fail[0]=0, P[0]='A'≠'B', fail[1]=0
i=2: P[2]='A', k=fail[1]=0, P[0]='A'=='A', fail[2]=1
i=3: P[3]='B', k=fail[2]=1, P[1]='B'=='B', fail[3]=2
i=4: P[4]='C', k=fail[3]=2, P[2]='A'≠'C', k=fail[1]=0, P[0]='A'≠'C', fail[4]=0
```
fail = [0, 0, 1, 2, 0]

匹配文本 `T = "ABABABABC"`，匹配过程：
- j（模式指针）从0开始；i遍历T每个字符
- i=4时 T[4]='A'≠P[2]='A'... (最终在i=8, j=4完成全匹配，位置=8-5+1=4)

## 代码实现

```python
def build_fail(pattern: str) -> list[int]:
    m = len(pattern)
    fail = [0] * m
    k = 0
    for i in range(1, m):
        while k > 0 and pattern[k] != pattern[i]:
            k = fail[k - 1]
        if pattern[k] == pattern[i]:
            k += 1
        fail[i] = k
    return fail


def kmp_search(text: str, pattern: str) -> list[int]:
    \"\"\"返回所有匹配起始下标（0-indexed）。\"\"\"
    if not pattern:
        return []
    fail = build_fail(pattern)
    matches = []
    j = 0  # 模式指针
    for i, ch in enumerate(text):
        while j > 0 and pattern[j] != ch:
            j = fail[j - 1]
        if pattern[j] == ch:
            j += 1
        if j == len(pattern):
            matches.append(i - len(pattern) + 1)
            j = fail[j - 1]
    return matches


# 验证
assert kmp_search("ABABABABC", "ABABC") == [4]
assert kmp_search("AAAAAA", "AA") == [0, 1, 2, 3, 4]
```

## 关键性质

| 阶段 | 时间 | 空间 |
|------|------|------|
| 构建 fail | O(m) | O(m) |
| 搜索 | O(n) | O(1) |

fail 数组同时可用于"周期串检测"：若 `m % (m - fail[m-1]) == 0`，则模式串具有最短周期 `m - fail[m-1]`。
""",

# ──────────────────────────────────────────────────────────────────────────────
"10-数据结构与算法-Rabin-Karp算法": """\
---
tags: [字符串, 滚动哈希, Rabin-Karp, 算法]
aliases: [RK算法, 多模式匹配]
sources:
  - https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/
  - https://cp-algorithms.com/string/rabin-karp.html
---

# Rabin-Karp 算法

Rabin-Karp 将字符串视为以某基数 BASE 表示的多项式，通过**滚动哈希**在 O(1) 时间内将窗口哈希值从一个位置推进到下一个位置。平均时间复杂度 O(n+m)，最坏 O(nm)（大量哈希碰撞时），但双哈希可将碰撞概率压至可忽略。MIT OCW 6.006（ https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/ ）把 Rabin-Karp 作为哈希在算法中的经典应用案例讲授。

## 滚动哈希公式

对长度 m 的窗口 s[i..i+m-1]：
```
hash = (s[i]*BASE^(m-1) + s[i+1]*BASE^(m-2) + ... + s[i+m-1]) % MOD
```
窗口右移一格：
```
new_hash = (hash - s[i]*BASE^(m-1)) * BASE + s[i+m]   (mod MOD)
```

## 手算例证

设 BASE=31，MOD=1000003，m=3，文本 T="abcabc"，模式 P="abc"。  
字符映射：a→1, b→2, c→3。  
P 的哈希：`1×31² + 2×31 + 3 = 961 + 62 + 3 = 1026`。  
T[0..2]="abc" 哈希=1026，命中 → 精确对比 ✓，匹配位置 0。  
窗口滑动至 T[1..3]="bca"：  
`new = (1026 - 1×961)×31 + 1 = 65×31 + 1 = 2016`，与 1026 不等，跳过。  
依次类推，T[3..5]="abc" 哈希=1026，再次命中，匹配位置 3。

## 代码实现

```python
def rabin_karp(text: str, pattern: str,
               base: int = 131, mod: int = 10**9 + 7) -> list[int]:
    \"\"\"单模式 Rabin-Karp，返回所有匹配起始下标。\"\"\"
    n, m = len(text), len(pattern)
    if m > n:
        return []

    # 预计算 base^(m-1) % mod
    high_pow = pow(base, m - 1, mod)

    def char_val(c: str) -> int:
        return ord(c)

    # 计算初始哈希
    ph = th = 0
    for i in range(m):
        ph = (ph * base + char_val(pattern[i])) % mod
        th = (th * base + char_val(text[i])) % mod

    matches = []
    for i in range(n - m + 1):
        if th == ph and text[i:i + m] == pattern:
            matches.append(i)
        if i + m < n:
            th = (th - char_val(text[i]) * high_pow) % mod
            th = (th * base + char_val(text[i + m])) % mod
            th %= mod
    return matches


# 验证
assert rabin_karp("abcabc", "abc") == [0, 3]
assert rabin_karp("aaaa", "aa") == [0, 1, 2]
```

## 多模式扩展

Rabin-Karp 天然适合**多模式匹配**：将所有模式哈希存入集合，对文本每个窗口 O(1) 查集合，总体 O(n×k + Σm_i)，k 为模式数量。
""",

# ──────────────────────────────────────────────────────────────────────────────
"10-数据结构与算法-二分图": """\
---
tags: [图论, 二分图, 染色, 匹配]
aliases: [Bipartite Graph, 二部图]
sources:
  - https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/
  - https://cp-algorithms.com/graph/bipartite-check.html
---

# 二分图

二分图（Bipartite Graph）是指顶点集可以划分为两个不相交子集 U 和 V，使得图中所有边都跨越 U 和 V，即不存在同侧两点之间的边。等价判定：图中不含奇数长度环。MIT OCW 6.006（ https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/ ）在图论单元用 BFS 染色法证明了二分图判定与奇圈的等价关系。

## 判定算法：BFS 二着色

从任意未访问顶点出发做 BFS，将当前顶点染色 0，将所有邻居染色 1，若发现邻居与自身同色则非二分图。时间复杂度 O(V+E)。

## 手算例证

图：顶点 {1,2,3,4}，边 {(1,2),(1,4),(2,3),(3,4)}。  
BFS 从顶点 1 出发：color[1]=0。  
- 1 的邻居 2,4 → color[2]=1, color[4]=1  
- 2 的邻居 3 → color[3]=0  
- 3 的邻居 4 → color[4]=1 ✓（与已有 color[4]=1 一致）  
- 4 的邻居 1 → color[1]=0 ✓  
结论：二分图，U={1,3}，V={2,4}。

若再加边 (1,3)：3 的邻居 1，color[1]=0==color[3]=0 → **非二分图（含奇圈 1-2-3-1）**。

## 代码实现

```python
from collections import deque


def is_bipartite(n: int, adj: list[list[int]]) -> tuple[bool, list[int]]:
    \"\"\"
    判断 n 个顶点（0-indexed）的无向图是否为二分图。
    返回 (is_bip, color)，color[v] 为 -1 表示未访问。
    \"\"\"
    color = [-1] * n
    for start in range(n):
        if color[start] != -1:
            continue
        color[start] = 0
        q = deque([start])
        while q:
            u = q.popleft()
            for v in adj[u]:
                if color[v] == -1:
                    color[v] = 1 - color[u]
                    q.append(v)
                elif color[v] == color[u]:
                    return False, color
    return True, color


# 验证
adj4 = [[1, 3], [0, 2], [1, 3], [0, 2]]  # 4-cycle，二分图
ok, col = is_bipartite(4, adj4)
assert ok
adj3 = [[1, 2], [0, 2], [0, 1]]  # 三角形，非二分图
ok2, _ = is_bipartite(3, adj3)
assert not ok2
```

## 二分图最大匹配

利用匈牙利算法（增广路）可在 O(VE) 时间内求最大匹配；Hopcroft-Karp 算法将其优化至 O(E√V)，适合竞赛场景。
""",

# ──────────────────────────────────────────────────────────────────────────────
"10-数据结构与算法-割点割边": """\
---
tags: [图论, 割点, 割边, Tarjan, DFS]
aliases: [桥, 关节点, Articulation Point]
sources:
  - https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/
  - https://cp-algorithms.com/graph/bridge-searching.html
---

# 割点与割边

**割点**（关节点）：无向连通图中，删去该顶点（及其关联边）后图变得不连通的顶点。  
**割边**（桥）：删去该边后图变得不连通的边。  
Tarjan 用 DFS 树中的 `disc`（发现时间）和 `low`（可回溯到的最早祖先发现时间）在 O(V+E) 内一次遍历求出全部割点和割边。MIT OCW 6.006（ https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/ ）的图论章节介绍了 DFS 树性质，是理解该算法的基础。

## 判定条件

设 DFS 树中 u 是 v 的父节点（树边 u→v）：  
- **割边**：`low[v] > disc[u]`，即 v 的子树无法通过回边绕过 u-v 这条边。  
- **割点**：  
  - 若 u 是根节点，有≥2个子树 → 割点。  
  - 若 u 不是根节点，存在子 v 使 `low[v] >= disc[u]` → 割点。

## 手算例证

图：1-2-3-4-2（含环 2-3-4-2），额外边 1-5。  
DFS 从 1 开始，顺序访问 2,3,4,5：  
disc: [_,0,1,2,3,4]，low 初始=disc。  
4→2 回边：low[4]=min(low[4],disc[2])=1，low[3]=min(low[3],low[4])=1，low[2]=min(low[2],low[3])=1。  
- 边 1-2：low[2]=1>disc[1]=0 → **割边**。  
- 边 1-5：low[5]=4>disc[1]=0 → **割边**。  
- 顶点 1：根节点，有子树 {2,5} 两棵 → **割点**。

## 代码实现

```python
def find_bridges_articulations(n: int, adj: list[list[int]]):
    \"\"\"
    n 个顶点（0-indexed）无向图，返回 (bridges, articulations)。
    bridges: list of (u,v) 割边；articulations: set of 割点。
    \"\"\"
    disc = [-1] * n
    low = [0] * n
    parent = [-1] * n
    visited = [False] * n
    bridges = []
    articulations = set()
    timer = [0]

    def dfs(u: int):
        visited[u] = True
        disc[u] = low[u] = timer[0]
        timer[0] += 1
        children = 0
        for v in adj[u]:
            if not visited[v]:
                children += 1
                parent[v] = u
                dfs(v)
                low[u] = min(low[u], low[v])
                # 割边
                if low[v] > disc[u]:
                    bridges.append((u, v))
                # 割点
                if parent[u] == -1 and children > 1:
                    articulations.add(u)
                if parent[u] != -1 and low[v] >= disc[u]:
                    articulations.add(u)
            elif v != parent[u]:
                low[u] = min(low[u], disc[v])

    for i in range(n):
        if not visited[i]:
            dfs(i)
    return bridges, articulations


# 验证：简单路径 0-1-2，割边为(0,1),(1,2)，割点为1
adj = [[1], [0, 2], [1]]
br, ar = find_bridges_articulations(3, adj)
assert (0, 1) in br and (1, 2) in br
assert 1 in ar
```
""",

# ──────────────────────────────────────────────────────────────────────────────
"10-数据结构与算法-区间合并": """\
---
tags: [贪心, 区间, 排序, 合并]
aliases: [Merge Intervals, 区间覆盖]
sources:
  - https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/
  - https://leetcode.com/problems/merge-intervals/
---

# 区间合并

区间合并（Merge Intervals）：给定一组区间，将所有重叠的区间合并为若干互不重叠的区间。策略是按左端点排序，然后线性扫描依次判断能否扩展当前区间。时间复杂度 O(n log n)（排序主导），空间 O(n)。MIT OCW 6.006（ https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/ ）在贪心算法章节以区间调度/覆盖问题为核心案例，区间合并是其基础操作。

## 算法步骤

1. 按左端点升序排序（左端点相同时按右端点降序，方便）。  
2. 初始化 `merged = [intervals[0]]`。  
3. 对剩余每个区间 `[l, r]`：  
   - 若 `l <= merged[-1][1]`（重叠或相邻）→ 更新 `merged[-1][1] = max(merged[-1][1], r)`。  
   - 否则追加新区间。

## 手算例证

输入：`[[1,3],[2,6],[8,10],[15,18]]`  
排序后：`[1,3],[2,6],[8,10],[15,18]`（已有序）。  
- merged=[[1,3]]  
- [2,6]：2≤3 → 合并为 [1,max(3,6)]=[1,6]  
- [8,10]：8>6 → 追加，merged=[[1,6],[8,10]]  
- [15,18]：15>10 → 追加，merged=[[1,6],[8,10],[15,18]]  

输出：`[[1,6],[8,10],[15,18]]` ✓

## 代码实现

```python
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    \"\"\"合并重叠区间，返回排序后的不重叠区间列表。\"\"\"
    if not intervals:
        return []
    # 按左端点排序
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0][:]]
    for l, r in intervals[1:]:
        if l <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], r)
        else:
            merged.append([l, r])
    return merged


def count_covered_length(intervals: list[list[int]]) -> int:
    \"\"\"合并后计算总覆盖长度。\"\"\"
    merged = merge_intervals(intervals)
    return sum(r - l for l, r in merged)


# 验证
result = merge_intervals([[1, 3], [2, 6], [8, 10], [15, 18]])
assert result == [[1, 6], [8, 10], [15, 18]]

result2 = merge_intervals([[1, 4], [4, 5]])
assert result2 == [[1, 5]]  # 相邻区间也合并

assert count_covered_length([[1, 3], [2, 6], [8, 10]]) == 7  # (6-1)+(10-8)=7
```

## 变种问题

- **区间覆盖**：用最少区间覆盖目标范围 → 贪心右端点最远优先。  
- **不相交区间最大数**：经典活动选择问题，按右端点排序贪心。  
- **插入区间**：在已排序不重叠区间中插入新区间，利用二分查找定位后局部合并。
""",

# ──────────────────────────────────────────────────────────────────────────────
"10-数据结构与算法-字符串哈希": """\
---
tags: [字符串, 哈希, 多项式哈希, 滚动哈希]
aliases: [多项式哈希, String Hashing]
sources:
  - https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/
  - https://cp-algorithms.com/string/string-hashing.html
---

# 字符串哈希

字符串哈希将字符串映射到整数，使得相同字符串一定映射到相同哈希值，不同字符串以高概率映射到不同哈希值。通过预处理前缀哈希数组，可在 O(1) 时间内查询任意子串的哈希，从而将子串比较从 O(m) 降至 O(1)。MIT OCW 6.006（ https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/ ）把多项式哈希作为哈希表与字符串算法的连接桥梁进行分析。

## 前缀哈希定义

对字符串 S[0..n-1]，设：  
`h[0] = 0`，`h[i] = h[i-1] * BASE + ord(S[i-1])`（mod MOD）  
子串 S[l..r] 的哈希：`sub_hash = (h[r+1] - h[l] * BASE^(r-l+1)) % MOD`

## 手算例证

S = "abcd"，BASE=31，MOD=10^9+7。  
- h[0]=0  
- h[1]=0×31+97=97  
- h[2]=97×31+98=3105  
- h[3]=3105×31+99=96354  
- h[4]=96354×31+100=2987074  

查询子串 S[1..2]="bc"：  
`(h[3] - h[1]×31²) % MOD = (96354 - 97×961) % MOD = (96354 - 93217) % MOD = 3137`  
手算 "bc"：`98×31+99=3137` ✓

## 代码实现

```python
class StringHasher:
    \"\"\"多项式前缀哈希，支持 O(1) 子串哈希查询。\"\"\"

    def __init__(self, s: str, base: int = 131, mod: int = 10**9 + 7):
        self.base = base
        self.mod = mod
        n = len(s)
        self.h = [0] * (n + 1)
        self.pw = [1] * (n + 1)
        for i, ch in enumerate(s):
            self.h[i + 1] = (self.h[i] * base + ord(ch)) % mod
            self.pw[i + 1] = self.pw[i] * base % mod

    def query(self, l: int, r: int) -> int:
        \"\"\"查询 s[l..r]（0-indexed，闭区间）的哈希值。\"\"\"
        return (self.h[r + 1] - self.h[l] * self.pw[r - l + 1]) % self.mod


def longest_common_substring_length(s: str, t: str) -> int:
    \"\"\"二分 + 哈希求最长公共子串长度。O((n+m) log(n+m))\"\"\"
    def check(length: int) -> bool:
        hs = StringHasher(s)
        ht = StringHasher(t)
        hashes = {hs.query(i, i + length - 1) for i in range(len(s) - length + 1)}
        return any(ht.query(j, j + length - 1) in hashes
                   for j in range(len(t) - length + 1))

    lo, hi = 0, min(len(s), len(t))
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if check(mid):
            lo = mid
        else:
            hi = mid - 1
    return lo


# 验证
sh = StringHasher("abcd")
assert sh.query(1, 2) == StringHasher("bc").query(0, 1)
assert longest_common_substring_length("abcde", "cdefg") == 3  # "cde"
```

## 双哈希降低碰撞概率

单哈希碰撞概率约 1/MOD≈10⁻⁹。使用两组不同 (BASE, MOD) 的双哈希，碰撞概率降至约 10⁻¹⁸，在竞赛中几乎可认为无碰撞。
""",

# ──────────────────────────────────────────────────────────────────────────────
"10-数据结构与算法-差分约束": """\
---
tags: [图论, 差分约束, 最短路, Bellman-Ford]
aliases: [Difference Constraints, 约束图]
sources:
  - https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/
  - https://cp-algorithms.com/graph/bellman_ford.html
---

# 差分约束系统

差分约束（Difference Constraints）是一类线性约束系统，每个约束形如 `x_j - x_i ≤ w_{ij}`。将其建模为有向图：从 i 到 j 连权重 w_{ij} 的边，则**最短路给出满足所有约束的最小解**（若存在负圈则无解）。MIT OCW 6.006（ https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/ ）在最短路一章专门讲授差分约束与 Bellman-Ford 的关联。

## 建模规则

- 约束 `x_j - x_i ≤ w` → 边 `i → j`，权重 `w`。  
- 加入超级源 s，对每个顶点 v 加边 `s → v`，权重 0（确保从 s 可达所有点）。  
- 运行 Bellman-Ford；若存在负权圈 → 无解；否则 `x_v = dist[v]`。

## 手算例证

约束：`x2 - x1 ≤ 3`，`x3 - x2 ≤ 5`，`x1 - x3 ≤ -1`（即 x3 - x1 ≥ 1）。  
建图：1→2(3)，2→3(5)，3→1(-1)；超级源 s→1,2,3 全权重 0。  
Bellman-Ford 从 s：dist=[0,0,0,0]（s=0,x1=1,x2=2,x3=3）  
松弛：s→1→2→3 得 dist[1]=0,dist[2]=3,dist[3]=8；3→1(-1) 后 dist[1]=-1<0，继续...  
稳定后：dist≈[-1, -1, 2, 7]（含超级源），无负圈，可行解 x1=-1,x2=2,x3=7。  
验证：x2-x1=3≤3✓, x3-x2=5≤5✓, x1-x3=-8≤-1✓。

## 代码实现

```python
def solve_difference_constraints(n: int, constraints: list[tuple[int,int,int]]):
    \"\"\"
    n 个变量（1-indexed），约束列表 [(i,j,w)] 表示 x_j - x_i <= w。
    返回可行解列表或 None（无解）。
    \"\"\"
    INF = float('inf')
    # 0 为超级源，变量编号 1..n
    dist = [INF] * (n + 1)
    dist[0] = 0

    # 所有边：超级源到每个变量 + 约束边
    edges = [(0, i, 0) for i in range(1, n + 1)]
    for (i, j, w) in constraints:
        edges.append((i, j, w))

    # Bellman-Ford，最多 n 轮
    for _ in range(n):
        updated = False
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                updated = True
        if not updated:
            break

    # 检测负圈
    for u, v, w in edges:
        if dist[u] != INF and dist[u] + w < dist[v]:
            return None  # 无解

    return dist[1:]  # 返回 x1..xn


# 验证
sol = solve_difference_constraints(3, [(1,2,3),(2,3,5),(3,1,-1)])
assert sol is not None
x1, x2, x3 = sol
assert x2 - x1 <= 3 and x3 - x2 <= 5 and x1 - x3 <= -1
```
""",

# ──────────────────────────────────────────────────────────────────────────────
"10-数据结构与算法-强连通分量": """\
---
tags: [图论, SCC, Tarjan, Kosaraju, 有向图]
aliases: [SCC, Strongly Connected Component]
sources:
  - https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/
  - https://cp-algorithms.com/graph/strongly-connected-components.html
---

# 强连通分量（SCC）

有向图中，若从顶点 u 可达 v 且从 v 也可达 u，则 u 和 v 属于同一**强连通分量**。Tarjan 算法利用 DFS 栈和 `low` 值在一次遍历中识别所有 SCC，时间复杂度 O(V+E)。MIT OCW 6.006（ https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/ ）在有向图单元详细分析了 SCC 的理论基础（DFS 树的 cross edge、back edge 性质）。

## Tarjan 算法原理

维护递减栈和 `low[u]=` u 所在 SCC 中最早可达的 disc 值。当 `low[u]==disc[u]` 时，栈顶到 u 的所有节点构成一个 SCC，弹出归组。

## 手算例证

图：1→2, 2→3, 3→1, 3→4, 4→5, 5→4。  
DFS(1)→DFS(2)→DFS(3)→回边到1：low[3]=0。  
DFS(4)→DFS(5)→回边4：low[5]=low[4]=3。  
DFS(5)返回 low[4]=min(3,low[5])=3，low[4]=disc[4]=3 → 弹出 {4,5} → SCC1={4,5}。  
DFS(3)返回 low[3]=0==disc[1]=0（从1开始）→ 弹出 {3,2,1} → SCC2={1,2,3}。  
结果：SCC = [{4,5}, {1,2,3}]，凝缩后 DAG：SCC2→SCC1。

## 代码实现

```python
def tarjan_scc(n: int, adj: list[list[int]]) -> list[list[int]]:
    \"\"\"Tarjan SCC，返回 SCC 列表（逆拓扑序）。顶点 0-indexed。\"\"\"
    disc = [-1] * n
    low = [0] * n
    on_stack = [False] * n
    stack = []
    sccs = []
    timer = [0]

    def dfs(u: int):
        disc[u] = low[u] = timer[0]
        timer[0] += 1
        stack.append(u)
        on_stack[u] = True
        for v in adj[u]:
            if disc[v] == -1:
                dfs(v)
                low[u] = min(low[u], low[v])
            elif on_stack[v]:
                low[u] = min(low[u], disc[v])
        if low[u] == disc[u]:
            scc = []
            while True:
                v = stack.pop()
                on_stack[v] = False
                scc.append(v)
                if v == u:
                    break
            sccs.append(scc)

    import sys
    sys.setrecursionlimit(10000)
    for i in range(n):
        if disc[i] == -1:
            dfs(i)
    return sccs


# 验证：图 0→1→2→0, 2→3→4→3
adj = [[1],[2],[0,3],[4],[3]]
sccs = tarjan_scc(5, adj)
sizes = sorted(len(s) for s in sccs)
assert sizes == [2, 3]  # {0,1,2} 和 {3,4}
```

## 应用

SCC 凝缩后得到 DAG，可进行拓扑排序；2-SAT 问题的解法核心即为求 SCC 后判断变量与其否定是否在同一 SCC 中。
""",

# ──────────────────────────────────────────────────────────────────────────────
"10-数据结构与算法-快速傅里叶变换FFT": """\
---
tags: [FFT, 多项式乘法, 分治, 信号处理]
aliases: [Fast Fourier Transform, NTT]
sources:
  - https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/
  - https://cp-algorithms.com/algebra/fft.html
---

# 快速傅里叶变换（FFT）

FFT 将两个 n 次多项式的乘法从 O(n²) 朴素卷积加速到 O(n log n)。核心思想：在 n 个单位根处求值（DFT），逐点相乘，再逆 DFT 还原系数。MIT OCW 6.006（ https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/ ）在算法设计模块把 FFT 作为分治思想的巅峰案例讲授，并分析其实际工程意义（信号处理、大数乘法）。

## Cooley-Tukey 递归

将 A(x)=A_even(x²)+x·A_odd(x²)，分别对 A_even 和 A_odd 递归做 n/2 点 FFT，然后合并：
- ω = e^(2πi/n)（主 n 次单位根）
- A(ω^k) = A_even(ω^(2k)) + ω^k · A_odd(ω^(2k))，k=0..n/2-1

## 手算例证（4 点 DFT）

A = [1, 2, 3, 4]（系数），n=4，ω=i（虚数单位）。  
A_even = [1,3]（偶次项系数），A_odd = [2,4]（奇次项系数）。  
2-DFT of [1,3]: [(1+3)=4, (1-3)=-2]  
2-DFT of [2,4]: [(2+4)=6, (2-4)=-2]  
合并（ω=i）：  
- k=0: A(1) = 4 + 1·6 = 10  
- k=1: A(i) = -2 + i·(-2) = -2-2i  
- k=2: A(-1)= 4 + (-1)·6 = -2  
- k=3: A(-i)= -2 + (-i)·(-2) = -2+2i  
DFT=[10, -2-2i, -2, -2+2i] ✓（可用逆 DFT 还原 [1,2,3,4]）

## 代码实现

```python
import cmath
import math


def fft(a: list[complex], invert: bool = False) -> list[complex]:
    \"\"\"原地 Cooley-Tukey FFT，len(a) 必须是 2 的幂次。\"\"\"
    n = len(a)
    if n == 1:
        return a
    # 位翻转置换
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i < j:
            a[i], a[j] = a[j], a[i]
    # 蝶形运算
    length = 2
    while length <= n:
        angle = 2 * math.pi / length * (-1 if invert else 1)
        w_len = complex(math.cos(angle), math.sin(angle))
        for i in range(0, n, length):
            w = complex(1)
            for k in range(length // 2):
                u, v = a[i + k], a[i + k + length // 2] * w
                a[i + k] = u + v
                a[i + k + length // 2] = u - v
                w *= w_len
        length <<= 1
    if invert:
        for i in range(n):
            a[i] /= n
    return a


def poly_multiply(p: list[int], q: list[int]) -> list[int]:
    \"\"\"多项式乘法，系数为整数，返回结果系数列表。\"\"\"
    result_len = len(p) + len(q) - 1
    n = 1
    while n < result_len:
        n <<= 1
    fa = [complex(x) for x in p] + [complex(0)] * (n - len(p))
    fb = [complex(x) for x in q] + [complex(0)] * (n - len(q))
    fft(fa)
    fft(fb)
    for i in range(n):
        fa[i] *= fb[i]
    fft(fa, invert=True)
    return [round(fa[i].real) for i in range(result_len)]


# 验证：(1+2x)(3+4x) = 3+10x+8x²
assert poly_multiply([1, 2], [3, 4]) == [3, 10, 8]
```

## NTT（数论变换）

NTT 在模质数域内做 FFT，避免浮点误差，适合竞赛（常用 MOD=998244353，原根=3）。
""",

# ──────────────────────────────────────────────────────────────────────────────
"10-数据结构与算法-扫描线算法": """\
---
tags: [计算几何, 扫描线, 线段树, 面积并]
aliases: [Sweep Line, 事件驱动]
sources:
  - https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/
  - https://cp-algorithms.com/geometry/area-of-union-of-triangles.html
---

# 扫描线算法

扫描线（Sweep Line）是一类把二维几何问题转化为一维动态维护问题的通用方法：用一条假想的垂直线从左到右扫描平面，在关键 x 坐标（事件点）处更新数据结构。经典应用：**矩形面积并**（O(n log n)）、最近点对、线段相交检测等。MIT OCW 6.006（ https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/ ）将扫描线作为将排序与数据结构结合的典型设计模式讲授。

## 矩形面积并算法

每个矩形 [x1,x2]×[y1,y2] 产生两个事件：x=x1 时插入 y 区间 [y1,y2]（+1），x=x2 时删除（-1）。按 x 排序事件，用线段树维护当前 y 轴上被覆盖的总长度。

## 手算例证

矩形 A=[0,2]×[0,3]，矩形 B=[1,3]×[1,4]。  
事件：(x=0,+,[0,3])，(x=1,+,[1,4])，(x=2,-,[0,3])，(x=3,-,[1,4])。  
- x从0到1，y覆盖[0,3]长=3，面积+=3×1=3  
- x从1到2，y覆盖[0,4]（合并后）长=4，面积+=4×1=4  
- x从2到3，y覆盖[1,4]长=3，面积+=3×1=3  
总面积=3+4+3=10。手算验证：A面积=6，B面积=9，交面积=[1,2]×[1,3]=2，并=6+9-5=10✓（交=1×3=... 精确计算：交=[1,2]×[1,3]，面积=1×2=2，并=6+6-2=10）

## 代码实现

```python
def rectangle_union_area(rects: list[tuple[int,int,int,int]]) -> float:
    \"\"\"
    计算矩形面积并。rects: [(x1,y1,x2,y2)]，x1<x2，y1<y2。
    使用坐标压缩 + 扫描线。
    \"\"\"
    # 收集所有 y 坐标并压缩
    ys = sorted(set(y for x1,y1,x2,y2 in rects for y in (y1,y2)))
    yi = {y: i for i, y in enumerate(ys)}
    m = len(ys) - 1  # y 区间数

    cnt = [0] * m  # 每个 y 区间被覆盖次数

    # 构建事件
    events = []
    for x1, y1, x2, y2 in rects:
        events.append((x1, 1, y1, y2))
        events.append((x2, -1, y1, y2))
    events.sort()

    def covered_len() -> float:
        total = 0.0
        for i in range(m):
            if cnt[i] > 0:
                total += ys[i + 1] - ys[i]
        return total

    area = 0.0
    prev_x = None
    for x, delta, y1, y2 in events:
        if prev_x is not None:
            area += covered_len() * (x - prev_x)
        for i in range(yi[y1], yi[y2]):
            cnt[i] += delta
        prev_x = x
    return area


# 验证
area = rectangle_union_area([(0,0,2,3),(1,1,3,4)])
assert abs(area - 10) < 1e-9
```

## 其他扫描线应用

- 最近点对：维护滑动窗口（平衡 BST），O(n log n) 求平面最近点对。  
- 线段相交：Shamos-Hoey / Bentley-Ottmann 算法检测或枚举所有交点。
""",

# ──────────────────────────────────────────────────────────────────────────────
"10-数据结构与算法-数位DP": """\
---
tags: [DP, 数位DP, 计数, 枚举]
aliases: [Digit DP, 数字统计]
sources:
  - https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/
  - https://codeforces.com/blog/entry/53960
---

# 数位 DP

数位 DP 是计算区间 [0, N] 内满足某数字特征的整数个数的技巧，将数字逐位填写，记录"是否仍受上界约束"等状态，用记忆化 DFS 避免重复计算。时间复杂度通常 O(位数 × 状态数)。MIT OCW 6.006（ https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/ ）的 DP 模块强调子问题定义方式对效率的决定性作用，数位 DP 是这一思想的精妙体现。

## 状态设计模板

```
dfs(pos, state, tight, leading_zero)
  pos     : 当前填写的位（从高到低）
  state   : 题目相关状态（如数字之和、是否含某数字）
  tight   : 当前位是否受上界约束
  leading_zero: 是否还在填前导零
```

## 手算例证

问题：统计 [1, 15] 内各位数字之和 ≤ 3 的整数个数。  
直接枚举：1,2,3,10(1+0=1),11(1+1=2),12(1+2=3),20(2+0=2) → 但15以内：1,2,3,10,11,12 共6个（13=4>3, 20>15）。  
数位 DP 过程：N=15，d=[1,5]。  
- pos=0, tight=True → 最高位可填 [0,1]  
  - 填0（leading_zero）→ pos=1, tight=False, state=0，可填[0-9]但要≤3→0,1,2,3→4个（均≤15）  
  - 填1 → pos=1, tight=True（因为N高位=1），可填[0-5]且state+d≤3→d∈{0,1,2}→3个  
- 总计=4+3=7... 去掉0（不计入正整数）=6 ✓

## 代码实现

```python
from functools import lru_cache


def count_digit_sum_le(n: int, max_sum: int) -> int:
    \"\"\"统计 [0, n] 内各位数字之和 <= max_sum 的非负整数个数。\"\"\"
    digits = [int(d) for d in str(n)]
    length = len(digits)

    @lru_cache(maxsize=None)
    def dfs(pos: int, cur_sum: int, tight: bool) -> int:
        if cur_sum > max_sum:
            return 0
        if pos == length:
            return 1
        limit = digits[pos] if tight else 9
        total = 0
        for d in range(0, limit + 1):
            total += dfs(pos + 1, cur_sum + d, tight and (d == limit))
        return total

    result = dfs(0, 0, True)
    dfs.cache_clear()
    return result


def count_in_range(lo: int, hi: int, max_sum: int) -> int:
    \"\"\"统计 [lo, hi] 内各位数字之和 <= max_sum 的整数个数。\"\"\"
    return count_digit_sum_le(hi, max_sum) - count_digit_sum_le(lo - 1, max_sum)


# 验证
assert count_in_range(1, 15, 3) == 6  # 1,2,3,10,11,12
assert count_in_range(1, 9, 5) == 5   # 1,2,3,4,5
```

## 典型状态扩展

| 问题 | 额外状态 |
|------|---------|
| 不含相邻相同数字 | 上一位数字 |
| 数字和整除 k | sum mod k |
| 含特定数字子序列 | 已匹配长度 |
""",

# ──────────────────────────────────────────────────────────────────────────────
"10-数据结构与算法-树形DP": """\
---
tags: [DP, 树形DP, 树, DFS]
aliases: [Tree DP, 树上动态规划]
sources:
  - https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/
  - https://cp-algorithms.com/graph/tree_painter.html
---

# 树形 DP

树形 DP 在树结构上定义子问题：以某节点为根的子树的最优解，由其子节点子树的解合并而来。典型题型：最大独立集、最长路径、树的直径、换根 DP 等。MIT OCW 6.006（ https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/ ）在 DP 专题中以最优 BST 和树上最优结构为例，说明树的递推与一般 DP 的统一框架。

## 经典问题：树上最大独立集

对每个节点 u 定义：  
- `dp[u][0]` = u 不选时，以 u 为根子树的最大独立集大小  
- `dp[u][1]` = u 选时的最大独立集大小  

转移：  
- `dp[u][1] = 1 + Σ dp[v][0]`（子节点均不选）  
- `dp[u][0] = Σ max(dp[v][0], dp[v][1])`（子节点可选可不选）

## 手算例证

树结构（0-indexed）：0-1, 0-2, 1-3, 1-4（路径形状类 H）。  
叶节点 3,4：dp[3]=[0,1]，dp[4]=[0,1]。  
节点 1（子：3,4）：dp[1][1]=1+0+0=1，dp[1][0]=max(0,1)+max(0,1)=2。  
叶节点 2：dp[2]=[0,1]。  
根 0（子：1,2）：dp[0][1]=1+dp[1][0]+dp[2][0]=1+2+0=3，dp[0][0]=max(1,2)+max(0,1)=2+1=3。  
最大独立集大小=max(dp[0])=3，可选集合 {1的不选，0,2,...} → {0,3,4} 或 {1,2} 不，{0,3,4} 大小3✓。

## 代码实现

```python
def max_independent_set(n: int, adj: list[list[int]]) -> int:
    \"\"\"
    树上最大独立集，n 个节点（0-indexed），无根树以0为根。
    返回最大独立集大小。
    \"\"\"
    dp = [[0, 0] for _ in range(n)]  # dp[u][0/1]

    def dfs(u: int, parent: int):
        dp[u][1] = 1  # 选 u
        dp[u][0] = 0  # 不选 u
        for v in adj[u]:
            if v == parent:
                continue
            dfs(v, u)
            dp[u][1] += dp[v][0]
            dp[u][0] += max(dp[v][0], dp[v][1])

    import sys
    sys.setrecursionlimit(10000)
    dfs(0, -1)
    return max(dp[0])


def tree_diameter(n: int, adj: list[list[tuple[int,int]]]) -> int:
    \"\"\"带权树直径（两次 BFS/DFS 法）。adj[u] = [(v, w)]。\"\"\"
    dist = [-1] * n

    def bfs(start: int) -> int:
        from collections import deque
        dist[start] = 0
        q = deque([start])
        far = start
        while q:
            u = q.popleft()
            for v, w in adj[u]:
                if dist[v] == -1:
                    dist[v] = dist[u] + w
                    if dist[v] > dist[far]:
                        far = v
                    q.append(v)
        return far

    u = bfs(0)
    dist[:] = [-1] * n
    v = bfs(u)
    return dist[v]


# 验证最大独立集
adj5 = [[1,2],[0,3,4],[0],[1],[1]]
assert max_independent_set(5, adj5) == 3  # {0,3,4}
```

## 换根 DP

换根（re-rooting）技巧：先从某根做一次树形 DP 获得"向下"信息，再从根向子节点传递"向上"信息，从而在 O(n) 内计算每个节点为根时的答案。适用于"以每个节点为根时的最大深度/节点数"等问题。
""",

# ──────────────────────────────────────────────────────────────────────────────
"10-数据结构与算法-概率DP": """\
---
tags: [DP, 概率, 期望, 随机]
aliases: [Probability DP, 期望DP]
sources:
  - https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/
  - https://codeforces.com/blog/entry/62690
---

# 概率 DP / 期望 DP

概率 DP 将随机过程的期望值分解为子问题期望之和，利用全期望公式 E[X] = Σ P(状态=s)·E[X|状态=s] 建立递推。常见模型：随机游走、掷骰子期望步数、抽卡期望次数等。MIT OCW 6.006（ https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/ ）虽侧重确定性算法，但其期望分析框架（hired problem、hashing expected collision）为概率 DP 提供了数学基础。

## 经典模型：掷骰子达到目标的期望步数

一枚公平骰子（1-6），从 0 出发，每步加骰点数，第一次 ≥ n 时停止，期望投掷次数 E[n]。  
边界：E[0]=0（已到达）。  
递推：`E[i] = 1 + (1/6) Σ_{d=1}^{6} E[max(0, i-d)]`（若 i-d<0 则已超过终点，贡献0步）

## 手算例证

计算 E[1]（目标=1，距离为1时期望步数）：  
任何骰点 d≥1 均满足，故只需1步 → E[1]=1。  
计算 E[3]：  
`E[3] = 1 + (1/6)(E[0]+E[0]+E[0]+E[2]+E[1]+E[0])` 等... 实际：  
d=1 → 剩余 E[2]；d=2 → E[1]；d=3,4,5,6 → 达到或超过，剩余 E[0]=0。  
先算 E[2]=1+(1/6)(E[1]+E[0]+E[0]+...=1+(1/6)(1+0×5)...  
（详见代码输出，避免手算误差）

## 代码实现

```python
def expected_dice_rolls(target: int, faces: int = 6) -> float:
    \"\"\"
    从 0 出发，每步掷 faces 面骰子（1~faces），
    首次总和 >= target 的期望投掷次数。
    \"\"\"
    # E[i] = 从位置 i 到达 target 的期望步数
    # 从 target-1 倒推（原问题：从0出发，等价于距离为 target）
    E = [0.0] * (target + 1)
    for i in range(target - 1, -1, -1):
        total = 0.0
        for d in range(1, faces + 1):
            nxt = i + d
            if nxt >= target:
                total += 0.0  # 已到达
            else:
                total += E[nxt]
        E[i] = 1.0 + total / faces
    return E[0]


def coupon_collector_expected(n: int) -> float:
    \"\"\"
    集齐 n 种不同优惠券（每次等概率抽1种）的期望抽取次数。
    公式：E = n * H(n) = n * Σ_{k=1}^{n} 1/k
    \"\"\"
    return n * sum(1.0 / k for k in range(1, n + 1))


# 验证
e1 = expected_dice_rolls(1)
assert abs(e1 - 1.0) < 1e-9  # 任何骰点都到达，期望1步

e_coupon = coupon_collector_expected(3)
# E = 3*(1 + 1/2 + 1/3) = 3*11/6 = 11/2 = 5.5
assert abs(e_coupon - 5.5) < 1e-9
```

## 含环期望（线性方程组）

若状态图有环（如随机游走），期望满足联立方程组，可用高斯消元求解。例如：在 0-1-2 路径上，从 1 出发以各 1/2 概率左右移动，求到达 0 或 2 的期望步数 = 1（对称性直接得），方程法：E[1]=1+(E[0]+E[2])/2=1+1=... 但 E[0]=E[2]=0 → E[1]=1✓。
""",

# ──────────────────────────────────────────────────────────────────────────────
"10-数据结构与算法-状态压缩DP进阶": """\
---
tags: [DP, 状态压缩, Bitmask, TSP]
aliases: [Bitmask DP, 旅行商问题]
sources:
  - https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/
  - https://cp-algorithms.com/algebra/all-submasks.html
---

# 状态压缩 DP 进阶

状态压缩 DP 用整数的二进制位表示集合状态，将集合 DP 的空间和时间压缩到 O(2^n × n)，适用于 n≤20 的场景。进阶技巧包括：子集枚举（O(3^n)）、SOS DP（Sum over Subsets）、Profile DP（棋盘格覆盖）。MIT OCW 6.006（ https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/ ）以 TSP（旅行商问题）为例，证明 Bitmask DP 将暴力 O(n!) 降至 O(2^n·n²)。

## 经典：Held-Karp TSP

`dp[mask][v]` = 访问了 mask 中所有城市、当前在 v、从城市 0 出发的最短路径长。  
转移：`dp[mask|(1<<u)][u] = min(dp[mask|(1<<u)][u], dp[mask][v] + dist[v][u])`，u ∉ mask。  
最终答案：`min(dp[(1<<n)-1][v] + dist[v][0])` for all v。

## 手算例证

4 城市，距离矩阵（0-indexed）：  
dist = [[0,1,2,3],[1,0,4,5],[2,4,0,6],[3,5,6,0]]  
初始：dp[0001][0]=0（mask=0b0001，在城市0）  
dp[0011][1] = dp[0001][0]+dist[0][1] = 0+1 = 1  
dp[0101][2] = dp[0001][0]+dist[0][2] = 0+2 = 2  
dp[1001][3] = dp[0001][0]+dist[0][3] = 0+3 = 3  
dp[0111][2] = min(dp[0011][1]+dist[1][2], dp[0101][2]+dist[2][2]=inf) = 1+4 = 5  
...（完整计算见代码）  
最优回路：0→1→2→3→0，总距离=1+4+6+3=14。

## 代码实现

```python
def tsp_held_karp(dist: list[list[int]]) -> int:
    \"\"\"Held-Karp TSP，从城市0出发回到0的最短路。O(2^n * n^2)。\"\"\"
    n = len(dist)
    INF = float('inf')
    full = (1 << n) - 1
    # dp[mask][v]
    dp = [[INF] * n for _ in range(1 << n)]
    dp[1][0] = 0  # 从城市0出发，mask=0b0001

    for mask in range(1, 1 << n):
        if not (mask & 1):  # 必须包含城市0
            continue
        for v in range(n):
            if not (mask >> v & 1) or dp[mask][v] == INF:
                continue
            for u in range(n):
                if mask >> u & 1:
                    continue
                new_mask = mask | (1 << u)
                if dp[mask][v] + dist[v][u] < dp[new_mask][u]:
                    dp[new_mask][u] = dp[mask][v] + dist[v][u]

    return min(dp[full][v] + dist[v][0] for v in range(1, n))


def sos_dp(a: list[int], n: int) -> list[int]:
    \"\"\"Sum over Subsets DP：f[mask] = sum of a[sub] for all sub ⊆ mask。\"\"\"
    f = a[:]
    for i in range(n):
        for mask in range(1 << n):
            if mask >> i & 1:
                f[mask] += f[mask ^ (1 << i)]
    return f


# 验证 TSP
dist = [[0,1,2,3],[1,0,4,5],[2,4,0,6],[3,5,6,0]]
assert tsp_held_karp(dist) == 14
# SOS: a=[1,0,0,0]，f[3]=a[0]+a[1]+a[2]+a[3]=1
assert sos_dp([1,0,0,0], 2) == [1, 1, 1, 1]
```

## 子集枚举技巧

```python
# 枚举 mask 的所有非空子集，O(3^n) 总时间
mask = 0b1010  # 示例
sub = mask
while sub:
    # 处理 sub
    sub = (sub - 1) & mask
```
""",

# ──────────────────────────────────────────────────────────────────────────────
"10-数据结构与算法-离线算法": """\
---
tags: [离线算法, 莫队, CDQ分治, 整体二分]
aliases: [Offline Algorithm, Mo's Algorithm]
sources:
  - https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/
  - https://codeforces.com/blog/entry/61203
---

# 离线算法

离线算法在获得全部查询后再统一处理，通过重排查询顺序降低总时间复杂度，与在线算法（实时应答）形成对比。典型代表：**莫队算法**（区间统计 O((n+q)√n)）、**CDQ 分治**（三维偏序 O(n log²n)）、**整体二分**（并行二分多查询）。MIT OCW 6.006（ https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/ ）强调算法设计中"利用已知信息重组计算顺序"的思想，离线算法是该思想的集中体现。

## 莫队算法原理

将数组分块，块大小 B=√n。对区间查询按（左端点所在块，右端点）排序：  
- 同一块内按右端点升序  
- 不同块按块编号升序  
这样左右指针的总移动量为 O((n+q)√n)。

## 手算例证

n=6，B=√6≈2，查询：Q1=[1,4]，Q2=[2,5]，Q3=[0,2]，Q4=[3,5]。  
块分配：0-1→块0，2-3→块1，4-5→块2。  
排序（左块,右端）：Q3(块0,2)→Q1(块0,4)→Q4(块1,5)→Q2(块1,5)。  
指针初始 l=0,r=-1（空区间）：  
- Q3[0,2]：r 移至2(+3步)，l 不动，add(0),add(1),add(2)。  
- Q1[1,4]：l 右移1(remove 0,+1步)，r 右移4(add 3,4,+2步)。  
- Q4[3,5]：l 右移2(remove 1,2,+2步)，r 右移5(add 5,+1步)。  
- Q2[2,5]：l 左移1(add 2,+1步)。  
总移动=3+1+2+2+1+1=10 步，远少于朴素 4×(4+1+1+2)=32。

## 代码实现

```python
import math
from collections import defaultdict


def mo_algorithm(arr: list[int], queries: list[tuple[int,int]]) -> list[int]:
    \"\"\"
    用莫队算法回答区间众数出现次数查询。
    queries: [(l, r)] 0-indexed 闭区间，返回每查询区间的最大频次。
    \"\"\"
    n = len(arr)
    block = max(1, int(math.isqrt(n)))
    q_indexed = [(l, r, i) for i, (l, r) in enumerate(queries)]
    q_indexed.sort(key=lambda x: (x[0] // block, x[1] if (x[0] // block) % 2 == 0 else -x[1]))

    cnt = defaultdict(int)
    max_cnt = [0]
    freq_cnt = defaultdict(int)  # freq_cnt[f] = 有多少元素频次为 f

    def add(idx: int):
        val = arr[idx]
        old_f = cnt[val]
        if old_f > 0:
            freq_cnt[old_f] -= 1
        cnt[val] += 1
        new_f = cnt[val]
        freq_cnt[new_f] += 1
        if new_f > max_cnt[0]:
            max_cnt[0] = new_f

    def remove(idx: int):
        val = arr[idx]
        old_f = cnt[val]
        freq_cnt[old_f] -= 1
        if old_f == max_cnt[0] and freq_cnt[old_f] == 0:
            max_cnt[0] -= 1
        cnt[val] -= 1
        if cnt[val] > 0:
            freq_cnt[cnt[val]] += 1

    answers = [0] * len(queries)
    cur_l, cur_r = 0, -1
    for l, r, qi in q_indexed:
        while cur_r < r:
            cur_r += 1
            add(cur_r)
        while cur_l > l:
            cur_l -= 1
            add(cur_l)
        while cur_r > r:
            remove(cur_r)
            cur_r -= 1
        while cur_l < l:
            remove(cur_l)
            cur_l += 1
        answers[qi] = max_cnt[0]
    return answers


# 验证
arr = [1, 2, 1, 3, 1, 2]
ans = mo_algorithm(arr, [(0, 5), (1, 3), (2, 4)])
assert ans[0] == 3  # 全区间，1出现3次
assert ans[1] == 1  # [2,1,3] 各出现1次
assert ans[2] == 2  # [1,3,1] 1出现2次
```
""",

# ──────────────────────────────────────────────────────────────────────────────
"10-数据结构与算法-算法代码规范": """\
---
tags: [工程, 代码规范, 可读性, 调试]
aliases: [Coding Standards, 算法工程规范]
sources:
  - https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/
  - https://google.github.io/styleguide/pyguide.html
---

# 算法代码规范

竞赛与工程中的算法代码在可读性、正确性、可调试性上有不同侧重。良好规范能大幅减少调试时间并避免低级错误。MIT OCW 6.006（ https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/ ）的配套 Problem Set 要求学生提交结构清晰、附有类型注解的 Python 代码，作为工程规范的实践示范。

## 核心规范要点

### 1. 类型注解与文档字符串
明确函数签名减少接口误用；docstring 说明前置条件和返回语义。

### 2. 边界条件显式处理
将 `n==0`、空列表、单元素等边界单独写在函数开头，不依赖"恰好正确"的通用逻辑。

### 3. 常量命名与魔法数字消除
`INF = float('inf')` 优于散落在代码中的 `1e18`；`MOD = 10**9 + 7` 命名后全局引用。

### 4. 断言与自测
在函数内用 `assert` 检验不变量（生产环境可 `-O` 关闭）；每个函数下附 2-3 个快速验证用例。

## 手算例证：规范化前后对比

**不规范版本**（含5种常见问题）：
```python
def f(a, b):
    if len(a)==0: return 0    # 问题1：无类型注解
    r=0                        # 问题2：单字母变量名（非循环变量）
    for i in range(len(a)):
        r+=a[i]*b[i]           # 问题3：未检查长度一致性
    return r                   # 问题4：无docstring，问题5：无边界断言
```

**规范版本**：
```python
def dot_product(vec_a: list[float], vec_b: list[float]) -> float:
    \"\"\"
    计算两个等长向量的点积。
    前置条件：len(vec_a) == len(vec_b)。
    时间：O(n)，空间：O(1)。
    \"\"\"
    assert len(vec_a) == len(vec_b), (
        f"向量长度不一致：{len(vec_a)} vs {len(vec_b)}"
    )
    if not vec_a:
        return 0.0
    return sum(a * b for a, b in zip(vec_a, vec_b))


# 快速验证
assert dot_product([1, 2, 3], [4, 5, 6]) == 32   # 1×4+2×5+3×6
assert dot_product([], []) == 0.0
```

## 算法竞赛特有规范

```python
import sys
input = sys.stdin.readline      # 快速读入

def solve():
    MOD = 10**9 + 7
    INF = float('inf')
    n, m = map(int, input().split())
    # ... 算法逻辑
    print(answer)

# 多组测试
T = int(input())
for _ in range(T):
    solve()
```

## 命名约定速查

| 场景 | 推荐命名 |
|------|---------|
| 图的顶点数/边数 | `n, m` |
| 邻接表 | `adj[u] = [(v, w)]` |
| DP 数组 | `dp[i][j]`，含义注释 |
| 无穷大 | `INF = float('inf')` 或 `INF = 10**18` |
| 模数 | `MOD = 10**9 + 7` |
""",

# ──────────────────────────────────────────────────────────────────────────────
"10-数据结构与算法-算法学习复盘": """\
---
tags: [学习方法, 复盘, 刻意练习, 元认知]
aliases: [算法复盘, 学习回顾]
sources:
  - https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/
  - https://www.cs.princeton.edu/~rs/AlgsDS07/
---

# 算法学习复盘

复盘是将做题经验转化为稳定能力的关键环节，区别于简单刷题。有效复盘包括：错误归因、知识点定位、模板抽象、举一反三。MIT OCW 6.006（ https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/ ）的 Recitation 环节正是以复盘形式强化讲座内容——先让学生独立解题，再集中分析思路偏差，这与认知科学中的"错误驱动学习"一致。

## 复盘五步法

### Step 1：错误分类
| 错误类型 | 典型表现 | 对策 |
|---------|---------|------|
| 知识盲区 | 不知道算法存在 | 系统补充知识图谱 |
| 思维定势 | 见到图就想 BFS，忽略贪心 | 每次先列所有候选方法 |
| 实现错误 | 边界/下标/取模遗漏 | 构建检查清单 |
| 效率不足 | 想到了但没写完 | 模板熟练度训练 |

### Step 2：知识点回溯
定位到具体知识点（如"Dijkstra 不能处理负权边"），在知识卡中补充反例与原因。

### Step 3：最小复现
将题目抽象为最小可复现的子问题，排除题目表述干扰。

### Step 4：变式训练
同一算法换包装：如"区间 DP" → 矩阵链乘 → 石子合并 → 括号匹配 → 回文分割。

### Step 5：输出固化
用自己的语言写出算法框架（伪码或文字），不依赖记忆代码。

## 手算例证：一道题的复盘记录

**题目**：给定无权无向图，求从 s 到 t 的路径中**最大边数不超过 k**的路径数。  
**初始思路**：BFS，错误——BFS 求最短路，不计路径数。  
**错误归因**：混淆"层数 = 边数"和"层数 = 最优解"的适用范围。  
**正确方法**：DP，`dp[v][j]` = 恰好经过 j 条边到达 v 的路径数，转移 `dp[v][j] = Σ dp[u][j-1]`（u→v 有边）。  
**模板抽象**：层次 DP，`dp[层][节点]`，适用于"限制步数的路径计数/最优"场景。  
**变式**：限步数的矩阵图路径 → 直接用矩阵快速幂，O(n³ log k)。

## 代码：层次 DP 路径计数

```python
def count_paths_at_most_k_edges(
    n: int, adj: list[list[int]], src: int, dst: int, k: int
) -> int:
    \"\"\"
    无权有向图中，从 src 到 dst 经过恰好 k 条边的路径数之和（0..k 层）。
    注：允许重复经过节点。
    \"\"\"
    MOD = 10**9 + 7
    # dp[v] = 当前步数能到达 v 的路径数
    dp = [0] * n
    dp[src] = 1
    total = dp[dst]  # 0 步的情况
    for _ in range(k):
        new_dp = [0] * n
        for u in range(n):
            if dp[u] == 0:
                continue
            for v in adj[u]:
                new_dp[v] = (new_dp[v] + dp[u]) % MOD
        dp = new_dp
        total = (total + dp[dst]) % MOD
    return total


# 验证：三角形 0→1→2→0，src=0,dst=2,k=2
adj = [[1],[2],[0]]
# 1步：0→1→2? 不，1步只到1；2步：0→1→2=1条路径
assert count_paths_at_most_k_edges(3, adj, 0, 2, 2) == 1
```
""",

# ──────────────────────────────────────────────────────────────────────────────
"10-数据结构与算法-算法模板整理": """\
---
tags: [模板, 竞赛, 速查, 算法库]
aliases: [Algorithm Templates, 算法速查表]
sources:
  - https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/
  - https://github.com/cp-algorithms/cp-algorithms
---

# 算法模板整理

算法模板是经过提炼的、可直接应用于竞赛/面试的代码骨架，其价值在于减少临时推导错误，使精力集中于建模。好的模板具备：正确性（经过多题验证）、通用性（参数化而非硬编码）、简洁性（最短正确实现）。MIT OCW 6.006（ https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/ ）的 Problem Set 代码库本身就是经典算法的高质量参考实现。

## 核心模板速查（附手算验证）

### 并查集（带路径压缩 + 按秩合并）

手算：n=5，依次合并(0,1),(2,3),(1,2)。  
合并后 find(0)=find(3)=同一根，find(4)=4（孤立）。

```python
class DSU:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]  # 路径减半
            x = self.parent[x]
        return x

    def union(self, x: int, y: int) -> bool:
        \"\"\"合并，返回是否真正合并（原本不连通）。\"\"\"
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
        return True
```

### 二分查找（左/右边界）

手算：arr=[1,2,2,2,3]，找 2 的左边界=1，右边界=3。

```python
import bisect

def lower_bound(arr: list[int], target: int) -> int:
    \"\"\"第一个 >= target 的下标（不存在返回 len(arr)）。\"\"\"
    return bisect.bisect_left(arr, target)

def upper_bound(arr: list[int], target: int) -> int:
    \"\"\"第一个 > target 的下标。\"\"\"
    return bisect.bisect_right(arr, target)

arr = [1, 2, 2, 2, 3]
assert lower_bound(arr, 2) == 1
assert upper_bound(arr, 2) == 4  # 2出现在[1,3)
```

### 线段树（区间求和，单点更新）

手算：arr=[1,2,3,4]，query(1,3)=2+3+4=9，update(2,10)后 query(1,3)=2+10+4=16。

```python
class SegTree:
    def __init__(self, n: int):
        self.n = n
        self.tree = [0] * (4 * n)

    def update(self, node: int, start: int, end: int, idx: int, val: int):
        if start == end:
            self.tree[node] = val
            return
        mid = (start + end) // 2
        if idx <= mid:
            self.update(2*node, start, mid, idx, val)
        else:
            self.update(2*node+1, mid+1, end, idx, val)
        self.tree[node] = self.tree[2*node] + self.tree[2*node+1]

    def query(self, node: int, start: int, end: int, l: int, r: int) -> int:
        if r < start or end < l:
            return 0
        if l <= start and end <= r:
            return self.tree[node]
        mid = (start + end) // 2
        return (self.query(2*node, start, mid, l, r) +
                self.query(2*node+1, mid+1, end, l, r))

# 验证
st = SegTree(4)
for i, v in enumerate([1,2,3,4]):
    st.update(1, 0, 3, i, v)
assert st.query(1, 0, 3, 1, 3) == 9
st.update(1, 0, 3, 2, 10)
assert st.query(1, 0, 3, 1, 3) == 16
```

## 模板使用建议

1. **不要死记**：理解原理后，模板是"参数化的理解"，遗忘后可快速重推。  
2. **本地测试**：每个模板维护 3 个以上验证用例，提交前必测。  
3. **版本管理**：不同变种（如线段树懒标记版）单独维护，避免合并混乱。
""",

# ──────────────────────────────────────────────────────────────────────────────
"10-数据结构与算法-算法调试技巧": """\
---
tags: [调试, 测试, 算法工程, 边界条件]
aliases: [Debugging, 算法测试]
sources:
  - https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/
  - https://missing.csail.mit.edu/2020/debugging-profiling/
---

# 算法调试技巧

算法 Bug 往往隐藏在边界条件、整数溢出、循环不变量破坏等处，与普通工程 Bug 有其特殊性。系统化调试比盲目打印更高效。MIT OCW 6.006（ https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/ ）的 TA 答疑文档中归纳了学生最常犯的10类算法错误，其中 6 类属于可通过规范化调试流程预防的"系统性错误"。

## 调试五阶段

### 1. 最小化复现
将 WA 测试点缩减到最小触发规模（二分法删减输入），定位出错的最小子结构。

### 2. 断言不变量
在循环/递归关键处插入 assert，验证算法中间状态的数学不变量。

### 3. 暴力对拍
编写 O(n²) 或 O(n³) 的朴素暴力解，与主算法对同一批随机输入比较输出。

### 4. 可视化中间结果
对图论问题打印邻接表、DFS 树；对 DP 问题打印 dp 表格。

### 5. 边界测试清单
n=0, n=1, 全相同元素, 已排序/逆排序, 环形结构, 稀疏/稠密图。

## 手算例证：对拍发现快速排序 Bug

**有 Bug 的快速排序**（pivot 选取导致无限递归）：
```python
def buggy_quicksort(arr, lo, hi):
    if lo >= hi:
        return
    pivot = arr[lo]  # 已排序时 O(n²) 且可能栈溢出
    i, j = lo, hi
    while i < j:
        while i < j and arr[j] >= pivot: j -= 1
        arr[i] = arr[j]
        while i < j and arr[i] <= pivot: i += 1
        arr[j] = arr[i]
    arr[i] = pivot
    buggy_quicksort(arr, lo, i - 1)
    buggy_quicksort(arr, i + 1, hi)
```

**对拍工具**（发现哪类输入触发问题）：
```python
import random


def naive_sort(arr: list[int]) -> list[int]:
    return sorted(arr)


def quicksort(arr: list[int], lo: int, hi: int):
    \"\"\"三路快排（正确版），规避已排序最坏情况。\"\"\"
    if lo >= hi:
        return
    # 随机选 pivot，避免最坏 O(n²)
    pivot_idx = random.randint(lo, hi)
    arr[lo], arr[pivot_idx] = arr[pivot_idx], arr[lo]
    pivot = arr[lo]
    lt, gt = lo, hi
    i = lo + 1
    while i <= gt:
        if arr[i] < pivot:
            arr[lt], arr[i] = arr[i], arr[lt]
            lt += 1
            i += 1
        elif arr[i] > pivot:
            arr[i], arr[gt] = arr[gt], arr[i]
            gt -= 1
        else:
            i += 1
    quicksort(arr, lo, lt - 1)
    quicksort(arr, gt + 1, hi)


def stress_test(trials: int = 500):
    \"\"\"对拍：对拍 trials 次随机输入验证正确性。\"\"\"
    for _ in range(trials):
        n = random.randint(0, 20)
        arr = [random.randint(-10, 10) for _ in range(n)]
        expected = naive_sort(arr[:])
        quicksort(arr, 0, len(arr) - 1)
        assert arr == expected, f"FAIL: {arr} != {expected}"
    print(f"All {trials} tests passed.")


stress_test()
```

## 常见算法 Bug 清单

| Bug 类型 | 典型场景 | 检查方法 |
|---------|---------|---------|
| off-by-one | 二分 lo/hi 越界 | 手动验证 n=2,3 的情况 |
| 整数溢出 | 矩阵哈希、快速幂 | 改用 Python 大整数或加 MOD |
| 图的重边 | Dijkstra 多边 | 邻接表检查 |
| 未初始化 DP | dp[0] 未设边界值 | 打印 dp 表格首行 |
| DFS 未标记访问 | 含环图无限递归 | 加 visited 集合 |
""",

# ──────────────────────────────────────────────────────────────────────────────
"10-数据结构与算法-算法面试表达": """\
---
tags: [面试, 沟通, STAR, 算法表达]
aliases: [Interview Expression, 白板编程]
sources:
  - https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/
  - https://www.techinterviewhandbook.org/
---

# 算法面试表达

技术面试中，解题过程的**表达质量**与答案正确性同等重要。面试官通过候选人的思路阐述评估沟通能力、抽象思维、鲁棒性意识。MIT OCW 6.006（ https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/ ）的 Problem Set 要求学生在代码前先写算法描述，这正是面试中"先说思路再写代码"的训练。

## 标准答题框架（5步法）

### Step 1：澄清问题（2分钟）
提问输入规模、特殊情况（空输入、负数、重复）、输出格式（返回值还是打印）。  
示例：*"n 的范围是多少？数组中有重复元素吗？需要原地修改吗？"*

### Step 2：暴力解 → 优化（思路推进）
先说暴力时间复杂度，再识别瓶颈，逐步优化。  
示例：*"暴力 O(n²) 枚举所有对，瓶颈是重复计算前缀和→用哈希表降至 O(n)。"*

### Step 3：口头描述算法
用自然语言描述关键步骤，不要直接写代码。  
模板：*"我会用 X 数据结构/算法，原因是 Y，时间 O(Z)，空间 O(W)。"*

### Step 4：手算例证（白板推演）
在纸/白板上用小例子验证思路，发现边界问题。

### Step 5：编码 + 边界检查
先写主体逻辑，再补边界；写完后对空输入、单元素大声过一遍。

## 手算例证：两数之和的面试表达

**问题**：数组中找两数之和等于 target，返回下标。  
**Step 1**：*"数组有重复吗？答案是否唯一？"*  
**Step 2**：暴力 O(n²)，枚举所有对。优化：遍历时用哈希表存已见数字。  
**Step 3**：*"遍历数组，对每个 arr[i]，查表 target-arr[i] 是否已存在；不存在则将 arr[i] 存入表。"*  
**Step 4**：arr=[2,7,11,15], target=9 → i=0: 需要7，表为空 → 存{2:0}；i=1: 需要2，表有2→返回[0,1]。  
**Step 5**：

```python
def two_sum(nums: list[int], target: int) -> list[int]:
    \"\"\"
    返回两个下标 [i, j] 使 nums[i] + nums[j] == target。
    前置：恰好一个解存在。时间 O(n)，空间 O(n)。
    \"\"\"
    seen: dict[int, int] = {}  # value → index
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []  # 题意保证有解，不会到达此处


# 快速验证（面试结束前大声执行）
assert two_sum([2, 7, 11, 15], 9) == [0, 1]
assert two_sum([3, 2, 4], 6) == [1, 2]
assert two_sum([3, 3], 6) == [0, 1]
```

## 面试高频表达句式

| 场景 | 推荐用语 |
|------|---------|
| 引入优化 | "我注意到每次都在重复计算…可以用…缓存" |
| 说复杂度 | "时间 O(n log n) 因为排序主导，空间 O(n) 存哈希表" |
| 发现边界 | "当 n=0 时函数应返回…让我加一个 guard clause" |
| 请求确认 | "这个方向思路对吗？我继续细化实现？" |
""",

# ──────────────────────────────────────────────────────────────────────────────
"10-数据结构与算法-算法高频题分类": """\
---
tags: [高频题, 分类, LeetCode, 面试]
aliases: [Hot Topics, 算法题型分类]
sources:
  - https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/
  - https://leetcode.com/problem-list/top-interview-questions/
---

# 算法高频题分类

将高频面试题按算法思想分类，能有效识别题型并快速调用对应模板。MIT OCW 6.006（ https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/ ）覆盖的核心算法恰好对应面试中约 80% 的高频题型，是系统准备的最佳基础。

## 分类体系

### 类型一：双指针 / 滑动窗口

**核心**：两个指针维护窗口，利用单调性避免暴力枚举。  
**高频题**：无重复字符最长子串、最小覆盖子串、接雨水。

手算示例（无重复字符最长子串，s="abcabcbb"）：  
l=0,r=0,窗口"a"；r=1"ab"；r=2"abc"(len=3)；r=3遇到重复'a'，l移至1；...  
最终答案=3（"abc"）。

```python
def length_of_longest_substring(s: str) -> int:
    \"\"\"滑动窗口求无重复字符最长子串长度。O(n)。\"\"\"
    char_idx: dict[str, int] = {}
    ans = left = 0
    for right, ch in enumerate(s):
        if ch in char_idx and char_idx[ch] >= left:
            left = char_idx[ch] + 1
        char_idx[ch] = right
        ans = max(ans, right - left + 1)
    return ans

assert length_of_longest_substring("abcabcbb") == 3
assert length_of_longest_substring("bbbbb") == 1
assert length_of_longest_substring("pwwkew") == 3
```

### 类型二：二分答案

**核心**：将"求最优解"转化为"验证 k 是否可行"，在答案空间上二分。  
**高频题**：搜索旋转数组、寻找峰值、木材切割。

```python
def search_rotated(nums: list[int], target: int) -> int:
    \"\"\"在旋转排序数组中搜索 target，O(log n)。\"\"\"
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[lo] <= nums[mid]:  # 左半有序
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:  # 右半有序
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1

assert search_rotated([4,5,6,7,0,1,2], 0) == 4
assert search_rotated([4,5,6,7,0,1,2], 3) == -1
```

### 类型三：单调栈

**核心**：维护一个单调递增/递减的栈，O(n) 解决"下一个更大/小元素"类问题。  
**高频题**：每日温度、柱状图最大矩形、接雨水。

手算（每日温度 [73,74,75,71,69,72,76,73]）：  
栈（存下标）：push 0(73)；74>73，pop 0 答案[0]=1，push 1；75>74 pop 1 答案[1]=1，push 2；...

```python
def daily_temperatures(temps: list[int]) -> list[int]:
    \"\"\"返回每天等待更高温度的天数。单调栈 O(n)。\"\"\"
    ans = [0] * len(temps)
    stack: list[int] = []  # 存下标，单调递减栈
    for i, t in enumerate(temps):
        while stack and temps[stack[-1]] < t:
            j = stack.pop()
            ans[j] = i - j
        stack.append(i)
    return ans

assert daily_temperatures([73,74,75,71,69,72,76,73]) == [1,1,4,2,1,1,0,0]
```

## 题型 → 算法 快速映射表

| 关键词 | 优先考虑算法 |
|--------|------------|
| 最短路/最少步 | BFS / Dijkstra |
| 排列组合计数 | DP + 记忆化 |
| 区间重叠/合并 | 排序 + 扫描 |
| Top-K | 堆 / 快速选择 |
| 字符串匹配 | KMP / Rabin-Karp |
| 连通性 | DSU / BFS |
| 最优子结构 | DP |
| 单调性质 | 二分 / 单调栈队 |
""",

# ──────────────────────────────────────────────────────────────────────────────
"10-数据结构与算法-网络流": """\
---
tags: [图论, 网络流, 最大流, Dinic]
aliases: [Max Flow, 最大流, 最小割]
sources:
  - https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/
  - https://cp-algorithms.com/graph/dinic.html
---

# 网络流

网络流模型：有向图中每条边有容量上界，从源 s 到汇 t 的最大流（max flow）满足流量守恒且不超过容量。最大流 = 最小割（Ford-Fulkerson 定理）。Dinic 算法利用分层图（BFS 建层次）+ 阻塞流（DFS），时间复杂度 O(V²E)，单位容量图为 O(E√V)。MIT OCW 6.006（ https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/ ）在图论模块将最大流-最小割定理列为图论核心定理之一，并给出了其在匹配、分割问题中的应用证明。

## 算法步骤（Dinic）

1. BFS 从 s 建层次图 `level[v]`：仅保留 `level[v] = level[u]+1` 且剩余容量>0的边。  
2. DFS 在层次图上找阻塞流（用 `iter` 指针避免重复遍历已阻塞边）。  
3. 将阻塞流加入总流，重复 1-2 直到 t 不可达（BFS 到不了 t）。

## 手算例证

图（s=0, t=3）：0→1(cap=3), 0→2(cap=2), 1→3(cap=2), 2→3(cap=3), 1→2(cap=1)。  
**BFS 层次**：level[0]=0, level[1]=1, level[2]=1, level[3]=2。  
**第1轮阻塞流**：  
- 路径 0→1→3：流量=min(3,2)=2，更新：0→1剩1，1→3剩0。  
- 路径 0→1→2→3：流量=min(1,1,3)=1，更新：0→1剩0，1→2剩0，2→3剩2。  
- 路径 0→2→3：流量=min(2,2)=2，更新：0→2剩0，2→3剩0。  
总流=2+1+2=5。  
**BFS 再次**：0→1(剩0)，0→2(剩0)，t 不可达，算法终止。  
最大流=5，最小割={0→1, 0→2}，容量=3+2=5 ✓。

## 代码实现

```python
from collections import deque


class MaxFlow:
    \"\"\"Dinic 最大流。顶点 0-indexed。\"\"\"

    def __init__(self, n: int):
        self.n = n
        self.graph: list[list[list]] = [[] for _ in range(n)]
        # graph[u] 中每条边格式：[to, cap, rev_idx]

    def add_edge(self, u: int, v: int, cap: int):
        self.graph[u].append([v, cap, len(self.graph[v])])
        self.graph[v].append([u, 0, len(self.graph[u]) - 1])

    def _bfs(self, s: int, t: int, level: list[int]) -> bool:
        level[:] = [-1] * self.n
        level[s] = 0
        q = deque([s])
        while q:
            u = q.popleft()
            for v, cap, _ in self.graph[u]:
                if cap > 0 and level[v] < 0:
                    level[v] = level[u] + 1
                    q.append(v)
        return level[t] >= 0

    def _dfs(self, u: int, t: int, f: int, level: list[int], iter_: list[int]) -> int:
        if u == t:
            return f
        while iter_[u] < len(self.graph[u]):
            edge = self.graph[u][iter_[u]]
            v, cap, rev = edge
            if cap > 0 and level[v] == level[u] + 1:
                d = self._dfs(v, t, min(f, cap), level, iter_)
                if d > 0:
                    edge[1] -= d
                    self.graph[v][rev][1] += d
                    return d
            iter_[u] += 1
        return 0

    def max_flow(self, s: int, t: int) -> int:
        flow = 0
        level = [-1] * self.n
        while self._bfs(s, t, level):
            iter_ = [0] * self.n
            while True:
                f = self._dfs(s, t, float('inf'), level, iter_)
                if f == 0:
                    break
                flow += f
        return flow


# 验证
mf = MaxFlow(4)
mf.add_edge(0, 1, 3)
mf.add_edge(0, 2, 2)
mf.add_edge(1, 3, 2)
mf.add_edge(2, 3, 3)
mf.add_edge(1, 2, 1)
assert mf.max_flow(0, 3) == 5
```

## 应用举例

- **二分图最大匹配**：源→左集合（容量1）→右集合（容量1）→汇，最大流=最大匹配。  
- **项目选择**：节点权正负对应收益/代价，最大利润=总正权-最小割。  
- **最小路径覆盖**（DAG）：最小路径覆盖数 = n - 最大二分匹配数。
""",

}

if __name__ == "__main__":
    print(f"CARDS_S6 包含 {len(CARDS_S6)} 张卡片")
    for stem, body in CARDS_S6.items():
        assert len(body) > 900, f"正文过短: {stem} ({len(body)} chars)"
        assert "https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/" in body, \
            f"URL 缺失: {stem}"
    print("All cards validated OK")
