---
type: study
topic: "ODE初值问题与Runge-Kutta"
course: "数值分析"
created: 2026-08-08
status: ongoing
stage_moc: "[[🧭 阶段3-非线性与ODE数值解]]"
upstream: ["[[数值分析-前置-泰勒展开与截断误差]]"]
flow: knowledge
kind: concept
tags: [学习, 数值分析, 常微分方程, 初值问题, RungeKutta, 局部截断误差]
---

# 数值分析-ODE初值问题与Runge-Kutta

> "ODE 数值积分的本质是在离散网格上对斜率场进行数值积分。Runge-Kutta 方法通过在步长区间内巧妙采样多个中间斜率，实现了完全无需计算高阶解析导数的高阶精度。"

---

## 1. 严密数学定义与误差阶体系

考虑初值问题（IVP）：
$$y'(t) = f(t, y(t)), \quad y(t_0) = y_0$$

### 局部截断误差（LTE）与全局误差（Global Error）
设网格步长 $h = t_{n+1} - t_n$。
- **局部截断误差**：假定前一步精确，单步产生的偏差：
  $$d_{n+1} = y(t_{n+1}) - [y(t_n) + h \Phi(t_n, y(t_n), h)] = O(h^{p+1})$$
- **全局误差**：累积经过 $N = (T-t_0)/h$ 步后的总误差：
  $$e_N = |y(t_N) - y_N| = O(h^p)$$
  （全局误差阶比局部截断误差阶低 1 阶，因为累积了 $O(1/h)$ 步）。

### 经典四阶 Runge-Kutta 公式 (RK4)
$$y_{n+1} = y_n + \frac{h}{6}(k_1 + 2k_2 + 2k_3 + k_4)$$
其中：
$$\begin{cases}
k_1 = f(t_n, y_n) \\
k_2 = f\left(t_n + \frac{h}{2}, y_n + \frac{h}{2} k_1\right) \\
k_3 = f\left(t_n + \frac{h}{2}, y_n + \frac{h}{2} k_2\right) \\
k_4 = f(t_n + h, y_n + h k_3)
\end{cases}$$
RK4 的局部截断误差为 $O(h^5)$，全局收敛阶为严格的**四阶精度 $O(h^4)$**。

---

## 2. Python 步长倍减与收敛阶验证

```python
import numpy as np

# 测试问题: y' = -y, y(0)=1, 精确解 y(t) = exp(-t)
f = lambda t, y: -y
exact = lambda t: np.exp(-t)

def rk4_step(f, t, y, h):
    k1 = f(t, y)
    k2 = f(t + 0.5*h, y + 0.5*h*k1)
    k3 = f(t + 0.5*h, y + 0.5*h*k2)
    k4 = f(t + h, y + h*k3)
    return y + (h/6.0) * (k1 + 2*k2 + 2*k3 + k4)

# 步长序列
hs = [0.2, 0.1, 0.05, 0.025]
errors = []
for h in hs:
    t, y = 0.0, 1.0
    while t < 1.0 - 1e-10:
        y = rk4_step(f, t, y, h)
        t += h
    errors.append(abs(y - exact(1.0)))

orders = [np.log(errors[i]/errors[i+1])/np.log(2) for i in range(len(errors)-1)]
print("RK4 实测收敛阶:", [round(o, 2) for o in orders])
```

---

## 3. 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

---

## 4. 检索练习与自测

1. 写出一般 $s$ 级显式 Runge-Kutta 方法的 Butcher 增广表（Butcher Tableau）。
2. 解释嵌入式 Runge-Kutta（如 RKF45 / Dormand-Prince 5(4)）如何利用同一组斜率计算局部误差并自适应调整步长。
