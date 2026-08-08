---
type: study
topic: "UKF算法"
course: "控制与机器人学"
created: 2026-08-07
updated: 2026-08-09
status: completed
difficulty: advanced
stage_moc: "[[🧭 阶段10-状态估计]]"
flow: knowledge
kind: concept
concept: ["UKF", "Sigma点滤波"]
prerequisites: ["无迹变换", "预测步", "更新步"]
related: ["无迹变换", "与EKF对比", "EKF步骤"]
upstream: ["[[无迹变换]]"]
source: "Wan & van der Merwe, The Unscented Kalman Filter；Probabilistic Robotics (Thrun et al.) Ch.3 [待验证]"
tags: [学习, 控制与机器人学, 状态估计]
---

# UKF算法

## 0. 为什么学它

UKF（无迹卡尔曼滤波）= **用无迹变换替换 EKF 的线性化**：预测和更新都靠 Sigma 点传播，不用雅可比，强非线性下更准更稳。它在不增加太多实现难度的前提下把精度从一阶提到二阶，是"不想求导、又嫌 EKF 太糙"时的首选。本卡给出 UKF 的完整可执行算法与 EKF 的结构对照。

## 1. 算法流程

**初始化**：$\hat{\mathbf{x}}_0, P_0$

**预测步（时间更新）**：
1. 由 $(\hat{\mathbf{x}}_k, P_k)$ 生成 Sigma 点（见 [[无迹变换|无迹变换]]）；
2. 全部过过程模型：$\mathcal{X}^- = f(\mathcal{X})$；
3. 统计预测均值与协方差 $(\hat{\mathbf{x}}_{k+1}^-, P_{k+1}^-)$（加 $Q$）。

**更新步（测量更新）**：
4. 由预测分布再生成 Sigma 点，过测量模型：$h(\mathcal{X}^-)$；
5. 统计预测测量 $\hat{\mathbf{z}}$、互协方差 $P_{xz}$、测量协方差 $P_{zz}$（加 $R$）；
6. 增益：$K = P_{xz} P_{zz}^{-1}$；
7. 更新：$\hat{\mathbf{x}}^+ = \hat{\mathbf{x}}^- + K(\mathbf{z} - \hat{\mathbf{z}})$，$P^+ = P^- - K P_{zz} K^\top$。

## 2. 与 EKF 结构对比

| 环节 | EKF | UKF |
|:---|:---|:---|
| 模型使用 | 雅可比 $F, H$ | 直接 $f, h$ |
| 协方差传播 | $F P F^\top + Q$ | Sigma 点统计 |
| 增益 | 公式含 $H$ | $P_{xz} P_{zz}^{-1}$ |
| 雅可比 | 需要 | **不需要** |

## 3. 最小可手算例子（一步预测）

**题目**：一维 $x \sim \mathcal{N}(1, 1)$，$f(x) = x^2$，$Q = 0.5$。用 UT 求预测均值与方差。

**解**：由无迹变换卡例子，$f(\mathcal{X}) = \{1, 7.464, 0.536\}$，均值 $\bar{y} = 2.0$。协方差（协方差权重 $w_0^c = \frac{2}{3}, w_{1,2}^c = \frac{1}{6}$）：

$$
P_y = \frac{2}{3}(1-2)^2 + \frac{1}{6}(7.464-2)^2 + \frac{1}{6}(0.536-2)^2
$$

$$
= 0.667 + 4.980 + 0.357 = 6.00
$$

加 $Q$：$P^- = 6.00 + 0.5 = 6.5$。

**解读**：对比 EKF 的 $P^- = F^2 P + Q = 4\times 1 + 0.5 = 4.5$——UKF 给出更大的诚实方差（6.5 vs 4.5），因为 $x^2$ 的非线性让不确定性显著放大，UKF 捕捉到了，EKF 低估了。

## 4. 优点与注意

| 优点 | 注意 |
|:---|:---|
| 二阶精度，强非线性更准 | 高维时 Sigma 点权重可为负 → 协方差可能非正定，需小心 |
| 无需求导（黑盒友好） | 仍假设高斯分布（与粒子滤波的区别） |
| 实现难度与 EKF 相当 | 参数 $\alpha, \kappa, \beta$ 需调 |

## 5. 常见误区

| 误区 | 正确理解 |
|:---|:---|
| "UKF 一定能处理非高斯" | UKF 仍假设高斯；非高斯/多峰要粒子滤波 |
| "UKF 比 EKF 一定贵很多" | 每步 $2n+1$ 次传播，$n$ 适中时与 EKF 同量级 |
| "不用算雅可比 = 免建模" | 模型 $f, h$ 还是要写，只是不求导 |
| "UKF 永远收敛" | 高维权重为负、参数不当仍会发散 |

## 6. 检索练习（闭卷）

1. 默写 UKF 七步流程；
2. 手算一步 UKF 预测（$f=x^2$）；
3. 说出 UKF 与 EKF 的四组结构差异；
4. UKF 的两个注意点。

## 7. 通过标准

- 能默写并执行 UKF 算法；
- 能手算一步 Sigma 点传播；
- 能对比 EKF/UKF 的精度与成本；
- 能识别 UKF 的适用边界（高斯 + 非线性）。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/系统与硬件/15-控制与机器人学"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 复习

- 下次复习：把 UKF 七步与 `filterpy` 的 `UnscentedKalmanFilter` API 对照；
- 薄弱点写入 [[控制与机器人学错题漏洞入口]]；
- 关联：[[与EKF对比\|与EKF对比]]、[[无迹变换\|无迹变换]]。
