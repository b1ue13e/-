---
type: study
topic: "DH参数"
course: "控制与机器人学"
created: 2026-04-18
updated: 2026-08-07
status: completed
difficulty: intermediate
stage_moc: "[[🧭 阶段2-机器人学基础模型]]"
flow: knowledge
kind: concept
concept: ["DH参数", "连杆描述", "正运动学"]
prerequisites: ["齐次变换矩阵", "变换链"]
related: ["MDH参数", "PUMA560", "机械臂DH参数与逆运动学"]
upstream: ["[[02-机器人学基础模型/变换链]]"]
source: "Modern Robotics (Lynch & Park), Ch.4; 机器人学导论 (Craig) Ch.3"
tags: [学习, 控制与机器人学, 机器人学]
---

# DH参数

## 0. 为什么学它

机械臂每个连杆/关节的几何关系要统一描述，否则没法编程。**Denavit-Hartenberg（DH）参数**用 4 个量（$a_i,\alpha_i,d_i,\theta_i$）唯一定义相邻连杆坐标系的变换，是正运动学建模的标准方法。

## 1. 核心定义

**DH 四参数**（连杆 $i$）：

| 参数 | 含义 | 类型 |
|:---|:---|:---|
| $a_i$ | 沿 $x_i$ 的连杆长度 | 常量 |
| $\alpha_i$ | 绕 $x_i$ 的连杆扭转角 | 常量 |
| $d_i$ | 沿 $z_{i-1}$ 的偏置 | 常量或变量 |
| $\theta_i$ | 绕 $z_{i-1}$ 的关节角 | 旋转关节为变量 |

**标准 DH 变换矩阵**（连杆 $i-1$ 系 → 连杆 $i$ 系）：

$$T_{i-1,i}=\begin{pmatrix}
\cos\theta_i&-\sin\theta_i\cos\alpha_i&\sin\theta_i\sin\alpha_i&a_i\cos\theta_i\\
\sin\theta_i&\cos\theta_i\cos\alpha_i&-\cos\theta_i\sin\alpha_i&a_i\sin\theta_i\\
0&\sin\alpha_i&\cos\alpha_i&d_i\\
0&0&0&1
\end{pmatrix}$$

## 2. 建模步骤（口诀）

1. 给每个关节建立 $z_{i-1}$ 轴（沿关节轴线）；
2. 建立 $x_i$ 轴：沿相邻 $z$ 轴的公垂线；
3. 读取四个参数；旋转关节 $\theta_i$ 为变量，移动关节 $d_i$ 为变量；
4. 末端位姿 = 变换链连乘。

## 3. 最小可手算例子

**题目**：2R 平面机械臂（两旋转关节，臂长 $l_1,l_2$），写 DH 表。

**解**：

| $i$ | $a$ | $\alpha$ | $d$ | $\theta$ |
|:---|:---|:---|:---|:---|
| 1 | $l_1$ | 0 | 0 | $\theta_1$ |
| 2 | $l_2$ | 0 | 0 | $\theta_2$ |

代入 $T_{01},T_{12}$ 连乘即得与 [[变换链]] 一致的 2R 正解。

**易错点**：$\alpha_i$ 绕 $x_i$ 的符号；$d_i$ 沿 $z_{i-1}$ 的方向约定。

## 4. 常见误区

| 误区 | 正确理解 |
|:---|:---|
| 标准 DH 与改进 DH 混用 | 两者 $x$ 轴定义/矩阵形式不同（见 [[MDH参数]]） |
| 忘写参数表中的零项 | 表必须完整，每行 4 个参数 |
| 坐标系方向选错 | 违反右手定则导致 $T$ 不正确 |

## 5. 与后续知识连接

- [[MDH参数]]：Craig 改进约定对比；
- [[PUMA560]]：完整 6DOF DH 表实例；
- [[变换链]]：连乘得正解；
- [[机械臂DH参数与逆运动学]]：综合大卡（含逆解）；
- 工程：URDF、Robotics Toolbox 均用 DH。

## 6. 检索练习（闭卷）

1. 默写 DH 四参数定义与 $T_{i-1,i}$ 矩阵；
2. 给 2R 臂写 DH 表并推导正解；
3. 说明旋转关节哪个参数是变量；
4. 标准 DH 与改进 DH 的核心差异。

## 7. 通过标准

- 能写 DH 表并生成变换矩阵；
- 能完成简单臂正运动学；
- 能区分标准/改进 DH。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/系统与硬件/15-控制与机器人学"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 复习

- 下次复习：3 天后重写 DH 表；
- 薄弱点写入 [[控制与机器人学错题漏洞入口]]。
