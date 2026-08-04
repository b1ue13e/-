---
title: "计算机组成原理-题型-MallocLab与位运算拆弹阶梯作业"
type: problem-type
kind: problem-type
flow: knowledge
topic: "计算机组成原理作业"
course: "11-计算机组成原理"
created: 2026-07-29
updated: 2026-07-29
date: 2026-07-29
status: learning
difficulty: advanced
importance: A
concept: ["计算机体系结构", "CSAPP", "内存分配器"]
prerequisites: ["[[02-Knowledge/🧠 学习系统/10-数据结构与算法/🗺️ 数据结构与算法学习路径|数据结构]]"]
related: ["[[数据结构与算法-题型-BYOW迷宫与高级数据结构阶梯作业]]"]
upstream: ["[[11-计算机组成原理/🗺️ 阶段零：总图景|计算机组成原理学习路径]]"]
downstream: []
tags: [学习, 11-计算机组成原理, 作业, 实战, 阶梯作业]
aliases: ["CSAPP-MallocLab-作业"]
---

# 计算机组成原理 - HW02：MallocLab 与位运算拆弹阶梯作业

> 🎯 **作业目标**：通关 CS:APP 经典 Lab：`DataLab` (位运算), `BombLab` (逆向拆弹), 以及手写 C 语言显式空闲链表内存分配器 (`MallocLab`)。

---

## 1. ⚙️ 环境与 Starter Code 准备
- **Starter Code 路径**：`03-Projects/projects-csapp/malloclab/`
- **开源标杆仓库**：[CMU 15-213 CS:APP Labs](https://csapp.cs.cmu.edu/3e/labs.html)
- **核心依赖**：`gcc`, `gdb`, `make`, `valgrind`

---

## 2. 🎯 阶梯式 Baseline / 难度设计 (4-Tier Difficulty)

| 梯度级别 | 目标 / 性能分 | 关键实现细节与要求 |
| :--- | :--- | :--- |
| 🟢 **L1 - Simple Baseline** | DataLab 全通 | 仅受限使用位运算符（`~`, `&`, `^`, `|`, `+`, `<<`, `>>`）实现整数与浮点数特定逻辑。 |
| 🟡 **L2 - Medium Baseline** | BombLab & AttackLab | 使用 GDB 逆向汇编代码破解 6 阶段密码，利用 ROP (Return-Oriented Programming) 实施缓冲区溢出攻击。 |
| 🔴 **L3 - Strong Baseline** | MallocLab 性能分 ≥ 85 | **手写 C 语言显式空闲链表内存分配器** (`mm_malloc`, `mm_free`, `mm_realloc`)，实现双向合并 (Coalescing)。 |
| 👑 **L4 - Boss Baseline** | 5 级流水线 CPU | 在 Logisim 或 Verilog 中完整设计并实现带 Cache 和 Forwarding / Hazard Unit 的 RISC-V 5 级流水线 CPU。 |

---

## 3. 🧪 自动化测试 Harness (C Driver Benchmark)

在 `malloclab` 目录下执行自动评测：
```bash
make
./mdriver -V
```

要求输出测试得分：
```text
Results for mm malloc:
Trace                        Valid  Util     Ops  Time  Kops
amptjp-bal.rep                 yes   90%   24000 0.002 12000
cccp-bal.rep                   yes   89%   58000 0.005 11600
...
Perf index = 55 (util) + 35 (thru) = 90/100
```

---

## 🃏 Anki 卡片

- Q: 在手写 `malloc` 内存分配器时，为什么“脚部 (Footer / Boundary Tag)”对于 $O(1)$ 时间内进行前向合并 (Coalesce With Previous Block) 至关重要？
- A: 如果没有脚部，释放当前块时无法直接获知前一个块的大小和空闲状态。脚部在块的末尾记录了大小和使用位，使当前块只需检查上一字节（即前一块的脚部）即可在 $O(1)$ 时间判定并合并。
