---
type: project
project_type: homework
course: "强化学习"
title: "强化学习-课后作业-CS188-P1-Pacman搜索"
assignment_id: "CS188-P1"
assignment_level: lesson
assignment_format: lab
stage_id: "01"
requires:
  - "[[搜索：BFS与DFS与A星]]"
  - "[[博弈：Minimax与Expectimax]]"
  - "[[🧭 强化学习-前置知识]]"
source_type: official_assignment
source_url: "https://inst.eecs.berkeley.edu/~cs188/fa24/assets/projects/search/search.zip"
created: 2026-08-06
updated: 2026-08-06
status: ongoing
flow: project
tags: [作业, 强化学习, 搜索, 课后作业]
---

# 强化学习-课后作业-CS188-P1-Pacman搜索

> 🎯 **作业目标**：在 Pacman 网格世界中手写四种经典搜索算法（DFS / BFS / UCS / A*），为 CornersProblem 与 FoodSearchProblem 构造可采纳（admissible）启发函数，并实现次优搜索代理。通过官方 autograder 验收，并对比最优搜索与次优搜索在真实迷宫上的得分差距。本作业是后续强化学习课程的**搜索前置作业**：它训练你用「状态—动作—代价」语言建模问题，这正是 MDP 建模的前身。

---

## 1. 身份与边界

- **身份**：强化学习课程课后作业（lesson 级），对应阶段 1（基础与本质）的搜索前置。
- **对应知识**：`[[搜索：BFS与DFS与A星]]`、`[[博弈：Minimax与Expectimax]]`、`[[🧭 强化学习-前置知识]]`。
- **边界（允许 / 禁止）**：
  - ✅ 允许：在 `search.py` 与 `searchAgents.py` 中补全 `search` / `problem` / `heuristic` 函数与类。
  - ❌ 禁止：修改 `autograder.py`、`game.py`、`pacman.py`、`util.py` 的评测逻辑；禁止在启发函数中「作弊」（如直接返回真实最优剩余代价）来通过节点数检查。
  - ⚠️ 启发函数必须**可采纳**（对任意状态 `h(n) ≤ 真实最优剩余代价`），否则 A\* 最优性证明不成立。

---

## 2. 环境与 Starter Code

- **官方来源**：UC Berkeley CS188 *Intro to AI* — Project 1: Search。
- **获取方式**（二选一）：
  - 官方压缩包：`https://inst.eecs.berkeley.edu/~cs188/fa24/assets/projects/search/search.zip`
  - 镜像仓库：`git clone https://github.com/jwb133/project1`（仅用于取 Starter Code，答案仍需独立完成）。
- **关键文件**：
  - `search.py`：实现 `depthFirstSearch` / `breadthFirstSearch` / `uniformCostSearch` / `aStarSearch`。
  - `searchAgents.py`：实现 `CornersProblem` / `cornersHeuristic` / `foodHeuristic` / `findPathToClosestDot`。
  - `pacman.py`（主入口）、`game.py`、`util.py`（已备好 `Stack` / `Queue` / `PriorityQueue`）。
- **运行方式**：

```bash
python pacman.py -l tinyMaze -p SearchAgent -a fn=tinyMazeSearch   # 冒烟测试：验证环境可跑
python pacman.py -l mediumMaze -p SearchAgent -a fn=bfs            # 可视化查看 BFS 轨迹
python pacman.py -l mediumDottedMaze -p StayEastSearchAgent        # 次优搜索示例
python autograder.py --project=search                              # 官方自动评测（按题打分）
```

- **验收口径**：autograder 按 q1→q8 逐题打分，每题检查轨迹合法性、路径代价最优性与扩展节点数。`Honor Code`：官方 solutions 仅用于完成后自查。

---

## 3. 题目详述（自包含，题号与官方一致）

### Q1 — 深度优先搜索（DFS）
在 `search.py` 中实现 `depthFirstSearch(problem)`，返回从起点到目标的动作列表 `[North, South, ...]`。
- 要求：用 `util.Stack` 做 fringe；**不要重复扩展已放入 fringe 的节点**（否则会陷入环）。
- 评测：在 `tinyMaze` / `mediumMaze` 上能找到一条合法路径（不要求最短）。

### Q2 — 广度优先搜索（BFS）
实现 `breadthFirstSearch(problem)`，返回**最短**路径。
- 要求：用 `util.Queue`；用 `visited` 集合记录已扩展状态，保证每个状态只扩展一次。
- 关键数据：在 `mediumMaze`（代价全为 1）上，最优路径长度 = 68 步；UCS 与 BFS 结果应一致。

### Q3 — 一致代价搜索（UCS）
实现 `uniformCostSearch(problem)`。
- 要求：用 `util.PriorityQueue`，优先级 = 累计代价 `g`；记录到达每个状态的当前最小代价，遇到更小代价时更新。
- 关键数据：`tinyMaze` 中一条边代价为 1、另一条为 2，UCS 应能避开高代价边选择更长但总代价更小的路径。

### Q4 — A\* 搜索
实现 `aStarSearch(problem, heuristic)`，并给出 `nullHeuristic(position, problem)`（恒返回 0）。
- 要求：优先级 `f = g + h`；以 `manhattanHeuristic`（曼哈顿距离）作为默认启发式。
- 性质：曼哈顿距离忽略墙壁，恒不超过真实步数 ⇒ **admissible**。在 `mediumMaze` 上 A\* 扩展节点数应明显少于 UCS。

### Q5 — CornersProblem（图搜索建模）
在 `searchAgents.py` 中实现 `CornersProblem`：
- 状态 = `(pacman位置, 已访问角落集合)`。迷宫有四个角落，初始集合为空。
- 实现 `getStartState` / `isGoalState`（四角落全访问）/ `getSuccessors` / `getCostOfActions`。
- 评测：autograder 用 `mediumCorners` 检查状态编码与可解性。

### Q6 — Corners 启发函数
实现 `cornersHeuristic(state, problem)`，返回剩余角落的真实最短代价**下界**。
- 提示：可计算「未访问角落两两之间 + 当前位置到最近未访问角落」的最小生成树（MST）长度，或取「当前位置到各未访问角落的 BFS 距离之和」的某种下界。
- 红线：**必须 admissible**（autograder 会随机抽查若干状态，若 `h > 真实最优剩余代价` 直接判错）。

### Q7 — FoodSearchProblem 与 foodHeuristic
`FoodSearchProblem` 已给出；实现 `foodHeuristic(state, problem)` 用于吃光全部食物。
- 要求：admissible 且尽量紧；在 `bigSearch`（大迷宫）上扩展节点数越少越好。
- 常用下界：所有食物点最小生成树长度、或「当前位置到最近食物 + 食物间 MST」。

### Q8 — 次优搜索（Suboptimal Search）
实现 `findPathToClosestDot(problem, gameState)`，返回到**最近食物点**的路径（用于 `ClosestDotSearchAgent`）。
- 要求：不必是最优全解，只需可靠地逐步吃到最近食物；测试布局 `mediumDottedMaze`。
- 对照：`StayEastSearchAgent` / `StayWestSearchAgent` 已实现，跑 `mediumDottedMaze` 对比「次优 vs 最优」得分差距。

---

## 4. 提交产物

- 修改后文件：`search.py`、`searchAgents.py`（仅这两个文件）。
- 提交形式：将两文件打包（或推到个人仓库），附一份 `README` 说明：各题最终得分、`bigSearch` 上 `foodHeuristic` 的扩展节点数、你采用的启发函数思路（≤200 字）。
- 禁止提交官方 `autograder` 输出以外的「答案文件」。

---

## 5. 评分 Rubric（满分 100）

| 维度 | 分值 | 标准 |
| :--- | :---: | :--- |
| 四类搜索正确性 | 30 | DFS/BFS/UCS/A\* 在对应布局上输出合法且（BFS/UCS/A\*）最优路径 |
| 问题建模（Q5） | 15 | 状态含「位置+已访问角落」，成功/后继/代价正确 |
| 启发函数可采纳性（Q6/Q7） | 25 | `h ≤ 真实剩余代价`（抽查不破），且在 `bigSearch` 上显著优于无启发 |
| 次优搜索（Q8） | 15 | `findPathToClosestDot` 能逐步吃豆，得分高于 Stay 系列基线 |
| 代码与 README | 15 | 仅改规定文件、思路说明清晰、无修改评测逻辑 |

---

## 6. 基础要求、必要提示与常见错误

- **必要提示**：BFS/UCS 的 `visited` 必须在「出队扩展」时标记，而非「入队」时标记，否则可能漏掉更优路径；A\* 的 `PriorityQueue` 用 `(f, count, item)` 避免比较 item。
- **常见错误**：① DFS 不记录 visited 导致死循环；② BFS 把节点在入队时标记 visited，使更短路径被忽略；③ 启发函数为了「过节点数检查」偷偷返回真实最优值（违反 admissible，逻辑错误）；④ UCS 优先级只存 `g` 却忘了用 `g` 去重。
- **调试建议**：先用 `tinyMaze` 冒烟，再上 `mediumMaze` 看轨迹，最后用 `autograder.py -q qN` 单题复跑。

---

## 7. 可选进阶任务（非主任务前置）

- 实现 `ManhattanCornersHeuristic` 之外的第三种角落启发式（如真 MST），对比节点数。
- 把 `foodHeuristic` 改成「一致性（consistent）」启发式并证明 `h(x) ≤ cost(x,y)+h(y)` 恒成立。
- 在 `bigSearch` 上对比 A\*（曼哈顿 / 食物 MST）扩展节点数，绘制条形图。

---

## 8. 自检清单

- [ ] `autograder.py --project=search` 全 8 题通过
- [ ] BFS/UCS 在 `mediumMaze` 上路径长度 = 68
- [ ] `cornersHeuristic` / `foodHeuristic` 通过 admissible 抽查
- [ ] `mediumDottedMaze` 上我的 agent 得分 > `StayEastSearchAgent`

---

## 9. 来源与后续入口

- **来源**：题号、要求、布局与评分口径翻译自 UC Berkeley CS188 Project 1（教育用途，CC-BY 课程材料），保持原题意图；本地未改写公式与提交语义。
- **后续入口**：完成本作业后进入 `[[强化学习-课后作业-CS188-P2-多智能体搜索|课后作业 P2 多智能体搜索]]`（对抗搜索），再到 `[[强化学习-阶段作业-CS188-P3-Q学习与近似Q学习|阶段作业 P3 Q-Learning]]`（正式进入强化学习）。
- **复习卡**：`[[搜索：BFS与DFS与A星]]`、`[[博弈：Minimax与Expectimax]]`。

---

## 🃏 知识内化卡片

- Q：为什么 A\* 要求启发函数 admissible（可采纳）？曼哈顿距离对网格问题为何 admissible？
- A：admissible 指 `h(n) ≤ 真实最优剩余代价`，保证 A\* 第一次弹出目标时即为最优路径（高估会错过更优解）。曼哈顿距离忽略墙壁，恒不超过真实步数，故 admissible。
- Q：CornersProblem 中「已吃角落集合」应如何编码进状态？
- A：状态 = `(当前位置, 已吃角落的位掩码/集合)`；到达新角落时更新掩码，目标判定为掩码覆盖全部 4 个角落。问题退化为标准图搜索，DFS/BFS/UCS/A\* 均可直接求解。
- Q：为什么 UCS 在 bigSearch 上扩展节点数远多于带曼哈顿启发式的 A\*？
- A：UCS 无启发信息，按累积代价 `g` 盲目扩展；A\* 按 `f = g + h` 优先扩展「估计总代价」最小的节点，曼哈顿距离引导推进，扩展节点显著减少。
- Q：次优搜索（StayEast/StayWest）与最优搜索的得分对比说明了什么？
- A：次优策略只按简单规则行动，可能代价更高或漏吃食物，得分低于最优搜索；说明搜索质量直接转化为游戏得分，这正是 suboptimal search 题目的验收意义。
