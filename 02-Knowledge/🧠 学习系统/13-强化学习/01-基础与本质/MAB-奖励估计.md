---
type: study
topic: "MAB-奖励估计"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段1-基础与本质]]"
flow: knowledge
kind: concept
difficulty: beginner
concept: ["奖励估计", "增量更新"]
upstream: ["[[多臂老虎机与探索-利用]]", "[[概率论基础]]"]
tags: [学习, 强化学习]
---

# MAB-奖励估计

> 所属模块：[[🧭 阶段1-基础与本质]] · 主线：多臂老虎机
> 前置：[[多臂老虎机与探索-利用]] · [[概率论基础]]

## 动机

要决定"利用哪根臂"，先得估准每根臂的价值。这是所有 bandit 算法的共同第一步。

## 正式定义 / 公式

- **样本均值** $\hat Q_t(a)=\frac{1}{N_t(a)}\sum_{i=1}^{t-1} R_i\mathbf{1}_{A_i=a}$。
- **增量更新**（省内存）：$\hat Q_{t+1}(a)=\hat Q_t(a)+\frac{1}{N_t(a)}\big(R_t-\hat Q_t(a)\big)$。
- 由大数定律，当 $N_t(a)\to\infty$ 时 $\hat Q_t(a)\to q_*(a)$。

## 最小手算例子

臂 1 前 3 次奖励 1,0,1：$N=3,\hat Q=2/3$。第 4 次得 1，则 $\hat Q\leftarrow 2/3+(1/3)(1-2/3)=3/4$。

## 对比与常见错误

- **初值偏差**：未拉过的臂 $N=0$ 无法除，需给初始乐观值或单独处理。
- **忘记增量更新**：暴力重算均值在大 $t$ 下低效。

## 闭卷自测
- 写出增量更新式并说明为何等价样本均值。
- $N_t(a)=0$ 时 $\hat Q_t(a)$ 怎么处理？

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
