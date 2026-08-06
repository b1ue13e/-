---
type: project
project_type: homework
course: "运筹学"
assignment_id: "运筹学-C01"
assignment_level: capstone
assignment_format: project
stage_id: "02"
requires:
  - "[[运筹学-线性规划与单纯形法]]"
  - "[[运筹学-整数规划与分支定界]]"
  - "[[运筹学-约束规划与CP-SAT]]"
  - "[[运筹学-VRP与路径优化]]"
  - "[[运筹学-网络流模型]]"
  - "[[运筹学-元启发式方法]]"
  - "[[运筹学-前置-OR-Tools环境与建模]]"
source_type: open_source_project_task
adapted_from: "历史 HW05（VRP 阶梯作业，2026-08-03）"
source_url: "https://developers.google.com/optimization/routing"
created: 2026-08-06
status: planned
flow: project
tags: [作业, 运筹学, 大作业, VRP]
---

# 运筹学-大作业-01-VRP车辆路径问题

> 所属阶段：[[🧭 阶段2-整数与网络优化|阶段 2]]（跨阶段综合） ｜ 形态：项目（project）

## 学习目标

以 Google OR-Tools Routing 官方教程（https://developers.google.com/optimization/routing ）为验收源，端到端完成车辆路径问题（VRP）项目：掌握 Routing 建模（distance matrix、demand、capacity、time windows、`RoutingIndexManager`），理解"初始解 + guided local search"机制，在小规模 CVRP 上与暴力枚举/CP-SAT 对照验证最优性，完成 VRPTW 扩展与规模-求解时间-最优性差距分析。

## 所需知识

- [[运筹学-VRP与路径优化]]：建模要素与求解路线图。
- [[运筹学-约束规划与CP-SAT]]：小规模精确对照（`AddCircuit`）。
- [[运筹学-元启发式方法]]：guided local search 的机制理解。
- [[运筹学-网络流模型]]：PDP 扩展的建模直觉。

## 任务背景与边界

- 验收源：OR-Tools Routing 官方教程与示例（Apache-2.0，可阅读、可运行、可对照）。
- **Honor Code**：本作业的**建模与求解代码必须自己完成**，跑通后再对照官方示例复盘；禁止直接复制示例代码充当作业。
- 数据：`make_instance(n_customers, seed)` 在 100×100 方形区域按固定种子撒点生成客户坐标，仓库固定节点 0；欧氏距离（四舍五入取整）构造 `distance_matrix`；`demand ∈ [1,20]`，容量 = 「总需求 ÷ 车辆数 × 1.5」上取整；VRPTW 额外生成服务时间与时间窗（仓库时间窗覆盖全天）。

## 题目（基础 → 进阶 → 综合）

### 基础（必做）· CVRP 小规模精确对照

1. 实现 `make_instance(n_customers, seed)` 与 `build_solution(data)`（用 OR-Tools Routing：`RoutingIndexManager`、`RegisterTransitCallback` 距离回调、`AddDimensionWithVehicleCapacity` 容量约束）。
2. 实现 `brute_force_cvrp(data)` 暴力枚举（≤10 客户：枚举客户到车辆的分配与每车路线排列，过滤超载取最小总距离）。
3. 对 seed ∈ {0,1,2} 的 6-客户实例：断言 OR-Tools 解总距离 == 暴力最优解。

### 进阶（必做）· 规模与可视化

4. 50 客户 CVRP：`PATH_CHEAPEST_ARC` 初始解 + `GUIDED_LOCAL_SEARCH` 求解；matplotlib 画路线图（不同车辆不同颜色、仓库方形标记）；报告总距离、车辆数、平均装载率。

### 综合（必做）· 时间窗与差距分析

5. VRPTW：`routing.AddDimension(time_callback, slack_max, horizon, False, "Time")` + `SetRange` 约束；读取到达时刻，报告总等待时间与准时到达占比；收紧时间窗（60→30）分析对总距离的影响。
6. 规模扫描 10→100 客户（time_limit 固定）：报告求解时间曲线与最优性差距——小规模对暴力/精确解（第 3 题），大规模报告多次随机种子下的解方差。
7. 用 CP-SAT（`AddCircuit` + 容量/时间窗）对同一小规模实例（≤10 客户）精确建模求解，与 Routing 结果对比求解时间与最优性差距，说明 Routing 与 CP-SAT 的适用边界。

### 扩展（可选进阶，不阻塞主任务）

8. 多车场 MDVRP 或带取送货 PDP（每单 pickup/delivery 配对、先取后送），复用作第 6 题的规模扫描。

## Starter Code（最小骨架）

```python
# vrp_starter.py —— 完成以下签名（自行补充实现）
import numpy as np

def make_instance(n_customers, seed):
    """返回 data: {"distance_matrix", "demands", "capacities",
                  "num_vehicles", "depot", "time_windows"(可选),
                  "service_times"(可选)}"""
    rng = np.random.default_rng(seed)
    coords = rng.uniform(0, 100, size=(n_customers + 1, 2))
    dm = np.round(np.linalg.norm(coords[:, None] - coords[None, :], axis=-1)).astype(int)
    demands = rng.integers(1, 21, size=n_customers + 1); demands[0] = 0
    num_vehicles = 4
    cap = int(np.ceil(demands.sum() / num_vehicles * 1.5))
    return {"distance_matrix": dm.tolist(), "demands": demands.tolist(),
            "capacities": [cap] * num_vehicles, "num_vehicles": num_vehicles,
            "depot": 0}

def build_solution(data):
    """返回 (routes, total_distance, loads)；routes 每车从 depot 出发回 depot。"""
    raise NotImplementedError

def brute_force_cvrp(data):
    """≤10 客户暴力枚举，返回最优总距离。"""
    raise NotImplementedError
```

## 自动化测试（PyTest 验收）

```python
import pytest, numpy as np
from vrp_starter import make_instance, build_solution, brute_force_cvrp

def test_capacity_not_violated():
    data = make_instance(n_customers=8, seed=42)
    routes, _, loads = build_solution(data)
    for route, load in zip(routes, loads):
        assert load <= data["capacities"][0]

def test_all_customers_served():
    data = make_instance(n_customers=8, seed=42)
    routes, _, _ = build_solution(data)
    served = [n for r in routes for n in r if n != data["depot"]]
    assert sorted(served) == list(range(1, 9))

def test_routes_connected():
    data = make_instance(n_customers=8, seed=42)
    routes, total_distance, _ = build_solution(data)
    dm = data["distance_matrix"]
    expected = sum(dm[([data["depot"]] + r + [data["depot"]])[i]]
                     [([data["depot"]] + r + [data["depot"]])[i + 1]]
                   for r in routes for i in range(len(r) + 1))
    np.testing.assert_allclose(total_distance, expected, atol=1e-6)

def test_vs_bruteforce_optimal():
    for seed in [0, 1, 2]:
        data = make_instance(n_customers=6, seed=seed)
        _, total_distance, _ = build_solution(data)
        np.testing.assert_allclose(total_distance, brute_force_cvrp(data), atol=1e-6)
```

## 环境与复现

- `pip install ortools numpy matplotlib pytest`；固定随机种子；`time_limit` 统一（如每实例 60s）；提交 `pip freeze`。

## 提交产物

- `vrp_solver.py`（完整实现）、`test_vrp.py`（测试）、`report.md`（1-2 页：问题、模型、求解、对比、差距分析）、路线图与规模扫描图、运行日志。

## 验收标准（Rubric，100 分）

| 维度 | 分值 | 通过要求 |
|:---|:---:|:---|
| 正确性 | 25 | 4 个测试全过；小规模与暴力/CP-SAT 一致 |
| 完整度 | 25 | 基础+进阶+综合 7 题全部完成 |
| 分析与差距 | 20 | 时间窗影响、规模曲线、最优性差距有数据 |
| 可复现性 | 15 | 固定 seed、time_limit、依赖清单完整 |
| 报告质量 | 15 | 结论可复核、不夸大适用范围 |

≥75 分且正确性 ≥18 → 通过；通过后可进入课程 Capstone 验收轮。

## 引导与自检

- 常见失败：距离矩阵未取整导致索引不一致；漏 `AddDimension` 退化为 m-TSP；VRPTW 忘约束仓库时间窗。
- 提交前检查：测试全绿、图上有图例、差距分析有数字、报告标注"Routing 为启发式近似解"。

## 来源与后续

- 来源：OR-Tools Routing 官方教程（Apache-2.0，`open_source_project_task`）；改编自历史 HW05（任务语义保留，分层改名基础/进阶/综合）。
- 完成本作业后，可与 [[运筹学-大作业-02-排程与资源分配求解器]] 一起构成课程 Capstone 组合；复盘入口见 [[🧭 课程作业总索引]]。
