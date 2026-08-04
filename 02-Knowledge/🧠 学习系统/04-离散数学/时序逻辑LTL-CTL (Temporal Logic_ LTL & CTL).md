---
type: concept
topic: 时序逻辑LTL-CTL
created: 2026-07-28
status: learning
difficulty: advanced
concept:
- 线性时序逻辑LTL
- 计算树逻辑CTL
- 模型检测
- Kripke结构
prerequisites:
- '[[命题与联结词]]'
- '[[谓词]]'
related:
- '[[DFA]]'
tags:
- 学习
- 离散数学
- 数理逻辑
- 时序逻辑
- LTL
- CTL
- 模型检测
- 形式验证
- 克里普克结构
title: 时序逻辑LTL-CTL
date: 2026-07-28
updated: 2026-07-28
kind: concept
flow: knowledge
course: 离散数学
importance: A
upstream:
- '[[命题与联结词]]'
- '[[谓词]]'
- '[[自然演绎]]'
downstream:
- '[[程序形式化验证]]'
- '[[并发程序正确性]]'
stage: 🎯 第四阶段：融会贯通 (Synthesis & Mastery)
module: 数理逻辑与软件验证
---

# 时序逻辑LTL-CTL (Temporal Logic: LTL & CTL)

## 0. 先判断它值不值得深挖

- **分类结果**: **A 类（核心概念，必须深挖）**
- **分类理由**: 2007 年图灵奖授予了埃德蒙·克拉克 (Edmund Clarke)、欧伦·爱默生 (E. Allen Emerson) 与 约瑟夫·西法基斯 (Joseph Sifakis)，以表彰他们发明的 **模型检测 (Model Checking)** 技术。模型检测的核心规范语言正是 **线性时序逻辑 (Linear Temporal Logic, LTL)** 与 **计算树逻辑 (Computation Tree Logic, CTL)**。经典[[命题与联结词|命题逻辑]]只能断言“静态事实”的真假；而时序逻辑将逻辑学推向了**动态时间与状态迁移维度**。它能精确规范“死锁绝对不会发生 (Safety)”、“按请求最终必然得到响应 (Liveness)”以及“公平性 (Fairness)”。它是现代并发软件、操作系统内核、自动驾驶控制代码以及 Intel/AMD 芯片形式化验证的数理逻辑心脏。

---

## 1. 这个知识点解决什么问题？

**我们遇到了什么麻烦？**

对于一个并发系统（如交通信号灯控制器、多线程锁、操作系统调度器），普通的逻辑命题“$P \land Q$”显得无能为力：
- 我们想表达：“在任何时刻，两个方向的绿灯**绝不能同时亮起**”；
- 我们想表达：“只要按下电梯按钮，电梯在**未来某个时刻必然会到达**”；
- 我们想表达：“一旦发生故障，系统将**一直保持警告状态，直到管理员复位**”。

如果只靠自然语言描述这些规范，必定会导致歧义与漏洞。

为了**用严密无歧义的逻辑公式表达“随时间演化的系统行为”**，数理逻辑学家建立了 **LTL 与 CTL 时序逻辑**。

---

## 2. 为什么它重要？它有什么用？

- **课程逻辑与验证大图景位置**: 从静态数理逻辑向动态系统形式化验证跨越的最高理论总结。
- **后续知识支撑**:
  - [[程序形式化验证]]: 模型检测工具 (SPIN, NuSMV, PRISM) 的输入规范标准；
  - [[DFA]]: 将 LTL 公式转化为 Büchi 自动机进行全状态空间交叉检验；
  - **并发程序正确性**: 证明多线程无锁算法 (Lock-Free Algorithm) 的无死锁与无饥饿性质。
- **实战与跨学科应用**:
  - **硬件芯片验证**: 验证 CPU 缓存一致性协议 (MESI) 绝对不发生数据竞争；
  - **航天与医疗设备控制**: 验证波音飞机飞控软件与 Therac-25 辐射仪代码的 Safety 规范。

---

## 3. 学它之前需要哪些前置知识？

- **命题与谓词逻辑**: $\neg, \land, \lor, \to$。
- **状态迁移系统 (Transition System)**: 了解节点表示状态、有向边表示迁移的离散图。
  - *最小必要背景速补*: 时序逻辑作用在 **克里普克结构 (Kripke Structure)** 上。你可以把系统运行看作在有向图上沿着时间轴走出的无限路径。

---

## 4. 用直觉语言解释它

«“LTL 就像**坐在单程列车上看窗外的单线条时间线**；而 CTL 就像**站在命运的分叉路口看所有平行宇宙交织成的计算树**。”»

假设你在玩一个人生选择游戏：
1. **线性时序逻辑 (LTL)**：
   - 关注的是**某一根具体的未来时间线**。
   - 算子：**$X$ (NeXt 下一步)**、**$F$ (Future 未来某个时刻)**、**$G$ (Globally 永远)**、**$U$ (Until 直到)**。
   - 例子：$G(\text{健康})$ 表示“我**永远**健康”；$F(\text{成功})$ 表示“我**未来总有一天**会成功”。
2. **计算树逻辑 (CTL)**：
   - 关注的是**从当下展开的所有可能分支平行宇宙**。
   - 在 LTL 算子前强制加上路径量词：**$A$ (All 对所有可能平行宇宙)** 或 **$E$ (Exists 存在某个平行宇宙)**。
   - 例子：$AF(\text{成功})$ 表示“在**所有**可能的未来里，我都注定会成功”；$EF(\text{成功})$ 表示“在**至少某一个**平行宇宙里，我有成功的可能”。

---

## 5. 正式定义、核心公式、符号解释

### 1. 语义载体：克里普克结构 (Kripke Structure)

时序逻辑的语义定义在**克里普克结构** $M = (S, S_0, R, L, AP)$ 上：
- $S$: 有限状态集合；
- $S_0 \subseteq S$: 初始状态集合；
- $R \subseteq S \times S$: 状态迁移关系（要求对任意 $s \in S$，存在 $s'$ 使 $(s, s') \in R$，即无死端）；
- $AP$: 原子命题集合；
- $L: S \to \mathcal{P}(AP)$: 状态标注函数，标注每个状态下成立的原子命题。

---

### 2. 时序逻辑四大核心时序算子

对时间路径上的命题：

1. **下一个 (NeXt) $\mathbf{X} \, \phi$**:
   $\phi$ 在**紧接着的下一个状态**成立。
2. **未来 (Future / Eventually) $\mathbf{F} \, \phi$**:
   $\phi$ 在**未来的某个时刻（包含当前）**至少成立一次。
3. **全局 (Globally / Always) $\mathbf{G} \, \phi$**:
   $\phi$ 在**从今往后的所有未来时刻**恒成立。
4. **直到 (Until) $\phi \,\mathbf{U}\, \psi$**:
   $\phi$ 一直成立，**直到** $\psi$ 首次成立（且 $\psi$ 未来必须成立）。

---

### 3. LTL 与 CTL 的语法区别与公式

#### 线性时序逻辑 (LTL - Linear Temporal Logic)
LTL 语法公式由命题联结词与时序算子组合，隐式对所有路径成立：
$$ \phi ::= p \mid \neg \phi \mid \phi_1 \land \phi_2 \mid \mathbf{X} \phi \mid \mathbf{F} \phi \mid \mathbf{G} \phi \mid \phi_1 \mathbf{U} \phi_2 $$

#### 计算树逻辑 (CTL - Computation Tree Logic)
CTL 要求每个时序算子（$X, F, G, U$）必须**紧跟在路径量词 $A$ 或 $E$ 之后**：
- **$A$ (All Paths)**: 对从当前状态出发的**所有**路径成立；
- **$E$ (Exists Path)**: 存在**至少一条**从当前状态出发的路径成立。

CTL 的 8 大基本状态公式：
$$ \mathbf{AX} \phi, \quad \mathbf{EX} \phi, \quad \mathbf{AF} \phi, \quad \mathbf{EF} \phi, \quad \mathbf{AG} \phi, \quad \mathbf{EG} \phi, \quad \mathbf{A}[\phi_1 \mathbf{U} \phi_2], \quad \mathbf{E}[\phi_1 \mathbf{U} \phi_2] $$

---

### 4. 软件工程三大经典时序模式

| 规范模式 | 逻辑含义 | LTL 公式 | CTL 公式 |
|:---|:---|:---|:---|
| **安全性 (Safety)** | 坏事绝对不能发生 | $\mathbf{G} (\neg \text{bad})$ | $\mathbf{AG} (\neg \text{bad})$ |
| **活性 (Liveness)** | 好事最终必定发生 | $\mathbf{G} (\text{req} \to \mathbf{F} \, \text{ack})$ | $\mathbf{AG} (\text{req} \to \mathbf{AF} \, \text{ack})$ |
| **可达性 (Reachability)**| 存在状态可以到达目标 | - | $\mathbf{EF} \, \text{goal}$ |

---

### 符号解释表

| 符号 | 含义 | 对应英文 | 备注 |
|:---:|:---|:---|:---|
| $\mathbf{X}$ | 下一个状态 | NeXt | 仅往前跨 1 步 |
| $\mathbf{F}$ | 未来某个时刻 | Future / Eventually | 包含当前时刻在内的未来 |
| $\mathbf{G}$ | 永远 / 全局 | Globally / Always | 所有未来时刻无一例外 |
| $\mathbf{U}$ | 直到 | Until | $\phi \mathbf{U} \psi$ 意味着 $\psi$ 最终必发生 |
| $\mathbf{A}$ | 所有路径 | All paths | CTL 路径全称量词 |
| $\mathbf{E}$ | 存在路径 | Exists path | CTL 路径存在量词 |

---

## 6. 推导思路和思想来源

- **推导主线（时序算子之间的代数对偶关系）**:
  1. 就像谓词逻辑中 $\forall x \phi \equiv \neg \exists x \neg \phi$ 一样，时序算子满足极漂亮的对偶关：
  2. **$F$ 与 $G$ 的对偶律**:
     $$ \mathbf{F} \phi \equiv \neg \mathbf{G} (\neg \phi) $$
     （“未来一定会发生”等价于“不是永远不发生”）。
  3. **$F$ 与 $U$ 的表达关系**:
     $$ \mathbf{F} \phi \equiv \text{True} \;\mathbf{U}\; \phi $$
     （“未来一定会发生 $\phi$”等价于“True 一直成立直到 $\phi$ 发生”）。
  4. **CTL 中 $A$ 与 $E$ 的路径对偶律**:
     $$ \mathbf{AX} \phi \equiv \neg \mathbf{EX} (\neg \phi) $$
     $$ \mathbf{AG} \phi \equiv \neg \mathbf{EF} (\neg \phi) $$
     $$ \mathbf{AF} \phi \equiv \neg \mathbf{EG} (\neg \phi) $$
  5. 这一对偶律使得模型检测工具（如 NuSMV）只需要实现 3 个基本算子（如 $EX, EG, EU$），即可表达出所有 CTL 公式！

---

## 7. 例子：基础 → 中等 → 实际应用

### 例子 1：基础例子（交通信号灯防冲突逻辑表达）
- **题目**: 考虑两个交叉路口的红绿灯系统。原子命题为 $Green_1, Red_1, Green_2, Red_2$。
  写出表达以下三条规范的时序逻辑公式：
  1. “方向 1 和方向 2 **绝不能同时亮绿灯**”（Safety）；
  2. “只要方向 1 变为红灯，方向 2 **下一个时刻必定变为绿灯**”；
  3. “如果方向 1 提出了变绿请求 $Req_1$，它**未来最终必定变为绿灯**”（Liveness）。

- **解答过程**:
  1. **安全性公式**: $\mathbf{G} \neg (Green_1 \land Green_2)$ （或 CTL 的 $\mathbf{AG} \neg (Green_1 \land Green_2)$）；
  2. **下一个状态公式**: $\mathbf{G} (Red_1 \to \mathbf{X} Green_2)$；
  3. **活性公式**: $\mathbf{G} (Req_1 \to \mathbf{F} Green_1)$。

---

### 例子 2：中等例子（哲学家就餐问题 Dining Philosophers 死锁分析）
- **场景**: 5 个哲学家围坐吃面，每人需要同时拿到左右两根筷子才能进餐。
  - 命题 $Eat_i$：第 $i$ 个哲学家正在进餐；
  - 命题 $Starve_i$：第 $i$ 个哲学家处于饥饿等待状态。
- **形式化表达**:
  1. **无死锁规范 (No Deadlock)**:
     系统绝不能进入所有人都拿起左筷子、所有人陷入永久卡死的状态。
     LTL 公式：$\mathbf{G} \mathbf{F} (Eat_1 \lor Eat_2 \lor Eat_3 \lor Eat_4 \lor Eat_5)$ （永远会在未来某个时刻有人吃到面）；
  2. **无饥饿规范 (No Starvation)**:
     任何陷入饥饿等待的哲学家，最终都能吃到面。
     LTL 公式：$\mathbf{G} (Starve_i \to \mathbf{F} Eat_i)$；
  3. **模型检测**: 运行 SPIN 模型检测器，若公式被违反，SPIN 会输出一条反例反路径（Counterexample Path），精确复现死锁发生的线程调度序列！

---

### 例子 3：实际应用例子
- **真实场景**: **英特尔 CPU 缓存一致性协议 (MESI) 形式化验证**
  在多核 CPU 中，多个核心拥有独立的 L1 Cache。MESI 协议包含 4 种状态：Modified, Exclusive, Shared, Invalid。
  - **模型检测验证**:
    硬件工程师使用 NuSMV 模型检测器，将 MESI 状态机输入为 Kripke 结构，写出 CTL 规范：
    $$ \mathbf{AG} \Big( \text{Cache}_1.\text{state} == \text{Modified} \;\to\; \mathbf{AX} (\text{Cache}_2.\text{state} == \text{Invalid}) \Big) $$
    （即：“当核 1 将数据改写为 Modified 时，所有其他核在下一个时刻必须全部失效”）。
    如果在某个极其罕见的并发时序下公式不成立，模型检测器能在芯片流片前找到死锁漏洞，避免数亿美元的硬件召回！

---

## 8. 常见误区和易混概念

### 常见误区

#### 误区 1：混淆 LTL 与 CTL 的表达能力
- **错误直觉**: “CTL 一定包含 LTL，或者 LTL 一定包含 CTL。”
- **为什么错**: **两者表达能力是交错互补的**！
  - **LTL 能够表达** 复杂的公平性规范 $\mathbf{G}\mathbf{F} p \to \mathbf{G}\mathbf{F} q$（CTL 无法表达）；
  - **CTL 能够表达** 重置可能性 $\mathbf{AGEF} \, p$（“在任何状态下，都有可能返回初始状态 $p$”，LTL 无法表达）；
  - 组合两者得到了更强大的 **$CTL^*$**。

#### 误区 2：误以为 $\mathbf{F} \phi$ 不包含当前时刻
- **错误直觉**: “$\mathbf{F} \phi$ 意味着 $\phi$ 必须在 strictly 严格的未来（至少 1 步后）发生。”
- **为什么错**: 在标准 LTL/CTL 语义中，$\mathbf{F} \phi$ 包含**当前时刻**！如果当前时刻 $\phi$ 已经为真，则 $\mathbf{F} \phi$ 在当前立刻满足。若要求至少 1 步后发生，必须写为 $\mathbf{X} \mathbf{F} \phi$。

### LTL vs CTL vs $CTL^*$ 表达能力全方位对比表

| 时序逻辑 | 结构视角 | 路径量词规则 | 代表性强项 | 典型工具 |
|:---|:---|:---|:---|:---|
| **LTL** | 线性序列路径 | 全局隐式 $\forall \pi$ | 强于表达强公平性 (Fairness) 与长路径组合 | **SPIN** |
| **CTL** | 树状分支路径 | 量词 $A/E$ 与 $X,F,G,U$ **一对一绑定** | 强于表达可达性与重置可能 ($\mathbf{AGEF}$) | **NuSMV** |
| **$CTL^*$** | 树状分支路径 | 量词 $A/E$ 可自由嵌套时序算子 | 严格包含 LTL 与 CTL 的所有表达力 | 理论基准 |

---

## 9. 相关知识点与 Obsidian 双链建议

### 上游依赖
- [[命题与联结词]], [[谓词]]: 静态数理逻辑基础。
- [[自然演绎]]: 推导与公理化基础。

### 下游延伸
- [[程序形式化验证]]: 模型检测算法（如基于 BDD 的符号模型检测 SMV）。
- [[DFA]]: LTL 转化为 Büchi 自动机进行交叉乘积检验。

---

## 10. 闭卷复现任务

合上笔记后，请独立回答以下 10 个问题：
1. 用一句话说明时序逻辑打破了传统命题逻辑的什么局限。
2. 用“单程列车 vs 平行宇宙树”直觉解释 LTL 与 CTL 的区别。
3. 准确写出克里普克结构 (Kripke Structure) 的五元组定义。
4. 准确写出 4 大核心时序算子 $X, F, G, U$ 的含义。
5. 准确写出 CTL 的 2 个路径量词 $A, E$ 的含义。
6. 写出软件工程三大经典模式（Safety, Liveness, Reachability）的 LTL/CTL 公式。
7. 写出 $F \phi$ 与 $G \phi$ 的对偶律关系。
8. 区分 LTL 与 CTL 在表达能力上的差异。
9. 解释模型检测在硬件芯片与哲学家就餐死锁分析中的应用。
10. 对比 LTL, CTL 与 $CTL^*$ 的结构视角与工具。

---

## 11. 自测题：5 道

| 题号 | 类型 | 难度 | 考查点 |
|:---:|:---:|:---:|:---|
| 1 | 概念辨析 | 基础 | 4 大时序算子 $X, F, G, U$ 的含义识别 |
| 2 | 公式运用 | 基础 | 翻译自然语言规范为 LTL 时序逻辑公式 |
| 3 | 条件判断 | 中等 | CTL 语法合规性判定（量词与算子绑定） |
| 4 | 变式/综合 | 中等 | 给定简单的 Kripke 结构演练 CTL 公式真值求解 |
| 5 | 开放/证明 | 较难 | 利用展开等价式证明 $\mathbf{G} \phi \equiv \phi \land \mathbf{X} (\mathbf{G} \phi)$ |

### 题目 1
在 LTL 时序逻辑中，公式 $\mathbf{G} (Request \to \mathbf{F} Ack)$ 的精确含义是：
A. 请求和响应必须同时发生
B. 只要提出 Request，在下一个时刻必须收到 Ack
C. 只要提出 Request，在未来的某个时刻必定收到 Ack，且这一规律在全过程中恒成立
D. Ack 一直成立，直到 Request 发生

> [!question]- 答案解析
> **答案**: C
> **解析**: $\mathbf{G}$ 表示“永远/全局”，$\to$ 表示“蕴含”，$\mathbf{F}$ 表示“未来某个时刻”。整个公式是标准的**活性 (Liveness) 模式**：“在任何时刻，只要提出了 Request，未来最终必定会得到 Ack”（C 正确）。
> **Obsidian 标签**: `#自测题 #基础 #LTL公式`

---

### 题目 2
下列公式中，符合 **CTL 语法规范** 的是：
A. $\mathbf{A} (\mathbf{F} \phi \land \mathbf{G} \psi)$
B. $\mathbf{AG} (\phi \to \mathbf{AF} \psi)$
C. $\mathbf{F} \mathbf{G} \phi$
D. $\mathbf{E} (\mathbf{F} \phi \to \psi)$

> [!question]- 答案解析
> **答案**: B
> **解析**: 在 CTL 语法中，每一个时序算子（$X, F, G, U$）前面必须**紧跟**一个路径量词（$A$ 或 $E$）。
> - B 选项中，$\mathbf{AG}$ 和 $\mathbf{AF}$ 都是量词与算子一对一紧密绑定的，完全符合 CTL 语法！
> - A、C、D 选项中均存在量词缺失或多个时序算子直接组合的情况（这些属于 LTL 或 $CTL^*$ 语法，不符合严格的 CTL 语法）。
> **Obsidian 标签**: `#自测题 #基础 #CTL语法`

---

### 题目 3
判断命题正误：CTL 公式 $\mathbf{EF} \, p$ 的含义是“从当前状态出发，在所有可能的未来路径上， $p$ 都必然会在未来某个时刻成立”。

> [!question]- 答案解析
> **答案**: 错误
> **解析**: $\mathbf{E}$ 表示“**存在**至少一条路径”。因此 $\mathbf{EF} \, p$ 表示“**存在**某条未来路径，使得 $p$ 在其上最终成立”（即可达性）。如果要求“在**所有**可能的未来路径上”，必须使用全称量词 $\mathbf{AF} \, p$。
> **Obsidian 标签**: `#自测题 #中等 #CTL路径量词`

---

### 题目 4
考虑克里普克结构 $M$，包含两个状态 $S = \{s_0, s_1\}$，迁移关系为 $R = \{(s_0, s_1), (s_1, s_1)\}$。
原子命题 $p$ 只在 $s_1$ 状态下标注为真（即 $L(s_0)=\emptyset, L(s_1)=\{p\}$）。
初始状态为 $s_0$。判定下列公式在初始状态 $s_0$ 下是否成立：
1. $s_0 \models \mathbf{EX} \, p$
2. $s_0 \models \mathbf{AX} \, p$
3. $s_0 \models \mathbf{AF} \, p$

> [!question]- 答案解析
> **答案**: 见下述分析
> **解析**:
> 1. 从 $s_0$ 出发只有唯一的迁移目标 $s_1$。因为 $s_1 \models p$，所以在下一个状态 $p$ 成立。故 $s_0 \models \mathbf{EX} \, p$ **成立**；
> 2. 由于唯一的后继状态就是 $s_1$，所有后继状态均满足 $p$，故 $s_0 \models \mathbf{AX} \, p$ **成立**；
> 3. 唯一的执行路径为 $s_0 \to s_1 \to s_1 \to s_1 \dots$。在该路径上，第 2 个时刻节点 $s_1$ 满足 $p$，故 $p$ 最终成立。因此在所有路径上 $p$ 最终都会成立，故 $s_0 \models \mathbf{AF} \, p$ **成立**。
> **Obsidian 标签**: `#自测题 #综合 #Kripke结构验证`

---

### 题目 5
利用固定点与展开等价性，证明 LTL 公式：
$$ \mathbf{G} \phi \equiv \phi \land \mathbf{X} (\mathbf{G} \phi) $$

> [!question]- 答案解析
> **答案**: 见下述证明
> **解析**:
> 1. **证明方向 $\implies$ ($\mathbf{G} \phi \to \phi \land \mathbf{X} (\mathbf{G} \phi)$)**:
>    - 假设路径 $\pi = t_0, t_1, t_2, \dots \models \mathbf{G} \phi$；
>    - 根据 $\mathbf{G}$ 的定义，$\phi$ 在路径的每一个时刻 $t_i$ ($i \ge 0$) 均成立；
>    - 特别地，在 $i=0$ 时刻，$\phi$ 在 $t_0$ 成立，故 $\pi \models \phi$；
>    - 在 $i \ge 1$ 的所有时刻，$\phi$ 在子路径 $\pi^1 = t_1, t_2, \dots$ 上恒成立，故 $\pi^1 \models \mathbf{G} \phi \implies \pi \models \mathbf{X} (\mathbf{G} \phi)$；
>    - 结合两点，$\pi \models \phi \land \mathbf{X} (\mathbf{G} \phi)$。
> 2. **证明方向 $\impliedby$ ($\phi \land \mathbf{X} (\mathbf{G} \phi) \to \mathbf{G} \phi$)**:
>    - 假设 $\pi \models \phi \land \mathbf{X} (\mathbf{G} \phi)$；
>    - 这意味着 $\pi \models \phi$（时刻 0 满足 $\phi$），且 $\pi \models \mathbf{X} (\mathbf{G} \phi)$（在子路径 $\pi^1 = t_1, t_2 \dots$ 上 $\phi$ 恒成立）；
>    - 因此 $\phi$ 在时刻 0，以及时刻 $1, 2, 3 \dots$ 全线成立；
>    - 故 $\phi$ 在路径 $\pi$ 的所有时刻恒成立，即 $\pi \models \mathbf{G} \phi$。
> 3. 综上所述，$\mathbf{G} \phi \equiv \phi \land \mathbf{X} (\mathbf{G} \phi)$ 严格等价。得证！（该式为模型检测中展开计算全局特性的固定点展开基础）。
> **Obsidian 标签**: `#自测题 #证明 #较难 #固定点展开`

---

## 12. 我的主动回忆区

## 我的闭卷复述
> 不看上文，用自己的话解释这个知识点：

## 我的推导复现
> 不看上文，尝试写出核心公式或推导主线：

## 我的错误与卡点
- 

## 下次复习日期
- [ ] 明天
- [ ] 3 天后
- [ ] 7 天后
- [ ] 14 天后

---

## 13. 给 Obsidian 的归档建议

- **归档目录**: `04-离散数学/04-融会贯通/`
- **推荐关联笔记**: [[命题与联结词]], [[谓词]], [[自然演绎]], [[DFA]], [[程序形式化验证]]
- **建议标签**: `#学习 #离散数学 #数理逻辑 #时序逻辑 #LTL #CTL #模型检测 #形式验证 #克里普克结构 #核心概念`
- **拆分建议**: 本篇为时序逻辑与模型检测核心主卡（A类）。形式化
