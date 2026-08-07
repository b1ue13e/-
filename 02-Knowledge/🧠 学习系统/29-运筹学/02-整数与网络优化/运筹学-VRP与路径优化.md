---
type: study
topic: "VRP与路径优化"
course: "运筹学"
created: 2026-08-06
status: completed
stage_moc: "[[🧭 阶段2-整数与网络优化]]"
flow: knowledge
kind: concept
difficulty: advanced
concept: ["车辆路径问题", "TSP", "Routing求解器"]
upstream:
  - "[[运筹学-整数规划与分支定界]]"
  - "[[运筹学-约束规划与CP-SAT]]"
related: ["运筹学-网络流模型", "运筹学-元启发式方法"]
tags: [学习, 运筹学, VRP]
---

# 运筹学-VRP与路径优化

> 所属阶段：[[🧭 阶段2-整数与网络优化|🕸️ 第2阶段：整数与网络优化]]

## 这个知识点解决什么问题？

**我们遇到的麻烦**：物流公司每天要给几十上百个客户送货，车辆有容量、有时间窗——"先访问谁、每条路线怎么走"是指数级搜索空间（NP-hard）。TSP（单辆车）与 VRP（多辆车）是运筹学应用最广的问题族，也是 Google OR-Tools Routing 库的主要战场。本卡建立 TSP/VRP 建模要素，理解"精确方法做不到 → 启发式 + 局部搜索"的工程路线。

## 建模要素

### 1. TSP 与 VRP 的模型骨架

- **TSP**：$\min\sum_{(i,j)}c_{ij}x_{ij}$，约束：每点出度=入度=1（子回路消除约束 $\sum_{i\in S,j\notin S}x_{ij}\ge1$，或 subtour elimination）。
- **CVRP**（容量约束）：TSP + 车辆数 $K$ + 每车容量 $Q$ + 每客户需求 $q_i$（路线负载 $\le Q$）。
- **VRPTW**（时间窗）：CVRP + 每客户服务时间与服务窗 $[e_i,l_i]$（早到等待、晚到罚则）。

### 2. OR-Tools Routing 建模要素

| 元素 | 作用 |
|:---|:---|
| `RoutingIndexManager(n, K, depot)` | 节点索引、车辆数、车场 |
| `RegisterTransitCallback` | 距离/时间回调（distance matrix） |
| `AddDimensionWithVehicleCapacity` | 容量维度（负载约束） |
| `AddDimension` + `SetRange` | 时间维度（时间窗） |
| `first_solution_strategy = PATH_CHEAPEST_ARC` | 初始解 |
| `local_search_metaheuristic = GUIDED_LOCAL_SEARCH` | 改进搜索 |

### 3. 求解路线图

1. **小规模（≤10-15 节点）**：用 CP-SAT/MIP 精确解做 ground truth（`AddCircuit` 圈约束）。
2. **中大规模**：Routing 求解器（CP + 局部搜索，见 [[运筹学-元启发式方法]]），报告 gap 与求解时间。
3. **极大规模**：元启发式（模拟退火/禁忌搜索）自定义。

## 一个最小例子（手算）

4 节点（1 车场 + 3 客户），距离矩阵对称 $d=\begin{pmatrix}0&10&15&20\\10&0&35&25\\15&35&0&30\\20&25&30&0\end{pmatrix}$，车辆容量 10，需求 $q=(0,4,3,3)$。

- 暴力枚举路线（车场 0 出发回 0）：$0\to1\to2\to3\to0$：$10+35+30+20=95$；$0\to1\to3\to2\to0$：$10+25+30+15=80$；$0\to2\to1\to3\to0$：$15+35+25+20=95$。
- 最优 $0\to1\to3\to2\to0$，总距离 80，负载 $4+3+3=10=Q$ ✓（恰好满载）。
- OR-Tools Routing 同参数应得 80；小规模可手算对照。

## 用 OR-Tools Routing 求解（与手算对照）

```python
from ortools.constraint_solver import routing_enums_pb2, pywrapcp

dist = [[0,10,15,20],[10,0,35,25],[15,35,0,30],[20,25,30,0]]
demands = [0, 4, 3, 3]                      # 车场需求为 0
n, K, cap = 4, 1, 10

mgr = pywrapcp.RoutingIndexManager(n, K, 0)
routing = pywrapcp.RoutingModel(mgr)
def cost(from_idx, to_idx):
    return dist[mgr.IndexToNode(from_idx)][mgr.IndexToNode(to_idx)]
routing.SetArcCostEvaluatorOfAllVehicles(routing.RegisterTransitCallback(cost))
def demand(from_idx, to_idx):
    return demands[mgr.IndexToNode(from_idx)]
routing.AddDimensionWithVehicleCapacity(routing.RegisterTransitCallback(demand),
                                        0, [cap]*K, True, "Cap")   # 容量维度
params = pywrapcp.DefaultRoutingSearchParameters()
params.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
sol = routing.SolveWithParameters(params)
print("总距离 =", sol.ObjectiveValue())      # 80
idx = routing.Start(0); route = []
while not routing.IsEnd(idx):
    route.append(mgr.IndexToNode(idx)); idx = sol.Value(routing.NextVar(idx))
route.append(0); print("路线 =", route)      # [0, 1, 3, 2, 0]
```

输出：`总距离 = 80`、`路线 = [0, 1, 3, 2, 0]` —— 与手算最优完全一致。把 `K` 改为 2、`demands` 加大，即可观察容量约束如何把路线拆成多条——这就是 CVRP 与 TSP 的分水岭。

## 路径优化问题族对比

| 问题 | 车辆 | 容量/时间窗 | 精确解 | 工程解 |
|:---|:---|:---|:---|:---|
| TSP | 1 | 无 | DFJ/Miller-Tucker-Zemlin MIP | 启发式 + 2-opt |
| CVRP | K | 容量 $Q$ | 大 MIP（小规模） | Routing + 容量维度 |
| VRPTW | K | 容量 + 时间窗 | 几乎不可能 | Routing + 时间维度 |
| 配送网络流（[[运筹学-网络流模型]]） | — | 边容量 | 多项式算法 | MaxFlow/MinCostFlow |

**关系**：TSP 是 VRP 的单车特例，CVRP 加容量，VRPTW 再加工时窗；网络流是连续/多项式对照——问题每加一个约束，就从"精确可解"滑向"必须启发式"。

## 常见误区

- **误区 1**：VRP 当 TSP 解。多辆车、容量、时间窗是 VRP 的**核心约束**，漏掉容量约束就退化成 m-TSP，解不可用。
- **误区 2**：距离矩阵用浮点欧氏距离直接跑。Routing 通常要求整数距离（取整），否则求解器内部索引不一致。
- **误区 3**：以为 Routing 保证最优。它是**元启发式**（局部搜索），只给高质量近似解；要证明最优必须 CP-SAT/MIP 小规模对照。
- **误区 4**：忘掉需求回调查询的是"出发节点"。容量回调里 `demands[IndexToNode(from)]` 取的是**到达该节点前的负载增量**，车场节点需求必须为 0。

## 最小自测

- [#自测题/基础] 写出 TSP 的 subtour elimination 约束并解释为什么需要它。
- [#自测题/基础] 说出 CVRP 相对 TSP 新增的三个建模要素。
- [#自测题/中等] 解释为什么 VRP 在大规模下用"初始解 + 局部搜索"而非精确求解。
- [#自测题/中等] 运行上面的代码：把 `K` 改为 2 且 `cap=6`，观察路线如何拆分、总距离如何变化，并解释原因。
- [#自测题/较难] 给客户 3 加时间窗 $[0,5]$（服务时间 2），用 `AddDimension` 重解并解释早到等待/迟到罚则如何改变路线。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
