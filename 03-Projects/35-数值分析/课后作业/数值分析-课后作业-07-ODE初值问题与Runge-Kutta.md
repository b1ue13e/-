---
type: project
project_type: homework
course: "数值分析"
assignment_id: "数值分析-HW07"
assignment_level: lesson
assignment_format: lab
stage_id: "03"
requires: ["[[03-非线性与ODE数值解/数值分析-ODE初值问题与Runge-Kutta|数值分析-ODE初值问题与Runge-Kutta]]"]
source_type: official_assignment
created: 2026-08-08
updated: 2026-08-08
status: active
flow: project
tags: [作业, 课后作业, 数值分析, ODE数值解, Runge-Kutta, RK4, 局部截断误差]
---

# 数值分析-课后作业-07-ODE初值问题与Runge-Kutta

> 对齐官方源：**MIT 18.330 Problem Set 5 (Initial-Value Problems & Runge-Kutta)** 与 **FNC Chapter 7**

---

## 1. 学习目标与动机
- 理解常微分方程初值问题（IVP）单步法中局部截断误差（LTE）与全局误差（Global Error）的积累机理；
- 独立编写经典四阶 Runge-Kutta（RK4）积分器；
- 在已知解析解的非线性摆方程上，实测验证 RK4 的四阶代数收敛性 $O(h^4)$。

---

## 2. 任务边界与输入输出
- **输入**：一阶 ODE 系统导数函数 $f(t, y)$、初值 $y(t_0) = y_0$、积分区间 $[t_0, T]$ 及步长 $h$。
- **输出**：离散时间网格序列 $t_n$、数值解轨迹矩阵 $Y \in \mathbb{R}^{(N+1) \times d}$ 与实测全局误差斜率。

---

## 3. 详细实验任务与算法规范

### 任务 1：四阶 Runge-Kutta 积分器实现
实现函数 `rk4_solve(f, y0, t_span, h)`：
1. $k_1 = f(t_n, y_n)$；
2. $k_2 = f\left(t_n + \frac{h}{2}, y_n + \frac{h}{2} k_1\right)$；
3. $k_3 = f\left(t_n + \frac{h}{2}, y_n + \frac{h}{2} k_2\right)$；
4. $k_4 = f(t_n + h, y_n + h k_3)$；
5. $y_{n+1} = y_n + \frac{h}{6}(k_1 + 2k_2 + 2k_3 + k_4)$。

### 任务 2：非线性摆动力系统测试
考虑大角度非线性单摆方程（降阶为一维系统）：
$$\frac{d}{dt}\begin{bmatrix} \theta \\ \omega \end{bmatrix} = \begin{bmatrix} \omega \\ -\sin \theta \end{bmatrix}, \quad \theta(0) = \frac{\pi}{2}, \; \omega(0) = 0$$
在 $t \in [0, 10]$ 上积分，验证系统机械能守恒指标。

### 任务 3：收敛阶数实测（Convergence Rate Study）
对测试方程 $y' = y, \; y(0) = 1$（真解 $y(1) = e$）：
取步长序列 $h = [0.1, 0.05, 0.025, 0.0125]$，计算全局绝对误差，验证双对数拟合斜率是否严格等于 4.0。

---

## 4. 提交产物与代码规范
- 代码文件：`03-Projects/35-数值分析/scripts/hw07_runge_kutta.py`
- 自动化测试：集成至 `03-Projects/35-数值分析/tests/test_numerical_analysis.py`

---

## 5. 验收标准（Rubric）

| 验收维度 | 达标分 | 满分要点 |
| :--- | :---: | :--- |
| **RK4 实现正确性** | 35 | 单步测试 Butcher 格式匹配无误，能处理标量与多维向量系统 |
| **四阶收敛阶验证** | 40 | 双对数实测收敛斜率在 $[3.95, 4.05]$ 之间，严格展示四阶精度 |
| **动力系统能量监控** | 25 | 非线性摆长时积分中能量漂移与理论预期一致 |

---

## 6. 引导自检与易错陷阱
- **陷阱**：在计算 $k_2, k_3, k_4$ 时，时间参数 $t_n + h/2$ 被错误地写成了 $t_n$，导致在非自治系统（$f$ 显含 $t$）上降阶为二阶精度。

---

## 7. Starter Code 与可执行基线

```python
import numpy as np

def rk4_step(f, t, y, h):
    k1 = f(t, y)
    k2 = f(t + 0.5 * h, y + 0.5 * h * k1)
    k3 = f(t + 0.5 * h, y + 0.5 * h * k2)
    k4 = f(t + h, y + h * k3)
    return y + (h / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
```
