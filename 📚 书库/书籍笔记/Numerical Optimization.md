---
type: book
topic: Numerical Optimization
created: 2026-04-18
status: unread
tags:
- 书籍
- 阅读
- 最优化方法
- 数值优化
title: Numerical Optimization
author: Jorge Nocedal；Stephen J. Wright
category: 最优化方法 / 数值算法
topics:
- 线搜索
- 牛顿法
- 拟牛顿法
- 信赖域
- 约束优化
concept:
- Armijo条件
- 牛顿方向
- BFGS
- 信赖域
- 收敛性
related:
- 最优化方法
- 机器学习
- 数值分析
source_path: 📚 书库/书籍资源/Numerical Optimization (Jorge Nocedal  Stephen J. Wright) (z-library.sk,
  1lib.sk, z-lib.sk).pdf
---

# 📘 Numerical Optimization

> 这是 `07-最优化方法` 第三、四阶段的算法主教材，负责回答“算法怎么走、为什么收敛、什么时候稳定”。

## 🔗 资源入口

- [打开原书](<../书籍资源/Numerical Optimization (Jorge Nocedal  Stephen J. Wright) (z-library.sk, 1lib.sk, z-lib.sk).pdf>)
- [[🧠 学习系统/07-最优化方法/🗺️ 最优化方法学习路径|进入最优化方法学习路径]]

## 🧭 章节地图

| 章节 | 章节目标 | 对应路径阶段 | 对应模块 | 代表原子卡 |
|:---|:---|:---|:---|:---|
| Line Search Methods | 建立步长选择与下降保证的共同框架 | [[🧠 学习系统/07-最优化方法/03-经典数值优化算法/⚙️ 第三阶段：经典数值优化算法\|第三阶段]] | 线搜索基础 | [[🧠 学习系统/07-最优化方法/03-经典数值优化算法/Armijo条件\|Armijo条件]] |
| Newton and Quasi-Newton Methods | 理解二阶方法、近似 Hessian 与收敛行为 | [[🧠 学习系统/07-最优化方法/03-经典数值优化算法/⚙️ 第三阶段：经典数值优化算法\|第三阶段]] | 牛顿家族；拟牛顿家族 | [[🧠 学习系统/07-最优化方法/03-经典数值优化算法/BFGS思想\|BFGS思想]] |
| Trust-Region Methods | 把局部模型、半径更新与步长接受准则讲清楚 | [[🧠 学习系统/07-最优化方法/03-经典数值优化算法/⚙️ 第三阶段：经典数值优化算法\|第三阶段]] | 信赖域方法 | [[🧠 学习系统/07-最优化方法/03-经典数值优化算法/信赖域子问题\|信赖域子问题]] |
| Constrained Optimization | 连接约束问题、KKT 与数值求解流程 | [[🧠 学习系统/07-最优化方法/03-经典数值优化算法/⚙️ 第三阶段：经典数值优化算法\|第三阶段]] | 最小二乘与算法比较项目 | [[🧠 学习系统/07-最优化方法/03-经典数值优化算法/项目-最小二乘\|项目-最小二乘]] |
| Large-Scale Optimization | 面向大模型训练的近似、截断与稀疏策略 | [[🧠 学习系统/07-最优化方法/04-现代一阶与随机优化/🚀 第四阶段：现代一阶与随机优化\|第四阶段]] | 方差缩减与大规模实验 | [[🧠 学习系统/07-最优化方法/04-现代一阶与随机优化/项目-大规模优化\|项目-大规模优化]] |

## 🪜 推荐读法

1. 先完成线搜索、牛顿法、拟牛顿法三大块。
2. 然后把信赖域方法和最小二乘项目一起读，避免只记算法名字。
3. 第四阶段只抽取与大规模训练直接相关的思想，不需要一次性吃完整本书。
