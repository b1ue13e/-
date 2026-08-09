---
type: project
project_type: homework
course: "计算机组成原理"
assignment_id: "计算机组成原理-03"
assignment_level: capstone
assignment_format: project
stage_id: "03"
requires: ["[[01-CPU架构/CPU与取指执行循环]]", "[[01-CPU架构/数据通路与指令周期]]", "[[02-内存管理/缓存设计]]", "[[02-内存管理/缓存性能]]", "[[03-性能与优化/优化综合案例]]", "[[03-性能与优化/Roofline模型]]"]
source_type: open_source_project_task
adapted_from: "Nand2Tetris Project 5 + CSAPP Cache Lab 融合"
source_url: "https://www.nand2tetris.org/project05"
license: "Nand2Tetris 官方许可（个人学习可复用 Starter Code）；CSAPP Lab 仅用公开规格"
created: 2026-08-08
updated: 2026-08-08
status: planned
flow: project
tags: [作业, 计算机组成原理, 大作业]
---

# 计算机组成原理-大作业-从逻辑门到缓存感知的CPU

> 非官方中文版：任务结构保留 Nand2Tetris P5 官方编号与 CSAPP Cache Lab 公开规格，语义本地化。

## 1. 作业身份

- 课程：计算机组成原理（跨阶段1-3 综合）
- 规模：`capstone`（大作业）｜形态：`project`（硬件设计 + 性能分析）
- 来源：Nand2Tetris Project 5（CPU 构建）+ CSAPP Cache Lab（缓存分析），`adapted_from`
- 前置知识：[[01-CPU架构/数据通路与指令周期]]、[[02-内存管理/缓存设计]]、[[03-性能与优化/优化综合案例]]

## 2. 学习目标

完成后你应该能够：

1. 从零构建一个可运行的 16-bit CPU（取指→译码→执行闭环），并跑通官方测试；
2. 用 HDL 实现数据通路核心部件（PC/寄存器堆/ALU 连接）；
3. 用 CSAPP Cache Lab 的模拟器分析缓存参数对性能的影响，验证 4C 缺失模型；
4. 用 Roofline 模型解释"CPU 已到上限，瓶颈在访存"的典型场景；
5. 输出一份完整报告：问题定义、设计决策、测试证据、性能分析、错误与改进。

## 3. 任务背景与边界

- 环境：Nand2Tetris HardwareSimulator（CPU 部分）+ 自选语言实现缓存模拟器（Cache 部分）；
- 输入输出：`CPU.hdl` 通过官方 `.tst`；缓存模拟器对给定 trace 输出命中率/AMAT；
- 禁止事项：不得复制官方参考实现；缓存模拟器必须自己实现（可参考公开规格，不抄代码）。

## 4. 详细题目

### Part A：CPU 构建（Nand2Tetris P5）

- A1 数据通路：用先前芯片实现 `CPU.hdl`（含 PC、寄存器堆、ALU、控制逻辑）；
- A2 内存接口：连接 `Memory.hdl`，支持 `A-instruction`/`C-instruction`；
- A3 完整验证：通过官方 `CPU.tst`、`CPU-external.tst`，并跑通 P5 冒烟测试。

### Part B：缓存性能分析（CSAPP Cache Lab 公开规格）

- B1 实现一个参数化缓存模拟器（组数/路数/块大小可配），解析给定内存 trace；
- B2 做参数扫描：固定块大小变组数、固定组数变块大小，输出命中率对比表；
- B3 用 AMAT 公式把命中率转成平均访问时间，识别该 trace 的缺失类型（强制/容量/冲突）。

### Part C：综合分析与报告

- C1 用 Roofline 模型分析 CPU 构建中的"计算强度 vs 访存瓶颈"；
- C2 回答：如果缓存命中率提升 10%，AMAT 变化多少？对整体性能影响多大？
- C3 报告必须包含：问题定义、方法、数据、结果表、失败案例、限制与改进方向。

## 5. 环境与复现

- Nand2Tetris 软件套件（HardwareSimulator，Java）；
- 缓存模拟器：C 或 Python，需提供 `README`（运行命令、trace 格式、参数说明）；
- trace 数据：CSAPP 官方公开 trace（`csim.c` 规格内）或自造 3 个 trace（顺序/随机/步长跳变）；
- 随机种子：若模拟器含随机行为需固定种子；本作业模拟器应为确定性输入输出。

## 6. 提交产物

- `hdl/CPU.hdl`、`hdl/Memory.hdl` 及依赖芯片；
- `cache_sim/`（模拟器源码 + 3 个 trace + 输出日志）；
- `报告.md`（Part A-C 全部要求）；
- 测试证据：官方 `.tst` 通过截图/日志、缓存模拟器输出。

## 7. 验收标准与 Rubric（满分 100）

| 维度 | 分值 | 标准 |
|:---|:---:|:---|
| CPU 正确性 | 30 | 官方 .tst 全通过；能跑 P5 冒烟测试 |
| 缓存模拟器 | 25 | 参数可配、结果可复现；与手算/已知结果一致 |
| 参数扫描与分析 | 20 | B2 表格完整；B3 缺失类型判断有依据 |
| 报告质量 | 15 | 问题定义/方法/数据/结论完整；失败案例诚实 |
| Roofline 分析 | 10 | C1-C2 推导正确、结论与数据一致 |

- ≥85 且 CPU 部分（A1-A3）全部通过 → 大作业完成；
- 缓存模拟器允许部分参数正确（≥2 组扫描）降级为"通过但有改进项"。

## 8. 引导与自检（不泄露答案）

- 检查点 1：`CPU.hdl` 能否在无测试脚本下用 `add 1 2` 类指令手动验证？
- 检查点 2：缓存模拟器对"全顺序访问" trace 的命中率是否明显高于"全随机"？
- 常见失败：PC 更新时序错（组合 vs 时序混用）；缓存模拟器地址切分位错（索引/偏移算反）；
- 提交前清单：□ 官方测试全过；□ 模拟器输出可复现；□ 报告含失败案例。

## 9. 进阶任务（可选，非主任务前置）

- 在 CPU 上跑通一个自写汇编小程序（如乘法循环），验证"从 HDL 到程序"全链路；
- 缓存模拟器扩展：实现 LRU 替换并对比随机替换的命中率差异。

## 10. 后续入口

完成本作业 → 达到课程验收标准，可进入 [[🗺️ 计算机组成原理学习路径|课程复习]] 复习闭环或 [[🗺️ 计算机组成原理学习路径|课程复盘]]。
