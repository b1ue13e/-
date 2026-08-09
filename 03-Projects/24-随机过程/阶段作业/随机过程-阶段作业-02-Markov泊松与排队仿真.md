---
type: project
project_type: homework
course: "随机过程"
assignment_id: "SP-S02"
assignment_level: stage
assignment_format: lab
stage_id: "02"
requires: ["[[随机过程-离散时间马尔可夫链]]", "[[随机过程-状态分类与平稳分布]]", "[[随机过程-泊松过程指数等待与更新]]", "[[随机过程-连续时间马尔可夫链与生成元]]", "[[随机过程-MM1排队与Little律]]"]
source_type: local_integration_task
source: "本地原创阶段实验；覆盖 MIT 6.262 Chapters 2–6 的离散—连续结构"
source_url: "https://ocw.mit.edu/courses/6-262-discrete-stochastic-processes-spring-2011/pages/course-notes/"
license: "本地原创任务；MIT OCW link-only"
created: 2026-08-09
updated: 2026-08-09
status: planned
flow: project
tags: [作业, 阶段作业, Markov链, Poisson过程, 排队]
---

# 随机过程｜阶段作业 02：Markov、Poisson 与排队仿真

## 学习目标

完成本阶段后，学习者应能在离散转移、连续跳转、计数等待和排队时间平均之间切换表示，并对不存在稳态或不收敛的情形给出拒绝证据。

## 任务身份与目标

用同一份报告串起四种表示：离散转移矩阵、Poisson 到达、CTMC 生成元和 M/M/1 队列。每个经验结论必须先有理论对象，再说明有限样本和稳定性边界。

## 任务边界

所有速率统一使用“每小时”；有限 Markov 链的经验频率不替代常返性证明；M/M/1 的队长必须按事件区间面积计算。只使用已讲的有限状态和可数状态模型。

## 题面

1. 对给定三状态转移矩阵，计算一条三步路径概率、两步转移概率和分布推进，并检查归一化。
2. 对一个含两个闭类的矩阵，画出状态图，分类互达类、周期、常返/暂留和全部平稳分布；解释为何平稳分布不必唯一。
3. 对速率 $\lambda=3$/小时的 Poisson 过程，推导两小时计数概率、首次等待和第三次到达时间矩；再说明叠加、分裂和非齐次强度的适用条件。
4. 对 $Q=\begin{pmatrix}-2&2\\1&-1\end{pmatrix}$，求停留时间、嵌入链、平稳分布和一阶短时转移近似。
5. 对 $(\lambda,\mu)=(2,3)$ 推导 M/M/1 的 $\rho,L,L_q,W,W_q$，并解释 $\lambda=\mu$ 时为什么不报告稳态指标。
6. 使用 `simulate_markov_chain`、`simulate_poisson_counts` 和 `simulate_mm1`，对至少三个样本规模报告经验误差；M/M/1 必须采用时间加权面积，不得用等间隔采样点平均冒充时间平均。
7. 记录一个周期链、一个不稳定队列和一个 burn-in 改变后的结果，分别解释“分布不收敛”“稳态不存在”和“初始条件影响”。

## 提交产物

```text
submission/SP-S02/
├── report.md
├── simulate_stage2.py
├── markov-results.csv
├── poisson-results.csv
├── queue-results.csv
└── run.log
```

## Rubric（100 分）

| 维度 | 分值 | 通过证据 |
| :--- | ---: | :--- |
| DTMC 与状态分类 | 25 | 路径、类、周期和全部平稳分布正确 |
| Poisson 与 CTMC | 25 | 计数—等待—生成元转换无单位错误 |
| M/M/1 理论 | 20 | 稳定条件和四项长期指标完整 |
| 实验设计 | 20 | 时间加权、多规模、burn-in 和失败案例齐全 |
| 边界解释 | 10 | 不把有限样本或数值输出当定理 |

## 硬失败与进入门

硬失败包括：转移矩阵方向错误；可约链只写一个平稳分布；对 $\rho\ge1$ 返回稳态；删除不稳定异常；未记录速率单位。通过线为 80/100；通过后进入阶段 3。

## 引导自检

- 先画状态图，再列矩阵；先判断稳定条件，再计算队列指标。
- 每个经验值同时写出样本规模、burn-in、种子和理论基线。
- 检查离散时间平均与连续时间加权平均是否被误换。
