---
type: study
topic: "MPC代码生成"
course: "控制与机器人学"
created: 2026-08-07
updated: 2026-08-08
status: completed
difficulty: advanced
stage_moc: "[[🧭 阶段9-MPC深入]]"
flow: knowledge
kind: concept
concept: ["代码生成", "嵌入式部署"]
prerequisites: ["OSQP", "QP标准形式", "稀疏QP"]
related: ["OSQP", "稀疏QP", "显式MPC"]
upstream: ["[[09-MPC深入/OSQP]]"]
source: "OSQP codegen / CVXGEN / acados 文档"
tags: [学习, 控制与机器人学, MPC]
---

# MPC代码生成

> **一句话**：MPC 的结构固定 → 把求解器的"循环与数据"提前编译成专用 C 代码——去掉解释开销，嵌入式平台也能跑实时 MPC。

## 0. 为什么学它

Python 原型跑得动 ≠ 车载 ECU 跑得动。代码生成是"原型 → 量产"的桥梁：固定结构 + 预编译 + 静态内存，让 MPC 在资源受限平台上实时运行。

## 1. 为什么需要代码生成

- Python/MATLAB 原型慢、依赖重；
- 嵌入式平台（ECU/MCU）资源有限；
- 问题结构固定（矩阵维度不变）→ 可离线优化编译。

## 2. 生成的内容

| 模块 | 内容 |
|:---|:---|
| 矩阵组装 | $H, g, A, l, u$（提前符号化） |
| 求解内核 | 专用迭代循环（去通用化） |
| 预分解 | 因子分解离线完成（固定结构） |
| 接口 | 输入 $\mathbf{x}_k$，输出 $u_k$ 的 C API |

## 3. 工具链

| 工具 | 说明 |
|:---|:---|
| OSQP codegen | 生成稀疏 QP C 代码 |
| CVXGEN | 凸优化代码生成（早期经典） |
| FORCES Pro | 商用 NMPC 代码生成 |
| acados | 高性能嵌入式 NMPC |
| MATLAB Coder | 通用转换 |

## 4. 部署流程

1. 原型验证（Python/MATLAB）；
2. 固定问题结构（维度、时域）；
3. 代码生成 → 交叉编译 → 烧录；
4. 硬件在环（HIL）测试。

## 5. 常见误区

| 误区 | 正确理解 |
|:---|:---|
| 生成代码仍需求解器 | 生成的是专用求解内核，不依赖通用库 |
| 代码生成一劳永逸 | 结构变化（$N_p$ 等）需重新生成 |
| 只有 MPC 需要 | 任何固定结构优化问题都受益 |

## 6. 关键收益

- 求解时间：毫秒级 → 微秒级（预编译 + 稀疏）；
- 内存：静态分配，无运行时依赖；
- 确定性：无 GC、无动态内存。

## 7. 检索练习（闭卷）

1. 说明代码生成解决的问题；
2. 列出生成模块；
3. 说明主流工具链。

## 8. 通过标准

- 能解释代码生成必要性；
- 能列出生成内容；
- 能说明部署流程。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/系统与硬件/15-控制与机器人学"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 复习

- 薄弱点写入 [[控制与机器人学错题漏洞入口]]；下次复习：重述工具链。
