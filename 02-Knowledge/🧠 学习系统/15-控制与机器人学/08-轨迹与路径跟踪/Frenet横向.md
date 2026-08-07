---
title: "Frenet横向"
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
  - "[[d坐标]]"
concept: ["横向运动", "横向多项式"]
prerequisites: ["d坐标", "Frenet转换"]
related: ["横向多项式", "横向边界条件", "Frenet纵向"]
---

# Frenet横向

> **一句话**:横向运动就是描述 $d$ 如何变化——车道保持(不动)与换道(平滑过渡)是两个典型模式。

## 横向状态

$$[d(t),\; \dot{d}(t),\; \ddot{d}(t)]$$

- $d$:横向偏移
- $\dot{d}$:横向速度
- $\ddot{d}$:横向加速度

## 横向规划模式

### 1. 车道保持
$$d(t) \equiv d_{ref}(\text{车道中心或当前值}), \quad \dot d = \ddot d = 0$$

### 2. 换道(横向多项式)
用五阶多项式连接当前横向状态与目标横向状态(见[[横向多项式]]):

$$d(t) = a_0 + a_1 t + \cdots + a_5 t^5$$

边界:$(d_0, \dot d_0, \ddot d_0) \to (d_f, 0, 0)$,换道宽度 $\Delta d = d_f - d_0$。

### 3. 避障偏移
临时偏出当前车道再回来(见[[横向避障]])。

## 横向代价与约束

- 最小 jerk:$J = \int \dddot{d}^2 dt$(舒适,见[[横向优化]])
- 车道边界:$d_{min} \le d \le d_{max}$
- 横向加速度:$|\ddot d| \le a_{lat,max}$

## 横向 vs 转向

注意:**横向运动 $d$ 不是直接转向角**。$d$ 通过曲率/航向与转向相关:

$$\kappa \approx \frac{d''}{(1-\kappa_r d)^2} + \kappa_r, \quad \delta = \arctan(L\kappa)$$

横向规划 → 曲率 → 转向角(见[[曲率约束]])。

## 自检

- [ ] 横向状态三量是什么?
- [ ] 换道横向轨迹用什么函数形式?
- [ ] 横向 $d$ 如何转化为转向指令?
