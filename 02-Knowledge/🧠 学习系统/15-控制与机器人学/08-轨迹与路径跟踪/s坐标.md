---
title: "s坐标"
type: concept
course: "15-控制与机器人学"
stage_moc: "[[🧭 阶段8-轨迹与路径跟踪]]"
flow: knowledge
kind: concept
importance: "A"
status: completed
created: 2026-08-07
updated: 2026-08-07
tags: [学习, 控制与机器人学, Frenet]
upstream:
  - "[[参考线]]"
concept: ["弧长", "纵向坐标"]
prerequisites: ["参考线"]
related: ["d坐标", "Frenet转换", "Frenet纵向"]
---

# s坐标

> **一句话**:$s$ 是沿参考线走过的弧长——Frenet 系里的"纵向位置",相当于高速公路上的里程桩。

## 定义

$s$ = 参考线上从起点到投影点的弧长:

$$s(p) = \int_0^{s^*} \|\mathbf{r}'(u)\| du$$

其中 $s^*$ 是点 $p$ 在参考线上**最近投影点**的弧长参数。

## 性质

| 性质 | 说明 |
|:---|:---|
| 一维单调 | $s \in [0, L]$,沿前进方向递增 |
| 长度单位(m) | 直接对应行驶距离 |
| 由投影决定 | $s$ 由最近点投影给出(见[[Frenet转换]]) |

## 纵向运动学

$s$ 对时间求导得纵向运动:

- 纵向速度:$\dot{s}$(≈ 车速沿参考线分量)
- 纵向加速度:$\ddot{s}$
- 纵向 jerk:$\dddot{s}$

轨迹规划在 $(s, \dot{s}, \ddot{s})$ 上做一维规划(见[[Frenet纵向]])。

## 为什么用 s

- 一维化:纵横向解耦,各做一维规划(见[[Frenet耦合]])
- 直观:车距、停车点、限速区间都用 $s$ 表达
- 计算:积分/采样都沿 $s$ 均匀进行

## 典型应用

| 场景 | s 的用法 |
|:---|:---|
| ACC 跟车 | 前车在 $s_f$,$s_f - s$ = 车间距 |
| 停车 | 停止线在 $s_{stop}$,规划 $s(t) \to s_{stop}$ |
| 限速 | $v_{limit}(s)$ 分段函数 |
| 交通灯 | 时间对齐 $t_{arrive}$ 对应 $s_{stop}$ |

## 自检

- [ ] s 坐标如何由平面点计算?
- [ ] 纵向速度为什么是 $\dot{s}$?
- [ ] 车间距在 Frenet 系如何表达?
