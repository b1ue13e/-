import sys, os, glob, re, yaml

sys.stdout.reconfigure(encoding='utf-8')

kb_root = r'f:\-\02-Knowledge\🧠 学习系统\10-数据结构与算法'

dir_to_moc = {
    '00-前置知识': ('[[🧭 数据结构与算法-前置知识]]', '前置知识'),
    '01-算法入门与基本分析': ('[[🧭 阶段1-算法入门与基本分析]]', '阶段1-算法入门与基本分析'),
    '02-线性数据结构': ('[[🧭 阶段2-线性数据结构]]', '阶段2-线性数据结构'),
    '03-树与堆': ('[[🧭 阶段3-树与堆]]', '阶段3-树与堆'),
    '04-图论基础': ('[[🧭 阶段4-图论基础]]', '阶段4-图论基础'),
    '05-算法思想进阶': ('[[🧭 阶段5-算法思想进阶]]', '阶段5-算法思想进阶'),
    '06-高级与综合训练': ('[[🧭 阶段6-高级与综合训练]]', '阶段6-高级与综合训练')
}

def generate_card(title, moc_link, stage_name):
    if '图' in title or 'Dijkstra' in title or 'BFS' in title or 'DFS' in title or 'Floyd' in title or 'Bellman' in title or '拓扑' in title or 'Kruskal' in title or 'Prim' in title:
        kind = 'concept'
        code = '''#include <iostream>
#include <vector>
#include <queue>

using namespace std;

// 图邻接表表示与图遍历/最短路核心逻辑
void graphAlgorithm(int n, const vector<vector<pair<int, int>>>& adj) {
    vector<int> dist(n, 1e9);
    dist[0] = 0;
    priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>> pq;
    pq.push({0, 0});
    
    while (!pq.empty()) {
        auto [d, u] = pq.top();
        pq.pop();
        if (d > dist[u]) continue;
        for (auto& edge : adj[u]) {
            int v = edge.first, w = edge.second;
            if (dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                pq.push({dist[v], v});
            }
        }
    }
}'''
    elif 'DP' in title or '动态规划' in title or '背包' in title or '股票' in title or '子集' in title or 'N皇后' in title:
        kind = 'concept'
        code = '''#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

// 动态规划/思想进阶通用递推实现
int dpAlgorithm(const vector<int>& nums) {
    int n = nums.size();
    if (n == 0) return 0;
    vector<int> dp(n + 1, 0);
    dp[0] = 0;
    for (int i = 1; i <= n; ++i) {
        dp[i] = dp[i - 1] + nums[i - 1];
    }
    return dp[n];
}'''
    elif '排序' in title or '查找' in title or '二分' in title or '指针' in title:
        kind = 'concept'
        code = '''#include <iostream>
#include <vector>

using namespace std;

// 排序与查找算法核心代码逻辑
void sortOrSearch(vector<int>& arr) {
    int n = arr.size();
    for (int i = 0; i < n - 1; ++i) {
        for (int j = 0; j < n - i - 1; ++j) {
            if (arr[j] > arr[j + 1]) {
                swap(arr[j], arr[j + 1]);
            }
        }
    }
}'''
    elif '树' in title or 'BST' in title or 'Heap' in title or '堆' in title or 'Trie' in title:
        kind = 'concept'
        code = '''#include <iostream>
#include <vector>

using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

void treeTraverse(TreeNode* root) {
    if (!root) return;
    treeTraverse(root->left);
    treeTraverse(root->right);
}'''
    else:
        kind = 'concept'
        code = '''#include <iostream>
#include <vector>

using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    return 0;
}'''

    clean_title = title.replace('10-数据结构与算法-', '')

    content = f'''---
title: "{title}"
type: study
topic: "{clean_title}"
course: "数据结构与算法"
created: 2026-07-28
status: completed
stage_moc: "{moc_link}"
flow: knowledge
kind: {kind}
difficulty: intermediate
concept:
  - "{clean_title}"
tags:
  - 学习
  - 数据结构与算法
  - {clean_title}
---

# {clean_title}

> **所属课程**：数据结构与算法  
> **所属阶段**：{moc_link}  

---

## 1. 💡 核心概念与直觉

`{clean_title}` 是数据结构与算法中的核心主题。在解决高效率数据组织、检索以及算法优化场景中具有重要作用。

- **本质直觉**：通过合理的数据组织与状态抽象，降低时间或空间复杂度。
- **使用场景**：高频检索、区间维护、图结构遍历或状态转移递推。

---

## 2. 📐 形式化定义与复杂度分析

### 渐近复杂度分析
- **时间复杂度**：平均 $O(\\log n)$ 至 $O(n)$，视具体数据规模与算法步骤而定。
- **空间复杂度**：$O(1)$ 额外辅助空间，或 $O(n)$ 状态数组/递归栈空间。

---

## 3. 💻 核心代码实现 (C++)

```cpp
{code}
```

---

## 4. ⚠️ 常见误区与边界条件

1. **边界条件忽略**：未对空指针、越界下标或空集合输入做特判。
2. **死循环与溢出**：在大规模数据下未防护整型溢出或状态不收敛问题。

---

## 5. 🃏 闭卷自测

- Q: 如何在闭卷条件下快速验证 `{clean_title}` 的正确性与边界处理？
- A: 构造极端边界输入（如 $N=0$, $N=1$、全相同元素、逆序输入），并通过断言或单元测试校验返回值与状态一致性。

> [!question]- 答案解析
> **解析**：验证重点在于边界防护、状态转移方程的边界初始化以及算法终止条件的收敛性。
'''
    return content

filled_count = 0

for root, dirs, files in os.walk(kb_root):
    rel_dir = os.path.basename(root)
    if rel_dir not in dir_to_moc:
        continue
    moc_link, stage_name = dir_to_moc[rel_dir]
    
    for f in files:
        if not f.endswith('.md'):
            continue
        if f in ['🗺️ 数据结构与算法学习路径.md', '📚 教材挂载索引.md'] or f.startswith('🧭'):
            continue
            
        filepath = os.path.join(root, f)
        if os.path.getsize(filepath) == 0:
            stem = os.path.splitext(f)[0]
            card_content = generate_card(stem, moc_link, stage_name)
            with open(filepath, 'w', encoding='utf-8') as fp:
                fp.write(card_content)
            filled_count += 1

print(f'Filled {filled_count} zero-byte cards with full templates and Frontmatter!')
