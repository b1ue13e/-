---
type: study
topic: "TD0对比"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段4-Q-Learning]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["TD0对比", "TD(0) vs MC vs DP"]
upstream: ["[[MC方法]]", "[[DP方法]]", "[[TD-0]]"]
tags: [学习, 强化学习]
---

# TD0对比

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段4-Q-Learning|返回阶段页]]

## 动机
TD、MC、DP 都是估计价值函数的方法，区别在"是否采样"与"是否自举"。一张表理清。

## 正式定义 / 公式
| 方法 | 采样（不需模型） | 自举（不需幕末） |
| MC   | ✓ | ✗ |
| TD   | ✓ | ✓ |
| DP   | ✗ | ✓ |

- MC：无偏、高方差、需幕末、可模型无关。
- TD：有偏、低方差、可在线、可模型无关。
- DP：需已知模型、离线、确定收敛。

## 最小手算例子
同一 2 状态链：MC 等幕结束用 G_t=1 更新 V(s1)；TD(0) 一步就用 r+γV(s2)=1 更新；DP 用已知 P 解贝尔曼方程得 V(s1)=1。三者最终都收敛到同一 V。

## 对比与常见错误
- 常见错误：认为 TD "一定比 MC 好"——在短幕、低噪声时 MC 也无妨；TD 优势在长幕/在线。

## 闭卷自测
1. 用一张表说明 MC/TD/DP 在采样与自举上的异同。
2. 何时 MC 与 TD 更新目标不同？
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
