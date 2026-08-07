---
type: study
topic: "UCB算法"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段1-基础与本质]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["UCB", "置信上界"]
upstream: ["[[探索与利用]]", "[[概率论基础]]"]
tags: [学习, 强化学习]
---

# UCB算法

> 所属模块：[[🧭 阶段1-基础与本质]] · 主线：探索策略
> 前置：[[探索与利用]] · [[概率论基础]]

## 动机

$\varepsilon$-greedy 均匀随机探索，效率低。UCB（Upper Confidence Bound）按"不确定性"定向探索：越不确定的臂越值得试。

## 正式定义 / 公式

$$A_t=\arg\max_a\left[\hat Q_t(a)+\sqrt{\frac{2\ln t}{N_t(a)}}\right]$$

- $\hat Q_t(a)$：利用项（已知价值）。
- $\sqrt{2\ln t/N_t(a)}$：探索项，随 $N_t(a)$ 增大而减小（试得多就不必再试）。
- 由 Hoeffding 不等式可证遗憾 $O(\sqrt{kt\ln t})$（次线性）。

## 最小手算例子

臂 A 试 100 次、臂 B 试 2 次：即使 $\hat Q(A)>\hat Q(B)$，B 的探索项很大，仍会被选中。

## 对比与常见错误

- **未拉过的臂** $N=0$ 时分母为 0，需先每臂试一次（oracle 初始化）。
- **与 $\varepsilon$-greedy 混为一谈**：UCB 是确定性、不确定性驱动的。

## 闭卷自测
- 写出 UCB 选择式并解释两项含义。
- 为何 UCB 的 regret 是次线性的？

## 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 相关下游知识

```dataview
LIST
FROM "02-Knowledge/🧠 学习系统"
WHERE contains(upstream, this.file.link)
SORT file.name ASC
```
