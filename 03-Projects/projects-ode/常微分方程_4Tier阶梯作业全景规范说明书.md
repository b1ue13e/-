---
title: "常微分方程 4-Tier 阶梯作业全景规范说明书"
type: project
topic: "常微分方程 4-Tier 阶梯作业规范"
course: "常微分方程"
created: 2026-08-02
updated: 2026-08-02
status: active
flow: project
kind: moc
tags: [常微分方程, 4Tier作业, 阶梯作业, 编程实战, PyTest, MIT1803]
---

# 🌀 常微分方程 4-Tier 阶梯作业全景规范说明书 (MIT 18.03 & Arnold 范式)

> 本说明书为 **06-常微分方程** 路径（基于 MIT 18.03 与 V.I. Arnold《常微分方程》）提供严格的 **4-Tier Baseline** 划分标准与测试校验 Harness 规范。

---

## 🧭 4-Tier Baseline 梯队划分原则

```
🟢 L1 - Simple Baseline   │ SciPy `odeint` / `solve_ivp` 调包求解 / 绘制方向场 (Direction Field)
🟡 L2 - Medium Baseline   │ 龙格-库塔法 (RK4) / 拉普拉斯变换分析线性系统
🔴 L3 - Strong Baseline   │ [核心] 不调用 SciPy，从零手撕 隐式欧拉法 (Implicit Euler) / 刚性方程 (Stiff ODE) 求解器 / 雅可比矩阵
👑 L4 - Boss Baseline     │ 辛积分器 (Symplectic Integrators) / 微分方程的几何动力学流形分析 (相空间可视化)
```

---

## 🎯 常微分方程阶梯作业 4-Tier 细化规格清单

### 1. HW01 - 一阶微分方程与方向场 (First-Order ODEs & Direction Fields)
- **开源溯源**：MIT 18.03 Unit 1 / Arnold Ch 1
- 🟢 **L1**: 针对一阶方程 $y' = f(x,y)$，使用 matplotlib 画出方向场及几条积分曲线。
- 🟡 **L2**: 实现显式欧拉法 (Explicit Euler) 求解 IVP (初值问题)，并计算截断误差阶数。
- 🔴 **L3 (手撕核心)**：**手撕 隐式欧拉法 (Implicit Euler) 与 牛顿-拉夫逊 (Newton-Raphson) 迭代求解非线性刚性微分方程**。
- 👑 **L4**: 实现自适应步长的 Runge-Kutta-Fehlberg (RK45) 算法。

### 2. HW02 - 二阶线性常系数微分方程 (Second-Order Linear ODEs)
- **开源溯源**：MIT 18.03 Unit 2
- 🟢 **L1**: 分析阻尼谐振子 (Damped Harmonic Oscillator) $mx'' + bx' + kx = 0$，分类过阻尼、临界阻尼、欠阻尼。
- 🟡 **L2**: 利用待定系数法计算特解 (Particular Solution)，并可视化共振现象 (Resonance)。
- 🔴 **L3 (手撕核心)**：**手撕 拉普拉斯变换 (Laplace Transform) 符号计算与留数定理计算逆拉普拉斯变换 (Inverse Laplace) 生成解析解**。
- 👑 **L4**: 实现状态空间法 (State-Space Formulation) $\dot{\mathbf{x}} = A\mathbf{x}$ 的矩阵指数 $e^{At}$ 高效计算。

### 3. HW03 - 线性方程组与相平面分析 (Systems of ODEs & Phase Plane)
- **开源溯源**：MIT 18.03 Unit 3 / Arnold Ch 3
- 🟢 **L1**: 求解 $2 \times 2$ 常系数线性方程组，绘制特征值不同情况下的相平面 (Phase Portrait：节点、鞍点、焦点、中心)。
- 🟡 **L2**: 实现洛伦兹吸引子 (Lorenz Attractor) 混沌系统的 3D 轨迹求解与动画绘制。
- 🔴 **L3 (手撕核心)**：**手撕 雅可比矩阵 (Jacobian Matrix) 局部线性化算法，用于非线性系统平衡点 (Equilibrium Points) 的稳定性判定**。
- 👑 **L4**: 构建李雅普诺夫函数 (Lyapunov Function) 的数值验证系统。

### 4. HW04 - 傅里叶级数与边值问题 (Fourier Series & Boundary Value Problems)
- **开源溯源**：MIT 18.03 Unit 4
- 🟢 **L1**: 计算方波、三角波的傅里叶级数展开，并可视化随项数增加的逼近效果。
- 🟡 **L2**: 使用 SciPy `solve_bvp` 求解两点边值问题 (BVP)。
- 🔴 **L3 (手撕核心)**：**手撕 打靶法 (Shooting Method) 求解非线性边值问题，利用二分法调整初始斜率使得边界残差为零**。
- 👑 **L4**: 基于有限差分法 (Finite Difference Method, FDM) 将 BVP 转化为大型稀疏矩阵方程 $AU = F$ 并手写共轭梯度法 (CG) 求解。

---

## 🧪 测试校验 Harness 规范 (`pytest`)

在 `03-Projects/projects-ode/tests/` 目录下运行单元测试：

```bash
pytest 03-Projects/projects-ode/tests/test_hw01_implicit_euler.py
pytest 03-Projects/projects-ode/tests/test_hw03_jacobian.py
pytest 03-Projects/projects-ode/tests/test_hw04_shooting_method.py
```
