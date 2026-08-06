---
title: "运筹学-题型-VRP车辆路径阶梯作业"
type: problem-type
kind: problem-type
flow: knowledge
topic: "运筹学作业"
course: "29-运筹学"
created: 2026-08-03
updated: 2026-08-03
date: 2026-08-03
status: learning
difficulty: advanced
importance: A
concept: ["车辆路径问题", "约束规划", "组合优化"]
prerequisites: ["[[约束规划与CP-SAT]]"]
related: ["[[整数规划与分支定界]]", "[[线性规划与单纯形法]]", "[[🧭 开源作业体系-运筹学]]"]
upstream: ["[[🗺️ 运筹学学习路径|运筹学学习路径]]"]
downstream: []
tags: [学习, 29-运筹学, 作业, 实战, 阶梯作业]
aliases: ["OR-HW05-VRP车辆路径作业"]
---

# 运筹学 - HW05：VRP 车辆路径问题阶梯作业

> 🎯 **作业目标**：以 Google OR-Tools Routing 官方教程（https://developers.google.com/optimization/routing ）为验收源，完成车辆路径问题 (Vehicle Routing Problem, VRP) 的阶梯式实战：掌握 Routing Model 建模（distance matrix、demand、capacity、time windows、RoutingIndexManager），理解 path-cheapest-arc 初始解 + guided local search 的求解机制，在小规模 CVRP 上与暴力枚举对照验证最优性，并最终完成 VRPTW 与多车场/取送货扩展及规模-求解时间-最优性差距分析。

---

## 1. ⚙️ 环境与 Starter Code 准备
- **Starter Code 路径**：`03-Projects/projects-opt/hw05_vrp.ipynb`
- **官方教程（验收源）**：[OR-Tools Routing 教程](https://developers.google.com/optimization/routing)（Routing 简介：https://developers.google.com/optimization/routing/routing_options ）
- **核心依赖**：`ortools`, `numpy`, `matplotlib`, `pytest`
- **安装命令**：`pip install ortools numpy matplotlib pytest`
- **官方示例**：
  - CVRP 容量约束车辆路径：https://developers.google.com/optimization/routing/cvrp
  - VRPTW 带时间窗车辆路径：https://developers.google.com/optimization/routing/vrptw
  - 取送货 VRP (PDP)：https://developers.google.com/optimization/routing/pickup_delivery （L4 扩展参考）
- **数据生成脚本建议**（`make_instance(n_customers, seed)`）：在方形区域（如 100×100）内按随机种子撒点生成客户坐标，仓库（depot）固定为节点 0；用欧氏距离（四舍五入取整）构造 `distance_matrix`；随机生成需求量 `demand ∈ [1, 20]`，车辆容量取「总需求 ÷ 车辆数 × 1.5」上取整；VRPTW 额外生成每客户的服务时间与时间窗 `[ready, due]`（仓库时间窗覆盖全天）。固定 seed 保证可复现，便于对照与测试。
- **Honor Code**（见 [[🧭 开源作业体系-运筹学]]）：官方教程与示例可阅读、可运行、可对照；本 HW 的**建模与求解代码必须自己完成**，跑通后再对照官方示例复盘，禁止直接复制示例代码充当作业。

---

## 2. 🎯 阶梯式 Baseline / 难度设计 (4-Tier Difficulty)

| 梯度级别 | 目标 / 验证标准 | 关键实现细节与要求 |
| :--- | :--- | :--- |
| 🟢 **L1 - Simple Baseline** | 与暴力枚举最优解一致（≤10 节点） | 在 5-10 客户小规模 CVRP 上用 OR-Tools Routing 建模求解：构建 `RoutingIndexManager`、`RegisterTransitCallback` 距离回调、`AddDimensionWithVehicleCapacity` 容量约束；对同一实例手写**暴力枚举**（枚举客户到车辆的分配与每辆车的路线排列，过滤超载方案取最小总距离），断言 OR-Tools 解总距离 == 暴力最优解。 |
| 🟡 **L2 - Medium Baseline** | 50 节点 CVRP 求解成功 + 可视化与指标报告 | 50 客户 CVRP：配置多辆车（容量如 100），`first_solution_strategy = PATH_CHEAPEST_ARC` + `local_search_metaheuristic = GUIDED_LOCAL_SEARCH` 求解；用 matplotlib **画路线图**（不同车辆不同颜色、仓库为方形标记）；报告**总行驶距离**、车辆数与**平均装载率**（总需求 ÷ (车辆数 × 容量)）。 |
| 🔴 **L3 - Strong Baseline** | VRPTW 求解成功 + 等待时间报告 | 在 L2 实例上加入时间窗：每客户 `[ready, due]` 与服务时间，用 `routing.AddDimension(time_callback, slack_max, horizon, False, "Time")` 建模时间维度并 `SetRange` 约束累计时间；求解后通过 `TimeDimension().CumulVar()` 读取到达时刻，报告**总等待时间**（早到必须等待）与准时到达客户占比；收紧时间窗宽度（如 60→30）分析对总距离的影响。 |
| 👑 **L4 - Boss Baseline** | 规模-求解时间-最优性差距分析 | 扩展为**多车场 MDVRP**（多个 depot，各车从所属车场出发并返回）或**带取送货 PDP**（每单有 pickup 与 delivery 节点，配对且先取后送）；做 10→100 客户规模扫描，报告**求解时间曲线**（time_limit 固定）与**最优性差距**：小规模对暴力/精确解（见 L1），大规模报告多次随机种子下的解方差与 CP-SAT 上界对照。 |

> 💡 **与 CP-SAT 对照**：VRP 是 NP-hard 组合优化问题，同一个小规模实例（≤10 客户）可用 [[约束规划与CP-SAT]] 的 CP-SAT 精确建模（`AddCircuit` 圈约束 + 容量/时间窗约束）求解作为 ground truth；Routing 求解器走「启发式初始解 + guided local search」路线，面向大规模求高质量近似解。完成 L1 后建议用同一实例分别跑 CP-SAT 与 Routing，对比求解时间与最优性差距，明确两种求解器的适用边界（呼应 HW04-HW05 的求解器链手感）。

---

## 3. 🧪 自动化测试 Harness (PyTest Validation)

```python
import pytest
import numpy as np

# 学生实现（Starter Code 中给出签名与骨架）：
# make_instance(n_customers, seed) -> data
#   data: {"distance_matrix", "demands", "capacities", "num_vehicles",
#          "depot", "time_windows"(可选), "service_times"(可选)}
# build_solution(data) -> (routes, total_distance, loads)
#   routes: list[list[int]]，每辆车从 depot=0 出发、访问客户编号后回到 0
#   loads:  list[int]，每辆车的实际装载量（按路线顺序累加 demand）
# brute_force_cvrp(data) -> total_distance  # L1 专用暴力枚举（≤10 客户）

def test_capacity_not_violated():
    data = make_instance(n_customers=8, seed=42)
    routes, _, loads = build_solution(data)
    for route, load in zip(routes, loads):
        assert load <= data["capacities"][0], \
            f"路线 {route} 装载量 {load} 超过容量 {data['capacities'][0]}"

def test_all_customers_served():
    data = make_instance(n_customers=8, seed=42)
    routes, _, _ = build_solution(data)
    served = [n for route in routes for n in route if n != data["depot"]]
    assert sorted(served) == list(range(1, data["num_customers"] + 1)), \
        "所有客户必须且只能被服务一次（depot 除外）"

def test_routes_connected():
    data = make_instance(n_customers=8, seed=42)
    routes, total_distance, _ = build_solution(data)
    dm = data["distance_matrix"]
    expected = 0.0
    for route in routes:
        seq = [data["depot"]] + route + [data["depot"]]
        for i in range(len(seq) - 1):
            assert np.isfinite(dm[seq[i]][seq[i + 1]]), \
                f"路线 {route} 存在未定义弧段 {seq[i]} -> {seq[i+1]}"
            expected += dm[seq[i]][seq[i + 1]]
    np.testing.assert_allclose(total_distance, expected, atol=1e-6,
                               err_msg="报告的总距离必须等于路线弧段距离之和")

def test_vs_bruteforce_optimal():
    # L1 小规模（≤10 客户）：OR-Tools 解必须等于暴力枚举最优解
    for seed in [0, 1, 2]:
        data = make_instance(n_customers=6, seed=seed)
        routes, total_distance, _ = build_solution(data)
        opt = brute_force_cvrp(data)
        np.testing.assert_allclose(total_distance, opt, atol=1e-6,
                                   err_msg=f"seed={seed}: OR-Tools 解 {total_distance} "
                                           f"不等于暴力最优 {opt}")
```

---

## 🃏 Anki 卡片

- Q: OR-Tools Routing 中 `RoutingIndexManager` 的作用是什么？为什么必须用它？
- A: 它在求解器内部索引（index）与业务节点编号（node）之间建立双向映射（`NodeToIndex` / `IndexToNode`）。Routing 求解器内部使用自己的索引体系（含 start/end 哨兵节点），距离/需求/时间回调都基于 index 对，因此必须经 manager 转换，避免节点编号与索引错位。
- Q: CVRP 的容量约束在 OR-Tools Routing 中如何建模？其保证的数学性质是什么？
- A: 用 `routing.AddDimensionWithVehicleCapacity(demand_callback, 0, capacities, True, "Capacity")` 添加「容量维度」：沿每条路线将需求量单调累加进累加器，车辆从仓库出发时累加器为 0，任何时刻不得超过该车容量。等价于保证每条可行路线满足 $\sum_{i \in \text{route}} d_i \le Q_k$，从而过滤所有超载方案。
- Q: OR-Tools Routing 求解器默认的求解机制是什么（初始解 + 元启发式）？
- A: 分两阶段：先用 `first_solution_strategy`（默认 `PATH_CHEAPEST_ARC`，逐条弧贪心扩展）构造初始解；再用 `local_search_metaheuristic`（默认 `GUIDED_LOCAL_SEARCH`，引导式局部搜索，对未改进的邻域移动惩罚惩罚因子以逃离局部最优）迭代改进，直到 `time_limit` 或稳定条件触发。
- Q: 为什么 VRP 小规模（≤10 客户）可以与暴力枚举/CP-SAT 对照验证最优性，而大规模（50+ 客户）只能接受近似解？
- A: VRP 是 TSP 的推广，属 NP-hard：n 个客户的分配与排序方案数为阶乘级，精确枚举随 n 爆炸。≤10 客户时枚举可行，可作 ground truth 验证启发式最优性；50+ 客户时精确求解不可行，只能靠 guided local search 求高质量近似解，并以「最优性差距」（小规模对精确解、大规模对多次运行方差/上界）衡量解质量。
- Q: VRPTW 中「等待时间」是什么？在 Routing 中如何读取与约束时间窗？
- A: 时间维度 `routing.AddDimension(time_callback, slack_max, horizon, False, "Time")` 累加行驶与服务时间；每节点用 `time_dimension.CumulVar(i).SetRange(ready_i, due_i)` 约束到达时刻必须落在 `[ready, due]` 内。车辆早于 `ready_i` 到达必须等待，等待时间 = max(0, ready_i − 到达时刻)。求解后经 `solution.Value(time_dimension.CumulVar(i))` 读取到达时刻，累加得到总等待时间，用于评估解质量。
