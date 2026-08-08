---
type: study
topic: "LQG控制"
course: "控制与机器人学"
created: 2026-08-07
updated: 2026-08-09
status: completed
difficulty: advanced
stage_moc: "[[🧭 阶段10-状态估计]]"
flow: knowledge
kind: concept
concept: ["LQG", "最优随机控制"]
prerequisites: ["原理陈述", "LQR代价函数", "卡尔曼滤波KalmanFilter"]
related: ["原理陈述", "闭环极点", "回路传递恢复"]
upstream:
  - "[[原理陈述]]"
  - "[[LQR代价函数]]"
source: "Åström, Introduction to Stochastic Control Theory Ch.9；Simon, Optimal State Estimation Ch.12"
tags: [学习, 控制与机器人学, 状态估计]
---

# LQG控制

## 0. 为什么学它

LQG（Linear Quadratic Gaussian）= **LQR（最优控制）+ 卡尔曼滤波（最优估计）**，由分离定理组合——是线性高斯随机系统的最优输出反馈控制器。它是"状态估计 + 状态反馈"架构的教科书基准：车辆/飞行器/过程控制里大量系统（电机、倒立摆、导航）都能用它起步。理解 LQG = 理解现代控制"估计与决策"的完整闭环。

## 1. LQG 组成

$$
\text{LQG} = \text{LQR} + \text{Kalman Filter}
$$

| 部分 | 作用 | 设计 |
|:---|:---|:---|
| LQR | 状态反馈 $u = -Kx$（见 [[LQR代价函数\|LQR代价函数]]） | 解控制侧 ARE |
| Kalman | 状态估计 $\hat{x}$（见 [[卡尔曼滤波KalmanFilter\|卡尔曼滤波]]） | 解估计侧 ARE |
| 组合 | $u = -K\hat{x}$ | 分离定理保证最优（见 [[原理陈述\|原理陈述]]） |

## 2. 问题设定

线性高斯系统 + 二次代价的随机最优控制：

$$
dx = Ax\, dt + Bu\, dt + dw, \qquad dz = Cx\, dt + dv
$$

$$
\min \mathbb{E} \int_0^\infty \left(x^\top Q x + u^\top R u\right) dt
$$

## 3. 两个 Riccati 方程（对偶结构）

- 控制侧：LQR 的 ARE（见 [[ARE|ARE]]）→ 解出 $K$；
- 估计侧：Kalman 的 ARE → 解出 $L$；
- 两者结构对偶（控制与估计互为对偶问题，见 [[对偶原理|对偶原理]]）。

## 4. 最小可手算例子（增益结构）

**题目**：一阶系统 $A=1, B=1, C=1$，控制代价 $Q=1, R=1$，过程噪声 $Q_w=0.1$，测量噪声 $R_v=1$。求 $K$ 与 $L$。

**解**：控制侧 ARE：$P = A^2P - A^2 P^2 B^2/(B^2 P + R) + Q$，标量化简 $P = 1 - P/(P+1) + 1$ → $P = \frac{1+\sqrt{5}}{2} \approx 1.618$，$K = \frac{BP}{R} = 1.618$。

估计侧（对偶）：$\Sigma = 1 - \Sigma/(\Sigma+1) + 0.1$ → $\Sigma \approx 1.14$，$L = \frac{C\Sigma}{R_v} = 1.14$。

**解读**：控制与估计各自解 ARE，$K$、$L$ 独立得到——分离定理在此直接可验证；组合 $u = -1.618\hat{x}$ 即 LQG 控制器。

## 5. LQG 的局限

| 局限 | 说明 | 对策 |
|:---|:---|:---|
| 无鲁棒性保证 | 模型误差下无稳定裕度 | LTR（见 [[回路传递恢复\|回路传递恢复]]）/ H∞ |
| 高斯假设 | 非高斯非最优 | 粒子滤波 + NMPC |
| 线性假设 | 非线性失效 | NMPC + EKF 组合 |

## 6. 常见误区

| 误区 | 正确理解 |
|:---|:---|
| "LQG = 两个 ARE 随便拼" | 需要分离定理保证组合最优，且参数要对偶匹配 |
| "LQG 一定有鲁棒性" | LQG 的稳定裕度可能任意小（模型误差下），需要 LTR |
| "LQG 只适合理论" | 工程应用极广，是估计+控制架构的起点模板 |
| "LQG 与 LQR 等价" | LQR 假设状态已知；LQG 处理状态未知（含估计器） |

## 7. 检索练习（闭卷）

1. 写出 LQG 组成与问题设定；
2. 手算一阶 LQG 的 $K$ 与 $L$；
3. 解释控制/估计两个 ARE 的对偶关系；
4. 列出 LQG 的三个局限与对策。

## 8. 通过标准

- 能写出 LQG 的组成、设定与两方程；
- 能手算一阶 LQG 增益；
- 能解释分离定理在 LQG 中的作用；
- 能识别 LQG 的鲁棒性局限。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/系统与硬件/15-控制与机器人学"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 复习

- 下次复习：用 Python 仿真一阶 LQG（对比 LQR 纯状态反馈的差异）；
- 薄弱点写入 [[控制与机器人学错题漏洞入口]]；
- 关联：[[原理陈述\|原理陈述]]、[[回路传递恢复\|回路传递恢复]]。
