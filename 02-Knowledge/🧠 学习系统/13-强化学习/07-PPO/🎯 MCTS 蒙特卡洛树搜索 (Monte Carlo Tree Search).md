---
type: study
topic: "MCTS 蒙特卡洛树搜索"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段7-PPO]]"
flow: knowledge
kind: concept
difficulty: advanced
concept: ["MCTS", "蒙特卡洛树搜索", "UCB", "规划"]
upstream: ["[[蒙特卡洛方法]]", "[[策略梯度]]"]
tags: [学习, 强化学习]
---
> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段7-PPO|返回阶段页]]

# 🎯 MCTS 蒙特卡洛树搜索 (Monte Carlo Tree Search)

---

## 0. 学习边界

- **类别**：**A 类（核心概念，必须深挖）**
- **判断理由**：MCTS（Monte Carlo Tree Search，蒙特卡洛树搜索）由 Rémi Coulom 等人在 2006 年前后提出，是**解决超高维度状态空间决策（如围棋、复杂规划、LLM 推理思维链 Reasoning）的顶级决策树搜索算法**。它也是 DeepMind 现象级模型 **AlphaGo / AlphaZero** 以及 OpenAI o1 内部搜索思维链的绝对核心基石。不搞懂 MCTS 的四大循环步骤与 UCB 置信上限选择机制，就无法理解深度强化学习如何与树搜索结合战胜人类顶级棋手。

---

## 1. 这个知识点解决什么问题？

> **We Encountered a Problem (我们遇到了什么麻烦)**：
> 在围棋或复杂的决策游戏中，状态组合空间极度庞大（围棋的状态空间高达 $10^{170}$，远超宇宙原子总数）。
> 传统的 Minimax 极小化极大算法或 Alpha-Beta 剪枝必须遍历整棵搜索树，面对如此巨大的搜索空间会发生**组合爆炸**彻底崩溃；而普通的随机蒙特卡洛模拟又极度盲目，绝大部分时间浪费在了探索劣质解上。
> 我们迫切需要一种**既能非均匀地非对称展开高价值分支，又能在“利用已有经验”与“探索未知潜在分支”之间取得最佳平衡**的高效树搜索算法。

---

## 2. 为什么它重要？它有什么用？

- **连接大图景**：MCTS 是连接“启发式搜索”与“数据驱动学习”的桥梁。AlphaZero 将神经网络的 Policy/Value 输出注入 MCTS 中，实现了无须人类棋谱引导的自我博弈进化。
- **实际应用场景**：棋类游戏 AI（围棋、象棋）、自动化路线规划、机器人动作序列规划、大语言模型 Reasoning 过程（思维链搜索与 Step-by-Step 验算）。
- **高频考点/任务**：MCTS 四大步骤（Selection, Expansion, Simulation, Backpropagation）推导、UCB1 / PUCT 算法公式、访问次数 $N(s, a)$ 与价值 $Q(s, a)$ 的更新过程、Python 手写简单 MCTS。

---

## 3. 学它之前需要哪些前置知识？

最小必要背景：

1. **[[MDP 与贝尔曼方程|马尔可夫决策过程 (MDP)]]**：由状态 $S$、动作 $A$、转移概率 $P$ 和奖励 $R$ 构成的决策模型。
2. **[[多臂老虎机与探索-利用|多臂老虎机与 UCB 算法]]**：利用 Upper Confidence Bound (UCB) 平衡探索 (Exploration) 与利用 (Exploitation) 的经典算法。

---

## 4. 用直觉语言解释它

> «“这东西其实就像……”»

- **直觉类比**：MCTS 就像一个**极其理智的智囊团选拔最佳对策的过程**：
  - **1. 选择 (Selection)**：从当前局势出发，智囊团顺着过往积累的经验树往前看，**优先挑那些“过去赢面大，或者还没怎么研究过但看起来有潜力的路”**（用 UCB 选路线）；
  - **2. 扩展 (Expansion)**：走到了经验树的边缘，智囊团在未知节点上衍生出一个新对策分支；
  - **3. 模拟 (Simulation)**：智囊团派出一个“快棋小分队”，从这个新节点开始**快速随机下完整盘棋**（或用 Value 网络估分），看看最后是赢是输；
  - **4. 反向传播 (Backpropagation)**：快棋小分队拿着比赛结果（赢/输），逆向沿着刚才选出的路线一路汇报：“这条路我们又测试了一次，胜率加上去！”
- **为什么很自然**：好走的路多探索，没走过的路给机会，通过千百次快速模拟把搜索资源精准集中在最可能赢的核心主干上！
- **一句话直觉本质**：用 UCB 公式非对称展开决策树，用随机/神经网络采样估计节点价值并逆向更新。

---

## 5. 正式定义、核心公式、符号解释

### 1. MCTS 四大标准步骤循环
每次决策执行 $M$ 次搜索迭代，每次迭代包含：
1. **Selection (选择)**：从根节点出发，根据 UCB1 / PUCT 准则选择子节点，直至到达叶子节点；
2. **Expansion (扩展)**：若叶子节点非终止状态，创建一个或多个子节点；
3. **Simulation / Evaluation (模拟/评估)**：从新节点出发做随机 Rollout 或调用神经网络估计局势价值 $v$；
4. **Backpropagation (反向传播)**：将估计的价值 $v$ 沿选择路径反向更新所有祖先节点的访问次数 $N$ 与累积价值 $Q$。

### 2. 经典 UCB1 子节点选择公式
在节点 $s$ 下选择动作 $a$，满足：
$$a^* = \arg\max_{a \in A(s)} \left( Q(s, a) + c \cdot \sqrt{\frac{\ln N(s)}{N(s, a)}} \right)$$

### 3. AlphaGo / AlphaZero 使用的 PUCT 公式 (加入 Policy 概率)
$$a^* = \arg\max_{a \in A(s)} \left( Q(s, a) + c_{puct} \cdot P(s, a) \cdot \frac{\sqrt{N(s)}}{1 + N(s, a)} \right)$$

### 4. 节点更新公式 (Backpropagation)
对路径上的每个节点 $(s, a)$：
$$N(s, a) \leftarrow N(s, a) + 1$$
$$Q(s, a) \leftarrow Q(s, a) + \frac{v - Q(s, a)}{N(s, a)}$$

### 5. 符号说明表

| 符号 | 含义 | 取值范围 / 量纲 | 备注 |
| :--- | :--- | :--- | :--- |
| $N(s, a)$ | 状态 $s$ 下选择动作 $a$ 的累积访问次数 | 整数 $\ge 0$ | **访问次数越多，估计越准，探索项越小** |
| $N(s)$ | 节点 $s$ 的总访问次数 | $\sum_a N(s, a)$ | 父节点的访问量 |
| $Q(s, a)$ | 动作 $a$ 的平均收益/胜率 | $[-1, +1]$ 或 $[0, 1]$ | 利用项 (Exploitation) |
| $P(s, a)$ | 深度策略网络预测的先验概率 | $[0, 1], \sum P=1$ | 引导搜索先考虑高概率动作 |
| $c, c_{puct}$ | 探索常数 (Exploration Constant) | 常数 (如 1.414 或 5.0) | 越大越倾向于尝试未知分支 |

---

## 6. 推导思路和思想来源

- **最初困难**：深度有限的剪枝搜索需要人工设计极度精准的局势评估函数（Evaluation Function）。然而像围棋这种复杂博弈，人类根本写不出精准的估分表达式。
- **关键转念 1（用随机采样代替评估函数）**：
  如果没有评估函数，那就**让两个随机棋手快速乱下到终局 (Rollout)**！虽然单次乱下随机性极大，但只要跑几百次，胜率统计的均值就会根据大数定律收敛到真实的局势优势！
- **关键转念 2（用 UCB1 克服盲目性）**：
  如果纯随机选择节点，搜索树会展开成对称的大圆盘，效率极低。引入多臂老虎机的 UCB1 理论：
  $$\text{总得分} = \text{已知平均胜率 } Q(s,a) + \text{不确定性奖励 } c \sqrt{\frac{\ln N}{N_a}}$$
  当一个动作 $N_a$ 很小时，不确定性奖励很大，强迫算法去“探索”；当 $N_a$ 变大后，不确定性奖励衰减，算法自动转向“利用”胜率高的高度分支！使决策树呈现极度高效的非对称生长。

---

## 7. 例子：基础 → 中等 → 实际应用

### 例子 1：基础例子（UCB1 节点选择计算）
- **题目**：父节点 $s$ 已被访问 $N(s) = 10$ 次。当前有两个子节点：
  - 动作 $A$: 访问 $N_A = 4$ 次，胜率 $Q_A = 0.75$；
  - 动作 $B$: 访问 $N_B = 1$ 次，胜率 $Q_B = 0.50$。
  探索常数 $c = 1.0$。求下一个应选择哪一个动作？
- **解答过程**：
  1. 计算 $\ln N(s) = \ln(10) \approx 2.3026$。
  2. 计算动作 $A$ 的 UCB1 得分：
     $$\text{UCB}_A = Q_A + c \sqrt{\frac{\ln N(s)}{N_A}} = 0.75 + 1.0 \times \sqrt{\frac{2.3026}{4}} = 0.75 + \sqrt{0.5756} = 0.75 + 0.758 = 1.508$$
  3. 计算动作 $B$ 的 UCB1 得分：
     $$\text{UCB}_B = Q_B + c \sqrt{\frac{\ln N(s)}{N_B}} = 0.50 + 1.0 \times \sqrt{\frac{2.3026}{1}} = 0.50 + 1.517 = 2.017$$
  4. 对比得分：$\text{UCB}_B (2.017) > \text{UCB}_A (1.508)$，因此算法会选择动作 $B$ 进行探索！
- **🤔 追问**：为什么胜率低的 $B$ 反而会被选择？
  - *答*：因为 $B$ 只被测试过 1 次，不确定性极高，UCB 算法必须给它一次机会验证它是否只是偶然输了一把！

### 2. 中等例子（AlphaZero 搜索完成后的最终动作决策）
在 MCTS 跑完 800 次迭代后，根节点得到了各个动作的访问次数分布 $N(s_0, a)$。
最后真正落子时，**并不选择 $Q$ 值最高的动作，而是根据访问次数分布选择！**
- 温度采样公式：$\pi(a \mid s_0) = \frac{N(s_0, a)^{1/\tau}}{\sum_b N(s_0, b)^{1/\tau}}$；
- **原因**：访问次数 $N(s, a)$ 经过数百次 UCB 筛选与反向更新，比容易被噪点影响的 $Q$ 值要**稳定可靠得多**！

### 例子 3：实际应用（Python 手写简单 MCTS 决策树节点与搜索循环）

```python
import math
import random

class MCTSNode:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = {} # action -> MCTSNode
        self.N = 0         # 访问次数
        self.Q = 0.0       # 累积价值

    def is_fully_expanded(self, legal_actions):
        return len(self.children) == len(legal_actions)

    def ucb1(self, action, c_param=1.414):
        child = self.children[action]
        return child.Q / (child.N + 1e-8) + c_param * math.sqrt(math.log(self.N + 1) / (child.N + 1e-8))

def mcts_search(root_state, num_simulations=500):
    root = MCTSNode(root_state)
    
    for _ in range(num_simulations):
        node = root
        state = root_state.clone()
        
        # 1. Selection (选择)
        while not state.is_terminal() and node.is_fully_expanded(state.get_legal_actions()):
            action = max(state.get_legal_actions(), key=lambda a: node.ucb1(a))
            state.apply_action(action)
            node = node.children[action]
            
        # 2. Expansion (扩展)
        legal_actions = state.get_legal_actions()
        if not state.is_terminal():
            untested_actions = [a for a in legal_actions if a not in node.children]
            action = random.choice(untested_actions)
            state.apply_action(action)
            new_node = MCTSNode(state, parent=node)
            node.children[action] = new_node
            node = new_node
            
        # 3. Simulation (随机模拟/评估)
        while not state.is_terminal():
            state.apply_action(random.choice(state.get_legal_actions()))
        reward = state.get_reward() # 1.0 为赢, 0.0 为输
        
        # 4. Backpropagation (反向传播)
        while node is not None:
            node.N += 1
            node.Q += reward
            node = node.parent
            
    # 综合决策：选择访问次数最多的动作
    best_action = max(root.children.keys(), key=lambda a: root.children[a].N)
    return best_action
```

---

## 8. 常见误区和易混概念

### 误区 1：MCTS 搜索结束后，落子决策选择 $Q$ 值最大的动作
- **错误直觉**：“$Q$ 表达了动作的平均胜率，当然选胜率最高的那步棋。”
- **为什么错**：在搜索初期或样本较少时，单次好运可能导致某个劣质动作的 $Q$ 值虚高；而访问次数 $N(s, a)$ 包含了 UCB 的全方位鲁棒检验。选 $N(s, a)$ 最大的动作能够极其有效地抵御偶发噪点。
- **正确理解**：训练初期用按 $N$ 比例采样，最终竞技选 $N$ 最大的动作。

### 概念对比表

| 算法 | 搜索空间展开形态 | 节点评估机制 | 剪枝/终止条件 | 代表领域 |
| :--- | :--- | :--- | :--- | :--- |
| **Alpha-Beta 剪枝** | 深度优先对齐（对称树） | 人工硬编码评估函数 | 极大极小剪枝边界 | 深蓝 (Deep Blue) 国际象棋 |
| **纯蒙特卡洛搜索** | 完全随机大圆盘 | 随机 Rollout 终局胜率 | 固定采样次数 | 传统博弈 AI |
| **MCTS (AlphaZero)** | **非对称非均匀扩展** | **深度神经网络 Policy+Value** | **UCB1 / PUCT 引导** | **AlphaGo / AlphaZero / LLM 搜索** |

---

## 9. 相关知识点与 Obsidian 双链建议

### 上游依赖
- [[MDP 与贝尔曼方程|马尔可夫决策过程]]：MCTS 状态转移的环境模型原型。
- [[多臂老虎机与探索-利用|多臂老虎机]]：UCB1 平衡探索与利用的理论源泉。

### 下游延伸
- AlphaGo / AlphaZero：MCTS 结合 Policy/Value 神经网络的巅峰架构。

### 横向关联
- [[DQN深度Q网络|DQN]] ↔ MCTS：DQN 适合无模型的即时反应策略，MCTS 适合有模型的前瞻 Planning 规划。

---

## 10. 闭卷复现任务

- [ ] 1. 用一句话说清楚 MCTS 解决什么问题（超大状态空间下的高效非对称决策搜索）。
- [ ] 2. 用直觉语言解释它（«“这东西其实就像智囊团测试对策并反向汇报胜率……”»）。
- [ ] 3. 详细列出 MCTS 的四大循环步骤（Selection, Expansion, Simulation, Backprop）。
- [ ] 4. 写出 UCB1 公式并解释探索项与利用项。
- [ ] 5. 写出 PUCT 公式，说明先验概率 $P(s, a)$ 的引入意义。
- [ ] 6. 解释为什么决策时选择访问次数 $N$ 最大的动作而不是 $Q$ 最大的动作。
- [ ] 7. 手算 2 个动作在给定访问量下的 UCB1 得分。
- [ ] 8. 对比 Alpha-Beta 剪枝与 MCTS 的搜索形态区别。
- [ ] 9. 手写包含节点与四大步骤循环的 Python MCTS 基础代码。
- [ ] 10. 简述 MCTS 在大语言模型 (LLM) 思维链 Reasoning 中的应用。

---

## 11. 自测题：5 道

| 题号 | 类型 | 难度 | 考查点 |
| :--- | :--- | :--- | :--- |
| 1 | 概念辨析 | 基础 | MCTS 四大步骤的顺序 |
| 2 | 公式计算 | 基础 | UCB1 公式代入计算 |
| 3 | 条件判断 | 中等 | 探索常数 $c$ 过大或过小的后果 |
| 4 | 变式/综合 | 中等 | AlphaZero 如何用 Value 网络取代随机 Rollout |
| 5 | 开放/证明 | 较难 | 说明为什么 MCTS 在采样数 $N \to \infty$ 时渐进收敛于最优解 |

### 题目与解析

#### 1. MCTS（蒙特卡洛树搜索）算法的标准执行顺序是？
- A. 扩展 (Expansion) $\to$ 选择 (Selection) $\to$ 模拟 (Simulation) $\to$ 反向传播 (Backprop)
- B. 选择 (Selection) $\to$ 扩展 (Expansion) $\to$ 模拟 (Simulation) $\to$ 反向传播 (Backprop)
- C. 模拟 (Simulation) $\to$ 选择 (Selection) $\to$ 扩展 (Expansion) $\to$ 反向传播 (Backprop)
- D. 选择 (Selection) $\to$ 模拟 (Simulation) $\to$ 扩展 (Expansion) $\to$ 反向传播 (Backprop)

> [!question]- 答案解析
> - **答案**：B
> - **解析**：标准顺序为：先从根节点选择 (Selection) 走到叶子，然后扩展 (Expansion) 出新节点，接着对新节点进行模拟估分 (Simulation)，最后将结果沿路径反向传播 (Backpropagation) 更新统计量。

#### 2. 在 UCB1 公式中，如果将探索常数 $c$ 设置为 0，MCTS 算法的行为会变成什么？
> [!question]- 答案解析
> - **答案**：算法彻底失去探索能力，退化为纯粹的贪心算法 (Greedy Search)。
> - **解析**：当 $c=0$ 时，$\text{UCB} = Q(s, a)$，算法每次只会死板地选择当前平均胜率最大的动作，一旦某个好动作第一次尝试偶然输了，算法将再也没有机会去重新探索它（陷入局部最优陷阱）。

#### 3. AlphaZero 是如何改造传统 MCTS 中的 Simulation（模拟）步骤的？
> [!question]- 答案解析
> - **答案**：用深度价值网络 $V_{\theta}(s)$ 的一次前向推理，直接取代慢速且有噪的随机 Rollout 到终局。
> - **解析**：传统 MCTS 需要从新节点随机下完整盘棋（数千步采样）；AlphaZero 直接把新节点输入给 Value 神经网络，一行代码得到评估分 $v \in [-1, 1]$，将模拟开销降低了几百倍且精度更高！

#### 4. 在 MCTS 反向传播步骤中，为什么父节点的访问次数 $N(s)$ 和子节点的访问次数 $N(s, a)$ 都要加 1？
> [!question]- 答案解析
> - **答案**：维护 UCB 不确定性开方项 $\sqrt{\frac{\ln N(s)}{N(s, a)}}$ 的正确比例。
> - **解析**：每多一次模拟，路径上所有父节点的总样本量 $N(s)$ 增加，使得其他未被选择的兄弟节点的 $\ln N(s)$ 增大（提高了不确定性）；同时被选择动作的 $N(s, a)$ 增加（降低了自身的不确定性），从而动态调整下一次搜索的选择偏好。

#### 5. 【开放/大模型迁移】在 OpenAI o1 / 思考大模型中，MCTS 是如何被用于思维链（Chain of Thought, CoT）搜索的？
> [!question]- 答案解析
> - **答案**：将每一个推理步骤（Reasoning Step）作为树节点，用 Process Reward Model (PRM) 作为节点评估。
> - **解析**：在复杂数学/代码推理中，大模型生成解题步骤。MCTS 将每个推理步骤设为动作 $a$，利用 PRM（过程奖励模型）对每个步骤打分，通过 MCTS 进行多路径探索与自纠错，遇到推导错误的死胡同自动回溯，从而大幅提升了复杂问题的求解准确率。

---

## 12. 我的主动回忆区

### 我的闭卷复述
> 不看上文，用自己的话解释这个知识点：

### 我的推导复现
> 不看上文，尝试写出核心公式或推导主线：

### 我的错误与卡点
- 

### 下次复习日期
- [ ] 明天
- [ ] 3 天后
- [ ] 7 天后
- [ ] 14 天后

---

## 13. 给 Obsidian 的归档建议

- **归档目录**：`02-Knowledge/🧠 学习系统/13-强化学习/`
- **建议双链**：
  - [[🗺️ 强化学习学习路径|强化学习学习路径]]

## 闭卷自测
1. MCTS 四阶段（选择/扩展/模拟/回溯）各做什么？
2. UCB 公式如何平衡探索与利用？
3. MCTS 与 AlphaGo 的关系？

## 学完后可以完成

```dataview
TABLE assignment_level, source_type FROM "03-Projects"
WHERE contains(requires, this.file.link)
```

## 相关下游知识

```dataview
LIST FROM "02-Knowledge/🧠 学习系统"
WHERE contains(upstream, this.file.link)
```

