---
title: "强化学习-题型-CS188-P1-Pacman搜索阶梯作业"
type: problem-type
kind: problem-type
flow: knowledge
topic: "强化学习作业"
course: "13-强化学习"
created: 2026-08-03
updated: 2026-08-03
date: 2026-08-03
status: learning
difficulty: advanced
importance: A
concept: ["搜索算法", "DFS", "BFS", "UCS", "A*算法", "启发函数"]
prerequisites: ["[[02-Knowledge/🧠 学习系统/13-强化学习/MDP与贝尔曼方程|MDP与贝尔曼方程]]", "[[02-Knowledge/🧠 学习系统/13-强化学习/探索与利用|探索与利用]]"]
related: ["[[强化学习 - CS188-P2：多智能体搜索阶梯作业]]", "[[强化学习 - CS188-P3：Pacman 强化学习阶梯作业]]"]
upstream: ["[[02-Knowledge/🧠 学习系统/13-强化学习/🧭 开源作业体系-强化学习|开源作业体系-强化学习]]"]
downstream: []
tags: [学习, 13-强化学习, 作业, 实战, 阶梯作业]
aliases: ["CS188-P1-Search", "Pacman搜索作业"]
---

# 强化学习 - CS188-P1：Pacman 搜索阶梯作业

> 🎯 **作业目标**：在 Pacman 世界中手写经典搜索算法（DFS / BFS / UCS / A*），构造 CornersProblem 与 FoodSearchProblem 的启发函数，通过 CS188 官方 autograder 验收，并对比最优搜索与次优搜索（suboptimal search）在真实迷宫上的得分差距。

---

## 1. ⚙️ 环境与 Starter Code（CS188 官方 Pacman 项目）

- **官方来源**：Berkeley CS188 Intro to AI Project 1 Search（http://ai.berkeley.edu/project_overview.html）
- **关键文件**：`search.py`（实现 DFS/BFS/UCS/A*）、`searchAgents.py`（CornersProblem、FoodSearchProblem 与启发函数）、`pacman.py`（主入口）、`game.py`、`util.py`（Stack / Queue / PriorityQueue 已备好）
- **核心依赖**：Python 3 + 官方 pacman 项目包（无第三方深度学习依赖，纯搜索算法）
- **运行方式**：

```bash
python pacman.py -l tinyMaze -p SearchAgent -a fn=tinyMazeSearch   # 冒烟测试：验证环境可跑
python pacman.py -l mediumMaze -p SearchAgent -a fn=bfs            # 可视化查看 BFS 轨迹
python pacman.py -l mediumDottedMaze -p StayEastSearchAgent        # 次优搜索示例
python autograder.py -q q1 -q q2                                   # 官方自动评测（按题打分）
```

- **验收口径**：官方 autograder 按 question（q1 DFS → q8 suboptimal）逐题打分，每题包含轨迹合法性、路径代价最优性与扩展节点数检查；只允许补全 `search.py` / `searchAgents.py` 中的实现，不得修改评测逻辑。Honor Code：官方 solutions 只用于完成后自查。

---

## 2. 🎯 阶梯式 Baseline / 难度设计 (4-Tier Difficulty)

| 梯度级别 | 评测环境 / 验收 | 关键实现细节与要求 |
| :--- | :--- | :--- |
| 🟢 **L1 - Simple Baseline** | tinyMaze / mediumMaze，autograder q1-q3 | 在 `search.py` 中实现 `depthFirstSearch`（Stack）、`breadthFirstSearch`（Queue）、`uniformCostSearch`（PriorityQueue + 累积代价 g）；轨迹为合法移动序列，BFS/UCS 结果须最优。 |
| 🟡 **L2 - Medium Baseline** | mediumMaze / bigMaze，autograder q4 | 实现 `aStarSearch` 与 `heuristic`（曼哈顿距离）；A* 在 mediumMaze 上通过且扩展节点数明显少于 UCS，启发函数必须 admissible。 |
| 🔴 **L3 - Strong Baseline** | CornersProblem，autograder q5-q6 | 定义 `CornersProblem`（状态 = 位置 + 已吃角落集合），实现 `cornersHeuristic`（吃掉所有角落的 admissible 下界），在 mediumCorners 上扩展节点数达标。 |
| 👑 **L4 - Boss Baseline** | FoodSearchProblem，autograder q7-q8 | 实现 `foodHeuristic`（admissible 且尽量紧，bigSearch 上扩展节点数越少越好）；实现 `StayEastSearchAgent` / `StayWestSearchAgent` 次优搜索，对比最优 vs 次优在 mediumDottedMaze 等迷宫上的得分。 |

---

## 3. 🧪 自动化测试 Harness（官方 autograder + Python 断言）

```bash
# 官方 autograder 全量评测（P1 共 8 题）
python autograder.py --project=search
# 单题复跑（写代码时最常用）
python autograder.py -q q3   # UCS
python autograder.py -q q6   # cornersHeuristic
python autograder.py -q q7   # foodHeuristic
```

```python
# 本地轻量断言：启发函数可采纳性检查（h 值恒不超过真实最短剩余距离）
from searchAgents import foodHeuristic

def test_food_heuristic_admissible():
    # 用官方 layout 构造 GameState 后计算
    state = load_state("mediumSearch")      # 简化示意：实际经 pacman.py 加载
    h = foodHeuristic(state, state.getFoodGrid())
    true_cost = solve_optimal_remaining(state)   # 用 BFS 求真实剩余代价
    assert h <= true_cost, "admissible 要求 h(n) ≤ 真实最优剩余代价"
```

> 注：启发函数是纯函数，可直接单测；完整游戏轨迹验收以 `autograder.py` 输出为准。

---

## 🃏 Anki 卡片

- Q: 为什么 A* 要求启发函数 admissible（可采纳）？曼哈顿距离对 Pacman 网格问题为何 admissible？
- A: admissible 指 h(n) ≤ 真实最优剩余代价，保证 A* 第一次弹出目标时即为最优路径（高估会错过更优解）。曼哈顿距离忽略墙壁，恒不超过真实步数，故 admissible。
- Q: CornersProblem 中「已吃角落集合」应如何编码进状态？
- A: 状态 = (当前位置, 已吃角落的位掩码/集合)；到达新角落时更新掩码，目标判定为掩码覆盖全部 4 个角落。这样问题退化为标准图搜索，DFS/BFS/UCS/A* 均可直接求解。
- Q: 为什么 UCS 在 bigSearch 上扩展节点数远多于带曼哈顿启发式的 A*？
- A: UCS 无启发信息，按累积代价 g 盲目扩展；A* 按 f = g + h 优先扩展「估计总代价」最小的节点，曼哈顿距离引导 Pacman 朝目标推进，扩展节点显著减少。
- Q: 次优搜索（StayEast/StayWest）与最优搜索的得分对比说明了什么？
- A: 次优策略只按简单规则（如尽量留在东侧）行动，可能代价更高或漏吃食物，得分低于最优搜索；说明搜索质量直接转化为游戏得分，这正是 suboptimal search 题目设计的验收意义。

---
