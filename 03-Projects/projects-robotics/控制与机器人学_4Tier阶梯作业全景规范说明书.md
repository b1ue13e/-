---
title: "控制与机器人学 4-Tier 阶梯作业全景规范说明书"
type: project
topic: "控制与机器人学 4-Tier 阶梯作业规范"
course: "控制与机器人学"
created: 2026-08-02
updated: 2026-08-02
status: active
flow: project
kind: moc
tags: [控制与机器人学, 4Tier作业, 阶梯作业, 编程实战, PyTest, ModernRobotics, Underactuated]
---

# 🤖 控制与机器人学 4-Tier 阶梯作业全景规范说明书 (Modern Robotics 范式)

> 本说明书为 **15-控制与机器人学** 路径（基于 Kevin Lynch《Modern Robotics》与 MIT 6.832 Underactuated Robotics）提供严格的 **4-Tier Baseline** 划分标准与测试校验 Harness 规范。

---

## 🧭 4-Tier Baseline 梯队划分原则

```
🟢 L1 - Simple Baseline   │ Python Control 库调包 / 齐次变换矩阵乘法
🟡 L2 - Medium Baseline   │ 根轨迹 (Root Locus) 与 伯德图 (Bode Plot) 绘制 / 基础 PID 控制调参
🔴 L3 - Strong Baseline   │ [核心] 不调用高级机器人库，从零手撕 旋量理论 (Screw Theory) 运动学正逆解 / LQR 控制器 / RRT 路径规划
👑 L4 - Boss Baseline     │ 线性模型预测控制 (MPC) / 基于控制屏障函数 (CBF) 的避障安全控制
```

---

## 🎯 控制与机器人学阶梯作业 4-Tier 细化规格清单

### 1. HW01 - 刚体运动与旋量理论 (Rigid Body Motions & Screw Theory)
- **开源溯源**：Modern Robotics Ch 3-4
- 🟢 **L1**: 实现三维空间的旋转矩阵 (Rotation Matrix) 与齐次变换矩阵 (Homogeneous Transformation) 运算。
- 🟡 **L2**: 实现欧拉角 (Euler Angles)、四元数 (Quaternions) 与旋转矩阵的相互转换。
- 🔴 **L3 (手撕核心)**：**基于旋量理论 (Screw Theory)，从零手撕 指数坐标 (Exponential Coordinates) 映射，以及机器人开链正向运动学 (Forward Kinematics, FK)**：
  $$ T(\theta) = e^{[\mathcal{S}_1]\theta_1} e^{[\mathcal{S}_2]\theta_2} \cdots e^{[\mathcal{S}_n]\theta_n} M $$
- 👑 **L4**: 实现李群 $SE(3)$ 与李代数 $se(3)$ 上的伴随变换 (Adjoint Transformation) 运算引擎。

### 2. HW02 - 逆运动学与雅可比矩阵 (Inverse Kinematics & Velocity Kinematics)
- **开源溯源**：Modern Robotics Ch 5-6
- 🟢 **L1**: 对 2-DOF 平面机械臂使用几何法解析求解逆运动学 (IK)。
- 🟡 **L2**: 计算机器人各关节的空间雅可比矩阵 (Space Jacobian) 与物体雅可比矩阵 (Body Jacobian)。
- 🔴 **L3 (手撕核心)**：**手撕 基于伪逆雅可比矩阵 (Pseudo-Inverse Jacobian) 的牛顿-拉夫逊 (Newton-Raphson) 迭代数值逆运动学求解器**，用于任意 6-DOF 机械臂。
- 👑 **L4**: 实现考虑奇异点 (Singularity) 回避的阻尼最小二乘法 (Damped Least Squares) IK。

### 3. HW03 - 动力学与 LQR 最优控制 (Dynamics & Linear Quadratic Regulator)
- **开源溯源**：Modern Robotics Ch 8 / MIT Underactuated Lec 1-3
- 🟢 **L1**: 利用拉格朗日方程手工推导倒立摆 (Inverted Pendulum) 的动力学方程。
- 🟡 **L2**: 设计 PID 控制器使一维倒立摆保持在不平衡直立点。
- 🔴 **L3 (手撕核心)**：**从零手撕 离散时间代数黎卡提方程 (DARE) 求解器，构建无限视野 LQR 最优控制器** $u = -Kx$，实现多连杆机器人的极点配置与镇定。
- 👑 **L4**: 实现迭代 LQR (iLQR) 用于非线性系统的轨迹优化 (Trajectory Optimization)。

### 4. HW04 - 路径规划与碰撞检测 (Path Planning & Collision Avoidance)
- **开源溯源**：Modern Robotics Ch 10
- 🟢 **L1**: 在 2D 栅格地图上使用 $A^*$ 算法寻找最短无碰撞路径。
- 🟡 **L2**: 为生成的一维路径点添加五次多项式时间缩放 (Quintic Time Scaling) 轨迹生成。
- 🔴 **L3 (手撕核心)**：**从零手撕 RRT (Rapidly-exploring Random Tree) 与 RRT* 算法**，实现在复杂多边形障碍物环境中的概率完备机器人关节空间 (C-Space) 路径规划。
- 👑 **L4**: 实现控制屏障函数 (Control Barrier Functions, CBF) 结合二次规划 (QP) 的实时反应式避障控制。

---

## 🧪 测试校验 Harness 规范 (`pytest`)

在 `03-Projects/projects-robotics/tests/` 目录下运行单元测试：

```bash
pytest 03-Projects/projects-robotics/tests/test_hw01_forward_kinematics.py
pytest 03-Projects/projects-robotics/tests/test_hw02_inverse_kinematics.py
pytest 03-Projects/projects-robotics/tests/test_hw03_lqr.py
```
