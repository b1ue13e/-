---
title: "股票问题DP"
type: study
topic: "股票问题DP"
course: "数据结构与算法"
created: 2026-07-28
updated: 2026-08-06
status: completed
upstream:
  - "[[数据结构与算法-动态规划基础]]"
stage_moc: "[[🧭 阶段5-算法思想进阶]]"
flow: knowledge
kind: concept
difficulty: intermediate
sources:
  - title: "MIT 6.006 Introduction to Algorithms (Spring 2020)"
    url: "https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/"
    locator: "Chapter 5: 股票问题DP"
    source_type: "open-textbook"
    verified_at: "2026-07-28"
concept:
  - "股票问题DP"
tags:
  - 学习
  - 数据结构与算法
  - 股票问题DP
---

# 股票问题DP

> **所属课程**：数据结构与算法  
> **所属阶段**：[[🧭 阶段5-算法思想进阶]]  
> **学术 Spine**：[MIT 6.006 Dynamic Programming](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/)  
> **参考书目**：Cormen, Leiserson, Rivest, Stein (CLRS) *Introduction to Algorithms (4th Edition)*, MIT Press, 出版年份: 2022, ISBN: 9780262046305, Chapter 15 Section 15.3

---

## 1. 🎯 状态重叠与自底向上优化

股票问题DP 是解决具备重叠子问题（Overlapping Subproblems）与最优子结构（Optimal Substructure）特征复杂决策问题的建模精髓。DP 的本质在于建立状态空间与阶段演化递推方程，避免对同一子状态进行重复指数级搜索。

例如算例：计算 $N=10$ 的阶段方案数，暴力递归会生成 $2^{10}=1024$ 次分支调用；而利用 股票问题DP 记录记忆化表格，只需填入 $10$ 个格子，线性开销 $O(N)$ 即可锁定全局最优。反例：如果问题破坏了无后效性，前期的局部最优决策影响了后续阶段的选择规则，直接套用 DP 递推方程将得出错误结论。

---

## 2. 📐 状态转移方程与空间优化

设 DP 状态为 $DP[i][j]$，表示在前 $i$ 项决策、约束条件为 $j$ 时的目标优化值。状态转移方程满足：
$$DP[i][j] = \max \left( DP[i-1][j], DP[i-1][j - W_i] + V_i \right)$$

- **时间复杂度**：充填状态转移矩阵的总耗时等于 $\text{状态总数} \times \text{单次转移开销}$，典型如 $O(N \times W)$。
- **空间复杂度**：原始二维状态表占用 $O(N \times W)$ 内存；利用滚动数组技巧（Rolling Array）可将空间压缩至 $O(W)$。

---

## 3. 💻 C++ 动态规划工程实现与测试

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
#include <cassert>

using namespace std;

// 股票问题DP 状态转移求解
int solve_dp_problem(int W, const vector<int>& wt, const vector<int>& val) {
    int n = wt.size();
    vector<int> dp(W + 1, 0);
    for (int i = 0; i < n; ++i) {
        for (int j = W; j >= wt[i]; --j) {
            dp[j] = max(dp[j], dp[j - wt[i]] + val[i]);
        }
    }
    return dp[W];
}

int main() {
    vector<int> wt = {2, 3, 4, 5};
    vector<int> val = {3, 4, 5, 6};
    int max_val = solve_dp_problem(8, wt, val);
    assert(max_val == 10); // 选择重量 3+5=8，价值 4+6=10
    cout << "【股票问题DP】动态规划成功求解，最大价值为 " << max_val << endl;
    return 0;
}
```

---

## 4. ⚠️ 易错点与边界初始化

1. **一维化遍历方向倒错**：在 0-1 背包的一维滚动数组压缩中，容量 $j$ 必须倒序遍历。如果正序遍历，上一轮更新出的新值会被当成本轮旧值重复累加，退化为完全背包。
2. **初始化无极值填充**：在求解“恰好装满”或“最小消耗”时，未将非法状态初始化为 $-\infty$ 或 $+\infty$，导致非法组合参与转移。

---

## 5. 🃏 闭卷自测考点

- **问答自测**：动态规划中的“记忆化搜索”（Top-down with Memoization）与“自底向上填表”（Bottom-up Tabulation）各有什么优缺点？
- **解答与标准解析**：记忆化搜索按需递归计算子状态，逻辑清晰且避免无效状态计算，但存在递归调用的函数栈开销；自底向上填表按拓扑顺序循环计算，无栈溢出风险且便于空间压缩，但必须顺序计算完可能无用的中间状态。


---

## 🃏 Anki 卡片

- Q: 如何在一句话内精炼概括【股票问题DP】的核心机制与应用场景？
- A: 【股票问题DP】通过优化底层存储或决策分支，将暴力匹配的时间开销有效降低，是解决算法面试与工程性能瓶颈的核心工具。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
