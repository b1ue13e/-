---
title: "数据结构与算法-大作业-BYOW随机迷宫生成与高级数据结构"
type: project
project_type: homework
course: "数据结构与算法"
assignment_id: "数据结构与算法-大作业-BYOW"
assignment_level: capstone
assignment_format: project
stage_id: "06"
requires:
  - "[[数据结构与算法-算法代码规范]]"
  - "[[数据结构与算法-算法学习复盘]]"
  - "[[数据结构与算法-算法模板整理]]"
  - "[[数据结构与算法-算法调试技巧]]"
  - "[[数据结构与算法-算法面试表达]]"
  - "[[数据结构与算法-算法高频题分类]]"
source_type: open_source_project_task
created: 2026-07-29
updated: 2026-08-06
status: planned
flow: project
tags:
  - 作业
  - 10-数据结构与算法
  - 大作业
  - 迷宫生成
source: "https://sp18.datastructur.es/materials/proj/proj3/proj3"
---



# 10-数据结构与算法 - 大作业：BYOW 随机迷宫生成与高级数据结构

> **所属课程**：数据结构与算法  
> **所属阶段**：Stage 06 Capstone 综合大作业  
> **学术来源**：UC Berkeley CS61B Project 2 (BYOW) 本地化改编  

---

## 🎯 学习目标

1. 综合应用并查集 (Union-Find)、红黑树 (Red-Black Tree)、线段树 (Segment Tree) 等高级数据结构。
2. 基于随机种子 (Random Seed) 与图论生成算法（如随机 Prim 算法、递归分割法或 Kruskal 生成树）设计可再现的 2D 迷宫地图生成引擎。
3. 掌握软件设计模式、交互控制（WASD 移动、HUD 界面显示）及游戏状态持久化（Save / Load 序列化）。

---

## 🚧 任务边界与假设

- **环境要求**：Java 17+ (StdDraw / JUnit 5) 或 Python 3.10+ (Pygame / Pytest)。
- **随机重现性**：给定相同的 Seed 字符串（如 `N123456S`），必须生成完全一致的 2D 世界。
- **地图连通性假设**：生成的房间与走廊必须保证 100% 连通，不可出现无法到达的隔离房间。

---

## ⚙️ 阶梯式难度设计与功能需求

| 难度层级 | 验收标准 / 功能细节 | 关键实现细节与要求 |
| :--- | :--- | :--- |
| **基础 (Level 1)** | 基础数据结构正确性 100% | 独立手写双向链表、二叉搜索树 (BST) 与快速排序，通过 JUnit 单元测试。 |
| **进阶 (Level 2)** | 复杂结构与图算法 | 手撕并查集 (Disjoint Set) 与红黑树 (Red-Black Tree) 旋转平衡逻辑。 |
| **综合 (Level 3)** | 随机迷宫与世界生成 | 根据 Seed 随机生成由房间与弯曲走廊相连的 2D 迷宫，支持键盘 WASD 角色探索与 HUD 显示。 |
| **扩展 (Level 4)** | 持久化与线段树优化 | 从零手撕线段树 / 树状数组，并为迷宫增加视线阻挡 (Line-of-Sight) 与游戏存档/加载系统。 |

---

## 📦 提交产物清单

- `byow_engine/`：迷宫生成与核心高级数据结构源码。
- `byow_report.pdf` / `byow_report.md`：架构设计说明、Seed 随机重现性测试报告与数据结构性能分析。
- `tests/`：自动化测试 Harness (PyTest / JUnit Validation)。

---

## 📏 验收标准与 Rubric

- **数据结构正确性** (30%)：红黑树、并查集及线段树独立手写且通过 100% 单元测试。
- **随机世界生成** (30%)：Seed 完全重现，地图房间与走廊无缝连通，无越界与非法悬空。
- **探索交互与 HUD** (20%)：WASD 移动顺畅，HUD 实时呈现光标悬停处瓦片类型（Wall / Floor / Player）。
- **存档持久化** (20%)：支持 Save `:Q` 退出与 Load 重新载入，玩家状态与地图状态完全恢复。

---

## 💡 引导与自检

- [ ] 输入 Seed 逻辑是否能妥善处理任意长度的数字输入与字符串解析？
- [ ] 房间重叠与走廊连接算法是否借助了并查集来检测和连通不同连通块？
- [ ] 视线渲染（Line of Sight）算法是否避免了 $O(\text{Width} \times \text{Height})$ 的暴力重复扫描？

---

## 🃏 Anki 卡片

- Q: 为什么在并查集 (Union-Find) 中同时使用“路径压缩 (Path Compression)”与“按秩合并 (Union by Rank)”后，单次操作的均摊时间复杂度为 $O(\alpha(n))$？
- A: 按秩合并保证树的高度不会剧烈增长，路径压缩在查找根节点时将沿途所有节点直接挂载到根节点上，使得树的平均深度收敛为阿克曼函数的反函数 $\alpha(n) \le 5$，几乎等于常数时间 $O(1)$。
