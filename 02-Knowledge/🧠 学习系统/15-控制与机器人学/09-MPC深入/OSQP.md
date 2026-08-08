---
type: study
topic: "OSQP"
course: "控制与机器人学"
created: 2026-08-07
updated: 2026-08-08
status: completed
difficulty: intermediate
stage_moc: "[[🧭 阶段9-MPC深入]]"
flow: knowledge
kind: concept
concept: ["ADMM求解器", "嵌入式优化"]
prerequisites: ["一阶QP", "QP标准形式"]
related: ["稀疏QP", "热启动", "MPC代码生成"]
upstream: ["[[一阶QP]]"]
source: "OSQP 官方文档（oxfordcontrol/OSQP）"
tags: [学习, 控制与机器人学, MPC]
---

# OSQP

> **一句话**：OSQP 是基于 ADMM 的开源 QP 求解器——为实时 MPC 而生：稀疏、可热启动、可提前终止，工业与学术界的事实标准。

## 0. 为什么学它

阶段作业-09 与车辆 MPC 的求解器就是 OSQP（或同族）。它是"一阶方法 + 稀疏 + 热启动 + 提前终止"四项能力合一的工程成品——本卡把前面的理论串成可直接使用的工具。

## 1. 什么是 OSQP

- **O**perator **S**plitting **Q**uadratic **P**rogram（算子分裂 QP）；
- 基于 ADMM 的一阶方法；
- 支持稀疏矩阵、不等式/等式约束、无导数要求。

## 2. 求解形式

$$\min \frac{1}{2} z^\top P z + q^\top z \quad \text{s.t.} \quad l \le Az \le u$$

## 3. 核心优势

| 优势 | 机制 |
|:---|:---|
| 稀疏 | 只处理非零元素 → 大规模可行 |
| 热启动 | 上次解作初值（见[[热启动]]） |
| 提前终止 | 每迭代检查精度，达标即停（见[[早期终止]]） |
| 多项式复杂度 | 迭代与问题规模弱相关 |
| 跨平台 | C 实现，嵌入式可用 |

## 4. 最小可手算例子（装配输入）

**题目**：QP 装配 $P = [2],\ q = [-4]$，约束 $z \le 3$（$A=[1], l=[-\infty], u=[3]$）。解释 OSQP 的输入与解。

**步骤**：
1. 无约束最优：$z^* = -q/P = 2$；
2. 约束 $z \le 3$：$2 \le 3$ 不激活 → 解 $z^* = 2$；
3. OSQP 输入 $(P, q, A, l, u)$ 五元组，输出 $z^*=2$ 与对偶乘子。

**含义**：MPC 每周期把 $(H, g, A_c, l_b, u_b)$ 塞给 OSQP（见[[QP标准形式]]），返回 $U^*$。

## 5. 常见误区

| 误区 | 正确理解 |
|:---|:---|
| OSQP 是内点法 | OSQP 是一阶 ADMM |
| 必须精确收敛 | 提前终止即可，MPC 只要足够好 |
| 求解器与问题无关 | 结构匹配（稀疏+热启动）决定速度 |

## 6. 代码生成与部署

- OSQP 支持生成独立 C 代码（见[[MPC代码生成]]）；
- 配合 CVXGEN/ECOS 生态，嵌入式 MPC 常用；
- Python 接口：cvxpy 默认后端之一。

## 7. 检索练习（闭卷）

1. 写出 OSQP 求解形式与输入五元组；
2. 手算一个装配例子；
3. 说明三大实时性优势。

## 8. 通过标准

- 能使用 OSQP 接口；
- 能手算简单 QP；
- 能说明部署路径。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/系统与硬件/15-控制与机器人学"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 复习

- 薄弱点写入 [[控制与机器人学错题漏洞入口]]；下次复习：重做装配手算。
