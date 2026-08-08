---
type: study
topic: "卡尔曼滤波"
course: "控制与机器人学"
created: 2026-08-01
updated: 2026-08-09
status: completed
difficulty: intermediate
stage_moc: "[[🧭 阶段10-状态估计]]"
flow: knowledge
kind: concept
concept: ["卡尔曼滤波", "贝叶斯估计", "协方差更新"]
prerequisites: ["观测器结构", "能观性定义", "噪声模型"]
related: ["问题设定", "预测步", "更新步", "卡尔曼增益", "最优性", "EKF非线性状态估计"]
upstream:
  - "[[观测器结构]]"
  - "[[能观性定义]]"
source: "Kalman (1960), A New Approach to Linear Filtering and Prediction Problems；Probabilistic Robotics (Thrun et al.) Ch.3"
tags: [学习, 控制与机器人学, 卡尔曼滤波, 状态估计]
---

# 卡尔曼滤波 Kalman Filter

## 0. 为什么学它

阶段 5 的状态反馈假设"状态已知"，但真实系统只有带噪声的测量。卡尔曼滤波是**最优线性高斯状态估计**的基石：在"模型不准 + 测量有噪"的情况下，用预测-更新两步循环在线融合两者。它是 LQG 控制、GPS/IMU 组合导航、SLAM 的公共算法内核——1960 年由 Kálmán 提出，直接用于阿波罗登月导航，至今仍是状态估计的第一课。**本卡是模块 B 的总览卡**，给出完整算法与 5 大递推公式；细节卡（问题设定/预测步/更新步/增益）逐项展开。

## 1. 定义与核心性质

**核心定义**：基于线性系统方程与高斯白噪声假设，利用"预测-更新"双步循环，在最小均方误差（MMSE）意义下融合过程模型与传感器观测的最优高斯状态估计算法。

三大性质：
1. **递归估计**：无需存储全部历史测量，只依赖上一时刻估计 $\hat{\mathbf{x}}_{k-1|k-1}$ 与当前观测 $\mathbf{z}_k$；
2. **高斯封闭性**：线性变换 + 高斯噪声仍为高斯分布，均值与协方差完整表征状态分布；
3. **动态加权**：增益 $K_k$ 根据预测不确定性 $P_{k|k-1}$ 与测量噪声 $R$ 的比值，自动分配信任。

## 2. 系统建模与 5 大核心递推公式

**线性离散模型**：
- 状态方程：$\mathbf{x}_k = A \mathbf{x}_{k-1} + B \mathbf{u}_k + \mathbf{w}_k$，$\mathbf{w}_k \sim \mathcal{N}(0, Q)$
- 观测方程：$\mathbf{z}_k = H \mathbf{x}_k + \mathbf{v}_k$，$\mathbf{v}_k \sim \mathcal{N}(0, R)$

**五步递推（KF 全部内容）**：

| # | 步骤 | 公式 |
|:--|:--|:--|
| 1 | 状态预测 | $\hat{\mathbf{x}}_{k|k-1} = A \hat{\mathbf{x}}_{k-1|k-1} + B \mathbf{u}_k$ |
| 2 | 协方差预测 | $P_{k|k-1} = A P_{k-1|k-1} A^\top + Q$ |
| 3 | 卡尔曼增益 | $K_k = P_{k|k-1} H^\top (H P_{k|k-1} H^\top + R)^{-1}$ |
| 4 | 状态更新 | $\hat{\mathbf{x}}_{k|k} = \hat{\mathbf{x}}_{k|k-1} + K_k(\mathbf{z}_k - H\hat{\mathbf{x}}_{k|k-1})$ |
| 5 | 协方差更新 | $P_{k|k} = (I - K_k H) P_{k|k-1}$ |

**增益推导要点**：选择 $K_k$ 使后验协方差迹 $\text{tr}(P_{k|k})$ 最小，对 $K_k$ 求导得第 3 式。

**极端情形**：$R \to 0$ 时 $K_k \to H^{-1}$，完全信任测量；$Q \to 0$ 时 $K_k \to 0$，完全信任模型。

## 3. KF / EKF / UKF / 粒子滤波对比

| 算法 | 系统假设 | 噪声假设 | 复杂度 | 优势与局限 |
|:---|:---|:---|:---|:---|
| **KF** | 严格线性 | 高斯白噪声 | $O(d^3)$ | 理论最优；无法处理非线性 |
| **EKF** | 非线性（一阶泰勒） | 高斯白噪声 | $O(d^3)$ | 实用；依赖雅可比，高度非线性下发散 |
| **UKF** | 非线性（UT 变换） | 高斯白噪声 | $O(d^3)$ | 无需雅可比，精度达二阶 |
| **粒子滤波** | 强非线性 | 任意分布 | $O(N_{\text{particles}} d)$ | 最通用；高维粒子匮乏 |

> **局限与反例**：当噪声为有色噪声或非高斯双峰分布时，KF 会产生严重偏置——此时必须改用粒子滤波或抗差方法。这也是"高斯假设不成立则最优性失效"的直接例子（见 [[最优性|最优性]]）。

## 4. Python 手写一维卡尔曼滤波（可运行 + 自测）

```python
import numpy as np

class KalmanFilter1D:
    """一维卡尔曼滤波：验证预测-更新两步循环与收敛性"""
    def __init__(self, A=1.0, H=1.0, Q=1e-5, R=0.1, x0=0.0, P0=1.0):
        self.A, self.H, self.Q, self.R = A, H, Q, R
        self.x, self.P = x0, P0

    def step(self, z: float) -> float:
        # Predict
        x_pred = self.A * self.x
        P_pred = self.A * self.P * self.A + self.Q
        # Update
        K = P_pred * self.H / (self.H * P_pred * self.H + self.R)
        self.x = x_pred + K * (z - self.H * x_pred)
        self.P = (1.0 - K * self.H) * P_pred
        return self.x

if __name__ == "__main__":
    np.random.seed(42)
    true_x = 5.0
    kf = KalmanFilter1D(x0=0.0, P0=10.0, Q=1e-4, R=0.2)
    measurements = true_x + np.random.normal(0, np.sqrt(0.2), 100)
    estimates = [kf.step(z) for z in measurements]

    # 自测 1: 后验估计收敛到真实值
    assert abs(estimates[-1] - true_x) < 0.2, f"KF 未收敛: {estimates[-1]}"
    # 自测 2: 滤波后误差方差小于原始测量方差
    err_raw = np.mean((measurements - true_x)**2)
    err_kf = np.mean((np.array(estimates[20:]) - true_x)**2)
    assert err_kf < err_raw, "KF 必须降低噪声方差"

    print(f"最终估计 = {estimates[-1]:.4f} (真实 5.0)")
    print(f"原始测量 MSE = {err_raw:.4f}, KF 后 MSE = {err_kf:.4f}")
```

**运行说明**：`python -X utf8 本文件名.py` 即可；预期输出"最终估计 ≈ 5.0、KF 后 MSE < 原始 MSE"。

## 5. 最小手算例子

**题目**：一维系统 $A=1, H=1, Q=0.1, R=1$。$\hat{x}_{0|0}=0, P_{0|0}=1$，$u=0$，测量 $z_1=2$。求 $\hat{x}_{1|1}$。

**解**：
$$
P_{1|0} = 1+0.1 = 1.1,\quad K_1 = \frac{1.1}{1.1+1}=0.524,\quad \hat{x}_{1|1} = 0 + 0.524(2-0) = 1.048
$$
**解读**：模型信度与测量信度接近（$P^-=1.1$ vs $R=1$），增益约 0.52，估计取两者中点附近。

## 6. 常见误区

| 误区 | 正确理解 |
|:---|:---|
| "KF 能处理非线性" | 标准 KF 只适用于线性系统；非线性必须用 EKF/UKF/PF |
| "噪声不是高斯也能最优" | 高斯假设是 KF 最优性的前提，破坏后只是"最优中的次优" |
| "$Q,R$ 随便设" | $Q/R$ 决定增益与收敛行为，须按噪声模型/Allan 方差标定 |
| "KF 一定收敛" | 能观性 + 模型准确 + 噪声合理三者缺一会发散（见 [[稳定性\|稳定性]]） |
| 增益一直要在线算 | 时不变系统增益收敛到常值，可离线求解（见 [[稳态KF\|稳态KF]]） |

## 7. 检索练习（闭卷）

1. 默写 KF 的 5 大递推公式并说明每一步含义；
2. 推导（简述）增益为何取 $P_{k|k-1}H^\top(HP_{k|k-1}H^\top+R)^{-1}$；
3. 说明 $R\to 0$ 与 $Q\to 0$ 两个极端下滤波器行为；
4. 手算上面的最小例子（换 $R=9$ 观察增益变化）。

## 8. 通过标准

- 能默写并解释 5 大递推公式；
- 能手算一维 KF 两步迭代；
- 能运行 Python 示例并解释收敛现象；
- 能判断非线性/非高斯场景该换什么算法。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/系统与硬件/15-控制与机器人学"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 复习

- 下次复习：重跑 Python 示例（改 $Q=1.0$ 观察增益与抖动）；
- 薄弱点写入 [[控制与机器人学错题漏洞入口]]；
- 关联：[[问题设定\|问题设定]]、[[EKF非线性状态估计\|EKF非线性状态估计]]。

## 参考文献

- Kalman, R. E. (1960). A new approach to linear filtering and prediction problems. *Journal of Basic Engineering*, 82(1), 35-45. https://doi.org/10.1115/1.3662552
- Thrun, S., Burgard, W., & Fox, D. (2005). *Probabilistic Robotics*. MIT Press. Ch.3.
- Gelb, A. (1974). *Applied Optimal Estimation*. MIT Press.
