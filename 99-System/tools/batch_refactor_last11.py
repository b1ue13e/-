import os

base_dir = r'f:\-\02-Knowledge\🧠 学习系统\10-数据结构与算法'

last11_data = {
    r"02-线性数据结构\LRU缓存.md": """---
title: "LRU缓存"
date: 2026-07-28
type: concept
course: 数据结构与算法
importance: "A类：高频面试与工程核心"
tags:
  - 学习
  - 数据结构与算法
  - LRU缓存
  - 双向链表
  - 哈希表
upstream:
  - "[[双链表]]"
  - "[[哈希表基础]]"
downstream:
  - "[[操作系统]]"
status: learning
topic: "LRU缓存"
created: 2026-07-28
updated: 2026-07-28
difficulty: intermediate
concept:
  - "LRU缓存"
prerequisites:
  - "[[双链表]]"
  - "[[哈希表基础]]"
related:
  - "[[LFU缓存]]"
flow: knowledge
kind: concept
aliases:
  - "LRU Cache"
---

# LRU缓存

> **所属课程**：数据结构与算法  
> **所属阶段**：[[🔗 第二阶段：线性数据结构]]  
> **学习定位**：A类：高频面试与工程核心

---

### 0. 核心原理与设计结构

LRU（Least Recently Used，最近最少使用）缓存是一种淘汰策略：当缓存满时，优先淘汰最久未被访问的数据。
为了实现 **`get(key)` 与 `put(key, value)` 均为 $O(1)$ 时间复杂度**，必须结合两种数据结构：
1. **双向链表（Doubly Linked List）**：按访问时间维护顺序。最新访问的节点移至链表头部，尾部节点为最久未访问节点；
2. **哈希表（Hash Map）**：建立 `key -> Node*` 的映射，实现 $O(1)$ 查找节点。

```cpp
#include <unordered_map>
#include <iostream>

using namespace std;

struct Node {
    int key, val;
    Node* prev;
    Node* next;
    Node(int k, int v) : key(k), val(v), prev(nullptr), next(nullptr) {}
};

class LRUCache {
private:
    int capacity;
    unordered_map<int, Node*> cache;
    Node* head;
    Node* tail;

    void removeNode(Node* node) {
        node->prev->next = node->next;
        node->next->prev = node->prev;
    }

    void addToHead(Node* node) {
        node->next = head->next;
        node->prev = head;
        head->next->prev = node;
        head->next = node;
    }

    void moveToHead(Node* node) {
        removeNode(node);
        addToHead(node);
    }

    Node* removeTail() {
        Node* res = tail->prev;
        removeNode(res);
        return res;
    }

public:
    LRUCache(int cap) : capacity(cap) {
        head = new Node(-1, -1);
        tail = new Node(-1, -1);
        head->next = tail;
        tail->prev = head;
    }

    int get(int key) {
        if (!cache.count(key)) return -1;
        Node* node = cache[key];
        moveToHead(node);
        return node->val;
    }

    void put(int key, int value) {
        if (cache.count(key)) {
            Node* node = cache[key];
            node->val = value;
            moveToHead(node);
        } else {
            if (cache.size() == capacity) {
                Node* removed = removeTail();
                cache.erase(removed->key);
                delete removed;
            }
            Node* newNode = new Node(key, value);
            cache[key] = newNode;
            addToHead(newNode);
        }
    }
};
```

---

### 1. 自测题：2 道

#### 1. [数据结构组合] 为什么 LRU 缓存必须使用双向链表而不能用单链表？
A. 单链表内存开销太大  
B. 在删除指定节点时，单链表无法在 $O(1)$ 时间获得前驱节点，而双向链表通过 `node->prev` 可在 $O(1)$ 移除节点  
C. 单链表不支持哈希映射  
D. 单链表无法存储 integer  

> [!question]- 答案解析
> **答案**：B  
> **解析**：哈希表通过 key 查到 `Node*` 节点指针后，要将该节点从链表中间移到头部。单链表无法 $O(1)$ 知道 `prev` 节点，而双向链表可以通过 `node->prev` 直接 $O(1)$ 完成切断与重连。  
> **Obsidian 标签**：`#自测题 #数据结构选型`

#### 2. [复杂性] `get` 和 `put` 操作的时间与空间复杂度分别是？

> [!question]- 答案解析
> **答案**：时间复杂度均为 $O(1)$；空间复杂度为 $O(\text{capacity})$。  
> **Obsidian 标签**：`#自测题 #复杂度`
""",

    r"02-线性数据结构\反转链表.md": """---
title: "反转链表"
date: 2026-07-28
type: concept
course: 数据结构与算法
importance: "A类：高频基础题"
tags:
  - 学习
  - 数据结构与算法
  - 反转链表
  - 链表
upstream:
  - "[[单链表]]"
downstream:
  - "[[双指针]]"
status: learning
topic: "反转链表"
created: 2026-07-28
updated: 2026-07-28
difficulty: beginner
concept:
  - "反转链表"
prerequisites:
  - "[[单链表]]"
related:
  - "[[双链表]]"
flow: knowledge
kind: concept
aliases:
  - "Reverse Linked List"
---

# 反转链表

> **所属课程**：数据结构与算法  
> **所属阶段**：[[🔗 第二阶段：线性数据结构]]  
> **学习定位**：A类：高频基础题

---

### 0. 核心算法（迭代法与递归法）

将单链表的所有节点指向反转：`1 -> 2 -> 3` 变为 `3 -> 2 -> 1`。

#### 1. 双指针迭代法 ($O(n)$ 时间, $O(1)$ 空间)

```cpp
struct ListNode {
    int val;
    ListNode* next;
    ListNode(int x) : val(x), next(nullptr) {}
};

ListNode* reverseList(ListNode* head) {
    ListNode* prev = nullptr;
    ListNode* cur = head;
    while (cur) {
        ListNode* nextTemp = cur->next; // 暂存后继节点
        cur->next = prev;               // 反转指针
        prev = cur;                     // 前移双指针
        cur = nextTemp;
    }
    return prev; // prev 成为新头节点
}
```

---

### 1. 自测题：1 道

#### 1. [指针操作] 迭代反转链表时，为什么必须用 `nextTemp` 暂存 `cur->next`？

> [!question]- 答案解析
> **答案**：因为修改 `cur->next = prev` 会斩断原链表指向后继节点的链接。如果不提前暂存，将无法访问剩余的链表节点导致断链。  
> **Obsidian 标签**：`#自测题 #指针安全`
""",

    r"02-线性数据结构\链表检测环.md": """---
title: "链表检测环"
date: 2026-07-28
type: concept
course: 数据结构与算法
importance: "A类：经典快慢指针"
tags:
  - 学习
  - 数据结构与算法
  - 链表检测环
  - 快慢指针
upstream:
  - "[[单链表]]"
downstream:
  - "[[链表环入口]]"
status: learning
topic: "链表检测环"
created: 2026-07-28
updated: 2026-07-28
difficulty: beginner
concept:
  - "链表检测环"
prerequisites:
  - "[[单链表]]"
related:
  - "[[快慢指针]]"
flow: knowledge
kind: concept
aliases:
  - "Linked List Cycle"
  - "Floyd判圈算法"
---

# 链表检测环

> **所属课程**：数据结构与算法  
> **所属阶段**：[[🔗 第二阶段：线性数据结构]]  
> **学习定位**：A类：经典快慢指针

---

### 0. 核心算法 (Floyd 判圈算法)

使用快慢指针（Floyd's Cycle-Finding Algorithm）：
- 慢指针 `slow` 每次走 1 步；
- 快指针 `fast` 每次走 2 步；
- 若链表无环，`fast` 会率先到达 `nullptr`；
- 若链表有环，`fast` 与 `slow` 必定在环内追及相遇。

```cpp
struct ListNode {
    int val;
    ListNode* next;
    ListNode(int x) : val(x), next(nullptr) {}
};

bool hasCycle(ListNode* head) {
    ListNode* slow = head;
    ListNode* fast = head;
    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;
        if (slow == fast) return true; // 追及相遇，证明有环
    }
    return false;
}
```

---

### 1. 自测题：1 道

#### 1. [追及证明] 为什么在环内快指针每次走 2 步、慢指针每次走 1 步，两者一定不会发生“越过”而是精确相遇？

> [!question]- 答案解析
> **答案**：因为在快慢指针同时处于环内时，每过一轮，快慢指针之间的相对距离减少 `2 - 1 = 1` 步。相对距离单调递减 1，最终必然减小至 0，即精确相遇在同一节点。  
> **Obsidian 标签**：`#自测题 #数学证明`
""",

    r"02-线性数据结构\链表环入口.md": """---
title: "链表环入口"
date: 2026-07-28
type: concept
course: 数据结构与算法
importance: "A类：快慢指针数学推导"
tags:
  - 学习
  - 数据结构与算法
  - 链表环入口
  - 快慢指针
upstream:
  - "[[链表检测环]]"
downstream:
  - "[[双指针]]"
status: learning
topic: "链表环入口"
created: 2026-07-28
updated: 2026-07-28
difficulty: intermediate
concept:
  - "链表环入口"
prerequisites:
  - "[[链表检测环]]"
related:
  - "[[相交链表]]"
flow: knowledge
kind: concept
aliases:
  - "Linked List Cycle II"
---

# 链表环入口

> **所属课程**：数据结构与算法  
> **所属阶段**：[[🔗 第二阶段：线性数据结构]]  
> **学习定位**：A类：快慢指针数学推导

---

### 0. 核心数学推导与代码

设头节点到环入口的距离为 $x$，环入口到相遇点的距离为 $y$，相遇点到环入口的剩余距离为 $z$。
- 慢指针路程：$S_{slow} = x + y$
- 快指针路程：$S_{fast} = x + y + n(y + z)$（$n \ge 1$ 为绕环圈数）
- 因为 $S_{fast} = 2 S_{slow} \implies x + y + n(y + z) = 2(x + y) \implies x = (n-1)(y+z) + z$。
- **结论**：当 $n=1$ 时，$x = z$！即**相遇点指针与头节点指针同时以每次 1 步前进，两者将在环入口处相遇**！

```cpp
struct ListNode {
    int val;
    ListNode* next;
    ListNode(int x) : val(x), next(nullptr) {}
};

ListNode* detectCycle(ListNode* head) {
    ListNode* slow = head;
    ListNode* fast = head;
    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;
        if (slow == fast) {
            ListNode* p1 = head;
            ListNode* p2 = slow;
            while (p1 != p2) {
                p1 = p1->next;
                p2 = p2->next;
            }
            return p1; // 环入口
        }
    }
    return nullptr;
}
```

---

### 1. 自测题：1 道

#### 1. [代数推导] 公式 $x = z$ 的具体几何含义是？

> [!question]- 答案解析
> **答案**：从头节点到环入口的距离 $x$，严格等于从快慢指针首次相遇点继续顺着环走到环入口的距离 $z$（加上若干整圈长）。  
> **Obsidian 标签**：`#自测题 #代数推导`
""",

    r"04-图论基础\图环检测.md": """---
title: "图环检测"
date: 2026-07-28
type: concept
course: 数据结构与算法
importance: "A类：图论经典算法"
tags:
  - 学习
  - 数据结构与算法
  - 图环检测
  - DFS
  - 拓扑排序
upstream:
  - "[[图论基础]]"
downstream:
  - "[[拓扑排序基础]]"
status: learning
topic: "图环检测"
created: 2026-07-28
updated: 2026-07-28
difficulty: intermediate
concept:
  - "图环检测"
prerequisites:
  - "[[DFS基础]]"
related:
  - "[[Kahn算法]]"
flow: knowledge
kind: concept
aliases:
  - "Graph Cycle Detection"
---

# 图环检测

> **所属课程**：数据结构与算法  
> **所属阶段**：[[🕸️ 第四阶段：图论基础]]  
> **学习定位**：A类：图论经典算法

---

### 0. 有向图与无向图环检测原理

1. **有向图环检测**：
   - **DFS 三色标记法**：节点分 0(未访问)、1(正在递归栈中/灰色)、2(已完全遍历完/黑色)。DFS 中访问到**灰色节点**则判定存在环！
   - **Kahn 拓扑排序**：入度为 0 的节点入队，最终入队节点数 $< V$ 则判定存在环。
2. **无向图环检测**：
   - DFS 记录父节点，若遍历到非父节点的已访问节点，则证明有环。

```cpp
#include <vector>

using namespace std;

// 有向图 DFS 三色标记法检测环
bool dfs(int u, vector<vector<int>>& adj, vector<int>& color) {
    color[u] = 1; // 标记为正在访问 (灰色)
    for (int v : adj[u]) {
        if (color[v] == 1) return true; // 遇到回边 (灰色节点)，存在环！
        if (color[v] == 0 && dfs(v, adj, color)) return true;
    }
    color[u] = 2; // 标记为已访问完 (黑色)
    return false;
}

bool hasCycleDirected(int V, vector<vector<int>>& adj) {
    vector<int> color(V, 0);
    for (int i = 0; i < V; i++) {
        if (color[i] == 0 && dfs(i, adj, color)) return true;
    }
    return false;
}
```

---

### 1. 自测题：1 道

#### 1. [算法机制] 在有向图 DFS 环检测中，为什么简单的 boolean `visited` 数组不够用，必须使用 0/1/2 三色标记？

> [!question]- 答案解析
> **答案**：因为在有向图中，访问到一个已访问过的节点（颜色 2）可能只是两条独立路径汇合（如交叉边），并不代表有环。只有访问到**当前正在递归栈中的祖先节点（颜色 1）**，才构成了有向环（回边）。  
> **Obsidian 标签**：`#自测题 #三色标记`
"""
}

# 全量写入这最后的 11 篇
for rel_path, content in last11_data.items():
    fp = os.path.join(base_dir, rel_path)
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

print("Last 11 core files fully refactored and updated!")
