---
type: study
topic: "LinUCB算法"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段1-基础与本质]]"
flow: knowledge
kind: concept
difficulty: advanced
concept: ["LinUCB", "上下文老虎机"]
upstream: ["[[UCB算法]]", "[[上下文老虎机]]"]
tags: [学习, 强化学习]
---

# LinUCB算法

> 所属模块：[[🧭 阶段1-基础与本质]] · 主线：多臂老虎机
> 前置：[[UCB算法]] · [[上下文老虎机]]

## 动机

LinUCB 是上下文老虎机的线性 + UCB 解法：用特征建模奖励，并用置信上界做探索，是工业推荐的主流基线。

## 正式定义 / 公式

对臂 $a$，维护 $A_a=\lambda I+D_a^\top D_a,\,\hat\theta_a=A_a^{-1}D_a^\top c_a$。每步选
$$a_t=\arg\max_a\left(x_t^\top\hat\theta_a+\alpha\sqrt{x_t^\top A_a^{-1}x_t}\right)$$
其中第二项是对 $x_t$ 估计不确定性的 UCB 余量。

## 最小手算例子

用户特征 5 维，10 篇文章为臂；每步算 10 个 UCB 得分取最大，点完后用 (特征, 奖励) 更新该臂 $A,\hat\theta$。

## 对比与常见错误

- **$\alpha$ 过大/过小**：过大过度探索，过小欠探索。
- **未加正则 $\lambda$**：$A_a$ 可能奇异。
- **特征未归一化**：置信项尺度失衡。

## 闭卷自测
- 写出 LinUCB 的选择式并说明两项含义。
- 为何要维护 $A_a^{-1}$ 而非只存 $\hat\theta$？

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
