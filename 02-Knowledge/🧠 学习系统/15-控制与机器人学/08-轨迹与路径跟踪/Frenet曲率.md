---
title: "Frenet曲率"
type: concept
course: "15-控制与机器人学"
stage_moc: "[[🧭 阶段8-轨迹与路径跟踪]]"
flow: knowledge
kind: concept
importance: "B"
status: completed
created: 2026-08-07
updated: 2026-08-07
tags: [学习, 控制与机器人学, Frenet]
upstream:
  - "[[Frenet转换]]"
concept: ["曲率传递", "横向导数"]
prerequisites: ["Frenet转换"]
related: ["曲率约束", "Frenet横向", "轨迹可行性"]
---

# Frenet曲率

> **一句话**:车辆实际行驶轨迹的曲率 = 参考线曲率 + 横向运动的贡献——在 Frenet 系里精确表达横向运动对转向的影响。

## 轨迹曲率公式

车辆轨迹曲率 $\kappa$(由 $d(s)$ 及其导数表达):

$$\kappa(s) = \frac{\kappa_r(s) + \frac{d''(s)}{(1 - \kappa_r d)^2}}{\sqrt{1 + (d'(s)/\dot{s})^2}}$$

常见简化(横向速度小、$\kappa_r d \ll 1$):

$$\kappa \approx \kappa_r + d''$$

**直觉:横向加速度由 $d''$ 提供,换道轨迹的曲率 = 参考线曲率 + 自身横向弯曲**。

## 曲率受限速度

转向角上限 $\delta_{max}$ → 曲率上限 $\kappa_{max} = \tan\delta_{max}/L$ → 速度上限:

$$v_{max}(s) = \sqrt{\frac{a_{lat,max}}{\kappa(s)}}$$

## Frenet 中曲率的影响

| 影响 | 说明 |
|:---|:---|
| 坐标转换 | 参考线曲率进入 $\dot{s}$ 分解(见[[Frenet转换]]) |
| 可行性 | 横向多项式生成的 $d(s)$ 可能使 $\kappa$ 超限 |
| 限速 | 弯道按 $\kappa(s)$ 限速 |
| 奇异性 | $1-\kappa_r d \to 0$ 时公式失效 |

## 工程要点

- 换道轨迹验证必须检查合成曲率 $\kappa(s) \le \kappa_{max}$(见[[轨迹可行性]])
- 高速换道:横向加速度约束自动限制换道速度
- 曲率突变点(参考线急弯)要降低纵向速度

## 自检

- [ ] 合成曲率由哪两部分构成?
- [ ] 曲率如何转化为转向角?
- [ ] 为什么换道时也要检查曲率?
