---
type: study
topic: "PUMA560"
course: "控制与机器人学"
created: 2026-04-18
updated: 2026-08-07
status: completed
difficulty: advanced
stage_moc: "[[🧭 阶段2-机器人学基础模型]]"
flow: knowledge
kind: derivation
concept: ["PUMA560", "正运动学", "6DOF机械臂"]
prerequisites: ["DH参数", "变换链"]
related: ["机械臂DH参数与逆运动学", "几何Jacobian"]
upstream: ["[[02-机器人学基础模型/DH参数]]"]
source: "Modern Robotics (Lynch & Park), Ch.4 习题; Craig Ch.3 例"
tags: [学习, 控制与机器人学, 机器人学]
---

# PUMA560

## 0. 为什么学它

PUMA560 是教材中最经典的 6DOF 工业机械臂。它的 DH 参数表、正运动学推导、逆运动学（Pieper 解）是检验你是否真正掌握运动学的**标准例题**——几乎所有教材都用它做完整推导示范。

## 1. PUMA560 标准 DH 表

PUMA560 有 6 个旋转关节，标准 DH 参数（教材常用值，单位 mm/deg）：

| $i$ | $a_i$ | $\alpha_i$ | $d_i$ | $\theta_i$ |
|:---|:---|:---|:---|:---|
| 1 | 0 | $-90^\circ$ | 0 | $\theta_1$ |
| 2 | $a_2$ | 0 | $d_2$ | $\theta_2$ |
| 3 | $a_3$ | $-90^\circ$ | $d_3$ | $\theta_3$ |
| 4 | 0 | $90^\circ$ | $d_4$ | $\theta_4$ |
| 5 | 0 | $-90^\circ$ | 0 | $\theta_5$ |
| 6 | 0 | 0 | $d_6$ | $\theta_6$ |

> 不同教材参数略有差异，以所用教材为准；重点是推导方法而非数值。

## 2. 正运动学

末端位姿 $T_{06}=T_{01}T_{12}T_{23}T_{34}T_{45}T_{56}$。代入各 $T_{i-1,i}$（DH 矩阵）连乘，得到末端位置与姿态的封闭表达式（通常用 $\theta_2+\theta_3$ 等组合化简）。

**结构特点**：关节 2、3 决定腕部中心位置（球坐标臂），关节 4、5、6 构成球腕（Roll-Pitch-Yaw），腕部中心解耦——这是逆解可解析的关键（Pieper 准则）。

## 3. 最小可手算例子

**题目**：求 $\theta_1=\theta_2=\cdots=\theta_6=0$ 时末端位姿。

**解**：逐矩阵代入。$\theta_i=0$ 时各 $T_{i-1,i}$ 退化为单位附近的简单旋转+平移，连乘得 $T_{06}$（位置 = $a_2,a_3,d_3,d_6$ 组合，姿态由 $\alpha$ 链决定）。具体数值以 DH 表为准代入即可——建议用 `Robotics Toolbox` 或手算 + 数值验证。

**易错点**：某个 $\alpha_i$ 符号错导致整条链错；连乘顺序错。

## 4. 常见误区

| 误区 | 正确理解 |
|:---|:---|
| 死记 DH 表数值 | 参数因教材/装配而异，重点在方法与结构 |
| 不验证正解 | 用数值库（Robotics Toolbox）交叉验证 |
| 忽略球腕解耦 | 解耦是解析逆解的前提 |

## 5. 与后续知识连接

- [[DH参数]]：表来源；
- [[机械臂DH参数与逆运动学]]：综合大卡（逆解方法）；
- [[几何Jacobian]]：PUMA 的速度映射；
- [[奇异位形]]：球腕与臂的奇异；
- 项目：[[项目-PUMA仿真]]。

## 6. 检索练习（闭卷）

1. 默写 PUMA560 DH 表（参数含义）；
2. 说明正运动学的计算路径；
3. 解释球腕结构为何使逆解解耦；
4. 用 Robotics Toolbox 验证 $\theta=0$ 的末端位姿。

## 7. 通过标准

- 能写出 PUMA560 DH 表并解释结构；
- 能完成正运动学连乘推导；
- 能说明逆解可解析的结构原因。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/系统与硬件/15-控制与机器人学"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 复习

- 下次复习：3 天后重推正解；
- 薄弱点写入 [[控制与机器人学错题漏洞入口]]。
