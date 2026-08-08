---
type: study
topic: "MPC横向代价"
course: "控制与机器人学"
created: 2026-04-18
updated: 2026-08-07
status: completed
difficulty: advanced
stage_moc: "[[🧭 阶段6-横向控制]]"
flow: knowledge
kind: derivation
concept: ["MPC横向", "代价函数", "QP目标"]
prerequisites: ["MPC横向预测", "MPC代价函数"]
related: ["MPC横向预测", "MPC横向求解"]
upstream: ["[[MPC横向预测]]"]
source: "MPC 标准文献; PythonRobotics"
tags: [学习, 控制与机器人学, MPC横向]
---

# MPC横向代价

## 0. 为什么学它

MPC 的"目标"由**代价函数**定义：跟踪误差要小、转向要平顺。横向 MPC 代价把这些翻译成 QP 的二次目标，让优化器找到"最合适的转向序列"。

## 1. 核心代价

**横向 MPC 代价**（预测域 $N$）：

$$J=\sum_{k=0}^{N-1}\Big(x_k^\top Q x_k+\delta_k^\top R \delta_k+\Delta\delta_k^\top S\Delta\delta_k\Big)+x_N^\top P x_N,$$

- $Q$：误差权重（$e_y,e_\psi$ 等）；
- $R$：转向幅值权重（省力）；
- $S$：转向**速率**权重（平顺，防抖振）；
- $P$：终端权重（保证稳定性，常取 ARE 解）。

**QP 形式**：$J=\frac12 z^\top H z + c^\top z$（$z$ 为转向序列）——求解见 [[MPC横向求解]]。

## 2. 最小可手算例子（决策练习）

**题目**：跟踪急弯出现抖振，调哪个权重？

**解**：增大 $S$（转向速率权重）抑制转向抖动；或增大 $R$ 减小转向幅度。若仍抖，缩短 $N$ 或检查模型。

**易错点**：$Q,R,S$ 需按量级标定；速率项依赖 $\Delta\delta$ 需引入增量变量。

## 3. 常见误区

| 误区 | 正确理解 |
|:---|:---|
| 只有 $Q,R$ | 速率项 $S$ 对平顺关键 |
| 终端项可省 | 终端 $P$ 保证稳定（见 [[终端代价]]） |
| 权重与约束独立 | 代价与约束共同决定行为 |

## 4. 与后续知识连接

- [[MPC横向求解]]：QP 求解；
- [[MPC代价函数]]：一般形式；
- [[终端代价]]：稳定保证。

## 5. 检索练习（闭卷）

1. 写出横向 MPC 代价；
2. 说明各权重作用；
3. 抖振时调什么；
4. 终端项意义。

## 6. 通过标准

- 能写代价函数；
- 能整定权重；
- 能理解 QP 目标。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/系统与硬件/15-控制与机器人学"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 复习

- 下次复习：3 天后重写代价；
- 薄弱点写入 [[控制与机器人学错题漏洞入口]]。
