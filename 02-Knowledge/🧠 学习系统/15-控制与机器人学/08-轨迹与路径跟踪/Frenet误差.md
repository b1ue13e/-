---
title: "Frenet误差"
type: concept
course: "15-控制与机器人学"
stage_moc: "[[🧭 阶段8-轨迹与路径跟踪]]"
flow: knowledge
kind: concept
importance: "A"
status: completed
created: 2026-08-07
updated: 2026-08-07
tags: [学习, 控制与机器人学, 轨迹跟踪]
upstream:
  - "[[Frenet转换]]"
concept: ["跟踪误差", "横纵向误差"]
prerequisites: ["Frenet转换"]
related: ["解耦控制", "横向偏差", "间距误差"]
---

# Frenet误差

> **一句话**:在 Frenet 系里定义跟踪误差——横向误差 $d_{error}$ 喂给方向盘,纵向误差 $s_{error}$ 喂给油门刹车,两个一维问题。

## 误差定义

### 横向误差(核心)
$$d_{error} = d_{cur} - d_{ref}$$
- $d_{cur}$:车辆当前横向偏移(见[[d坐标]])
- $d_{ref}$:参考轨迹的横向偏移(换道时是时变 $d_{ref}(t)$)

### 纵向误差
$$s_{error} = s_{ref} - s_{cur}$$

### 高阶误差
- $\dot d_{error}$:横向速度误差(阻尼项)
- $\dot s_{error}$:速度误差(见[[PI速度控制]])

## 为什么 Frenet 误差好用

| 优势 | 说明 |
|:---|:---|
| 解耦 | 横纵误差各自独立控制(见[[解耦控制]]) |
| 直观 | $d_{error}$ 直接对应"偏了几公分" |
| 物理 | 曲率/边界约束自然表达 |

## 误差到控制

- 横向:$d_{error} \to$ 转向角(Stanley/LQR,见[[横向偏差]])
- 纵向:$s_{error}, \dot s_{error} \to$ 加速度指令(ACC,见[[间距误差]])

## 误差 vs 轨迹规划关系

- 规划层输出**参考轨迹**(含 $d_{ref}, s_{ref}$)
- 控制层实时计算误差并修正
- 误差过大(> 阈值)触发**重规划**而非强控(见[[最优轨迹]])

## 自检

- [ ] 横纵向跟踪误差如何定义?
- [ ] 误差如何映射到转向/油门?
- [ ] 误差超限时应做什么?
