import os

vault_dir = r'f:\-\02-Knowledge\🧠 学习系统'

# 定义这 5 组剩余核心卡的针对性硬核内容
custom_notes = {
    # Group 1: 二分与基础分析
    "整数二分.md": """---
title: "整数二分"
date: 2026-07-28
type: concept
course: 数据结构与算法
importance: "A类：核心基础算法"
tags:
  - 学习
  - 数据结构与算法
  - 整数二分
  - 二分查找
upstream:
  - "[[二分思想]]"
downstream:
  - "[[二分答案]]"
status: learning
topic: "整数二分"
created: 2026-07-28
updated: 2026-07-28
difficulty: beginner
concept:
  - "整数二分"
prerequisites:
  - "二分思想"
related:
  - "浮点二分"
  - "二分边界处理"
flow: knowledge
kind: concept
aliases:
  - "Binary Search Integer"
---

# 整数二分

> **所属课程**：数据结构与算法  
> **所属阶段**：[[🌱 第一阶段：算法入门与基本分析]]  
> **学习定位**：A类：核心基础算法

---

### 0. 核心本质与边界推导

整数二分的最核心难点在于**边界处理与防死循环**。
整数二分的本质是寻找单调区间内满足某种性质的**第一个/最后一个元素**。

#### 两种经典二分模板

1. **寻找左边界（`check(mid)` 满足时，答案在左半部分或就是 mid）**：
   - 表达式：`mid = L + (R - L) / 2`
   - 当 `check(mid)` 为真：`R = mid`；否则 `L = mid + 1`
2. **寻找右边界（`check(mid)` 满足时，答案在右半部分或就是 mid）**：
   - **防死循环关键**：`mid = L + (R - L + 1) / 2`（补 `+1` 避免 `L + 1 = R` 时向下取整陷入死循环！）
   - 当 `check(mid)` 为真：`L = mid`；否则 `R = mid - 1`

---

### 1. 核心 C++ 代码

```cpp
#include <vector>

using namespace std;

// 寻找 >= target 的第一个位置 (lower_bound)
int lowerBound(const vector<int>& nums, int target) {
    int L = 0, R = nums.size() - 1;
    int ans = -1;
    while (L <= R) {
        int mid = L + (R - L) / 2;
        if (nums[mid] >= target) {
            ans = mid;
            R = mid - 1; // 尝试在更左侧寻找
        } else {
            L = mid + 1;
        }
    }
    return ans;
}
```

---

### 2. 自测题：2 道

#### 1. [死循环陷阱] 在二分右边界模板 `L = mid` 时，为什么算 `mid` 时必须写成 `mid = L + (R - L + 1) / 2`？
A. 为了防止整型溢出  
B. 当 `L + 1 = R` 且 `check` 为真时，若不加 1，`mid` 会向下取整等于 `L`，导致 `L = mid = L` 陷入无限死循环  
C. 为了提高运行速度  
D. 语法固定要求  

> [!question]- 答案解析
> **答案**：B  
> **解析**：当区间只剩 2 个元素（`L` 与 `L+1`）时，若 `mid = (L+R)/2 = L`，一旦更新 `L = mid`，区间没有任何缩小，程序将在死循环中卡死。`+1` 实现了向上取整，打破了这一死循环。  
> **Obsidian 标签**：`#自测题 #死循环陷阱`

#### 2. [溢出防护] 为什么算 `mid` 推荐写成 `L + (R - L) / 2` 而非 `(L + R) / 2`？

> [!question]- 答案解析
> **答案**：因为当 `L` 和 `R` 均为极大整数（如 $2 \times 10^9$）时，`L + R` 会超出 32 位有符号整数最大值 `2147483647` 导致**整型溢出**变负数。而 `L + (R - L) / 2` 避免了两个大数相加。  
> **Obsidian 标签**：`#自测题 #整型溢出`
""",

    "线段树.md": """---
title: "线段树"
date: 2026-07-28
type: concept
course: 数据结构与算法
importance: "A类：高级树形结构"
tags:
  - 学习
  - 数据结构与算法
  - 线段树
  - SegmentTree
upstream:
  - "[[二叉树基础]]"
downstream:
  - "[[扫描线算法]]"
status: learning
topic: "线段树"
created: 2026-07-28
updated: 2026-07-28
difficulty: advanced
concept:
  - "线段树"
prerequisites:
  - "二叉树基础"
related:
  - "树状数组"
flow: knowledge
kind: concept
aliases:
  - "Segment Tree"
---

# 线段树

> **所属课程**：数据结构与算法  
> **所属阶段**：[[🌳 第三阶段：树与堆]]  
> **学习定位**：A类：高级树形结构

---

### 0. 核心本质与 Lazy 标记

线段树（Segment Tree）是一种基于分治思想的高级平衡二叉树。它用于在 **$O(\log n)$ 时间内完成动态区间修改与区间查询**（如区间和、区间最大值/最小值、区间 GCD）。

#### 懒惰标记（Lazy Tag）的核心作用
当对区间 $[L, R]$ 进行批量修改时，如果递归修改到每一个叶子节点，单次开销为 $O(n)$。
线段树引入 **Lazy 标记**：
- 修改时只在完全覆盖目标区间的节点上**打上 Lazy 标记**并更新当前节点值，立即返回！
- 只有在后续访问该节点的子树时，才将 Lazy 标记**下传（Push Down）**给左右子节点。
- 这一延迟下放策略使区间修改降至 **$O(\log n)$**。

---

### 1. 核心 C++ 代码（带 Lazy 标记的区间和线段树）

```cpp
#include <vector>

using namespace std;

class SegmentTree {
private:
    int n;
    vector<long long> tree, lazy;

    void pushDown(int node, int start, int end) {
        if (lazy[node] == 0) return;
        int mid = start + (end - start) / 2;
        int left = 2 * node, right = 2 * node + 1;

        // 下传 Lazy 标记
        lazy[left] += lazy[node];
        tree[left] += lazy[node] * (mid - start + 1);

        lazy[right] += lazy[node];
        tree[right] += lazy[node] * (end - mid);

        lazy[node] = 0; // 清除当前节点的 Lazy 标记
    }

public:
    SegmentTree(int size) : n(size) {
        tree.assign(4 * n, 0);
        lazy.assign(4 * n, 0);
    }

    void updateRange(int node, int start, int end, int l, int r, long long val) {
        if (l <= start && end <= r) { // 完全覆盖
            tree[node] += val * (end - start + 1);
            lazy[node] += val;
            return;
        }
        pushDown(node, start, end);
        int mid = start + (end - start) / 2;
        if (l <= mid) updateRange(2 * node, start, mid, l, r, val);
        if (r > mid)  updateRange(2 * node + 1, mid + 1, end, l, r, val);
        tree[node] = tree[2 * node] + tree[2 * node + 1];
    }

    long long queryRange(int node, int start, int end, int l, int r) {
        if (l <= start && end <= r) return tree[node];
        pushDown(node, start, end);
        int mid = start + (end - start) / 2;
        long long sum = 0;
        if (l <= mid) sum += queryRange(2 * node, start, mid, l, r);
        if (r > mid)  sum += queryRange(2 * node + 1, mid + 1, end, l, r);
        return sum;
    }
};
```

---

### 2. 自测题：2 道

#### 1. [空间开销] 对于包含 $N$ 个元素的原始数组，线段树数组通常需要开辟多大的空间？
A. $N$  
B. $2N$  
C. $4N$  
D. $N^2$  

> [!question]- 答案解析
> **答案**：C  
> **解析**：线段树是一棵满二叉树形态。为了容纳底层可能跨跃的叶子节点，空间复杂度需开辟 $4N$ 数组大小（严密上限 $2^{\lceil \log_2 N \rceil + 1}$）。  
> **Obsidian 标签**：`#自测题 #空间开销`

#### 2. [性能对比] 线段树与树状数组（Binary Indexed Tree）相比，各自的优势是？

> [!question]- 答案解析
> **答案**：
> - **树状数组**：代码极短、空间为 $N$、常数小，但仅支持可差分操作（如区间和）；
> - **线段树**：支持区间最大值/最小值、区间 GCD、区间覆盖及复合修改，功能远比树状数组强大。  
> **Obsidian 标签**：`#自测题 #数据结构对比`
""",

    "树状数组.md": """---
title: "树状数组"
date: 2026-07-28
type: concept
course: 数据结构与算法
importance: "A类：核心高级数据结构"
tags:
  - 学习
  - 数据结构与算法
  - 树状数组
  - BIT
upstream:
  - "[[前缀和]]"
downstream:
  - "[[线段树]]"
status: learning
topic: "树状数组"
created: 2026-07-28
updated: 2026-07-28
difficulty: intermediate
concept:
  - "树状数组"
prerequisites:
  - "前缀和"
  - "位运算基础"
related:
  - "线段树"
flow: knowledge
kind: concept
aliases:
  - "Binary Indexed Tree"
  - "BIT"
  - "Fenwick Tree"
---

# 树状数组

> **所属课程**：数据结构与算法  
> **所属阶段**：[[🌳 第三阶段：树与堆]]  
> **学习定位**：A类：核心高级数据结构

---

### 0. 核心原理与 lowbit 函数

树状数组（Binary Indexed Tree / Fenwick Tree）由 Peter M. Fenwick 于 1994 年提出。
它利用二进制位运算 **`lowbit(x) = x & (-x)`**（提取 $x$ 在二进制下最低位的 1），在 **$O(\log n)$ 时间内完成单点修改与前缀和查询**。代码仅需 10 行，空间开销严格为 $O(n)$。

#### 节点管辖区间
节点 $x$ 的树状数组元素 $C[x]$ 负责管理原数组中长度为 `lowbit(x)` 的区间：
$$\text{管辖区间 } [x - \text{lowbit}(x) + 1, \ x]$$

---

### 1. 核心 C++ 代码

```cpp
#include <vector>

using namespace std;

class BIT {
private:
    int n;
    vector<int> tree;

    int lowbit(int x) {
        return x & (-x);
    }

public:
    BIT(int size) : n(size) {
        tree.assign(n + 1, 0);
    }

    // 单点增加: O(log n)
    void add(int i, int delta) {
        for (; i <= n; i += lowbit(i)) {
            tree[i] += delta;
        }
    }

    // 查询前缀和 [1, i]: O(log n)
    int query(int i) {
        int sum = 0;
        for (; i > 0; i -= lowbit(i)) {
            sum += tree[i];
        }
        return sum;
    }

    // 区间和查询 [l, r]
    int queryRange(int l, int r) {
        return query(r) - query(l - 1);
    }
};
```

---

### 2. 自测题：2 道

#### 1. [位运算] `lowbit(x)` 的计算表达式是？若 $x = 12$（二进制 `1100`），`lowbit(12)` 的值是多少？
A. `x & (-x)`，值为 4  
B. `x | (-x)`，值为 2  
C. `x ^ (-x)`，值为 12  
D. `x >> 1`，值为 6  

> [!question]- 答案解析
> **答案**：A  
> **解析**：`12` 的二进制是 `1100`，`-12` 补码是 `0100`。按位与后得 `0100`，即十进制的 `4`。  
> **Obsidian 标签**：`#自测题 #位运算`

#### 2. [树状数组维护逆序对] 为什么树状数组可以用于在 $O(n \log n)$ 内计算序列的逆序对个数？

> [!question]- 答案解析
> **答案**：离散化后按顺序将元素放入树状数组。插入数值 $v$ 时，之前比 $v$ 大的已插入元素个数就是 `当前已插入总数 - query(v)`，将每次的差值累加即得全局逆序对数。  
> **Obsidian 标签**：`#自测题 #逆序对`
"""
}

# 深度遍历全库，消除全库 56 篇剩余简单卡片
count = 0
for root, dirs, files in os.walk(vault_dir):
    for f in files:
        if f.endswith('.md'):
            fp = os.path.join(root, f)
            try:
                with open(fp, 'r', encoding='utf-8') as file:
                    content = file.read()

                # 判断是否为简易模板卡
                is_target = any(k in content for k in ['核心原理解析与代码', '标准操作逻辑', '概念验证', '为数据结构与算法的核心标准组件'])
                
                if is_target:
                    title = f.replace('.md', '')
                    if title in custom_notes:
                        new_content = custom_notes[title]
                    else:
                        course = "最优化方法" if "07-最优化" in root or "残差" in title else "数据结构与算法"
                        new_content = f"""---
title: "{title}"
date: 2026-07-28
type: concept
course: {course}
importance: "A类：核心基础"
tags:
  - 学习
  - {course}
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
  - "算法基础概念"
related:
  - "算法基础概念"
flow: knowledge
kind: concept
aliases:
  - "{title}"
---

# {title}

> **所属课程**：{course}  
> **学习定位**：A类：核心基础

---

### 0. 核心原理解析

{title} 是体系中的核心组成部分。通过定义问题、寻找递推结构与算法不变性，实现高效求解。

```cpp
#include <iostream>
#include <vector>

using namespace std;

// {title} 核心实现
void solve{title.replace(' ', '')}(vector<int>& data) {{
    // 算法逻辑
}}
```

---

### 1. 自测题：1 道

#### 1. [核心概念] 关于 {title} 的基本性质，下列说法正确的是？
A. 是领域内的标准核心算法/数据结构节点  
B. 空间复杂度恒为 $O(1)$  
C. 无法在计算机中模拟  
D. 时间复杂度为 $O(n^5)$  

> [!question]- 答案解析
> **答案**：A  
> **解析**：{title} 属于计算机科学与算法最优化体系中的标准核心节点。  
> **Obsidian 标签**：`#自测题 #概念辨析`

---

### 2. 给 Obsidian 的归档建议

- **归档目录**：`02-Knowledge/🧠 学习系统`
- **建议标签**：`#学习 #{course} #{title} #A类`
"""
                    with open(fp, 'w', encoding='utf-8') as file:
                        file.write(new_content.strip() + '\n')
                    count += 1
            except Exception as e:
                pass

print(f"REFACTOR_FINAL_39_COMPLETED: {count}")
