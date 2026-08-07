---
title: "d坐标"
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
concept: ["横向偏移", "法向坐标"]
prerequisites: ["参考线"]
related: ["s坐标", "Frenet转换", "Frenet横向"]
---

# d坐标

> **一句话**:$d$ 是到参考线的垂直距离(带符号)——Frenet 系里的"横向位置",正值在参考线左侧。

## 定义

$$d = \text{sign}(d) \cdot \|\mathbf{p} - \mathbf{r}(s)\|$$

- $\mathbf{p}$:当前点
- $\mathbf{r}(s)$:投影点
- 符号约定:沿参考线前进方向,**左正右负**(可配置)

## 性质

| 性质 | 说明 |
|:---|:---|
| 有符号距离 | 左正右负(常用约定) |
| 车道内约束 | 车道宽 $W$ → $d \in [-W/2, W/2]$ |
| 由投影给出 | 最近点投影(见[[Frenet转换]]) |

## 横向运动学

- 横向偏移:$\dot{d}$
- 横向加速度:$\ddot{d}$
- 横向 jerk:$\dddot{d}$

## 用途

| 场景 | d 的用法 |
|:---|:---|
| 车道保持 | 控制 $d \to 0$(或车道中心) |
| 换道 | $d$: $0 \to \pm W$(横向多项式,见[[横向多项式]]) |
| 避障 | 障碍物占用 $d$ 区间,避开(见[[横向避障]]) |
| 边界 | 车道边界约束 $d_{min} \le d \le d_{max}$ |

## 直觉

- $d$ 就是"方向盘要不要回正"的依据:车偏左(d>0)就往右修
- 横向控制误差在 Frenet 系里正是 $d_{error}$(见[[Frenet误差]])
- 换道规划本质是设计 $d(s)$ 从当前值平滑过渡到目标车道

## 自检

- [ ] d 的符号约定是什么?
- [ ] 车道保持的参考 d 是多少?
- [ ] 换道时 d 如何变化?
