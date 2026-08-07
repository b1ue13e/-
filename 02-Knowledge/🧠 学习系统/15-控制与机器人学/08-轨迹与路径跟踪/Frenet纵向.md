---
title: "Frenet纵向"
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
  - "[[s坐标]]"
concept: ["纵向运动", "s-sdot-ssdot"]
prerequisites: ["s坐标", "Frenet转换"]
related: ["Frenet横向", "Frenet耦合", "速度分配"]
---

# Frenet纵向

> **一句话**:Frenet 系把纵向运动抽成单自由度 $s(t)$——一维规划,跟车/停车/限速都在这条轴上解决。

## 纵向状态

$$[s(t),\; \dot{s}(t),\; \ddot{s}(t)]$$

- $\dot{s}$:纵向速度(沿参考线分量)
- $\ddot{s}$:纵向加速度
- 纵向 jerk:$\dddot{s}$(舒适性,见[[jerk约束]])

## 一维轨迹规划

纵向规划 = 给定边界状态,生成 $s(t)$ 曲线:

### 1. 多项式法(五阶)
$$s(t) = a_0 + a_1 t + a_2 t^2 + a_3 t^3 + a_4 t^4 + a_5 t^5$$

6 个系数由 6 个边界条件确定:$(s_0,\dot{s}_0,\ddot{s}_0)$ 和 $(s_f,\dot{s}_f,\ddot{s}_f)$。五阶保证加速度连续(最小 jerk 思路)。

### 2. 速度曲线法
设计 $\dot{s}(t)$ 剖面(梯形/S 曲线,见[[速度分配]]),积分得 $s(t)$。

## 典型纵向场景

| 场景 | 目标 | 约束 |
|:---|:---|:---|
| 巡航 | $\dot{s} \to v_{set}$ | 加速度/jerk |
| 跟车 | $s_{gap}(t)$ 安全 | 前车位置(见[[纵向跟车]]) |
| 停车 | $s(t) \to s_{stop}$ | 终点速度 0(见[[纵向停车]]) |
| 限速 | $\dot{s} \le v_{limit}(s)$ | 曲率/交通限速 |

## 与横向的关系

严格说纵横向有耦合(见[[Frenet耦合]]),但工程上先解耦:

- 纵向:规划 $s(t)$
- 横向:规划 $d(s)$ 或 $d(t)$
- 再统一合成轨迹并做可行性检查

## 自检

- [ ] 纵向状态由哪三个量描述?
- [ ] 五阶多项式为何常用于纵向规划?
- [ ] 跟车场景的纵向目标是什么?
