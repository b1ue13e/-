---
type: study
topic: "AC自动机"
course: "数据结构与算法"
created: 2026-08-07
status: completed
stage_moc: "[[🧭 阶段6-高级与综合训练]]"
flow: knowledge
kind: concept
---

# 数据结构与算法-AC自动机

> **摘要**：AC 自动机（Aho-Corasick Automaton）是用于解决多模式串匹配问题的经典数据结构。它将字典树（Trie）与 KMP 算法的 Fail 指针思想相结合，能够在 $O(N + \sum |P_i|)$ 的时间复杂度内完成文本串中多个模式串的查找。

---

## 1. 💡 问题动机与核心直觉

### 1.1 单模式串 vs 多模式串匹配
在文本检索中：
- **单模式串匹配**：使用 KMP 算法，文本串长度 $N$，模式串长度 $M$，时间复杂度 $O(N + M)$。
- **多模式串匹配**：文本串长度 $N$，包含 $k$ 个模式串 $P_1, P_2, \dots, P_k$。若逐一运行 KMP，时间复杂度为 $O(k \cdot N + \sum |P_i|)$。当 $k$ 很大时性能剧烈下降。

### 1.2 AC 自动机的核心直觉
AC 自动机通过以下两步解决多模式串检索：
1. **构建 Trie 树**：将所有模式串插入到一棵字典树中，实现前缀共享。
2. **构建 Fail 指针（失配指针）**：类似 KMP 算法的 `next` 数组。当在 Trie 树的某个节点失配时，跳转到**在 Trie 中存在的最长可匹配后缀节点**，避免回溯文本串指针。

---

## 2. 📐 正式定义与算法流程

### 2.1 Fail 指针的定义
记节点 $u$ 对应的字符串为 $S(u)$。$u$ 的 `fail` 指针指向节点 $v$，当且仅当 $S(v)$ 是 $S(u)$ 的**最长真后缀**，且 $v$ 在 Trie 树中存在。

### 2.2 构建 Fail 指针的 BFS 算法
Fail 指针按**层级（BFS 广度优先搜索）**构造：
1. **根节点（Root，深度 0）** 的所有直接子节点的 `fail` 指向根节点，并将这些直接子节点加入队列。
2. **队首出列节点 $u$**：
   - 遍历其所有字符 $c$ 的子节点 $v = \text{trie}[u][c]$：
     - 若子节点 $v$ 存在：$\text{fail}[v] = \text{trie}[\text{fail}[u]][c]$，并将 $v$ 入队。
     - 若子节点 $v$ 不存在（构造字典图 Trie Graph 优化）：可直接将 $\text{trie}[u][c]$ 赋值为 $\text{trie}[\text{fail}[u]][c]$，避免重复向上回溯。

---

## 3. 💻 Python 核心实现

```python
from collections import deque

class ACNode:
    def __init__(self):
        self.children = {}
        self.fail = None
        self.output = []  # 记录在该节点结尾的模式串索引或值

class ACAutomaton:
    def __init__(self):
        self.root = ACNode()

    def insert(self, pattern: str, pattern_id: int):
        node = self.root
        for char in pattern:
            if char not in node.children:
                node.children[char] = ACNode()
            node = node.children[char]
        node.output.append(pattern_id)

    def build_fail(self):
        queue = deque()
        # 根节点的直接子节点 fail 指向 root
        for char, child in self.root.children.items():
            child.fail = self.root
            queue.append(child)

        while queue:
            curr = queue.popleft()

            for char, child in curr.children.items():
                fail_node = curr.fail
                while fail_node and char not in fail_node.children:
                    fail_node = fail_node.fail
                
                child.fail = fail_node.children[char] if fail_node else self.root
                # 继承 fail 节点的匹配输出（后缀匹配）
                child.output.extend(child.fail.output)
                queue.append(child)

    def search(self, text: str):
        results = []
        curr = self.root

        for idx, char in enumerate(text):
            while curr and char not in curr.children:
                curr = curr.fail
            curr = curr.children[char] if curr else self.root
            
            # 收集当前匹配到的模式串
            if curr.output:
                for pattern_id in curr.output:
                    results.append((idx, pattern_id))

        return results
```

---

## 4. ⚠️ 常见误区与优化点

1. **死循环与 Fail 递归**：在未构建 Trie 图的情况下，若字符不在 `fail` 节点子节点中，需循环向上查找直到根节点；构建 Trie 图（Trie Graph）可将时间优化至严格线性。
2. **重复计数问题**：由于一个节点的 `fail` 指针可能指向另一个模式串的结尾节点，检索时必须合并 `fail` 链上的 `output`。

---

## 5. 🃏 Anki 闭卷自测点

- **Q1**: AC 自动机中 Fail 指针的几何含义是什么？它与 KMP 的 `next` 数组有何异同？
- **Q2**: 为什么构建 AC 自动机的 Fail 指针必须使用 BFS 广度优先搜索而不能使用 DFS？

---

## 6. 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
