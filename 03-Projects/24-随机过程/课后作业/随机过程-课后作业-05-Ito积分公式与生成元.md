---
type: project
project_type: homework
course: "随机过程"
assignment_id: "SP-L05"
assignment_level: lesson
assignment_format: problem-set
stage_id: "04"
requires: ["[[随机过程-Ito积分与Ito等距]]", "[[随机过程-Ito公式生成元与鞅构造]]"]
source_type: local_integration_task
source: "本地原创题集；知识顺序参考 MIT 15.070J Lectures 14–17"
source_url: "https://ocw.mit.edu/courses/15-070j-advanced-stochastic-processes-fall-2013/pages/lecture-notes/"
license: "本地原创任务；MIT OCW link-only"
created: 2026-08-08
updated: 2026-08-08
status: planned
flow: project
tags: [作业, 随机过程, Ito积分, Ito公式, 生成元]
---

# 随机过程｜课后作业 05：Itô 积分、公式与生成元

## 学习目标

从简单适应过程出发构造随机积分，使用 Itô 等距完成二阶矩计算，并把 Itô 公式转换为生成元与鞅构造，而不是只背 $(dW)^2=dt$。

## 任务边界与环境

- 理论部分必须写出适应性、平方可积性和光滑性条件。
- 代码只允许 Python 3.11+ 标准库；模拟使用左端点和式。
- 不允许使用右端点和式后仍称为 Itô 积分；比较不同和式时必须明确命名。

## 题目

### Q1｜简单过程与 Itô 等距（25 分）

令 $0<t_1<T$，

$$
H_t=2\mathbf 1_{(0,t_1]}(t)+W_{t_1}\mathbf 1_{(t_1,T]}(t).
$$

1. 验证 $H$ 适应且平方可积。
2. 写出 $\int_0^T H_t\,dW_t$ 的有限和表达式。
3. 用条件期望证明积分均值为 0。
4. 用 Itô 等距求二阶矩，并独立展开有限和复核交叉项。

### Q2｜Itô 公式与矩（30 分）

1. 对 $f(x)=x^4$ 应用 Itô 公式，推导 $E[W_T^4]=3T^2$。
2. 验证 $\exp(\theta W_t-\theta^2t/2)$ 是鞅，并写出所需可积性说明。
3. 对 $dX_t=bX_tdt+\sigma X_tdW_t$ 推导 $d\log X_t$，解释二阶修正。
4. 指出把随机链式法则写成普通链式法则会在哪个可观察量上产生偏差。

### Q3｜生成元与 Dynkin 入口（20 分）

对 OU 过程 $dX_t=\kappa(\theta-X_t)dt+\sigma dW_t$：

1. 写出生成元 $\mathcal L$。
2. 分别取 $f(x)=x$ 与 $f(x)=x^2$，推导均值和二阶矩微分方程。
3. 给出使 $u(t,X_t)$ 成为局部鞅的 PDE 条件。
4. 说明局部鞅升级为真鞅还需要哪类可积性控制。

### Q4｜左端点和式数值检查（25 分）

自行实现同一 Brownian 路径上的

$$
I_N=\sum_{k=0}^{N-1}W_{t_k}(W_{t_{k+1}}-W_{t_k})
$$

并与 $(W_T^2-T)/2$ 比较。

1. 使用 `N=50, 200, 800`，每档至少 4,000 条路径。
2. 报告均方误差和平均偏差，并使用同一批路径比较网格。
3. 额外实现右端点和式，观察极限差异，但不得把它标为 Itô 和式。
4. 解释误差来自离散网格还是 Monte Carlo 估计，并给出判断证据。

## 提交产物

```text
submission/SP-L05/
├── answers.md
├── ito_sum_experiment.py
├── ito-sum-results.csv
└── run.log
```

## 100 分 Rubric

| 维度 | 分值 | 通过证据 |
| :--- | ---: | :--- |
| 积分构造与等距 | 25 | 适应性、交叉项和二阶矩完整 |
| Itô 公式推导 | 30 | 四次矩、指数鞅和 GBM 修正正确 |
| 生成元与矩方程 | 20 | 作用对象、PDE 条件和可积性边界清楚 |
| 数值验证 | 15 | 同路径、多网格、左右端点区分正确 |
| 复现与解释 | 10 | 原始输出、误差定义和命令齐全 |

## 提示、硬失败与自检

- **必要提示**：展开 $W_t^4$ 后，随机积分项的期望为零需要先检查平方可积性。
- **硬失败**：把 Itô 等距写成路径等式；遗漏二阶项；用独立路径比较网格；左右端点和式不区分。
- **自检**：公式中每个导数的取值点是否明确？数值误差是否定义后再计算？

通过线为 80/100 且无硬失败。完成后继续[[随机过程-课后作业-06-SDE与Euler误差审计]]。

