---
title: "PID 控制器与状态空间法 (PID Controller and State Space Method)"
course: "控制与机器人学"
type: study
stage_moc: "[[🧭 阶段5-状态空间与现代控制]]"
flow: knowledge
kind: concept
tags:
  - 控制与机器人学
  - PID控制器
  - 状态空间法
  - 反馈控制
  - 可控性与可观性
  - 极点配置
status: completed
created: 2026-08-01
updated: 2026-08-07
---

# PID 控制器与状态空间法 (PID Controller and State Space Method)

## 1. PID 控制器与状态空间法的定义与控制范式

**PID 控制器与状态空间法 (PID Controller and State Space Method)** 的核心定义是：结合经典无模型 SISO 误差反馈控制 (PID) 与现代多变量 MIMO 状态变量建模 (State-Space) 的自动化控制理论体系。经典 PID 控制器与状态空间法由 Minorsky (1922) 与 Kalman (1960) 建立奠基。

**基本性质与双重范式**：
1. **经典 PID 控制器 (Proportional-Integral-Derivative)**：基于比例 (P 减少当前误差)、积分 (I 消除稳态误差)、微分 (D 预测未来趋势) 的无模型三项组合控制；
2. **现代状态空间法 (State-Space Representation)**：在时域内将系统建模为一阶向量微分方程组 $\dot{\mathbf{x}} = A \mathbf{x} + B \mathbf{u}$ 与 $\mathbf{y} = C \mathbf{x} + D \mathbf{u}$；
3. **可控性与可观性 (Controllability & Observability)**：系统的状态可控性矩阵 $\mathcal{C} = [B, AB, \dots, A^{n-1} B]$ 与可观性矩阵 $\mathcal{O}$ 判定能否通过状态反馈任意配置系统闭环极点。

---

## 2. PID 离散化控制律与状态空间极点配置形式化推导

**PID 连续控制律与位置式离散化推导**：
连续时间 PID 输出 $u(t) = K_p e(t) + K_i \int_0^t e(\tau) d\tau + K_d \frac{de(t)}{dt}$。采用后向差分离散化：
$$u(k) = K_p e(k) + K_i T_s \sum_{i=0}^k e(i) + K_d \frac{e(k) - e(k-1)}{T_s}$$
增量式 PID 公式：$\Delta u(k) = u(k) - u(k-1) = K_p [e(k) - e(k-1)] + K_i T_s e(k) + \frac{K_d}{T_s} [e(k) - 2e(k-1) + e(k-2)]$。

**状态空间法全状态反馈极点配置推导**：
1. 设控制输入 $\mathbf{u} = -K \mathbf{x}$（其中 $K$ 为反馈增益矩阵）；
2. 代入状态方程得闭环系统：$\dot{\mathbf{x}} = (A - B K) \mathbf{x}$；
3. **Kalman 极点配置定理**：若系统阶数为 $n$，且可控性矩阵满秩 $\text{rank}(\mathcal{C}) = n$，则存在唯一的 $K$，使得闭环系统特征方程 $\det(s I - (A - B K)) = 0$ 的根恰好匹配预设的任意稳定极点集合 $\{\mu_1, \dots, \mu_n\}$；
4. **因此**，状态空间法彻底克服了 PID 控制在多输入多输出 (MIMO) 系统中的耦合与极点配置困难。

---

## 3. 经典 PID 控制器与现代状态空间法全方位对比

| 维度 | 经典 PID 控制器 | 现代状态空间法 (State-Space) |
|:---|:---|:---|
| **系统建模需求** | **无需精确物理模型** (无模型/黑盒) | **依赖精确的线性/非线性状态转移矩阵 $A, B$** |
| **适用变量类型** | 单输入单输出 (SISO) | **多输入多输出 (MIMO) / 多变量** |
| **系统内部可观测** | 仅关注外部输入输出 (IO 关系) | **可深入洞察与控制内部状态向量 $\mathbf{x}$** |
| **极点配置能力** | 受限于 3 个标量参数参数试凑 | **可通过增益矩阵 $K$ 任意精确配置闭环极点** |
| **典型应用** | 工业温控、电机调速、无人机姿态 | 航空航天导引、机器人关节臂、LQR 最优控制 |

**局限（误区与反例）**：PID 控制器中积分项易产生**积分饱和 (Integral Windup)**，导致大误差下系统严重超调或振荡；状态空间法若物理模型矩阵 $A, B$ 存在建模误差，全状态反馈的鲁棒性将急剧下降。

关联知识点推荐：[[卡尔曼滤波KalmanFilter]]、[[拉普拉斯变换]]、[[拟牛顿法BFGS]]、[[红黑树]]。

---

## 4. Python 手写增量式 PID 控制器与状态空间可控性自测断言

```python
import numpy as np

class IncrementalPID:
    """手写离散增量式 PID 控制器"""
    def __init__(self, Kp: float, Ki: float, Kd: float, Ts: float = 0.01):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.Ts = Ts
        self.e1 = 0.0
        self.e2 = 0.0
        self.u = 0.0

    def update(self, target: float, current: float) -> float:
        e0 = target - current
        du = (self.Kp * (e0 - self.e1) +
              self.Ki * self.Ts * e0 +
              (self.Kd / self.Ts) * (e0 - 2.0 * self.e1 + self.e2))
        self.u += du
        self.e2 = self.e1
        self.e1 = e0
        return self.u

def check_controllability(A: np.ndarray, B: np.ndarray) -> bool:
    """计算状态空间矩阵可控性矩阵 C = [B, AB, A^2 B ... ] 秩"""
    n = A.shape[0]
    C_list = [B]
    for i in range(1, n):
        C_list.append(np.linalg.matrix_power(A, i) @ B)
    C_mat = np.hstack(C_list)
    return bool(np.linalg.matrix_rank(C_mat) == n)

if __name__ == "__main__":
    # 1. 增量式 PID 自测断言
    pid = IncrementalPID(Kp=1.0, Ki=0.5, Kd=0.1, Ts=0.01)
    target = 10.0
    val = 0.0
    for _ in range(50):
        u = pid.update(target, val)
        val += u * 0.1  # 简单一阶系统仿真

    # 验证稳态误差接近 0
    assert abs(target - val) < 0.5, f"PID 追逐未收敛: {val}"

    # 2. 状态空间可控性自测断言: 经典双积分系统 A=[[0,1],[0,0]], B=[[0],[1]]
    A = np.array([[0.0, 1.0], [0.0, 0.0]])
    B = np.array([[0.0], [1.0]])
    assert check_controllability(A, B) == True, "双积分系统必须满秩可控"

    print(f"PID 控制器与状态空间法 测试成功! 跟踪目标 10.0 -> {val:.2f}")
    print("PID 控制器与状态空间法 单元测试与自查验证全部成功！")
```

---

## 5. 权威参考文献
- Minorsky, N. (1922). Directional stability of automatically steered bodies. *Journal of the American Society for Naval Engineers*, 34(2), 280-309. DOI: https://doi.org/10.1111/j.1559-3584.1922.tb04958.x
- Ogata, K. (2010). *Modern Control Engineering* (5th ed.). Prentice Hall. Chapter 10 (Control Systems Analysis and Design in State Space). ISBN: 978-0136156734. URL: https://www.pearson.com/en-us/subject-catalog/p/modern-control-engineering/P200000003265
- Kalman, R. E. (1960). On the general theory of control systems. *Proceedings of the First International Congress of IFAC*, 481-492.
