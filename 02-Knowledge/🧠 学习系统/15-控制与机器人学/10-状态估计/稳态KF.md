---
type: study
topic: "稳态KF"
course: "控制与机器人学"
created: 2026-08-07
updated: 2026-08-09
status: completed
difficulty: intermediate
stage_moc: "[[🧭 阶段10-状态估计]]"
flow: knowledge
kind: concept
concept: ["稳态增益", "离线计算"]
prerequisites: ["卡尔曼滤波KalmanFilter", "卡尔曼增益"]
related: ["卡尔曼增益", "稳定性", "观测器结构"]
upstream: ["[[卡尔曼滤波KalmanFilter]]"]
source: "Probabilistic Robotics (Thrun et al.) Ch.3 [待验证]；Simon, Optimal State Estimation Ch.4"
tags: [学习, 控制与机器人学, 状态估计]
---

# 稳态KF

## 0. 为什么学它

对时不变系统，KF 的增益会**收敛到常值** $K_\infty$。这带来巨大的工程红利：把最重的矩阵运算（协方差递推）离线做完，在线只跑"状态更新"两步乘法——计算量从 $O(d^3)$ 降到 $O(d^2)$，且无数值发散风险。嵌入式、实时、低算力平台的滤波器几乎都用稳态形式。本卡讲清"什么时候能用、怎么算、代价是什么"。

## 1. 现象与原理

对时不变 $(A, H, Q, R)$，随着迭代：

$$
P_k^- \to P_\infty, \quad P_k^+ \to P_\infty^+, \quad K_k \to K_\infty
$$

$K_\infty$ 由离散代数 Riccati 方程（DARE）决定：

$$
P_\infty = A P_\infty A^\top - A P_\infty H^\top (H P_\infty H^\top + R)^{-1} H P_\infty A^\top + Q
$$

## 2. 稳态 KF 的在线实现

在线只需：

$$
\hat{\mathbf{x}}^+ = \hat{\mathbf{x}}^- + K_\infty (\mathbf{z} - H\hat{\mathbf{x}}^-)
$$

**无需协方差更新**——等价于固定增益观测器（见 [[观测器结构|观测器结构]]），$K_\infty$ 即观测器增益。

## 3. 优缺点

| 优点 | 缺点 |
|:---|:---|
| 计算量极小（嵌入式友好） | 参数/噪声变化时非最优 |
| 无数值问题 | 失去自适应能力 |
| 实时性确定（无迭代） | 需离线求解 DARE |

## 4. 适用场景

- 时不变/弱时变系统（GPS 融合、电机转速估计）；
- 计算受限平台（MCU 级）；
- 噪声统计稳定、不需要自适应的应用。

## 5. 与自适应 KF 的关系

| 形式 | 增益 | 复杂度 | 适用 |
|:---|:---|:---|:---|
| 稳态 KF | 固定 $K_\infty$ | 低 | 系统时不变 |
| 标准 KF | 每步在线递推 | 中 | 一般系统 |
| 自适应 KF | 在线调 $Q/R$ 或增益 | 高 | 噪声时变 |

## 6. 最小可手算例子

**题目**：一维系统 $A=1, H=1, Q=0.1, R=1$。求稳态增益 $K_\infty$。

**解**：稳态时 $P^-$ 满足 $P^- = P^- + Q - \frac{(P^-)^2}{P^-+R}$，即：

$$
\frac{(P^-)^2}{P^-+R} = Q \Rightarrow \frac{P^2}{P+1} = 0.1 \Rightarrow P^2 = 0.1P + 0.1
$$

$$
P = \frac{0.1 + \sqrt{0.01 + 0.4}}{2} = \frac{0.1 + 0.6403}{2} \approx 0.370
$$

$$
K_\infty = \frac{P}{P+1} = \frac{0.370}{1.370} \approx 0.270
$$

**解读**：约 27% 的稳态信任度；在线每步只需 $\hat{x}^+ = \hat{x}^- + 0.270(z - \hat{x}^-)$ 一次乘加。

## 7. 常见误区

| 误区 | 正确理解 |
|:---|:---|
| "稳态 KF 永远最优" | 只在时不变 + 噪声稳定时最优；环境变化需切回自适应 |
| "$K_\infty$ 随便取个常值" | 必须解 DARE/收敛得到，否则稳定性无保证 |
| "稳态形式没有协方差" | 只是不递推 $P$；$P_\infty$ 仍然存在（用于一致性检验） |
| "稳态 = 精度低" | 精度与标准 KF 相同（稳态后两者等价），省的是算力 |

## 8. 检索练习（闭卷）

1. 解释 $K_k \to K_\infty$ 的条件与原因；
2. 手算 $A=1,H=1,Q=1,R=1$ 的 $K_\infty$（提示：$P^2/(P+1)=1$）；
3. 稳态 KF 在线只需哪两步运算？
4. 何时不应使用稳态 KF？

## 9. 通过标准

- 能说明稳态增益的来源（DARE/收敛）；
- 能手算一维稳态增益；
- 能判断适用场景并说明代价；
- 能区分稳态/标准/自适应 KF。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/系统与硬件/15-控制与机器人学"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 复习

- 下次复习：换 $Q=1$ 重算 $K_\infty$，观察信任度变化；
- 薄弱点写入 [[控制与机器人学错题漏洞入口]]；
- 关联：[[卡尔曼增益\|卡尔曼增益]]、[[观测器结构\|观测器结构]]。
