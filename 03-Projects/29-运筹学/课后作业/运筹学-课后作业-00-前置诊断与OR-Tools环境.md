---
type: project
project_type: homework
course: "运筹学"
assignment_id: "运筹学-00"
assignment_level: lesson
assignment_format: problem-set
stage_id: "00"
requires:
  - "[[运筹学-前置-线性代数最小集]]"
  - "[[运筹学-前置-概率与期望]]"
  - "[[运筹学-前置-OR-Tools环境与建模]]"
source_type: local_integration_task
created: 2026-08-06
status: planned
flow: project
tags: [作业, 运筹学, 前置诊断]
---

# 运筹学-课后作业-00-前置诊断与OR-Tools环境

> 所属阶段：[[🧭 29-运筹学-前置知识|前置知识层]] ｜ 形态：题集（problem-set）

## 学习目标

证明你具备进入第一阶段的四件套：手算线代、写期望、判断凸性、跑通 OR-Tools。

## 所需知识

- [[运筹学-前置-线性代数最小集]]：高斯消元、秩、基。
- [[运筹学-前置-概率与期望]]：期望、条件期望、常用分布。
- [[运筹学-前置-OR-Tools环境与建模]]：安装、GLOP、状态码。

## 任务边界

输入为题目给定数据；Part A/B 必须手算并写出完整步骤，禁止用求解器代替；Part C 运行输出必须完整保留。

## 题目

### Part A 线性代数（手算）

1. 用高斯消元解 $\begin{cases}2x_1+x_2=4\\x_1+2x_2=3\end{cases}$，写出每一步行变换并说明解的唯一性依据。
2. 判断矩阵 $A=\begin{pmatrix}1&2\\2&4\end{pmatrix}$ 的秩，并解释为什么 $A\mathbf{x}=\mathbf{b}$ 可能无解。
3. 说明"基可行解"中"基"的线性代数含义（$m$ 个线性无关列）。

### Part B 概率与期望（手算）

4. $P(D=0)=0.3,P(D=1)=0.5,P(D=2)=0.2$，求 $E[D]$、$E[D^2]$、$E[(D-1)^+]$。
5. 掷硬币选分布：正面取 $X\sim\text{Bernoulli}(0.8)$、反面取 $X\sim\text{Bernoulli}(0.2)$，用全期望公式求 $E[X]$。
6. 解释塔性质 $E[X]=E[E[X\mid Y]]$ 在"先定产量、后见需求"问题中的含义。

### Part C 环境（可运行）

7. 安装 `ortools`，运行以下模型并解读输出（目标值、解、状态码含义）：

```python
from ortools.linear_solver import pywraplp
s = pywraplp.Solver.CreateSolver("GLOP")
x = s.NumVar(0, s.infinity(), "x"); y = s.NumVar(0, s.infinity(), "y")
s.Add(2*x + y <= 4); s.Add(x + 2*y <= 3)
s.Maximize(x + y)
st = s.Solve()
print(st, x.solution_value(), y.solution_value())
```

8. 把目标改为 `Minimize(x - y)` 重新求解，解释最优解变化的原因（影子价格/可行域角度）。

## 环境与复现

- Python 3.10+，`pip install ortools numpy matplotlib pytest`。
- 提交时附 `pip freeze` 输出；运行示例需固定输出并截图/记录。

## 提交产物

- `precheck.py`（Part C 代码）+ 运行输出。
- 手算部分（Part A/B）以 Markdown/PDF 提交，步骤完整。

## 验收标准（Rubric）

| 维度 | 通过要求 |
|:---|:---|
| 正确性 | Part A/B 手算答案正确，消元步骤完整（每题 10 分，共 60） |
| 可运行 | Part C 输出 `OPTIMAL` 且解与手算极点一致（20 分） |
| 解释质量 | 第 6、8 题解释清晰、用词准确（20 分） |

≥80 分且 Part A/B/C 各至少 1 题通过 → 进入第一阶段。

## 引导与自检

- 卡住先回看三张前置卡的最小自测；Part C 若报错，检查安装与 Python 版本。
- 提交前检查：消元步骤无跳步、期望计算有过程、运行输出完整。

## 来源与后续

- 来源：本地原创（`local_integration_task`），模型来自 [[运筹学-前置-OR-Tools环境与建模]] 最小示例。
- 通过后进入 [[运筹学-课后作业-01-建模与单纯形法]]。
