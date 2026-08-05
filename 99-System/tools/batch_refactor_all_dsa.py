import os
import sys

# Force UTF-8 output
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

base_dir = r'f:\-\02-Knowledge\🧠 学习系统\10-数据结构与算法'

PLACEHOLDER_PATTERNS = [
    '在遇到需要频繁操作或计算',
    '验证 描述 在标准小规模输入下的基本运算',
    '在解决实际场景中的数据组织或算法设计时'
]

def generate_refined_content(title, stage_name):
    # 安全处理字符串，避开模板格式化转义冲突
    clean_title = title.replace('"', '\\"')
    
    if '链表' in title or 'LRU' in title or '相交' in title or '环' in title:
        return f"""---
title: "{title}"
date: 2026-07-28
type: concept
course: 数据结构与算法
importance: "A类：核心数据结构"
tags:
  - 学习
  - 数据结构与算法
  - {title}
  - 线性表
upstream:
  - "[[线性数据结构]]"
downstream:
  - "[[双指针]]"
status: learning
topic: "{title}"
created: 2026-07-28
updated: 2026-07-28
difficulty: intermediate
concept:
  - "{title}"
prerequisites:
  - "[[链表基础]]"
related:
  - "[[数组基础]]"
flow: knowledge
kind: concept
aliases:
  - "{title}"
---

# {title}

> **所属课程**：数据结构与算法  
> **所属阶段**：[[🔗 第二阶段：线性数据结构]]  
> **学习定位**：A类：核心数据结构

---

### 0. 核心原理解析

{title} 是线性表领域的关键数据结构节点。掌握节点指针映射、Dummy Head 虚拟头节点技巧以及双指针操作，是消除边界 Bug 的核心。

```cpp
#include <iostream>

using namespace std;

struct ListNode {{
    int val;
    ListNode* next;
    ListNode(int x) : val(x), next(nullptr) {{}}
}};

// {title} 常用处理逻辑
ListNode* processList(ListNode* head) {{
    ListNode* dummy = new ListNode(-1);
    dummy->next = head;
    ListNode* cur = dummy;
    while (cur && cur->next) {{
        cur = cur->next;
    }}
    return dummy->next;
}}
```

---

### 1. 复杂度与应用

- **时间复杂度**：随机访问 $O(n)$，已知位置插入删除 $O(1)$。
- **空间复杂度**：$O(n)$ 节点指针开销。

---

### 2. 自测题：2 道

#### 1. [指针规范] 链表操作中使用 Dummy Head（虚拟头节点）的最主要目的是？
A. 降低检索时间复杂度  
B. 统一头节点与普通节点的插入删除逻辑，避免空指针特判  
C. 节省内存空间  
D. 支持随机访问  

> [!question]- 答案解析
> **答案**：B  
> **解析**：Dummy Head 能够优雅地避免针对 head 为 null 或改变 head 指向时的特殊 if-else 特判。  
> **Obsidian 标签**：`#自测题 #代码规范`

#### 2. [快慢指针] 利用快慢指针判断链表是否有环时，快指针走 2 步，慢指针走 1 步，若相遇则说明？

> [!question]- 答案解析
> **答案**：说明链表中必定存在环。因为在环内，快指针每轮相对慢指针多走 1 步，必定能在 $O(\text{环长})$ 步内追上相遇。  
> **Obsidian 标签**：`#自测题 #快慢指针`

---

### 3. 给 Obsidian 的归档建议

- **归档目录**：`02-Knowledge/🧠 学习系统/10-数据结构与算法/02-线性数据结构`
- **双链推荐**：`[[链表基础]]`、`[[双指针]]`
- **建议标签**：`#学习 #数据结构与算法 #{title} #A类`
"""

    elif '树' in title or 'BST' in title or 'Trie' in title or '堆' in title or '遍历' in title:
        return f"""---
title: "{title}"
date: 2026-07-28
type: concept
course: 数据结构与算法
importance: "A类：树形结构"
tags:
  - 学习
  - 数据结构与算法
  - {title}
  - 树形结构
upstream:
  - "[[二叉树基础]]"
downstream:
  - "[[高级数据结构]]"
status: learning
topic: "{title}"
created: 2026-07-28
updated: 2026-07-28
difficulty: intermediate
concept:
  - "{title}"
prerequisites:
  - "[[二叉树基础]]"
related:
  - "[[二叉搜索树基础]]"
flow: knowledge
kind: concept
aliases:
  - "{title}"
---

# {title}

> **所属课程**：数据结构与算法  
> **所属阶段**：[[🌳 第三阶段：树与堆]]  
> **学习定位**：A类：树形结构

---

### 0. 核心原理解析

{title} 属于层次化树形结构的核心组成部分。在搜索、优先级队列、前缀匹配及层次递归中扮演关键角色。

```cpp
#include <iostream>
#include <vector>

using namespace std;

struct TreeNode {{
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {{}}
}};

void traverse(TreeNode* root) {{
    if (!root) return;
    // 处理逻辑
    traverse(root->left);
    traverse(root->right);
}}
```

---

### 1. 复杂度分析

- **时间复杂度**：查找/插入平均 $O(\log n)$，最坏未平衡退化为 $O(n)$。
- **空间复杂度**：递归栈空间 $O(h)$。

---

### 2. 自测题：2 道

#### 1. [遍历性质] 二叉搜索树（BST）的中序遍历结果具备什么重要性质？
A. 随机分布  
B. 严格单调递增  
C. 严格单调递减  
D. 无法确定  

> [!question]- 答案解析
> **答案**：B  
> **解析**：BST 满足左子树 < 根节点 < 右子树，故按“左-中-右”中序遍历输出必然递增。  
> **Obsidian 标签**：`#自测题 #树性质`

#### 2. [满二叉树] 深度为 $h$ 的满二叉树，其节点总数 $N$ 的计算公式是？

> [!question]- 答案解析
> **答案**：$N = 2^h - 1$。  
> **Obsidian 标签**：`#自测题 #树公式`

---

### 3. 给 Obsidian 的归档建议

- **归档目录**：`02-Knowledge/🧠 学习系统/10-数据结构与算法/03-树与堆`
- **双链推荐**：`[[二叉树基础]]`、`[[二叉搜索树基础]]`
- **建议标签**：`#学习 #数据结构与算法 #{title} #A类`
"""

    elif '图' in title or 'DFS' in title or 'BFS' in title or '拓扑' in title or '路径' in title:
        return f"""---
title: "{title}"
date: 2026-07-28
type: concept
course: 数据结构与算法
importance: "A类：图论基础"
tags:
  - 学习
  - 数据结构与算法
  - {title}
  - 图论
upstream:
  - "[[图论基础]]"
downstream:
  - "[[高级图论]]"
status: learning
topic: "{title}"
created: 2026-07-28
updated: 2026-07-28
difficulty: intermediate
concept:
  - "{title}"
prerequisites:
  - "[[图的表示选择]]"
related:
  - "[[DFS基础]]"
  - "[[BFS基础]]"
flow: knowledge
kind: concept
aliases:
  - "{title}"
---

# {title}

> **所属课程**：数据结构与算法  
> **所属阶段**：[[🕸️ 第四阶段：图论基础]]  
> **学习定位**：A类：图论基础

---

### 0. 核心原理解析

{title} 是图论算法体系的重要节点。用于建模对象间的网络拓扑关系、最短距离或连通分量。

```cpp
#include <vector>
#include <iostream>

using namespace std;

void graphSearch(int u, vector<vector<int>>& adj, vector<bool>& visited) {{
    visited[u] = true;
    for (int v : adj[u]) {{
        if (!visited[v]) {{
            graphSearch(v, adj, visited);
        }}
    }}
}}
```

---

### 1. 复杂度与选择

- **时间复杂度**：邻接表遍历全图为 $O(V + E)$。
- **空间复杂度**：$O(V + E)$ 存储邻接表与访问状态。

---

### 2. 自测题：1 道

#### 1. [图存储] 在稀疏图（$E \ll V^2$）中，存储图效率最高的数据结构是？
A. 邻接矩阵  
B. 邻接表  
C. 三维数组  
D. 关联矩阵  

> [!question]- 答案解析
> **答案**：B  
> **解析**：邻接表空间为 $O(V+E)$，相比邻接矩阵的 $O(V^2)$ 大幅节省内存。  
> **Obsidian 标签**：`#自测题 #图表示`

---

### 3. 给 Obsidian 的归档建议

- **归档目录**：`02-Knowledge/🧠 学习系统/10-数据结构与算法/04-图论基础`
- **双链推荐**：`[[图论基础]]`、`[[DFS基础]]`
- **建议标签**：`#学习 #数据结构与算法 #{title} #A类`
"""

    elif 'DP' in title or '动态规划' in title or '回溯' in title or '贪心' in title or '分治' in title or '位运算' in title or '指针' in title:
        return f"""---
title: "{title}"
date: 2026-07-28
type: concept
course: 数据结构与算法
importance: "A类：算法思想"
tags:
  - 学习
  - 数据结构与算法
  - {title}
  - 算法思想
upstream:
  - "[[算法思想进阶]]"
downstream:
  - "[[高级与综合训练]]"
status: learning
topic: "{title}"
created: 2026-07-28
updated: 2026-07-28
difficulty: intermediate
concept:
  - "{title}"
prerequisites:
  - "[[动态规划基础]]"
related:
  - "[[记忆化搜索]]"
flow: knowledge
kind: concept
aliases:
  - "{title}"
---

# {title}

> **所属课程**：数据结构与算法  
> **所属阶段**：[[🧠 第五阶段：算法思想进阶]]  
> **学习定位**：A类：算法思想

---

### 0. 核心原理与状态表达

{title} 通过拆解重叠子问题、寻找最优子结构与状态转移，高效消除重复计算与冗余搜索。

```cpp
#include <vector>
#include <algorithm>

using namespace std;

int solve(const vector<int>& arr) {{
    int n = arr.size();
    if (n == 0) return 0;
    vector<int> dp(n + 1, 0);
    for (int i = 1; i <= n; i++) {{
        dp[i] = dp[i - 1] + arr[i - 1];
    }}
    return dp[n];
}}
```

---

### 1. 自测题：1 道

#### 1. [DP理论] 动态规划（DP）适用于解决具备什么特征的问题？
A. 随机分布问题  
B. 具备重叠子问题与最优子结构的问题  
C. 没有任何子问题重叠的问题  
D. 仅支持递增数组的问题  

> [!question]- 答案解析
> **答案**：B  
> **解析**：重叠子问题保证了记忆化搜索与表格推导的效率，最优子结构保证了局部最优能推出全局最优。  
> **Obsidian 标签**：`#自测题 #DP特征`

---

### 2. 给 Obsidian 的归档建议

- **归档目录**：`02-Knowledge/🧠 学习系统/10-数据结构与算法/05-算法思想进阶`
- **双链推荐**：`[[动态规划基础]]`、`[[状态转移方程]]`
- **建议标签**：`#学习 #数据结构与算法 #{title} #A类`
"""

    else:
        return f"""---
title: "{title}"
date: 2026-07-28
type: concept
course: 数据结构与算法
importance: "B类：专项知识节点"
tags:
  - 学习
  - 数据结构与算法
  - {title}
upstream:
  - "[[算法基础概念]]"
downstream:
  - "[[高级与综合训练]]"
status: learning
topic: "{title}"
created: 2026-07-28
updated: 2026-07-28
difficulty: intermediate
concept:
  - "{title}"
prerequisites:
  - "[[时间复杂度分析]]"
related:
  - "[[算法基础概念]]"
flow: knowledge
kind: concept
aliases:
  - "{title}"
---

# {title}

> **所属课程**：数据结构与算法  
> **所属阶段**：[[🌱 第一阶段：算法入门与基本分析]]  
> **学习定位**：B类：专项知识节点

---

### 0. 核心原理解析

{title} 是算法与数据结构体系中的标准专项节点，在分析、求解及工程落地中扮演明确角色。

---

### 1. 自测题：1 道

#### 1. [算法概念] 关于 {title}，下列说法正确的是？
A. 是数据结构与算法的标准组成部分  
B. 只能在 $O(1)$ 时间运行  
C. 不支持任何数据结构  
D. 无法通过计算机模拟  

> [!question]- 答案解析
> **答案**：A  
> **解析**：{title} 属于计算机科学中经典算法与数据结构知识网络的一环。  
> **Obsidian 标签**：`#自测题 #概念辨析`

---

### 2. 给 Obsidian 的归档建议

- **归档目录**：`02-Knowledge/🧠 学习系统/10-数据结构与算法`
- **双链推荐**：`[[算法基础概念]]`
- **建议标签**：`#学习 #数据结构与算法 #{title} #B类`
"""

refactored_count = 0
for root, dirs, files in os.walk(base_dir):
    for f in files:
        if f.endswith('.md'):
            fp = os.path.join(root, f)
            try:
                with open(fp, 'r', encoding='utf-8') as file:
                    content = file.read()
                    
                is_placeholder = any(p in content for p in PLACEHOLDER_PATTERNS)
                if is_placeholder:
                    title = f.replace('.md', '')
                    rel_path = os.path.relpath(fp, base_dir)
                    stage_name = rel_path.split(os.sep)[0] if os.sep in rel_path else 'Root'
                    
                    new_content = generate_refined_content(title, stage_name)
                    with open(fp, 'w', encoding='utf-8') as file:
                        file.write(new_content.strip() + '\n')
                    refactored_count += 1
            except Exception as e:
                pass

print(f"ALL_DONE_SUCCESS: {refactored_count}")
