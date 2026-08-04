---
title: "主线-系统与硬件"
type: moc
kind: moc
flow: knowledge
track: "系统与硬件"
status: active
created: 2026-07-30
updated: 2026-07-30
tags:
  - MOC
  - 主线
  - 系统与硬件
  - 计算机底座
  - 控制系统
  - 知识网络
---

# 💻 主线：系统与硬件 (Systems, Computing & Systems Control Track)

> 🧭 **主线宗旨**：涵盖数据结构与算法、计算机组成原理、信号与系统以及控制与机器人学 4 门经典底层课程。打通从离散数据组织、指令集/硬件架构到连续信号处理与状态空间控制的底层工程与计算底座。

---

## 🗺️ 4 门子线路径逻辑递进图

```mermaid
flowchart TD
    subgraph 计算机与算法底座
        S0_1["[[🗺️ 数据结构与算法学习路径|10-数据结构与算法]]<br/>(数组, 链表, 树, 图, 动态规划)"]
        S0_2["[[🗺️ 计算机组成原理学习路径|11-计算机组成原理]]<br/>(CPU, 寄存器, Cache, 汇编, 内存)"]
    end

    subgraph 信号、系统与控制理论
        S1_1["[[🗺️ 信号与系统学习路径|12-信号与系统]]<br/>(Fourier/Laplace/Z 变换, LTI 系统, 频域分析)"]
        S1_2["[[🗺️ 控制与机器人学学习路径|15-控制与机器人学]]<br/>(状态空间方程, PID, LQR, 机器人运动学)"]
        S1_1 --> S1_2
    end

    S0_1 --> S1_2
```

---

## 🔑 全库唯一 Master 概念卡

算法、体系结构与控制理论核心概念统一收拢至基础课程 Master 卡：

1. **渐进时间与空间复杂度**：[[算法时间与空间复杂度]] ($\mathcal{O}(n \log n)$)
2. **CPU 存储层级与 Cache 命中率**：[[计算机存储层级与Cache]] (L1/L2/L3 Cache, Cache Line, TLB)
3. **连续与离散傅里叶变换**：[[傅里叶变换FFT]] ($X(e^{j\omega}) = \sum x[n]e^{-j\omega n}$)
4. **状态空间表达与系统能控/能观性**：[[状态空间控制方程]] ($\dot{\mathbf{x}} = \mathbf{A}\mathbf{x} + \mathbf{B}\mathbf{u}$)
5. **LQR 线性二次型调节器**：[[LQR控制与代数Riccati方程]] ($\mathbf{P}\mathbf{A} + \mathbf{A}^T\mathbf{P} - \mathbf{P}\mathbf{B}\mathbf{R}^{-1}\mathbf{B}^T\mathbf{P} + \mathbf{Q} = \mathbf{0}$)

---

## 📊 包含子路径看板 (Dataview)

```dataview
TABLE course AS "课程名称", status AS "状态", importance AS "优先级", updated AS "最近更新"
FROM "02-Knowledge/🧠 学习系统"
WHERE type = "index" AND track = "系统与硬件"
SORT file.name ASC
```

---

*主线更新时间：2026-07-30 | 状态：active*
