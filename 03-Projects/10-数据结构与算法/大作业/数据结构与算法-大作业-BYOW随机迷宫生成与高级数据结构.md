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
  - "[[数据结构与算法-并查集与路径压缩]]"
  - "[[数据结构与算法-二叉搜索树与平衡树]]"
  - "[[数据结构与算法-树状数组与线段树]]"
  - "[[数据结构与算法-图的存储与BFS-DFS遍历]]"
  - "[[数据结构与算法-最小生成树]]"
source_type: open_source_project_task
created: 2026-07-29
updated: 2026-08-07
status: planned
flow: project
tags:
  - 作业
  - 数据结构与算法
  - 大作业
  - 迷宫生成
source: "https://sp18.datastructur.es/materials/proj/proj3/proj3"
---

# 数据结构与算法 - 大作业：BYOW 随机迷宫生成与高级数据结构

> **所属课程**：数据结构与算法  
> **所属阶段**：Stage 06 Capstone 综合大作业  
> **学术来源**：UC Berkeley CS61B Project 2 (BYOW) 本地化改编  

---

## 🎯 学习目标

1. 综合应用并查集 (Union-Find)、平衡二叉树、线段树等高级数据结构。
2. 基于随机种子与图论生成算法（如随机 Prim 算法或 Kruskal 生成树）设计可再现的 2D 迷宫地图生成引擎。
3. 掌握软件设计模式、交互控制与游戏状态持久化。

---

## 🚧 任务边界与假设

- **环境要求**：Java 17+ (StdDraw / JUnit 5) 或 Python 3.10+ (Pygame / Pytest)。
- **随机重现性**：给定相同的 Seed 字符串，必须生成完全一致的 2D 世界。
- **地图连通性假设**：生成的房间与走廊必须保证 100% 连通，不可出现无法到达的隔离房间。

---

## ⚙️ 功能需求

| 难度层级 | 验收标准 / 功能细节 | 关键实现细节与要求 |
| :--- | :--- | :--- |
| **基础** | 基础数据结构正确性 100% | 独立手写双向链表、二叉搜索树与快速排序，通过单元测试。 |
| **进阶** | 复杂结构与图算法 | 手撕并查集与平衡树旋转逻辑。 |
| **综合** | 随机迷宫与世界生成 | 根据 Seed 随机生成房间与走廊相连的 2D 迷宫。 |
| **扩展** | 持久化与线段树优化 | 从零手撕线段树，增加游戏存档/加载系统。 |

---

## 📦 提交产物清单

- `byow_engine/`：迷宫生成与核心高级数据结构源码。
- `byow_report.pdf` / `byow_report.md`：架构设计说明与数据结构性能分析。
