---
created: 2026-08-07
type: study
course: "强化学习"
title: "Sim-to-Real与域随机化 (Sim-to-Real & Domain Randomization)"
topic: "Sim-to-Real与域随机化 (Sim-to-Real & Domain Randomization)"
stage_moc: "[[🧭 阶段8-模型基与规划]]"
flow: knowledge
kind: concept
status: learning
importance: "B"
tags: [学习, 强化学习, 模型基, 迁移]
upstream: ["[[模型基RL概述]]", "[[模型不确定性与贝叶斯模型]]"]
concept: ["Sim-to-Real", "域随机化", "系统辨识", "现实差距"]
sources:
  - "Tobin et al. 2017 (domain randomization); Peng et al. 2018 (Sim-to-Real)"
---
# Sim-to-Real与域随机化 (Sim-to-Real & Domain Randomization)

> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 对应阶段：[[🧭 阶段8-模型基与规划|返回阶段页]]

## 动机
真实机器人又贵又易坏，我们想在仿真里训练、再部署到真实世界。但**仿真与真实永远有差距（reality gap）**：摩擦系数、质量、延迟、传感器噪声都对不上。模型基 RL 尤其怕这个——它在"假模型"里优化的策略，到了真机可能失效。域随机化是性价比最高的对策。

## 正式定义 / 公式
**域随机化**：在仿真训练时，把环境参数 θ（质量、摩擦、光照、相机位姿…）从分布 p(θ) 随机采样，训练策略 π 对**多种域**都有效：

  max_π E_{θ~p(θ)} [ E_{τ~p(·|θ,π)} R(τ) ]

理想情况下，真实域落在随机化覆盖的域内，策略直接泛化。更进阶：**系统辨识（system identification）** 先估出真实参数再精调；或 **域自适应** 把仿真特征对齐到真实。

## 最小手算例子
训练机械臂抓取：仿真里把物体质量随机在 [0.1,2.0]kg、摩擦在 [0.2,1.0] 间抖动地训练。真实物体质量 0.7kg 正好落在覆盖区间内，无需额外调参就能抓。若不随机化（只训 0.5kg、摩擦 0.6），真实 0.7kg/0.3 摩擦下抓力不对就会掉。

## 对比与常见错误
- 与纯模型基 RL：域随机化是"让模型误差分布可控"的工程手段，而非学精确模型。
- 与系统辨识：随机化无需真实参数，辨识更精准但需真实数据。
- **常见错误**：随机化范围太窄→覆盖不到真实域；太宽→策略被迫保守、性能上限低（偏置-方差权衡）。

## 闭卷自测
1. 域随机化靠什么让策略能迁移到真实世界？
2. 随机化范围过窄或过宽分别有什么后果？

## 学完后可以完成

```dataview
LIST FROM "03-Projects" WHERE contains(requires, this.file.link)
```

## 相关下游知识

```dataview
LIST FROM "02-Knowledge/🧠 学习系统" WHERE contains(upstream, this.file.link)
```
