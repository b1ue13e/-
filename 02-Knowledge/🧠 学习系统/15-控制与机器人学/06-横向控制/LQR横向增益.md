---
type: study
topic: "LQR横向增益"
course: "控制与机器人学"
created: 2026-04-18
updated: 2026-08-07
status: completed
difficulty: advanced
stage_moc: "[[🧭 阶段6-横向控制]]"
flow: knowledge
kind: derivation
concept: ["LQR横向", "增益", "实现"]
prerequisites: ["LQR横向状态", "横向系统矩阵"]
related: ["LQR横向状态", "横向系统矩阵"]
upstream: ["[[LQR横向状态]]"]
source: "PythonRobotics lqr_steering_control.py; Rajamani Ch.3"
tags: [学习, 控制与机器人学, 横向控制]
---

# LQR横向增益

## 0. 为什么学它

横向 LQR 的最终产物是**增益 $K=(k_1,k_2,k_3,k_4)$**，控制律 $\delta=-Kx+\delta_{ff}$。本卡给出 $K$ 的求解（ARE）与工程实现要点（离散化、车速调度、前馈配合）。

## 1. 核心实现

**增益求解**：对误差系统 $(A_e,B_e)$（含 $v_x$）解离散 ARE（`scipy.linalg.solve_discrete_are`）→ $K=(R+B^\top PB)^{-1}B^\top PA$。

**控制律**：

$$\delta=-k_1 e_y-k_2\dot e_y-k_3 e_\psi-k_4\dot e_\psi+\delta_{ff},\qquad \delta_{ff}=\arctan(\kappa L).$$

**实现要点**：
- **离散化**：$A_e,B_e$ 按采样时间 ZOH 离散（见 [[系统离散化]]）；
- **车速调度**：$A_e$ 含 $v_x$，不同车速重解 $K$（增益调度）；
- **前馈**：曲率项 $\delta_{ff}$ 处理弯道。

## 2. 最小可手算例子（概念验证）

**题目**：$v_x=20$ 与 $v_x=40$ 的 $K$ 为何不同？

**解**：$A_e$ 中 $v_x$ 在分母（$1/v_x$ 项）→ 特征值/增益随车速变化；高速时 $k_1$（偏差增益）通常降低（防抖），需重解 ARE 并调度 ✓。

**易错点**：离散与连续 ARE 混用；忘记按车速更新 $K$。

## 3. 常见误区

| 误区 | 正确理解 |
|:---|:---|
| $K$ 一次算好 | 车速变化需调度 |
| 忽略前馈 | 弯道需 $\delta_{ff}$ |
| 状态直接用 | 需估计/观测器 |

## 4. 与后续知识连接

- [[LQR横向状态]]：被控对象；
- [[LQR横向权重]]：$Q,R$；
- [[增益调度]]：车速变化。

## 5. 检索练习（闭卷）

1. 写出横向 LQR 控制律；
2. 说明 ARE 求解与离散；
3. 解释车速调度；
4. 前馈的作用。

## 6. 通过标准

- 能求横向 LQR 增益；
- 能实现控制律；
- 能处理车速与前馈。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/系统与硬件/15-控制与机器人学"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 复习

- 下次复习：3 天后重求 $K$；
- 薄弱点写入 [[控制与机器人学错题漏洞入口]]。
