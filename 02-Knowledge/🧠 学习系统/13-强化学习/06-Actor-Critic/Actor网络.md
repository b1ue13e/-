---
title: "Actor 网络（策略网络）"
type: study
topic: "Actor 网络"
course: "强化学习"
created: 2026-08-07
status: learning
stage_moc: "[[🧭 阶段6-Actor-Critic]]"
flow: knowledge
kind: concept
upstream: ["[[Actor-Critic架构]]", "[[策略梯度]]", "[[优势估计]]"]
tags: [学习, 强化学习, Actor-Critic, 策略网络]
---
> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段6-Actor-Critic|返回阶段页]]

# Actor 网络 (Actor Network / 策略网络)

---

## 0. 学习边界

- **类别**：**A 类（核心概念，必须深挖）**
- **判断理由**：Actor 是 Actor-Critic 框架中"出动作、被优化"的那一半；不理解它的结构、输出、更新，就无法写出任何 AC 算法的训练循环（A2C/A3C/PPO/TRPO 共用同一套 Actor 机制）。

---

## 1. Actor 的职责是什么？

Actor-Critic 把"策略"与"价值"拆成两个角色。**Actor 就是策略网络**，负责输出动作分布并执行探索，再用 Critic 给的"优势 A"做策略梯度更新：

$$\nabla_\theta J \approx \mathbb{E}\big[\nabla_\theta \log \pi_\theta(a|s)\cdot A(s,a)\big]$$

相比 REINFORCE 直接用裸回报 $G_t$，Actor 用 Critic 估计的优势 $A$，方差更低、可在线更新。

- **与 Critic 的分工**：Actor 学"做什么"（策略），Critic 学"多好"（价值），二者互相提供信号。
- **常见错误**：让 Actor 用原始 $G_t$ 而非优势——那退回高方差 REINFORCE。

---

## 2. Actor 的网络结构

Actor 通常就是一个神经网络：输入状态、输出动作分布的参数。

- **离散动作空间**：网络输出 logits → softmax 得到 $\pi_\theta(a|s)$。
- **连续动作空间**：网络输出 $(\mu, \log\sigma)$ → 高斯策略 $\pi_\theta(a|s)=\mathcal{N}(\mu,\sigma^2)$。
- 结构即普通策略网络（与「参数化-神经网络」同族）；可以与 Critic 共享底层特征，也可完全独立。

**最小手算例子**：CartPole 中 Actor 为 2 层 MLP，输入 4 维状态，输出 2 维 logits（对应左/右）。

- **常见错误**：Actor 与 Critic 共享底层却未小心初始化——可能互相拖累，需权衡共享与否。

---

## 3. Actor 的输出层与动作采样

输出层决定动作如何被采样，是 Actor 与环境的接口。

- **离散**：softmax(logits) → 按概率采样动作。
- **连续**：从 $\mathcal{N}(\mu,\sigma)$ 采样（reparameterization：$a=\mu+\sigma\cdot\varepsilon$）。
- 输出经采样得到实际执行的 $a$。

**最小手算例子**：logits = $(2, 0)$ → $\pi \approx (0.88, 0.12)$；训练时大概率取 $a_1$，但**仍按分布采样**以保持可微与探索。

- **常见错误**：训练阶段也用 argmax——会丢失探索且堵死可微链路（见「参数化-连续」）。

---

## 4. Actor 的策略梯度更新

把 Critic 的优势接到策略梯度上，得到 Actor 的实际更新：

$$\theta \leftarrow \theta + \alpha \cdot \nabla_\theta \log \pi_\theta(a|s)\cdot A(s,a)$$

$A$ 常取 TD 形式 $A\approx r+\gamma V(s')-V(s)$（见 [[优势估计]] 与 [[Actor-Critic架构]]）。可加熵项 $-\beta H(\pi)$ 鼓励探索（PPO 中常见）。

- **与 REINFORCE 更新**：仅把 $G_t$ 换成优势 $A$，机制一致，方差更低、可在线。
- **常见错误**：用 Critic 的 $V$ 直接当动作价值——应经 $A=\dots-V$ 转成"相对优势"。

---

## 5. 合并手算示例

场景：$(s,a,r,s')=(s,a_1,+1,s')$，$V(s)=0.4,\ V(s')=0.5,\ \gamma=0.9$。

1. 一步 TD 优势：$A = 1 + 0.9\times 0.5 - 0.4 = 1.05$。
2. Actor 更新方向：$\nabla_\theta \log\pi_\theta(a_1|s)$ 乘以 $1.05$，再乘学习率 $\alpha$ 沿此方向抬升 $\pi(a_1|s)$。
3. 若换动作 $a_2$ 且其优势 $A=-0.2$，则反向压低 $\pi(a_2|s)$。

> 直觉：Actor 只朝"超出平均（A>0）"的方向调整，自然降方差。

---

## 6. 常见误区小结

| 误区 | 正确理解 |
| :--- | :--- |
| 训练用 argmax 取动作 | 训练按分布采样，保探索与可微 |
| 用 $G_t$ 做 Actor 更新 | 用优势 $A$ 替代，降方差、可在线 |
| 把 $V$ 当动作价值 | 经 $A=Q-V$ 转成相对优势再用 |

---

## 闭卷自测
1. Actor-Critic 中 Actor 负责什么？用什么信号更新？
2. 离散与连续动作空间下 Actor 的输出层分别是什么？
3. 为何训练时按分布采样而非 argmax？
4. 写出 Actor 的策略梯度更新式，并说明 $A$ 从哪来。

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
