---
type: study
topic: "MPC横向约束"
course: "控制与机器人学"
created: 2026-04-18
updated: 2026-08-07
status: completed
difficulty: advanced
stage_moc: "[[🧭 阶段6-横向控制]]"
flow: knowledge
kind: derivation
concept: ["MPC横向", "约束", "QP"]
prerequisites: ["MPC横向预测", "输入幅值约束"]
related: ["MPC横向预测", "MPC横向代价"]
upstream: ["[[06-横向控制/MPC横向预测]]"]
source: "MPC 标准文献; PythonRobotics"
tags: [学习, 控制与机器人学, MPC横向]
---

# MPC横向约束

## 0. 为什么学它

横向 MPC 相对 LQR 的核心优势是**处理约束**：转向角有物理极限、转向速率有执行器限制。把这些写成线性约束加入优化，控制器就"知道"自己不能做什么——这是 MPC 区别于 LQR 的关键。

## 1. 核心约束

**转向幅值约束**（执行器物理极限）：

$$\delta_{min}\le\delta_k\le\delta_{max}\quad(\forall k).$$

**转向速率约束**（液压/电机限制）：

$$-\Delta\delta_{max}\le \delta_k-\delta_{k-1}\le\Delta\delta_{max}.$$

**可选状态约束**（如横向偏差限制/障碍避让）：

$$e_{y,min}\le e_{y,k}\le e_{y,max}.$$

**QP 形式**：所有约束对优化变量 $\delta$ 是线性的 → 整体构成 QP（见 [[QP标准形式]]、[[MPC横向求解]]）。

## 2. 最小可手算例子（概念验证）

**题目**：$\delta_{max}=35°$，MPC 优化出的 $\delta_k=40°$ 会怎样？

**解**：约束使 $\delta_k$ 钳位到 $35°$——控制器"知道"物理极限，规划时不超出（这是 MPC 与 LQR 的本质差异：LQR 会默默要求超限输入）✓。

**易错点**：约束不可行（矛盾）时需松弛变量；速率约束引入 $\delta_{k-1}$ 耦合。

## 3. 常见误区

| 误区 | 正确理解 |
|:---|:---|
| 约束越多越好 | 可能不可行，需松弛 |
| 只约束幅值 | 速率约束对执行器同样重要 |
| 状态约束随意加 | 过紧状态约束导致无解 |

## 4. 与后续知识连接

- [[MPC横向代价]]、[[MPC横向求解]]；
- [[输入幅值约束]]、[[输入速率约束]]：一般形式；
- [[松弛变量]]：不可行处理。

## 5. 检索练习（闭卷）

1. 写出三类横向约束；
2. 说明 QP 形式；
3. 对比 LQR 的约束处理；
4. 不可行如何处理。

## 6. 通过标准

- 能写横向约束；
- 能理解 QP 形式；
- 能处理不可行。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/系统与硬件/15-控制与机器人学"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 复习

- 下次复习：3 天后重写约束；
- 薄弱点写入 [[控制与机器人学错题漏洞入口]]。
