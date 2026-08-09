---
type: project
project_type: homework
course: "随机过程"
assignment_id: "SP-L03"
assignment_level: lesson
assignment_format: lab
stage_id: "02"
requires: ["[[随机过程-泊松过程指数等待与更新]]", "[[随机过程-连续时间马尔可夫链与生成元]]", "[[随机过程-MM1排队与Little律]]"]
source_type: local_integration_task
source: "本地原创实验；知识顺序参考 MIT 6.262 Chapters 2, 4, and 6"
source_url: "https://ocw.mit.edu/courses/6-262-discrete-stochastic-processes-spring-2011/pages/course-notes/"
license: "本地原创任务；MIT OCW link-only"
created: 2026-08-08
updated: 2026-08-08
status: planned
flow: project
tags: [作业, 随机过程, Poisson过程, CTMC, 排队]
---

# 随机过程｜课后作业 03：Poisson、CTMC 与排队

## 学习目标

在计数、等待、生成元和队列四种表示之间转换，并用事件驱动模拟检查理论量及不稳定边界。

## 任务边界

- 只使用本地原创参数；不复制外部题目或答案。
- 所有速率单位为“每小时”；报告中不得混入分钟而不换算。
- M/M/1 稳态分析只在 $\lambda<\mu$ 时进行；不稳定案例必须显式拒绝。
- Python 3.11+ 标准库；参考函数可导入，但主报告必须解释算法。

## 题目

### Q1｜计数与等待（20 分）

到达率 $\lambda=3$/小时。

1. 求两小时内恰好 4 次到达的概率。
2. 求首次等待超过 20 分钟的概率。
3. 求第三次到达时间的均值和方差。
4. 从 $P(N(t)=0)$ 推导指数等待，不直接引用结论。

### Q2｜叠加、分裂与非齐次（20 分）

1. 两个独立流速率为 2 和 5，写出叠加流分布。
2. 每个到达以 0.3 概率标记为高优先级，写出两类流速率及独立性条件。
3. 若 $\lambda(t)=2+t$，求区间 $[1,3]$ 的累计强度和零到达概率。
4. 给出一个依赖历史的标记规则，使独立分裂结论失效。

### Q3｜生成元（20 分）

给定

$$
Q=\begin{pmatrix}-2&2\\1&-1\end{pmatrix}.
$$

1. 检查其合法性。
2. 写出每个状态的平均停留时间和嵌入链。
3. 求平稳分布并验证 $\pi Q=0$。
4. 写出 $P(h)$ 的一阶短时近似。

### Q4｜M/M/1 理论（20 分）

对 $(\lambda,\mu)=(2,3)$ 推导 $\rho,\pi_n,L,L_q,W,W_q$。再对 $(3,3)$ 解释为何不能给稳态指标。

### Q5｜事件驱动模拟（20 分）

运行并保存：

```powershell
python scripts/stochastic_process_lab.py all --seed 20260808 --output submission/SP-L03/reference.json
```

随后自行调用 `simulate_mm1`，比较 horizon 为 2,000、20,000、100,000 时的时间平均 $L$。固定 burn-in 为总时长的 10%，至少使用三个不同种子，并报告误差范围。额外调用一次 $\lambda=\mu$，保存真实异常文本。

## 提交产物

```text
submission/SP-L03/
├── answers.md
├── queue_experiment.py
├── queue_metrics.csv
├── unstable-error.txt
├── reference.json
└── run.log
```

## 100 分 Rubric

| 维度 | 分值 | 通过证据 |
| :--- | ---: | :--- |
| Poisson/等待转换 | 20 | 参数和单位正确 |
| 叠加/分裂/非齐次 | 20 | 独立性与累计强度写全 |
| CTMC 生成元 | 20 | 速率、停留和稳态一致 |
| M/M/1 推导 | 20 | 稳定条件及四指标完整 |
| 实验与失败证据 | 20 | 时间加权、burn-in、多种子、异常保留 |

## 提示、硬失败与自检

- 提示：先判断对象是计数、等待还是速率；队长均值必须按时间加权。
- 硬失败：对 $\rho\ge1$ 返回稳态；用普通采样点平均代替时间平均；删掉异常；rate/scale 混用。
- 自检：每项结论是否标明理论值、经验值、样本量、种子和单位？

通过线 80/100。完成后可进入[[随机过程-阶段作业-02-Markov泊松与排队仿真]]。
