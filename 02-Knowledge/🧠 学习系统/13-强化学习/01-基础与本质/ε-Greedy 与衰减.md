---
type: study
topic: "ε-Greedy 与衰减"
course: "强化学习"
created: 2026-08-07
status: completed
stage_moc: "[[🧭 阶段1-基础与本质]]"
flow: knowledge
kind: concept
difficulty: beginner
concept: ["ε-greedy 选择规则", "ε 衰减调度", "探索-利用落地"]
upstream: ["[[探索与利用]]"]
tags: [学习, 强化学习]
---

# ε-Greedy 与衰减

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段1-基础与本质|返回阶段页]]

## 动机
最朴素也最常用的探索策略：以概率 $\varepsilon$ 随机、其余贪心。它是理解"探索如何落地"的入口；但固定 $\varepsilon$ 在训练后期仍浪费探索，于是有了**衰减**——让 Agent "先广撒网、后精耕"。

## 正式定义 / 公式

### 1. ε-Greedy 选择规则
每一步：以 $\varepsilon$ 均匀随机选动作；以 $1-\varepsilon$ 选当前估值最高 $\arg\max_a \hat Q(a)$。期望每步以 $\varepsilon$ 概率在"探索"。

### 2. ε 衰减调度
固定 $\varepsilon$ 在训练后期仍过度探索、遗憾线性增长，故引入衰减：
$$
\varepsilon_t=\max(\varepsilon_{\min},\ \varepsilon_0\cdot \gamma^t)\quad\text{或}\quad \varepsilon_t=\frac{\varepsilon_0}{1+kt}
$$
早期高 $\varepsilon$ 充分探索，后期趋近于 $\varepsilon_{\min}$ 专注利用。**衰减应作用于同一个 $\varepsilon$ 参数**。

## 最小手算例子
- **ε-greedy**：$\varepsilon=0.1$ → 90% 时间拉已知最好臂，10% 时间随便试一台，避免错过更好的。
- **衰减**：$\varepsilon_0=1.0,\ \gamma=0.99$ → 第 1 步全随机，第 100 步约 $0.37$，第 500 步约 $0.0066$，基本只利用。
- **遗憾量级**：固定 $\varepsilon$ 的累计遗憾为 $O(T)$（线性）；衰减后可显著改善（与 UCB/TS 的次线性遗憾对比见「多臂老虎机算法」）。

## 对比与常见错误
- **$\varepsilon$ 太大**：几乎纯随机，学得太慢；**$\varepsilon$ 太小**：陷在次优臂（贪心陷阱）；**固定 $\varepsilon$ 不衰减**：后期仍过度探索，遗憾线性增长。
- **衰减过快**：还没探索够就几乎不试，错过最优臂；**衰减过慢**：后期仍在随机，方差大、难收敛。
- **与乐观初始化混淆**：$\varepsilon$-greedy 靠随机探索；乐观初值靠"先当最好"驱动探索，二者可叠加但概念不同。

## 闭卷自测
1. 写出 $\varepsilon$-greedy 的选择规则；为何固定 $\varepsilon$ 的累计遗憾是 $O(T)$ 而非次线性？
2. 给出两种常见 $\varepsilon$ 衰减公式；衰减过快的主要风险？

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
