---
title: "MPC代码生成"
type: concept
course: "15-控制与机器人学"
stage_moc: "[[🧭 阶段9-MPC深入]]"
flow: knowledge
kind: concept
importance: "B"
status: completed
created: 2026-08-07
updated: 2026-08-07
tags: [学习, 控制与机器人学, MPC]
upstream:
  - "[[OSQP]]"
  - "[[QP标准形式]]"
concept: ["代码生成", "嵌入式部署"]
prerequisites: ["OSQP", "QP标准形式", "稀疏QP"]
related: ["OSQP", "稀疏QP", "显式MPC"]
---

# MPC代码生成

> **一句话**:MPC 的结构固定 → 把求解器的"循环与数据"提前编译成专用 C 代码——去掉解释开销,嵌入式平台也能跑实时 MPC。

## 为什么需要代码生成

- Python/MATLAB 原型慢、依赖重
- 嵌入式平台(ECU/MCU)资源有限
- 问题结构固定(矩阵维度不变)→ 可离线优化编译

## 生成的内容

| 模块 | 内容 |
|:---|:---|
| 矩阵组装 | $H, g, A, l, u$(提前符号化) |
| 求解内核 | 专用迭代循环(去通用化) |
| 预分解 | 因子分解离线完成(固定结构) |
| 接口 | 输入 $\mathbf{x}_k$,输出 $u_k$ 的 C API |

## 工具链

| 工具 | 说明 |
|:---|:---|
| OSQP codegen | 生成稀疏 QP C 代码 |
| CVXGEN | 凸优化代码生成(早期经典) |
| FORCES Pro | 商用 NMPC 代码生成 |
| acados | 高性能嵌入式 NMPC |
| MATLAB Coder | 通用转换 |

## 部署流程

1. 原型验证(Python/MATLAB)
2. 固定问题结构(维度、时域)
3. 代码生成 → 交叉编译 → 烧录
4. 硬件在环(HIL)测试

## 关键收益

- 求解时间:毫秒级 → 微秒级(预编译 + 稀疏)
- 内存:静态分配,无运行时依赖
- 确定性:无 GC、无动态内存

## 自检

- [ ] 代码生成解决什么问题?
- [ ] 生成模块包含什么?
- [ ] 主流工具链有哪些?
