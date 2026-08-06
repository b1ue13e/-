---
title: "10-数据结构与算法-大作业-BYOW随机迷宫生成与高级数据结构"
type: project
project_type: homework
course: "数据结构与算法"
assignment_id: "10-数据结构与算法-大作业-BYOW"
assignment_level: capstone
assignment_format: project
stage_id: "06"
requires:
  - "[[10-数据结构与算法-DFS基础]]"
  - "[[10-数据结构与算法-并查集基础]]"
  - "[[10-数据结构与算法-红黑树]]"
source_type: open_source_project_task
created: 2026-07-29
status: planned
flow: project
tags:
  - 作业
  - 10-数据结构与算法
  - 大作业
  - 迷宫生成
---

# 10-数据结构与算法 - 大作业：BYOW 随机迷宫生成与高级数据结构

> 🎯 **作业目标**：手写红黑树/并查集/线段树，并基于 Java/Python 独立实现带有随机地形、探索光照与交互控制的 2D 迷宫生成引擎 (Build Your Own World)。

---

## 1. ⚙️ 环境与 Starter Code 准备

- **Starter Code 路径**：`03-Projects/projects-dsa/hw02_byow.ipynb`
- **开源标杆仓库**：[UC Berkeley CS61B Project 2 (BYOW)](https://sp21.cs61b.org/)
- **核心依赖**：`java` / `pytest` / `numpy` / `junit`

---

## 2. 🎯 阶梯式难度设计与功能需求

| 难度层级 | 验收标准 / 功能细节 | 关键实现细节与要求 |
| :--- | :--- | :--- |
| **基础 (Level 1)** | 基础数据结构正确性 100% | 独立手写双向链表、二叉搜索树 (BST) 与快速排序，通过 JUnit 单元测试。 |
| **进阶 (Level 2)** | 复杂结构与图算法 | 手撕并查集 (Disjoint Set) 与红黑树 (Red-Black Tree) 旋转平衡逻辑。 |
| **综合 (Level 3)** | 随机迷宫与世界生成 | 根据 Seed 随机生成由房间与弯曲走廊相连的 2D 迷宫，支持键盘 WASD 角色探索与 HUD 显示。 |
| **扩展 (Level 4)** | 持久化与线段树优化 | 从零手撕线段树 / 树状数组，并为迷宫增加视线阻挡 (Line-of-Sight) 与游戏存档/加载系统。 |

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
