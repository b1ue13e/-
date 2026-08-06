---
type: study
topic: "ODE数值解"
course: "控制与机器人学"
created: 2026-04-18
updated: 2026-08-06
status: completed
difficulty: intermediate
stage_moc: "[[🧭 阶段1-控制地基]]"
flow: knowledge
kind: concept
concept: ["数值积分", "欧拉法", "龙格库塔法"]
prerequisites: ["ODE基础", "Python编程基础"]
related: ["ODE基础", "线性ODE"]
upstream: ["[[01-控制地基/ODE基础]]"]
source: "Modern Control Engineering (Ogata); scipy.integrate.solve_ivp 文档"
tags: [学习, 控制与机器人学, 数值方法]
---

# ODE数值解

## 0. 为什么学它

大部分真实系统（非线性、时变）没有解析解，只能数值求解。**欧拉法**建立直觉，**四阶龙格-库塔（RK4）**是工程默认工具，`scipy.integrate.solve_ivp` 则让仿真一行搞定。所有后续仿真（倒立摆、车辆、MPC）都建立在这套数值积分之上。

## 1. 核心方法

**问题**：$\dot{x}=f(t,x),\ x(t_0)=x_0$，步长 $h$。

**欧拉法**（一阶精度）：
$$x_{k+1}=x_k+h\,f(t_k,x_k)$$

**RK4**（四阶精度）：
$$x_{k+1}=x_k+\frac{h}{6}(k_1+2k_2+2k_3+k_4)$$
$$k_1=f(t_k,x_k),\quad k_2=f(t_k+\tfrac h2,\ x_k+\tfrac h2 k_1),\quad k_3=f(t_k+\tfrac h2,\ x_k+\tfrac h2 k_2),\quad k_4=f(t_k+h,\ x_k+h k_3)$$

**收敛性**：欧拉全局误差 $O(h)$，RK4 为 $O(h^4)$；步长减半误差约降为 $1/2^p$。

## 2. 最小可手算例子

**题目**：$\dot{x}=-x,\ x(0)=1$，用欧拉法 $h=0.5$ 计算 $x(1)$。

**解**：
- $x(0.5)=1+0.5\times(-1)=0.5$；
- $x(1)=0.5+0.5\times(-0.5)=0.25$。
解析解 $x(1)=e^{-1}\approx0.368$，欧拉误差约 0.118（步长越小越准）。

**易错点**：用旧 $x_k$ 而非更新值；$f$ 内状态混用新旧值。

## 3. Python 最小实现

```python
import numpy as np
from scipy.integrate import solve_ivp

def f(t, x):
    return -x

sol = solve_ivp(f, [0, 5], [1.0], method='RK45', max_step=0.01)
print(sol.y[0, -1])  # ≈ e^-5 ≈ 0.0067
```

## 4. 常见误区

| 误区 | 正确理解 |
|:---|:---|
| 欧拉法对所有系统足够 | 刚性系统/高精度需要 RK45、隐式法 |
| 步长越小一定越好 | 过小步长引入舍入误差与耗时，需平衡 |
| 数值发散=系统不稳定 | 也可能是步长过大导致数值不稳定（区分二者） |

## 5. 与后续知识连接

- [[ODE基础]]：被求解的对象；
- 工程：车辆动力学仿真、倒立摆仿真、MPC 预测模型离散化都用数值积分；
- [[离散状态空间]]（阶段 9）：MPC 的离散化基础。

## 6. 检索练习（闭卷）

1. 写出欧拉法与 RK4 公式；
2. 用欧拉法 $h=0.25$ 手算 $\dot{x}=x,\ x(0)=1$ 的 $x(1)$；
3. 解释 RK4 比欧拉法精度高的原因；
4. 区分"数值不稳定"与"系统不稳定"。

## 7. 通过标准

- 能手算欧拉法一步/多步；
- 能写出 RK4 公式；
- 能用 solve_ivp 仿真一阶/二阶系统；
- 能解释步长与精度的关系。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/系统与硬件/15-控制与机器人学"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 复习

- 下次复习：3 天后用 Python 重跑例子并比较步长；
- 薄弱点写入 [[控制与机器人学错题漏洞入口]]。
