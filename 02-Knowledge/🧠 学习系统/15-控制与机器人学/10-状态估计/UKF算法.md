---
title: "UKF算法"
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
  - "[[无迹变换]]"
concept: ["UKF", "Sigma点滤波"]
prerequisites: ["无迹变换", "预测步", "更新步"]
related: ["无迹变换", "与EKF对比", "EKF步骤"]
---

# UKF算法

> **一句话**:UKF = 用无迹变换替换 EKF 的线性化——预测和更新都靠 Sigma 点传播,不用雅可比,强非线性下更准更稳。

## 算法流程

**初始化**:$\hat{\mathbf{x}}_0, P_0$

**预测步(时间更新)**:
1. 由 $(\hat{\mathbf{x}}_k, P_k)$ 生成 Sigma 点
2. 全部过过程模型:$\mathcal{X}^- = f(\mathcal{X})$
3. 统计预测均值与协方差:$(\hat{\mathbf{x}}_{k+1}^-, P_{k+1}^-)$(+$Q$)

**更新步(测量更新)**:
4. 由预测分布再生成 Sigma 点,过测量模型:$h(\mathcal{X}^-)$
5. 统计预测测量 $\hat{\mathbf{z}}$,互协方差 $P_{xz}$,测量协方差 $P_{zz}$(+$R$)
6. 增益:$K = P_{xz} P_{zz}^{-1}$
7. 更新:$\hat{\mathbf{x}}^+ = \hat{\mathbf{x}}^- + K(\mathbf{z} - \hat{\mathbf{z}})$, $P^+ = P^- - K P_{zz} K^\top$

## 与 EKF 结构对比

| 环节 | EKF | UKF |
|:---|:---|:---|
| 模型使用 | 雅可比 $F, H$ | 直接 $f, h$ |
| 协方差传播 | $F P F^\top + Q$ | Sigma 点统计 |
| 增益 | 公式含 $H$ | $P_{xz} P_{zz}^{-1}$ |
| 雅可比 | 需要 | **不需要** |

## 优点

- 二阶精度,强非线性更准(见[[与EKF对比]])
- 无需求导(黑盒模型友好)
- 实现难度与 EKF 相当

## 注意

- 高维时 Sigma 点权重可负 → 数值小心
- 非高斯分布仍假设高斯(与粒子滤波的区别)

## 自检

- [ ] UKF 七步流程?
- [ ] UKF 与 EKF 的结构对应?
- [ ] UKF 的两个注意点?
