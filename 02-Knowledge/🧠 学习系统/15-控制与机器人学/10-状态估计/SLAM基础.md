---
title: "SLAM基础"
type: concept
course: "控制与机器人学"
stage_moc: "[[🧭 阶段10-状态估计]]"
flow: knowledge
kind: concept
importance: "A"
status: completed
created: 2026-08-07
updated: 2026-08-07
tags: [学习, 控制与机器人学, 状态估计]
upstream:
  - "[[EKF非线性状态估计]]"
  - "[[栅格地图与占据栅格]]"
concept: ["SLAM", "同时定位建图"]
prerequisites: ["EKF非线性状态估计", "栅格地图与占据栅格"]
related: ["数据关联", "目标跟踪", "联邦滤波"]
---

# SLAM基础

> **一句话**:SLAM 是"先有鸡还是先有蛋"的循环——定位需要地图,建图需要定位。核心思路:把地图特征也当成状态一起估计,鸡和蛋一起解。

## 问题定义

机器人位姿 $\mathbf{x}$ 与地图特征 $\mathbf{m}$ 都未知:

$$p(\mathbf{x}_{1:t}, \mathbf{m} | \mathbf{z}_{1:t}, \mathbf{u}_{1:t})$$

- 观测 $\mathbf{z}$:路标/特征测量
- 控制 $\mathbf{u}$:里程计/IMU

## 增广状态估计

把地图特征增广为状态:

$$\mathbf{X} = [\mathbf{x}; \mathbf{m}_1; \mathbf{m}_2; \cdots]$$

用 EKF 估计整个增广状态 → **EKF-SLAM**。特征不确定性与位姿不确定性互相校正。

## 闭环检测(关键)

- 机器人回到曾访问区域,重新看到特征 → 检测到闭环
- 闭环能"一锤定音"消除累积漂移
- 数据关联错误(见[[数据关联]])会让闭环失效 → 关联鲁棒性是核心

## SLAM 流派

| 流派 | 方法 | 特点 |
|:---|:---|:---|
| 滤波式 | EKF-SLAM / FastSLAM | 在线递推 |
| 图优化式 | GraphSLAM / ORB-SLAM | 批量优化,现代主流 |
| 因子图 | GTSAM / g2o | 概率图建模 |

## 工程要点

- 大规模地图 → 滤波式维度爆炸 → 图优化为主流
- 前端(特征提取/关联)+ 后端(优化)分离
- 视觉 SLAM / LiDAR SLAM 是两大载体

## 自检

- [ ] SLAM 的"鸡生蛋"难题?
- [ ] EKF-SLAM 如何增广状态?
- [ ] 闭环检测的作用?
