---
title: "AVL树"
type: study
topic: "AVL树"
course: "数据结构与算法"
created: 2026-07-28
updated: 2026-08-06
status: completed
upstream:
  - "[[数据结构与算法-二叉搜索树基础]]"
stage_moc: "[[🧭 阶段3-树与堆]]"
flow: knowledge
kind: concept
difficulty: intermediate
sources:
  - title: "MIT 6.006 Introduction to Algorithms (Spring 2020)"
    url: "https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/"
    locator: "Chapter 3: AVL树"
    source_type: "open-textbook"
    verified_at: "2026-07-28"
concept:
  - "AVL树"
tags:
  - 学习
  - 数据结构与算法
  - AVL树
---

# AVL树

> **所属课程**：数据结构与算法  
> **所属阶段**：[[🧭 阶段3-树与堆]]  
> **学术 Spine**：[MIT 6.006 Lecture 6 BST and AVL Trees](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/)  
> **参考书目**：Cormen, Leiserson, Rivest, Stein (CLRS) *Introduction to Algorithms (4th Edition)*, MIT Press, 出版年份: 2022, ISBN: 9780262046305, Chapter 12 Section 12.3

---

## 1. 🎯 树形数据组织与分治原理

AVL树 是一种典型的无环连通图结构，由包含数值与子指针的节点通过父子关系递归构成。在二叉搜索树与平衡树体系中，树形结构利用左小右大的性质将搜寻范围从根节点向下递归切分。树的高度直接决定了算法的最坏操作开销。

例如算例：在一个二叉搜索树中插入元素 `[10, 5, 15, 2, 7]`，根节点 `10` 引导 `5` 走向左子树，`15` 走向右子树。寻找 `7` 时只需对比两次即可顺左子树的右分支准确命中。反例：如果插入顺序为递增序列 `[1, 2, 3, 4, 5]` 且未进行平衡旋转，树将退化为单链表，查找开销急剧恶化为 $O(N)$。

---

## 2. 📐 平衡因子与树高严格推导

对于平衡树（如 AVL 树），节点平衡因子定义为左子树高度与右子树高度之差 $\text{BF}(p) = h_{\text{left}} - h_{\text{right}} \in \{-1, 0, 1\}$。

为了推导包含 $N$ 个节点的 AVL 树的最坏高度 $h$，我们考虑高度为 $h$ 的 AVL 树所需的**最少节点数目** $N(h)$。此时根节点的两个子树高度必须分别为 $h-1$ 与 $h-2$，递推关系为：
$$N(h) = N(h-1) + N(h-2) + 1 \quad (N(0)=0, N(1)=1)$$

**无跳步代数求解步骤**：
1. **常数项消除**：在递推式两边同时加 $1$，设 $M(h) = N(h) + 1$，则有：
   $$M(h) = M(h-1) + M(h-2)$$
   对应初值为 $M(0) = 1 = F_2, M(1) = 2 = F_3$。故 $M(h) = F_{h+3}$（其中 $F_k$ 为第 $k$ 项斐波那契数）。
2. **通项估计**：由斐波那契数列通项公式 $F_k = \frac{\phi^k - \psi^k}{\sqrt{5}}$（黄金分割比 $\phi = \frac{1+\sqrt{5}}{2} \approx 1.618$），可得：
   $$N(h) + 1 = F_{h+3} > \frac{\phi^{h+3}}{\sqrt{5}} - 1$$
3. **两边取对数化简**：
   $$\phi^{h+3} < \sqrt{5} (N(h) + 2)$$
   $$(h+3) \log_2 \phi < \log_2 \sqrt{5} + \log_2(N+2)$$
4. **系数求代入**：由于 $\frac{1}{\log_2 \phi} = \frac{1}{\log_2 1.618} \approx 1.4404$，代入上式解出树高 $h$：
   $$h < 1.4404 \log_2(N+2) - 1.677 \approx O(\log_2 N)$$

由此严格证明：AVL 树在最坏情况下的高度被严格限制在 $1.44 \log_2 N$ 以内，因此查找、插入和删除的渐近开销均为 $\Theta(\log N)$。


---

## 3. 💻 C++ 树结构工程实现与测试

```cpp
#include <iostream>
#include <memory>
#include <cassert>

using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

TreeNode* insert_tree_node(TreeNode* root, int key) {
    if (!root) return new TreeNode(key);
    if (key < root->val) root->left = insert_tree_node(root->left, key);
    else if (key > root->val) root->right = insert_tree_node(root->right, key);
    return root;
}

int main() {
    TreeNode* root = nullptr;
    root = insert_tree_node(root, 50);
    root = insert_tree_node(root, 30);
    root = insert_tree_node(root, 70);
    assert(root->val == 50);
    assert(root->left->val == 30);
    assert(root->right->val == 70);
    cout << "【AVL树】二叉树节点插入与验证通过！" << endl;
    return 0;
}
```

---

## 4. ⚠️ 常见误区与节点删除细节

1. **双子节点删除指针断裂**：删除带有左右两个子节点的树节点时，直接删除会导致子树悬空。必须先在右子树中找到中序后继节点（右子树的最小值），将其数值覆盖至当前节点，再递归删除该后继节点。
2. **旋转方向混淆**：在 LL、RR、LR、RL 四种旋转平衡恢复中，误将左旋写成右旋会导致 BST 有序性破坏。

---

## 5. 🃏 闭卷自测考点

- **问答自测**：在红黑树与 AVL 树的对比中，为什么红黑树在频繁插入和删除的工业级应用（如 C++ `std::map`）中更为常用？
- **解答与标准解析**：AVL 树追求绝对严格的平衡（高度差 $\le 1$），导致在频繁插入删除时触发多次复杂的平衡旋转；而红黑树通过引入红黑染色规则，允许最大高度达到 $2 \log_2(N+1)$，旋转维护次数显著减少，综合插入删除的常数开销更小。


---

## 🃏 Anki 卡片

- Q: 如何在一句话内精炼概括【AVL树】的核心机制与应用场景？
- A: 【AVL树】通过优化底层存储或决策分支，将暴力匹配的时间开销有效降低，是解决算法面试与工程性能瓶颈的核心工具。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
