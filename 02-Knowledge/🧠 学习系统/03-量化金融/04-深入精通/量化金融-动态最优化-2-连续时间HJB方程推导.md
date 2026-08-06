---
title: 贝尔曼方程 2：连续时间与 HJB 偏微分方程推导
type: study
topic: HJB方程推导
created: '2026-08-04'
status: ongoing
difficulty: advanced
course: 量化金融
importance: A
stage: 'Chapter 11: Dynamic Programming'
tags:
- 学习
- 动态规划
- HJB方程
- 随机过程
concept:
- HJB 方程
- 伊藤引理与泰勒展开
prerequisites:
- '[[量化金融-动态最优化-1-贝尔曼方程直觉与离散推导]]'
- '[[量化金融-随机过程-伊藤引理与随机微分方程]]'
related:
- '[[量化金融-动态最优化-3-Merton最优消费问题应用]]'
flow: knowledge
kind: derivation
source: 本课程历史知识卡；原始来源 [待验证]
source_url: '[待验证]'
accessed: '2026-08-06'
license: link-only；正文为本地学习整理
assessment_exempt: false
---

# HJB方程推导

---

## 0. 先判断它值不值得深挖

- **类别**：**A 类（核心定理，必须深挖）**
- **判断理由**：在上一张卡片中，我们理解了离散时间（一天一天算）的贝尔曼方程。但在金融市场，价格是按“秒”甚至“微秒”跳动的，我们需要把时间的间隔 $dt$ 无限缩短，推导出连续时间下的方程。这就是大名鼎鼎的 **HJB 偏微分方程 (Hamilton-Jacobi-Bellman Equation)**。这是整个连续时间金融学（Continuous-time Finance）的皇冠。

---

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦**：
> 当时间变为连续时，未来的状态 $x_{t+dt}$ 会是一个随机微分方程（包含布朗运动 $dW$）。对包含布朗运动的函数求极限，传统的牛顿微积分完全失效！我们必须引入伊藤引理。很多教材在这里会直接写出结果，导致初学者产生严重的“知识断层”。本卡片将一步一步，填平这个鸿沟。

---

## 2. 定理陈述与证明重建

### 1. 定理陈述 (HJB 方程)
如果状态变量 $X_t$ 遵循随机微分方程 (SDE)：
$$ dX_t = \mu(X_t, u_t, t)dt + \sigma(X_t, u_t, t)dW_t $$
并且动态规划原理成立、控制过程可容许、系数满足保证问题良定义的条件，且值函数具有经典解所需的 $C^{1,2}$ 光滑性，那么 $V(x,t)$ 满足以下 HJB 方程（还需配合具体问题的终端/边界条件）：
$$ - \frac{\partial V}{\partial t} = \max_{u} \left\{ U(x, u, t) + \frac{\partial V}{\partial x}\mu + \frac{1}{2}\frac{\partial^2 V}{\partial x^2}\sigma^2 \right\} $$

> [!warning] 正则性边界
> 值函数不一定可微，因此“必定存在经典光滑解”是错误的。更一般的随机控制问题通常把值函数解释为 HJB 方程的**黏性解**；本卡后面的计算是在 $V\in C^{1,2}$ 等条件下进行的形式推导。

### 2. 经典光滑情形的推导主线（不跳步版）

#### **第 1 步：写出极小时间间隔的贝尔曼方程**
考虑从时刻 $t$ 到 $t+dt$。你在这个极小的瞬间获得了效用 $U(x,u,t)dt$。你的状态变为了 $X_{t+dt}$，并将在未来产生价值 $V(X_{t+dt}, t+dt)$。
根据贝尔曼最优化原理：
$$ V(x,t) = \max_u \left\{ U(x,u,t) dt + \mathbb{E} \left[ V(X_{t+dt}, t+dt) \right] \right\} $$

#### **第 2 步：伊藤泰勒展开（填平知识断层的关键）**
现在，我们需要知道 $V(X_{t+dt}, t+dt)$ 到底等于什么。
由于 $dt$ 极小，我们可以用泰勒展开。**注意，由于 $X$ 包含布朗运动，我们必须展开到二阶（因为 $dW^2 = dt$）！**
$$ V(X_{t+dt}, t+dt) - V(x,t) = dV $$
根据伊藤引理展开 $dV$：
$$ dV = \frac{\partial V}{\partial t}dt + \frac{\partial V}{\partial x}dX + \frac{1}{2}\frac{\partial^2 V}{\partial x^2}(dX)^2 $$
把 $dX = \mu dt + \sigma dW$ 代入进去，重点计算 $(dX)^2$：
$$ (dX)^2 = (\mu dt + \sigma dW)^2 = \mu^2 (dt)^2 + 2\mu\sigma(dt)(dW) + \sigma^2 (dW)^2 $$
根据二次变差法则，$(dt)^2 \to 0$，$dt \cdot dW \to 0$，**而 $(dW)^2 = dt$**。因此：
$$ (dX)^2 = \sigma^2 dt $$
代回 $dV$ 的表达式：
$$ dV = \frac{\partial V}{\partial t}dt + \frac{\partial V}{\partial x}(\mu dt + \sigma dW) + \frac{1}{2}\frac{\partial^2 V}{\partial x^2}\sigma^2 dt $$

#### **第 3 步：取期望值消除布朗运动**
在第 1 步中，我们需要的是 $\mathbb{E}[dV]$。
由于布朗运动的增量 $dW$ 期望为 0，即 $\mathbb{E}[dW] = 0$，所以带 $dW$ 的项全被消掉了！
$$ \mathbb{E}[dV] = \left( \frac{\partial V}{\partial t} + \mu\frac{\partial V}{\partial x} + \frac{1}{2}\sigma^2\frac{\partial^2 V}{\partial x^2} \right) dt $$

#### **第 4 步：代回原方程，约掉 dt**
将 $\mathbb{E}[V(X_{t+dt}, t+dt)] = V(x,t) + \mathbb{E}[dV]$ 代回第 1 步：
$$ V(x,t) = \max_u \left\{ U dt + V(x,t) + \left( \frac{\partial V}{\partial t} + \mu\frac{\partial V}{\partial x} + \frac{1}{2}\sigma^2\frac{\partial^2 V}{\partial x^2} \right) dt \right\} $$
等式两边的 $V(x,t)$ 抵消：
$$ 0 = \max_u \left\{ U dt + \left( \frac{\partial V}{\partial t} + \mu\frac{\partial V}{\partial x} + \frac{1}{2}\sigma^2\frac{\partial^2 V}{\partial x^2} \right) dt \right\} $$
两边同时除以 $dt$：
$$ 0 = \max_u \left\{ U + \frac{\partial V}{\partial t} + \mu\frac{\partial V}{\partial x} + \frac{1}{2}\sigma^2\frac{\partial^2 V}{\partial x^2} \right\} $$
因为偏导数 $V_t$ 已经是给定的，不随控制变量 $u$ 改变，可以提到 max 外面，移项整理得到最终的 HJB 方程：
$$ - \frac{\partial V}{\partial t} = \max_u \left\{ U + \frac{\partial V}{\partial x}\mu + \frac{1}{2}\frac{\partial^2 V}{\partial x^2}\sigma^2 \right\} $$
推导完毕！

---

## 3. 直觉解读 HJB 的物理意义

不要被一堆偏导数吓倒，这个方程的右侧由三个极具物理意义的项组成：
1. $U$：**即时利益**（眼前的苟且）。
2. $\frac{\partial V}{\partial x}\mu$：**确定性漂移带来的未来价值**（诗和远方）。$\frac{\partial V}{\partial x}$ 是状态的边际价值，$\mu$ 是状态的变化速度。
3. $\frac{1}{2}\frac{\partial^2 V}{\partial x^2}\sigma^2$：**波动性带来的凸性惩罚（或奖励）**。这是最量化金融的一项！体现了风险（波动率 $\sigma$）对总价值的影响。如果你是一个厌恶风险的人，你的 $V$ 是凹函数，二阶导小于 0，波动率越大，你扣的分越多。

---

## 4. 闭卷验收（数学模式）

- [ ] 1. 为什么在展开 $dV$ 的时候，必须展开到二阶，而一阶不够？（提示：布朗运动的二次变差）
- [ ] 2. 在推导中，$dW$ 项是怎么消失的？
- [ ] 3. 独立默写从离散极限到 HJB 偏微分方程的完整四步推导。
- [ ] 4. 解释 HJB 方程等号右侧三项各自的经济学直觉。

## 🧪 学完本节后可完成的作业

- **可完成**：[[03-Projects/金融与时序/03-量化金融/阶段作业/量化金融-阶段作业-04-金融交易环境与PPO|金融交易环境与PPO]]。
- **为什么现在能做**：本卡已经提供该任务需要的定义、公式、条件或实现边界；若任务还依赖后续知识，先完成对应阶段 MOC 中排在本卡之后的知识卡。
- **提交产物**：闭卷定义/推导、一个可复查计算或代码结果、一个失败案例，以及对适用边界的说明。
