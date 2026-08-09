---
type: project
project_type: homework
course: "随机过程"
assignment_id: "SP-L02"
assignment_level: lesson
assignment_format: problem-set
stage_id: "02"
requires: ["[[随机过程-离散时间马尔可夫链]]", "[[随机过程-状态分类与平稳分布]]"]
source_type: local_integration_task
source: "本地原创题集；知识顺序参考 MIT 6.262 Chapters 3 and 5"
source_url: "https://ocw.mit.edu/courses/6-262-discrete-stochastic-processes-spring-2011/pages/course-notes/"
license: "本地原创任务；MIT OCW link-only"
created: 2026-08-08
updated: 2026-08-08
status: planned
flow: project
tags: [作业, 随机过程, Markov链, 平稳分布]
---

# 随机过程｜课后作业 02：Markov 链状态与稳态

## 学习目标

从条件概率、状态图和矩阵三个角度分析有限 Markov 链，严格区分平稳分布、分布收敛和时间平均。

## 任务边界

- 本作业只讨论有限齐次 Markov 链；不得把模拟频率当作常返性证明。
- 本地任务不复制 MIT 6.262 题目；官方材料只用于复习章节顺序。
- 数值部分使用 `scripts/stochastic_process_lab.py` 或自己等价实现，但必须保留矩阵合法性检查。

## 题目

### Q1｜路径概率与 Chapman-Kolmogorov（20 分）

给定

$$
P=\begin{pmatrix}
0.7&0.2&0.1\\
0.1&0.6&0.3\\
0.2&0.2&0.6
\end{pmatrix},\qquad \mu_0=(1,0,0).
$$

1. 计算路径 $0\to1\to2\to2$ 的概率。
2. 手算 $p_{02}^{(2)}$，明确列出三个中间状态。
3. 计算 $\mu_2$ 并检查归一化。

### Q2｜状态分类（25 分）

分析

$$
P_A=\begin{pmatrix}
1&0&0&0\\
0.4&0&0.6&0\\
0&0&0.5&0.5\\
0&0&0&1
\end{pmatrix}.
$$

1. 画状态图并找出互达类、闭类和吸收状态。
2. 判断各状态常返或暂留。
3. 写出全部平稳分布，并解释不唯一来源。

### Q3｜周期与收敛（25 分）

对确定性交替链和在每个状态增加 $0.1$ 自环后的链：

1. 分别求周期和平稳分布。
2. 从状态 0 出发描述 $P^n(0,\cdot)$ 的极限行为。
3. 解释为何自环会破坏周期，但不改变“存在平稳分布”的基本方程。

### Q4｜理论—经验对照（30 分）

使用矩阵

$$
P=\begin{pmatrix}0.8&0.2\\0.3&0.7\end{pmatrix}
$$

和种子 `20260808`：

1. 手算平稳分布。
2. 分别从状态 0、1 模拟 1,000、10,000、100,000 步。
3. 报告经验频率、绝对误差和前 100 步 burn-in 是否剔除。
4. 解释误差为何不应随样本量严格单调下降。

## 提交产物

```text
submission/SP-L02/
├── answers.md
├── simulate_markov.py
├── frequencies.csv
└── run.log
```

`frequencies.csv` 至少含 `initial_state, steps, burn_in, state, frequency, theory, abs_error, seed`。

## 100 分 Rubric

| 维度 | 分值 | 通过证据 |
| :--- | ---: | :--- |
| Markov 分解与矩阵 | 20 | 路径和中间状态求和正确 |
| 状态分类 | 25 | 类、闭性、常返性有依据 |
| 周期与长期行为 | 25 | 三种长期结论不混淆 |
| 模拟与复现 | 20 | 初值/长度/burn-in/种子完整 |
| 解释边界 | 10 | 不把有限频率当证明 |

## 提示、硬失败与自检

- 提示：先画状态图，再做矩阵；求平稳分布后必须代回检查。
- 硬失败：可约链只给一个平稳分布；不记录初始状态；把周期链的经验时间平均误写成 $P^n$ 收敛。
- 自检：每个概率向量是否非负且和为 1？每个分类是否说明“为什么”？

通过线 80/100。完成后继续学习 Poisson、CTMC 与排队三张卡。
