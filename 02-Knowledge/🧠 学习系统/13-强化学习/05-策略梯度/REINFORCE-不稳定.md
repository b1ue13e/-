---
type: study
topic: "REINFORCE-不稳定"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段5-策略梯度]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["REINFORCE-不稳定", "REINFORCE 训练不稳定"]
upstream: ["[[REINFORCE-高方差]]"]
tags: [学习, 强化学习]
---

# REINFORCE-不稳定

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段5-策略梯度|返回阶段页]]

## 动机
高方差进一步导致训练不稳定：策略可能剧烈震荡、甚至崩溃（概率塌缩到某动作后难恢复）。

## 正式定义 / 公式
因 ∇log π 在概率趋 0 或 1 时幅值变大，一次坏更新可把策略推入"概率塌缩"区域，后续难采样到其它动作。

## 最小手算例子
若 θ 把 π(a2) 推到≈0，则 a2 几乎不再被采样，即便它其实更好也无法被纠正——探索失效。

## 对比与常见错误
- 与信任域方法：TRPO/PPO 用 KL 约束限制单步更新幅度，专治不稳定（见阶段6/7）。
- 常见错误：把不稳定只怪"学习率"——根因是梯度噪声 + 无约束更新。

## 闭卷自测
1. 高方差如何导致训练不稳定？
2. 哪类方法从机制上缓解？
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
