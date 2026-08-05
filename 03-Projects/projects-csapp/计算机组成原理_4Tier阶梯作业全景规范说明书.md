---
title: "计算机组成原理 4-Tier 阶梯作业全景规范说明书"
type: project
topic: "计算机组成原理 4-Tier 阶梯作业规范"
course: "计算机组成原理"
created: 2026-08-02
updated: 2026-08-02
status: active
flow: project
kind: moc
tags: [计算机组成原理, 4Tier作业, 阶梯作业, 编程实战, PyTest, CSAPP, Nand2Tetris]
---

# 💻 计算机组成原理 4-Tier 阶梯作业全景规范说明书 (CSAPP & Nand2Tetris 范式)

> 本说明书为 **11-计算机组成原理** 路径（基于 CSAPP 与 Nand2Tetris）提供严格的 **4-Tier Baseline** 划分标准与测试校验 Harness 规范。

---

## 🧭 4-Tier Baseline 梯队划分原则

```
🟢 L1 - Simple Baseline   │ C语言基本位运算 (Bitwise) / 汇编语言阅读与翻译 (x86/MIPS)
🟡 L2 - Medium Baseline   │ 缓存 (Cache) 命中率分析与代码访存优化 / Bomb Lab 逆向拆弹
🔴 L3 - Strong Baseline   │ [核心] 不依赖现有仿真器，从零手撕 Nand2Tetris 硬件描述语言 (HDL) 芯片构建与 Cache Simulator
👑 L4 - Boss Baseline     │ 编写超标量乱序执行 (Out-of-Order Execution) 模拟器 (Tomasulo 算法) / 完整实现 Malloc/Free (Malloc Lab)
```

---

## 🎯 计算机组成原理阶梯作业 4-Tier 细化规格清单

### 1. HW01 - 逻辑门与布尔算术 (Boolean Logic & Arithmetic - Nand2Tetris 1-2)
- **开源溯源**：Nand2Tetris Project 1 & 2 / CSAPP Ch 2
- 🟢 **L1**: 在 C 语言中完成数据表示作业 (Data Lab)，如仅用位运算实现取反、判断正负号。
- 🟡 **L2**: 解释补码 (Two's Complement) 的溢出原理，以及浮点数 IEEE 754 标准的精度丢失。
- 🔴 **L3 (手撕核心)**：**使用底层硬件描述语言 (HDL) 从纯 Nand 门手撕 Not, And, Or, Mux，并逐步构建出 16-bit ALU (算术逻辑单元)**。
- 👑 **L4**: 扩展 ALU 以支持浮点数加法与乘法的硬件级逻辑实现。

### 2. HW02 - 机器语言与 CPU 架构 (Machine Language & CPU - Nand2Tetris 4-5)
- **开源溯源**：Nand2Tetris Project 4 & 5 / CSAPP Ch 3 & 4
- 🟢 **L1**: 编写一段 Hack/MIPS 汇编程序完成数组求和与循环。
- 🟡 **L2**: 阅读并理解给定的 x86-64 汇编程序逻辑 (Bomb Lab 逆向拆弹)。
- 🔴 **L3 (手撕核心)**：**基于构建的 ALU 与寄存器，使用 HDL 从零手撕整个 Hack CPU 的取指 (Fetch)、译码 (Decode) 与执行 (Execute) 控制逻辑，并接入 Memory 形成完整计算机**。
- 👑 **L4**: 实现一个支持流水线 (Pipelining) 且具备数据旁路 (Data Forwarding) 与分支预测 (Branch Prediction) 的五级流水线 CPU 模拟器。

### 3. HW03 - 汇编器与虚拟机 (Assembler & VM - Nand2Tetris 6-8)
- **开源溯源**：Nand2Tetris Project 6-8
- 🟢 **L1**: 用高级语言 (Python/C++) 编写脚本剔除汇编代码中的注释与空格。
- 🟡 **L2**: 设计符号表 (Symbol Table) 解析汇编语言中的 Label 与变量 (Two-Pass 解析)。
- 🔴 **L3 (手撕核心)**：**手撕一个完整的汇编器 (Assembler) 将 Hack 汇编翻译为机器码；接着手撕 虚拟机翻译器 (VM Translator) 将堆栈虚拟机字节码翻译为汇编语言**。
- 👑 **L4**: 优化 VM 翻译器，使其能够根据上下文进行窥孔优化 (Peephole Optimization) 消除冗余的 Push/Pop。

### 4. HW04 - 存储器层次结构与缓存 (Memory Hierarchy & Cache - CSAPP Cache Lab)
- **开源溯源**：CSAPP Ch 6 (Cache Lab)
- 🟢 **L1**: 分析给定 C 代码的访存步长 (Stride) 对时间局部性与空间局部性的影响。
- 🟡 **L2**: 对矩阵乘法进行分块 (Blocking / Tiling) 优化以显著提升 Cache 命中率。
- 🔴 **L3 (手撕核心)**：**从零手撕一个 Cache Simulator (缓存模拟器)，准确模拟 LRU 替换策略，并在给定的内存追踪文件 (Trace File) 上精确输出 Hit/Miss/Eviction 统计信息**。
- 👑 **L4**: 实现非阻塞缓存 (Non-blocking Cache) 模拟器或实现完整的动态内存分配器 (CSAPP Malloc Lab: `malloc`, `free`, `realloc`，含显式空闲链表与红黑树管理)。

---

## 🧪 测试校验 Harness 规范 (`pytest` & 评测脚本)

在 `03-Projects/projects-csapp/tests/` 目录下运行单元测试，或使用专门的 Autograder 脚本：

```bash
python 03-Projects/projects-csapp/tests/HardwareSimulator.py # 测试 HDL
pytest 03-Projects/projects-csapp/tests/test_hw03_assembler.py
./03-Projects/projects-csapp/tests/test-csim -s 4 -E 1 -b 4 -t traces/yi.trace # Cache Lab 验证
```
