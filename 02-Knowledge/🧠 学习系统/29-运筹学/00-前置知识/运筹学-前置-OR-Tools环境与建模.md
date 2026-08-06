---
type: study
topic: "OR-Tools环境与建模"
course: "运筹学"
created: 2026-08-06
status: completed
stage_moc: "[[🧭 29-运筹学-前置知识]]"
flow: knowledge
kind: concept
difficulty: beginner
concept: ["OR-Tools", "求解器", "建模"]
upstream:
  - "[[02-Knowledge/🧠 学习系统/07-最优化方法/02-凸分析与最优性条件/最优化方法-凸集与凸函数]]"
tags: [学习, 运筹学, 前置知识]
---

# 运筹学-前置-OR-Tools环境与建模

> 所属阶段：[[🧭 29-运筹学-前置知识|前置知识]]

## 这个知识点解决什么问题？

理论卡讲"算法怎么算"，作业要"真算出来"。**我们遇到的麻烦**：手写单纯形法只适合小例子，真实规模问题需要工业级求解器。Google OR-Tools（Apache-2.0）是本课程统一的建模与求解环境，覆盖 LP/MIP/CP-SAT/Routing/Scheduling/网络流。本卡建立最小环境与建模手感。

## 环境与安装

```bash
python -m pip install --upgrade ortools numpy matplotlib pytest
```

- 官方文档：https://developers.google.com/optimization （教程、API 参考）
- 源码：https://github.com/google/or-tools （Apache-2.0）
- 求解器家族与本课程的对应：

| OR-Tools 模块 | 求解器 | 对应运筹学主题 |
|:---|:---|:---|
| `pywraplp` | GLOP（LP）、SCIP（MIP 封装） | 线性规划、整数规划 |
| `cp_model` | CP-SAT | 约束规划、排班调度 |
| `routing` | Routing 求解器 | VRP、TSP |
| `graph` | MaxFlow、MinCostFlow | 网络流 |

## 最小建模流程（LP）

```python
from ortools.linear_solver import pywraplp
solver = pywraplp.Solver.CreateSolver("GLOP")
x = solver.NumVar(0, solver.infinity(), "x")
y = solver.NumVar(0, solver.infinity(), "y")
solver.Add(2*x + y <= 4)
solver.Add(x + 2*y <= 3)
solver.Maximize(x + y)
status = solver.Solve()          # 0 = OPTIMAL
print(status, x.solution_value(), y.solution_value())
```

输出：`0 1.666... 0.666...` —— 与手算高斯消元得到的极点 $(5/3,2/3)$ 一致（见 [[运筹学-前置-线性代数最小集]]）。

## 状态码解读

| 状态 | 含义 | 处理 |
|:---|:---|:---|
| `OPTIMAL` | 找到最优解 | 读取 `solution_value()` |
| `FEASIBLE` | 有可行解但不保证最优 | MIP 常用，配合 gap |
| `INFEASIBLE` | 无可行解 | 检查约束冲突 |
| `UNBOUNDED` | 目标无界 | 检查漏掉约束 |

## 常见误区

- **误区 1**：MIP 结果直接当最优。MIP 默认给 `FEASIBLE` + 相对 gap，须设 `solver.SetTimeLimit()` 与 gap 阈值判断是否可接受。
- **误区 2**：`NumVar`/`IntVar` 混用导致无解。整数变量必须用 `IntVar`，否则结果不可取整。
- **误区 3**：官方示例直接复制当作业。Honor Code：先自己建模，跑通后再对照官方示例复盘（见课程作业索引）。

## 与本课程的连接

- [[运筹学-线性规划与单纯形法]]：GLOP 内部就是单纯形法；理论卡讲手算，这里讲调用。
- [[运筹学-整数规划建模]]、[[运筹学-约束规划与CP-SAT]]、[[运筹学-VRP与路径优化]]：全部用本卡环境。
- 每份作业的 `requires` 都依赖本卡。

## 最小自测

- [ ] 安装 ortools 并运行上方最小示例，输出 `OPTIMAL`。
- [ ] 把最小示例改为 `Minimize(x-y)`，观察并解释结果变化。
- [ ] 说出 CP-SAT 与 GLOP 各适合什么问题类型。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
