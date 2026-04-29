---
type: book
topic: Numerical Linear Algebra
created: 2026-04-18
status: unread
tags:
- 书籍
- 阅读
- 高等代数
- 数值分析
title: Numerical Linear Algebra
author: Lloyd N. Trefethen；David Bau III
category: 数值线性代数 / 科学计算
topics:
- QR分解
- 最小二乘
- SVD
- 特征值计算
- 条件数
concept:
- QR分解
- 最小二乘
- 奇异值分解
- 幂迭代
- 条件数
- 数值稳定性
related:
- 高等代数
- 最优化方法
- 数值分析
source_path: 📚 书库/书籍资源/Numerical Linear Algebra (Lloyd N. Trefethen, David Bau III)
  (z-library.sk, 1lib.sk, z-lib.sk).pdf
---

# 📘 Numerical Linear Algebra

> 这本书把 `09-高等代数` 的第四阶段从“会公式”推进到“会考虑稳定性、条件数和算法实现”。

## 🔗 资源入口

- [打开原书](<../书籍资源/Numerical Linear Algebra (Lloyd N. Trefethen, David Bau III) (z-library.sk, 1lib.sk, z-lib.sk).pdf>)
- [[🧠 学习系统/09-高等代数/🗺️ 高等代数学习路径|进入高等代数学习路径]]

## 🧭 章节地图

| 章节 | 章节目标 | 对应路径阶段 | 对应模块 | 代表原子卡 |
|:---|:---|:---|:---|:---|
| Linear Systems and Conditioning | 理解病态问题、条件数与数值误差来源 | [[🧠 学习系统/09-高等代数/04-精通拓展/🚀 第四阶段：精通拓展\|第四阶段]] | 矩阵分析与数值稳定性 | [[🧠 学习系统/09-高等代数/04-精通拓展/矩阵范数\|矩阵范数]] |
| QR and Least Squares | 把正交化与最小二乘算法接到工程实现 | [[🧠 学习系统/09-高等代数/04-精通拓展/🚀 第四阶段：精通拓展\|第四阶段]] | 矩阵分解与最小二乘 | [[🧠 学习系统/09-高等代数/04-精通拓展/QR分解\|QR分解]] |
| Singular Value Decomposition | 理解 SVD 的几何、逼近与数据分析价值 | [[🧠 学习系统/09-高等代数/04-精通拓展/🚀 第四阶段：精通拓展\|第四阶段]] | 矩阵分解与最小二乘 | [[🧠 学习系统/09-高等代数/04-精通拓展/奇异值分解(SVD)\|奇异值分解(SVD)]] |
| Eigenvalue Algorithms | 把谱问题和迭代计算方法连起来 | [[🧠 学习系统/09-高等代数/04-精通拓展/🚀 第四阶段：精通拓展\|第四阶段]] | 矩阵分析与数值稳定性 | [[🧠 学习系统/09-高等代数/04-精通拓展/特征值计算\|特征值计算]] |
| Large-Scale Problems | 面向大规模矩阵的近似、迭代与稀疏计算 | [[🧠 学习系统/09-高等代数/04-精通拓展/🚀 第四阶段：精通拓展\|第四阶段]] | 前沿补充 | [[🧠 学习系统/09-高等代数/04-精通拓展/大规模计算\|大规模计算]] |

## 🪜 推荐读法

1. 先读 QR、Least Squares、SVD 三块，再去看条件数和特征值算法。
2. 读的时候始终把“算法为什么稳定/不稳定”写成自己的语言。
3. 和 `07-最优化方法` 的最小二乘、牛顿法、信赖域方法一起联动复习。
