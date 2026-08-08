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
  - "[[运筹学-前置-线性代数最小集]]"
tags: [学习, 运筹学, 前置知识]
source: "Google OR-Tools 官方教程与文档"
source_url: "https://developers.google.com/optimization"
accessed: 2026-08-08
license: "Apache-2.0（OR-Tools）；教程文档可阅读运行"
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

## 从 LP 到 MIP：整数变量的最小示例

连续变量的 LP 用 `NumVar`，**整数变量必须用 `IntVar`**。下面是一个 0-1 背包小实例（容量 10，物品 (重量,价值) = (6,8),(5,7),(4,6),(3,4)），用 SCIP 求解：

```python
from ortools.linear_solver import pywraplp
solver = pywraplp.Solver.CreateSolver("SCIP")
w = [6, 5, 4, 3]; v = [8, 7, 6, 4]
x = [solver.IntVar(0, 1, f"x{i}") for i in range(4)]   # 0-1 变量：选或不选
solver.Add(sum(w[i]*x[i] for i in range(4)) <= 10)     # 容量约束
solver.Maximize(sum(v[i]*x[i] for i in range(4)))
st = solver.Solve()
print(st, solver.Objective().Value())                  # 0 14.0
print([i for i in range(4) if x[i].solution_value() > 0.5])  # [0, 2]
```

输出：`0 14.0`、`[0, 2]` —— 选物品 0 和 2（重 6+4=10，价值 8+6=14），与手算密度贪心修正结果一致。**对比**：若把 `IntVar` 换成 `NumVar`，松弛解会允许"装 1/6 个物品 0"（价值 14.33），这就是整数约束的价值——见 [[运筹学-整数规划建模]]。

## 状态码解读

| 状态 | 含义 | 处理 |
|:---|:---|:---|
| `OPTIMAL` | 找到最优解 | 读取 `solution_value()` |
| `FEASIBLE` | 有可行解但不保证最优 | MIP 常用，配合 gap |
| `INFEASIBLE` | 无可行解 | 检查约束冲突 |
| `UNBOUNDED` | 目标无界 | 检查漏掉约束 |

## 求解器对比（GLOP vs SCIP vs CP-SAT）

| 求解器 | 问题类型 | 变量类型 | 典型场景 | 何时选它 |
|:---|:---|:---|:---|:---|
| GLOP | 线性规划（LP） | 连续 `NumVar` | 资源分配、运输、网络流松弛 | 手算对照、需要影子价格 |
| SCIP | 混合整数线性规划（MIP） | 整数/0-1 `IntVar` | 背包、选址、指派、B&B 验证 | 整数/逻辑约束的精确解 |
| CP-SAT | 约束规划（CP） | 整数 + 全局约束（`AddAllDifferent` 等） | 排班、车间调度、VRP 变体 | 组合/逻辑约束强、MIP 松弛差的问题 |

选型口诀：**连续 → GLOP；整数 + 线性 → SCIP；整数 + 组合约束 → CP-SAT**。同一个小问题三者往往都能解，但规模变大后"该用哪个"决定生死（见 [[运筹学-约束规划与CP-SAT]] 的对比实验）。

## 常见误区

- **误区 1**：MIP 结果直接当最优。MIP 默认给 `FEASIBLE` + 相对 gap，须设 `solver.SetTimeLimit()` 与 gap 阈值判断是否可接受。
- **误区 2**：`NumVar`/`IntVar` 混用导致无解。整数变量必须用 `IntVar`，否则结果不可取整。
- **误区 3**：官方示例直接复制当作业。Honor Code：先自己建模，跑通后再对照官方示例复盘（见课程作业索引）。
- **误区 4**：所有问题都先试 GLOP。GLOP 解不了整数约束（会报无解或给分数解），整数问题直接上 SCIP/CP-SAT。

## 与本课程的连接

- [[运筹学-线性规划与单纯形法]]：GLOP 内部就是单纯形法；理论卡讲手算，这里讲调用。
- [[运筹学-整数规划建模]]、[[运筹学-约束规划与CP-SAT]]、[[运筹学-VRP与路径优化]]：全部用本卡环境。
- 每份作业的 `requires` 都依赖本卡。

## 最小自测

- [#自测题/基础] 安装 ortools 并运行上方最小 LP 示例，输出 `OPTIMAL` 与解 $(5/3,2/3)$。
- [#自测题/基础] 说出 GLOP、SCIP、CP-SAT 各适合什么问题类型，并各举一个本课程场景。
- [#自测题/中等] 把最小 LP 示例改为 `Minimize(x-y)`，预测最优解并运行验证，解释结果变化。
- [#自测题/中等] 把背包示例的 `IntVar` 换成 `NumVar`，运行并解释为什么最优值从 14 变成 14.33。
- [#自测题/较难] 给背包加一个约束"物品 0 与物品 1 至多选一个"（`x[0]+x[1]<=1`），运行验证最优解如何变化并解释。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
