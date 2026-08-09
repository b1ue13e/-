---
type: project
project_type: homework
course: "随机过程"
assignment_id: "SP-S03"
assignment_level: stage
assignment_format: project
stage_id: "03"
requires: ["[[随机过程-布朗运动反射原理与二次变差]]", "[[随机过程-鞅停时与可选停止]]", "[[随机过程-鞅不等式与收敛]]"]
source_type: local_integration_task
source: "本地原创阶段项目；对齐 MIT 15.070J Lectures 6–12"
source_url: "https://ocw.mit.edu/courses/15-070j-advanced-stochastic-processes-fall-2013/pages/lecture-notes/"
license: "本地原创任务；MIT OCW link-only"
created: 2026-08-09
updated: 2026-08-09
status: planned
flow: project
tags: [作业, 阶段作业, Brownian运动, 鞅, 停时]
---

# 随机过程｜阶段作业 03：Brownian、鞅与停时双证据

## 学习目标

完成本阶段后，学习者应能同时处理连续路径事件、离散停时和鞅收敛条件，并在理论证明与数值证据冲突时优先检查假设和离散误差。

## 任务身份与目标

完成一次“证明—模拟—失败解释”闭环：用 Brownian 最大值和二次变差建立连续路径证据，用有限区间随机游走验证可选停止，再用不等式说明为何有限样本不能取代收敛证明。

## 任务边界

Brownian 最大值实验只使用离散网格近似；可选停止只在有限区间随机游走上使用；不得把有限样本、路径图或经验均值写成连续时间定理。

## 必做模块

### A｜Brownian 路径审计（35 分）

1. 推导 $P(M_T\ge a)$，并说明离散网格最大值的单调偏差。
2. 使用三个网格和至少 5,000 条路径，报告最大值概率、终点尾概率、二次变差均值及误差。
3. 解释网格加密同时改变了离散误差和计算成本，保留最不理想的一档结果。

### B｜停时与边界概率（35 分）

1. 对 $S_n$、$S_n^2-n$ 写出鞅验证。
2. 对 $\tau=\inf\{n:S_n\in\{0,10\}\}$ 逐项验证可选停止条件。
3. 推导从 3 出发命中 10 的概率与期望停止步数。
4. 调用 `simulate_gamblers_ruin`，用三个种子报告概率和停止时间的误差范围。

### C｜收敛与失败边界（30 分）

1. 比较非负上鞅、$L^p$ 有界鞅和一致可积鞅的结论。
2. 用一个尾部质量反例解释 a.s. 收敛不保证 $L^1$ 收敛。
3. 写一段“错误审稿意见”：指出把公平性、有限样本稳定和可选停止混为一谈的三处错误。

## 提交产物

```text
submission/SP-S03/
├── report.md
├── brownian_martingale_audit.py
├── brownian-results.csv
├── stopping-results.csv
├── figures/              # 可选；不得用图替代理论证明
└── run.log
```

## Rubric（100 分）

| 维度 | 分值 | 通过证据 |
| :--- | ---: | :--- |
| Brownian 理论 | 25 | 反射原理、二次变差与路径边界正确 |
| 停时证明 | 25 | 鞅、停时、可积性和停止条件完整 |
| 实验复现 | 25 | 多网格、多种子、误差范围和原始结果齐全 |
| 收敛辨析 | 15 | a.s./$L^1$/$L^p$/UI 不混淆 |
| 失败审计 | 10 | 能识别并解释错误结论 |

## 通过条件

总分至少 80，且 A、B 两模块均不得低于 60%。硬失败包括：把 Brownian 最大值公式用于任意过程；未验证停时条件；将路径离散结果写成连续定理；删除失败运行。

## 引导自检

- 每次使用可选停止前，列出停时、适应性、可积性和界条件。
- 先预测网格偏差方向，再运行模拟；预测错误必须保留并解释。
- 把“a.s. 收敛”“$L^1$ 收敛”和“经验频率接近”写成三个不同结论。
