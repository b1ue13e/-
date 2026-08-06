---
title: "数据结构与算法-题型-BYOW迷宫与高级数据结构阶梯作业"
type: problem-type
kind: problem-type
flow: knowledge
assignment_format: problem-set
stage_id: "02"
requires: ["[[10-数据结构与算法-图的深度优先搜索DFS]]", "[[10-数据结构与算法-并查集]]"]
source_type: open_textbook_exercise
topic: "数据结构与算法作业"
course: "10-数据结构与算法"
created: 2026-07-29
updated: 2026-07-29
date: 2026-07-29
status: learning
difficulty: advanced
importance: A
concept: ["数据结构", "图算法", "迷宫生成"]
prerequisites: ["[[02-Knowledge/🧠 学习系统/10-数据结构与算法/🗺️ 数据结构与算法学习路径|DSA学习路径]]"]
related: ["[[机器学习-题型-李宏毅式分类与深层模型阶梯作业]]"]
upstream: ["[[02-Knowledge/🧠 学习系统/10-数据结构与算法/🗺️ 数据结构与算法学习路径|数据结构与算法学习路径]]"]
downstream: []
tags: [学习, 10-数据结构与算法, 作业, 实战, 阶梯作业]
aliases: ["CS61B-Proj2-BYOW作业"]
---

# 数据结构与算法 - HW02：BYOW 随机迷宫生成与高级数据结构阶梯作业

> 🎯 **作业目标**：手写红黑树/并查集/线段树，并基于 Java/Python 独立实现带有随机地形、探索光照与交互控制的 2D 迷宫生成引擎 (Build Your Own World)。

---

## 1. ⚙️ 环境与 Starter Code 准备
- **Starter Code 路径**：`03-Projects/projects-dsa/hw02_byow.ipynb`
- **开源标杆仓库**：[sp21.cs61b.org](https://sp21.cs61b.org/) (UC Berkeley CS61B Project 2)
- **核心依赖**：`java` / `pytest` / `numpy` / `junit`

---

## 2. 🎯 阶梯式 Baseline / 难度设计 (4-Tier Difficulty)

| 梯度级别 | 验收标准 / 功能细节 | 关键实现细节与要求 |
| :--- | :--- | :--- |
| 🟢 **L1 - Simple Baseline** | 基础数据结构正确性 100% | 独立手写双向链表、二叉搜索树 (BST) 与快速排序，通过 JUnit 单元测试。 |
| 🟡 **L2 - Medium Baseline** | 解决 LeetCode Hard 题 | **手撕并查集 (Disjoint Set)** 与 **红黑树 (Red-Black Tree)** 旋转平衡逻辑。 |
| 🔴 **L3 - Strong Baseline** | **CS61B Proj 2 随机迷宫** | 根据 Seed 随机生成由房间与弯曲走廊相连的 2D 迷宫，支持键盘 WASD 角色探索与 HUD 显示。 |
| 👑 **L4 - Boss Baseline** | 持久化与线段树优化 | **从零手撕线段树 / 树状数组**，并为迷宫增加视线阻挡 (Line-of-Sight) 与游戏存档/加载系统。 |

---

## 3. 🧪 自动化测试 Harness (PyTest / JUnit Validation)

```python
import pytest

def test_disjoint_set_union_find():
    from dsa_lib import UnionFind
    uf = UnionFind(10)
    uf.union(1, 2)
    uf.union(2, 3)
    
    assert uf.is_connected(1, 3) == True, "1 与 3 必须连通"
    assert uf.is_connected(1, 5) == False, "1 与 5 不得连通"
```

---

## 🃏 Anki 卡片

- Q: 为什么在并查集 (Union-Find) 中同时使用“路径压缩 (Path Compression)”与“按秩合并 (Union by Rank)”后，单次操作的均摊时间复杂度为 $O(\alpha(n))$？
- A: 按秩合并保证树的高度不会剧烈增长，路径压缩在查找根节点时将沿途所有节点直接挂载到根节点上，使得树的平均深度收敛为阿克曼函数的反函数 $\alpha(n) \le 5$，几乎等于常数时间 $O(1)$。
