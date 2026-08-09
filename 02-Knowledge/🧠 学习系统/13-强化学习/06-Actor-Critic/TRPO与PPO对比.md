---
title: "TRPO 与 PPO 对比"
type: study
topic: "TRPO 与 PPO 对比"
course: "强化学习"
created: 2026-08-07
status: learning
stage_moc: "[[🧭 阶段6-Actor-Critic]]"
flow: knowledge
kind: concept
upstream: ["[[TRPO信任域优化]]", "[[Actor-Critic 与 PPO]]", "[[Actor-Critic 与 PPO]]", "[[优势估计]]"]
tags: [学习, 强化学习, TRPO, PPO, 对比]
---
> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段6-Actor-Critic|返回阶段页]]

# TRPO 与 PPO 对比 (TRPO vs PPO)

---

## 0. 学习边界

- **类别**：**A 类（核心概念，必须深挖）**
- **判断理由**：TRPO 与 PPO 是"稳定策略梯度"两条路线；面试与论文高频考点是二者在稳定性、步长控制、实现效率上的权衡，以及"PPO 是 TRPO 的实用近似"这一核心结论。

---

## 1. 稳定性来源对比

TRPO 的稳定性来自信任域约束，这是它相对原始 PG 的最大优势。

> KL 约束限制单步策略突变，避免 [[REINFORCE-不稳定]] 式的崩溃；PPO 的 clip 也提供类似稳定（近似约束）。

**稳定性要点**：二者都比 vanilla 策略梯度稳；TRPO 理论保证单调改进（近似），PPO 实践中同样稳且对超参更鲁棒。长训练里 TRPO/PPO 曲线平滑，原 PG 易震荡。

- **常见错误**：朴素 PG 加小学习率就能等同 TRPO——小 LR 不限分布变化，仍可能塌缩。

---

## 2. 步长控制对比

TRPO 用 KL 阈值 $\delta$ 控制步长，比手动调学习率更稳，但 $\delta$ 本身也要调。

> TRPO 步长≈由 $\delta$ 隐式决定（满足 KL$\le\delta$ 的最大步）；PPO 用 clip 范围 $\varepsilon$ 间接控步长。

**步长要点**：TRPO 用 KL 硬约束 $\mathrm{KL}\le\delta=0.01$ 并线搜保证不越界；PPO 用 $\varepsilon=0.2$ 软裁剪，步长更宽松、实现更简单。$\delta$ 太大→近似失效、不稳定；$\delta$ 太小→学习慢。

- **常见错误**：以为 TRPO"不用调步长"——$\delta$ 就是它的步长超参。

---

## 3. 计算效率对比

从计算效率看，TRPO 的 CG/线搜比 PPO 的 clip 更贵。

> TRPO 每步多次前向/反向估 Fisher 与 KL，单步成本高；PPO 复用普通梯度+裁剪成批更新，吞吐更高。

**效率要点**：TRPO 每轮需采足量 on-policy 数据（如 2048 步）且多次 CG 迭代；PPO 复用 $K=4\text{–}10$ 轮更省。同预算下 PPO 通常快 1–3×。同硬件下 PPO 每秒更新步数常高于 TRPO。

- **常见错误**：认为"复杂=效果好"——效率与最终性能需权衡。

---

## 4. 实现复杂度对比

TRPO 理论上漂亮，但工程复杂（CG+线搜+KL 计算）。这是它被 PPO 取代的主因之一。

> TRPO 每次更新需：估计 Fisher-vector 积、CG 迭代、KL 线搜；PPO 仅用裁剪（clip）即近似同等效果，代码量小很多。

**复杂度要点**：同样 AC 框架，TRPO 需额外 ~50 行 CG/线搜逻辑；PPO 几行 clip 即可。

- **常见错误**：为"理论优雅"硬上 TRPO——多数场景 PPO 性价比更高。

---

## 5. 综合对比表

| 维度 | TRPO | PPO |
| :--- | :--- | :--- |
| 稳定机制 | KL 硬约束 | clip 软约束（近似 KL） |
| 步长控制 | $\delta$（KL 阈值） | $\varepsilon$（裁剪范围） |
| 单步成本 | 高（CG+线搜） | 低（普通梯度+裁剪） |
| 理论保证 | 单调改进（近似） | 无严格单调，但实践中稳 |
| 实现量 | 大 | 小 |
| 默认地位 | 理论基准 | 工程默认 |

> 核心结论：**PPO 是 TRPO 的实用近似**——用裁剪替代 KL 约束，省去 CG/线搜，效果相近而实现简单。

---

## 闭卷自测
1. TRPO 的稳定性来源？小学习率能否替代信任域？
2. TRPO 如何控制步长？$\delta$ 过大/过小的影响？
3. TRPO 与 PPO 在计算效率上差异？如何权衡选哪个？
4. TRPO 的实现复杂度在哪？为何 PPO 更流行？

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
