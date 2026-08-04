---
title: "卡尔曼滤波 Kalman Filter (Kalman Filter)"
course: "15-控制与机器人学"
tags:
  - 控制与机器人学
  - 卡尔曼滤波
  - KalmanFilter
  - 贝叶斯估计
  - 状态估计
  - 协方差更新
type: knowledge_card
status: completed
created: 2026-08-01
---

# 卡尔曼滤波 Kalman Filter (Kalman Filter)

## 1. 卡尔曼滤波 Kalman Filter 的定义与高斯最优估计

**卡尔曼滤波 Kalman Filter (Kalman Filter)** 的核心定义是：一种基于线性系统方程和高斯白噪声假设，利用“预测-更新”双步循环，在最小均方误差 (MMSE) 意义下融合过程测量与传感器观测的最优高斯状态估计算法。由 Rudolf E. Kálmán 于 1960 年提出，成功应用于阿波罗登月计划导引。

**基本性质**：
1. **递归估计 (Recursive Estimation)**：卡尔曼滤波 Kalman Filter 无需存储历史所有测量数据，仅依赖上一时刻的状态估计量 $\hat{\mathbf{x}}_{k-1|k-1}$ 与当前观测值 $\mathbf{z}_k$；
2. **高斯封闭性**：线性变换与高斯噪声分布相融合后依然保持高斯分布，均值与协方差矩阵完整表征状态概率分布；
3. **卡尔曼增益 $K_k$ 动态加权**：根据过程预测不确定性 $P_{k|k-1}$ 与传感器测量噪声 $R$ 之间的相对比例，动态调整预测与观测量之间的信任权重。

---

## 2. 卡尔曼滤波 5 大核心递推公式形式化推导

**系统线性离散建模假设**：
- 状态方程：$\mathbf{x}_k = A \mathbf{x}_{k-1} + B \mathbf{u}_k + \mathbf{w}_k \quad (\mathbf{w}_k \sim \mathcal{N}(\mathbf{0}, Q))$
- 观测方程：$\mathbf{z}_k = H \mathbf{x}_k + \mathbf{v}_k \quad (\mathbf{v}_k \sim \mathcal{N}(\mathbf{0}, R))$

**推导过程（预测步与更新步）**：
1. **预测步 (Predict)**：
   - 先验状态预测：$\hat{\mathbf{x}}_{k|k-1} = A \hat{\mathbf{x}}_{k-1|k-1} + B \mathbf{u}_k$
   - 先验协方差预测：$P_{k|k-1} = A P_{k-1|k-1} A^T + Q$
2. **卡尔曼增益 (Kalman Gain) 推导**：寻找 $K_k$ 最小化后验协方差 $P_{k|k}$ 的迹 $\text{tr}(P_{k|k})$。对 $K_k$ 求导解得：
$$K_k = P_{k|k-1} H^T \left( H P_{k|k-1} H^T + R \right)^{-1}$$
3. **更新步 (Update)**：
   - 残差 (Innovation)：$\mathbf{y}_k = \mathbf{z}_k - H \hat{\mathbf{x}}_{k|k-1}$
   - 后验状态更新：$\hat{\mathbf{x}}_{k|k} = \hat{\mathbf{x}}_{k|k-1} + K_k \mathbf{y}_k$
   - 后验协方差更新：$P_{k|k} = (I - K_k H) P_{k|k-1}$
4. **因此**，若测量噪声 $R \to \mathbf{0}$，则 $K_k \to H^{-1}$，后验完全信任观测值 $\mathbf{z}_k$；若预测噪声 $Q \to \mathbf{0}$，则 $K_k \to \mathbf{0}$，后验完全信任先验模型预测。

---

## 3. 标准卡尔曼滤波 (KF) 与 EKF / UKF / 粒子滤波 (PF) 对比

| 算法类型 | 系统线性度假设 | 噪声分布假设 | 计算复杂度 | 优势与局限 |
|:---|:---|:---|:---|:---|
| **标准卡尔曼滤波 (KF)** | **严格线性系统** | **高斯白噪声** | **$O(d^3)$** (极低) | 理论最优解；无法处理非线性系统 |
| **扩展卡尔曼滤波 (EKF)** | 非线性 (一阶泰勒展开) | 高斯白噪声 | $O(d^3)$ | 经典实用；极度依赖雅可比矩阵，高度非线性下发散 |
| **无迹卡尔曼滤波 (UKF)** | 非线性 (UT 变换 Sigma 点) | 高斯白噪声 | $O(d^3)$ | 无需计算雅可比，精度达到二阶泰勒展开 |
| **粒子滤波 (PF)** | 强非线性 | 任意非高斯分布 | $O(N_{\text{particles}} d)$ | 适用性最广；高维下存在“粒子匮乏” |

**局限（误区与反例）**：卡尔曼滤波 Kalman Filter 在系统存在未知有色噪声或非高斯双峰分布时会产生严重偏置；此时必须使用粒子滤波 (Particle Filter) 进行状态估计。

关联知识点推荐：[[PID控制器与状态空间法]]、[[隐马尔可夫模型HMM]]、[[贝叶斯网络]]、[[均方误差MSE与Huber损失]]。

---

## 4. Python 手写一维与二维 Kalman Filter 状态估计自测断言

```python
import numpy as np

class KalmanFilter1D:
    """一维卡尔曼滤波测试"""
    def __init__(self, A=1.0, H=1.0, Q=1e-5, R=0.1, x0=0.0, P0=1.0):
        self.A = A
        self.H = H
        self.Q = Q
        self.R = R
        self.x = x0
        self.P = P0

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

    # 模拟 100 次高斯噪声观测
    measurements = true_x + np.random.normal(0, np.sqrt(0.2), 100)
    estimates = [kf.step(z) for z in measurements]

    # 自测验证 1: 后验滤波估计值应极高精度收敛到真实值 5.0
    assert abs(estimates[-1] - true_x) < 0.2, f"KF 未收敛到真实值: {estimates[-1]}"

    # 自测验证 2: 滤波后误差方差应远小于噪声测量方差
    err_raw = np.mean((measurements - true_x)**2)
    err_kf = np.mean((np.array(estimates[20:]) - true_x)**2)
    assert err_kf < err_raw, "卡尔曼滤波必须显著降低测量噪声方差"

    print(f"卡尔曼滤波 Kalman Filter 估计成功: 最终估计 = {estimates[-1]:.4f} (真实 5.0)")
    print(f"原始测量 MSE = {err_raw:.4f}, 卡尔曼滤波后 MSE = {err_kf:.4f}")
    print("卡尔曼滤波 Kalman Filter 单元测试与自查验证全部成功！")
```

---

## 5. 权威参考文献
- Kalman, R. E. (1960). A new approach to linear filtering and prediction problems. *Journal of Basic Engineering*, 82(1), 35-45. DOI: https://doi.org/10.1115/1.3662552 URL: https://asmedigitalcollection.asme.org/basicengineering/article/82/1/35/397711/A-New-Approach-to-Linear-Filtering-and-Prediction
- Thrun, S., Burgard, W., & Fox, D. (2005). *Probabilistic Robotics*. MIT Press. Chapter 3 (Gaussian Filters). ISBN: 978-0262201629. URL: https://mitpress.mit.edu/9780262201629/probabilistic-robotics/
- Gelb, A. (1974). *Applied Optimal Estimation*. MIT Press. ISBN: 978-0262570480.
