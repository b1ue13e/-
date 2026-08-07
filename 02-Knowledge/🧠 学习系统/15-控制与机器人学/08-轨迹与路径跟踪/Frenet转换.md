---
title: "Frenet转换"
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
  - "[[s坐标]]"
  - "[[d坐标]]"
concept: ["坐标变换", "最近点投影"]
prerequisites: ["参考线", "s坐标", "d坐标"]
related: ["Frenet横向", "Frenet纵向", "Frenet误差"]
---

# Frenet转换

> **一句话**:笛卡尔坐标 $(x,y)$ 与 Frenet 坐标 $(s,d)$ 互转,核心是"找最近投影点"。

## 笛卡尔 → Frenet(正变换)

**第 1 步:找投影点**。求解最近点:

$$s^* = \arg\min_s \|\mathbf{p} - \mathbf{r}(s)\|$$

工程上:离散搜索 + 牛顿迭代精化。

**第 2 步:算横向偏差**:

$$d = (\mathbf{p} - \mathbf{r}(s^*)) \cdot \mathbf{n}(s^*)$$

**第 3 步:纵向速度分解**(需要 $\dot{s}, \dot{d}$):

$$\dot{s} = \frac{v\cos(\theta - \theta_r)}{1 - \kappa_r d}, \qquad \dot{d} = v\sin(\theta - \theta_r)$$

其中 $\theta$:车航向,$\theta_r$:参考线切线角。

## Frenet → 笛卡尔(逆变换)

$$\mathbf{p} = \mathbf{r}(s) + d\,\mathbf{n}(s)$$

航向与曲率修正:

$$\theta = \theta_r + \arctan\left( \frac{\dot{d}}{\dot{s}} \right)$$

$$\kappa = \frac{\kappa_r + \frac{d''}{(1-\kappa_r d)^2}}{\sqrt{1+(d'/\dot{s})^2}} \cdot \text{修正}$$

## 关键公式:高阶量换算

给定 $d, d', d''$(对 $s$ 的导数)与参考线 $\kappa_r$:

$$\dot{d} = d' \dot{s}, \qquad \ddot{d} = d'' \dot{s}^2 + d' \ddot{s}$$

$$v = \sqrt{\dot{s}^2 + \dot{d}^2}$$

## 奇异点

- $1 - \kappa_r d = 0$:点在参考线曲率圆心 → 转换发散(远离参考线时易发生)
- 投影不唯一:参考线曲率大或点距参考线远时,多个局部最近点

## 自检

- [ ] 正变换的关键步骤是什么?
- [ ] 奇异条件 $1-\kappa_r d=0$ 何时出现?
- [ ] 如何从 $(s,d)$ 恢复笛卡尔坐标?
