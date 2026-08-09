---
title: "A3C 算法（异步优势 Actor-Critic）"
type: study
topic: "A3C 算法"
course: "强化学习"
created: 2026-08-07
status: learning
stage_moc: "[[🧭 阶段6-Actor-Critic]]"
flow: knowledge
kind: concept
upstream: ["[[Actor-Critic架构]]", "[[Actor网络]]", "[[Critic网络]]", "[[优势估计]]", "[[A2C算法]]"]
tags: [学习, 强化学习, A3C, Actor-Critic]
---
> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段6-Actor-Critic|返回阶段页]]

# A3C 算法 (Asynchronous Advantage Actor-Critic，异步优势 Actor-Critic)

---

## 0. 学习边界

- **类别**：**A 类（核心概念，必须深挖）**
- **判断理由**：A3C 开创"多 worker 异步更新"，是不依赖经验回放的 on-policy 并行范式代表；理解它的全局/局部网络、异步无锁更新与"并行去相关"是看懂现代并行 AC 的前提。

---

## 1. A3C 家族定位

A3C（Asynchronous Advantage Actor-Critic）是 Actor-Critic 的**异步并行**版，开创"多 worker 异步更新"。

- 多个 worker 异步地与全局网络交互、异步地用各自梯度更新全局参数（无锁）。
- 每个 worker 有局部网络，定期与全局同步。

**最小手算例子**：4 worker 各自独立跑环境，算出梯度后直接异步推给全局网络，互不等待。

- **与 A2C 对比**：A3C 异步、无 barrier；A2C 同步批量。
- **常见错误**：以为 A3C"更快一定更好"——异步有陈旧梯度，且 GPU 利用差。

---

## 2. 全局网络与局部网络

A3C 的中心是"全局网络"，所有 worker 围绕它读写参数。

- 全局网络 $\theta_g,\phi_g$ 存最新参数；worker $i$ 拷贝到局部 $(\theta_i,\phi_i)$，交互算梯度后异步更新全局。
- 局部网络仅用于本 worker 推演。

**最小手算例子**：worker 1 拉取全局参数→跑 20 步→算梯度→异步写回全局；worker 2 同时进行。

- **与同步 A2C**：无中心 barrier，worker 各自为政。
- **常见错误**：把全局网络当"会等待"——A3C 故意不等待。

---

## 3. 异步无锁更新

A3C 的"异步"是性能关键：worker 不互相等待，异步推梯度（如 Hogwild 式无锁更新）。不同 worker 用"略旧"参数，梯度天然带多样性。

> worker 算完梯度立即异步应用到全局；时间错开，参数持续被多 worker 扰动。

**最小手算例子**：worker 1 在 $t$ 时刻更新全局；worker 2 在 $t+\varepsilon$ 用更新后的全局参数继续——时间错开。

- **与同步对比**：异步省等待但梯度可能陈旧（stale）。
- **常见错误**：以为异步"白赚速度无代价"——陈旧梯度可能降收敛质量。

---

## 4. 并行去相关（为何不用经验回放）

多个并行 worker 在不同状态起步、各跑一段，样本天然去相关——这是 A3C 不依赖经验回放的原因。

> 并行 $n$ 个独立环境，样本来自不同轨迹的不同段，相关性远低于单环境连续样本；故无需 DQN 式经验回放来打破相关。

**最小手算例子**：4 worker 在 4 个不同状态各跑 20 步，合并的 80 样本彼此分散，近似独立。

- **与 DQN 经验回放**：A3C 用"并行去相关"替代"缓冲回放"。
- **常见错误**：在 A3C 里硬加经验回放——多此一举，并行已去相关。

---

## 5. 无经验回放（A3C-无ER）

正因为并行去相关，A3C 通常不使用经验回放缓冲。

- A3C 直接在线用并行 worker 的最新样本更新，省去 DQN 的 replay buffer 与采样（对比 [[DQN-经验回放]]：那是 off-policy Q-learning 的需求）。

**最小手算例子**：16 worker 各跑 $N=20$ 步 ⇒ 每轮约 320 步经验，无共享 replay buffer；worker 边采边更新，无环形缓冲，样本寿命 = 当前一步。

- **与 DQN 对比**：DQN 需回放（off-policy、相关样本）；A3C 在线、并行已去相关。
- **常见错误**：把"无 ER"当成缺陷——对 on-policy AC 是合理简化。

---

## 6. 合并要点

| 维度 | 要点 |
| :--- | :--- |
| 全局/局部 | worker 拷全局参数，算梯度异步写回 |
| 异步 | 无锁、无 barrier，省等待但有陈旧梯度 |
| 去相关 | 多环境并行替代经验回放 |
| 误区 | 异步≠无代价；无 ER 是简化非缺陷 |

---

## 闭卷自测
1. A3C 是什么？与 A2C 的核心差异？
2. 全局网络与局部网络各做什么？
3. A3C 异步更新如何工作？异步的代价？
4. 为何 A3C 不用经验回放？这相对 DQN 是简化还是缺陷？

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
