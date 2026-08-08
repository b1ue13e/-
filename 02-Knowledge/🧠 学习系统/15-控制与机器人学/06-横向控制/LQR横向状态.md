---
type: study
topic: "LQR横向状态"
course: "控制与机器人学"
created: 2026-04-18
updated: 2026-08-07
status: completed
difficulty: advanced
stage_moc: "[[🧭 阶段6-横向控制]]"
flow: knowledge
kind: derivation
concept: ["LQR横向", "误差状态", "横向控制"]
prerequisites: ["横向系统矩阵", "LQR增益"]
related: ["LQR横向权重", "LQR横向增益", "横向系统矩阵"]
upstream: ["[[横向系统矩阵]]"]
source: "Rajamani Ch.3; PythonRobotics lqr_steering_control.py"
tags: [学习, 控制与机器人学, 横向控制]
---

# LQR横向状态

## 0. 为什么学它

横向 LQR 用**误差状态**做被控对象：$x=(e_y,\dot e_y,e_\psi,\dot e_\psi)$，设计 $u=\delta=-Kx$ 使误差归零——"把车拉回路径"变成"最优镇定误差"。这是模型法横向控制的代表。

## 1. 核心模型

**误差状态**：$x=(e_y,\ \dot e_y,\ e_\psi,\ \dot e_\psi)$（横向偏差、偏差率、航向误差、横摆误差率）。

**误差动态**（见 [[横向系统矩阵]]）：

$$\dot x = A_e x + B_e \delta + D_e\ddot\psi_r.$$

**LQR 设计**：忽略/前馈 $D_e$，对 $(A_e,B_e)$ 解 ARE 得 $K$，控制 $\delta=-Kx+\delta_{ff}$（$\delta_{ff}$ 曲率前馈）。

**状态来源**：$e_y,e_\psi$ 由定位与路径计算；$\dot e_y,\dot e_\psi$ 由速度/IMU 估计（或观测器）。

## 2. 最小可手算例子（概念验证）

**题目**：为什么状态含 $e_\psi$ 而非只有 $e_y$？

**解**：只有 $e_y$ 反馈时，车可能"平行偏离"（$e_y$ 有值但航向同向）无法修正航向；$e_\psi$ 项保证车头转向路径方向，两者结合才完整镇定 ✓。

**易错点**：状态来源的坐标系（路径 Frenet）；$\dot e_y$ 与 $v_x e_\psi$ 的耦合。

## 3. 常见误区

| 误区 | 正确理解 |
|:---|:---|
| 横向 LQR 用绝对状态 | 用误差状态（相对路径） |
| 忽略 $D_e$ 曲率项 | 弯道需前馈或增广 |
| 状态不可测也直接反馈 | 需观测器/估计 |

## 4. 与后续知识连接

- [[LQR横向权重]]、[[LQR横向增益]]：设计；
- [[横向系统矩阵]]：模型；
- [[MPC横向预测]]：同类但带约束。

## 5. 检索练习（闭卷）

1. 写出横向误差状态；
2. 说明 LQR 设计步骤；
3. 解释为何含 $e_\psi$；
4. 状态来源。

## 6. 通过标准

- 能定义误差状态；
- 能设计横向 LQR；
- 能理解前馈配合。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/系统与硬件/15-控制与机器人学"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 复习

- 下次复习：3 天后重定义状态；
- 薄弱点写入 [[控制与机器人学错题漏洞入口]]。
