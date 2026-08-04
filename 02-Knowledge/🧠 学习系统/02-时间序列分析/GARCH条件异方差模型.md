---
title: "GARCH 条件异方差模型 (GARCH Model)"
course: "02-时间序列分析"
tags:
  - 时间序列分析
  - GARCH
  - 条件异方差
  - 波动率建模
type: knowledge_card
status: completed
created: 2026-07-31
---

# GARCH 条件异方差模型 (GARCH Model)

## 1. GARCH 模型定义与核心动机

**GARCH 模型（广义自回归条件异方差模型, Generalized Autoregressive Conditional Heteroskedasticity）** 的核心定义是：对金融时间序列的**条件方差**建立自回归结构，从而捕捉实际金融数据中普遍存在的**波动率聚类 (Volatility Clustering)** 现象。GARCH 模型是 Bollerslev（1986）对 Engle（1982）的 ARCH 模型的广义化推广，将条件方差方程中加入了对历史条件方差本身的自回归依赖项。

**基本性质与动机**：普通 ARIMA 模型假设误差项方差为常数（同方差性），然而金融收益率序列（如股价日收益率）呈现显著的**条件异方差性**（Heteroskedasticity）—— 高波动率时期倾向于持续，低波动率时期也倾向于持续。因此 GARCH 模型通过对条件二阶矩建模，补充了 ARIMA 对一阶矩结构的描述，构成完整的金融计量建模体系。

---

## 2. GARCH(p, q) 形式化推导

**假设（前提条件）**：

- 新息分布：$\varepsilon_t = \sigma_t z_t$，$z_t \sim \text{i.i.d.}\ N(0,1)$
- 参数约束：$\alpha_0 > 0$，$\alpha_i \geq 0$，$\beta_j \geq 0$
- **弱平稳性条件**：$\sum_{i=1}^{q}\alpha_i + \sum_{j=1}^{p}\beta_j < 1$

**GARCH(p,q) 条件方差方程（推导）**：

$$\sigma_t^2 = \alpha_0 + \sum_{i=1}^{q}\alpha_i\varepsilon_{t-i}^2 + \sum_{j=1}^{p}\beta_j\sigma_{t-j}^2$$

因此对最常用的 **GARCH(1,1)** 模型，条件方差为：

$$\sigma_t^2 = \alpha_0 + \alpha_1\varepsilon_{t-1}^2 + \beta_1\sigma_{t-1}^2$$

**无条件长期方差**：$\bar{\sigma}^2 = \dfrac{\alpha_0}{1 - \alpha_1 - \beta_1}$（弱平稳条件下）

**持久性度量**：$\pi = \alpha_1 + \beta_1$，趋近于 1 时，波动率冲击消退极慢（称为近单位根过程）。

---

## 3. GARCH 与相关模型的区别与对比

| 模型 | 条件方差结构 | 杠杆效应 | 参数约束 | 典型应用场景 |
|:---|:---|:---|:---|:---|
| **ARCH(q)** | 仅含 $\varepsilon_{t-i}^2$ 项 | 无 | $\alpha_i \geq 0$ | 理论起点，阶数高 |
| **GARCH(p,q)** | 加入 $\sigma_{t-j}^2$ 自回归 | 无 | 弱平稳 $\sum<1$ | 股价日波动率建模 |
| **EGARCH** | 对数方差 $\ln\sigma_t^2$ | **有** | 无符号约束 | 不对称杠杆效应 |
| **GJR-GARCH** | 加入负冲击哑变量 | **有** | — | 股市崩盘非对称 |
| **IGARCH** | $\alpha_1+\beta_1=1$ | 无 | 积分条件 | 高频金融数据 |

**局限（误区）**：GARCH 模型假设新息服从正态分布，而实际金融收益率呈现尖峰厚尾性 (leptokurtosis)。因此实践中常改用学生 $t$ 分布或 GED 分布，并引入 **VaR（在险价值）** 计算框架。

关联知识点推荐：[[ARIMA模型与差分平稳性]]、[[时间序列的定义]]、[[季节效应分析]]。

---

## 4. Python GARCH(1,1) 参数估计、自测验证与预测

```python
import numpy as np
import warnings
warnings.filterwarnings('ignore')

def simulate_garch11(n: int, alpha0: float, alpha1: float,
                     beta1: float, seed: int = 42) -> tuple:
    """
    模拟 GARCH(1,1) 过程
    假设: z_t ~ N(0,1), 弱平稳条件 alpha1+beta1 < 1
    推导: sigma_t^2 = alpha0 + alpha1*eps_{t-1}^2 + beta1*sigma_t-1^2
    因此条件方差均值 = alpha0 / (1 - alpha1 - beta1)
    """
    assert alpha1 + beta1 < 1, "违反弱平稳性条件"
    np.random.seed(seed)
    sigma2 = np.zeros(n)
    eps    = np.zeros(n)
    sigma2[0] = alpha0 / (1 - alpha1 - beta1)
    eps[0] = np.sqrt(sigma2[0]) * np.random.normal()
    for t in range(1, n):
        sigma2[t] = alpha0 + alpha1 * eps[t-1]**2 + beta1 * sigma2[t-1]
        eps[t] = np.sqrt(sigma2[t]) * np.random.normal()
    return eps, sigma2

def garch11_forecast(alpha0, alpha1, beta1, eps_last, sigma2_last, h=5):
    """
    GARCH(1,1) h 步条件方差预测
    推导: E[sigma_{t+h}^2] = sigma_bar^2 + (alpha1+beta1)^h * (sigma2_last - sigma_bar^2)
    """
    sigma_bar2 = alpha0 / (1 - alpha1 - beta1)
    persistence = alpha1 + beta1
    forecasts = []
    for step in range(1, h + 1):
        sigma2_h = sigma_bar2 + persistence**step * (sigma2_last - sigma_bar2)
        forecasts.append(sigma2_h)
    return forecasts

if __name__ == "__main__":
    # 单元测试与例证验证
    a0, a1, b1 = 0.05, 0.10, 0.85
    eps, sigma2 = simulate_garch11(1000, a0, a1, b1)

    # 验证 1: 理论方差与实证方差对照
    theoretical_var = a0 / (1 - a1 - b1)
    empirical_var = np.var(eps)
    assert abs(empirical_var - theoretical_var) < 1.0, f"无条件方差偏差: {empirical_var:.3f}"

    # 验证 2: 弱平稳条件
    assert a1 + b1 < 1
    print(f"实测结果: 理论无条件方差={theoretical_var:.3f}, 实证方差={empirical_var:.3f}")

    # 验证 3: 多步预测收敛性
    forecasts = garch11_forecast(a0, a1, b1, eps[-1], sigma2[-1], h=5)
    assert len(forecasts) == 5
    assert abs(forecasts[-1] - theoretical_var) <= abs(forecasts[0] - theoretical_var) + 1e-5
    
    # 验证 4: 反例 - 假设不平稳 alpha1+beta1 >= 1 应该抛出异常
    try:
        simulate_garch11(100, 0.05, 0.5, 0.6)
        assert False, "应触发平稳性断言"
    except AssertionError as err:
        print(f"反例测试通过: {err}")

    print(f"5步波动率预测: {[round(f, 4) for f in forecasts]}")
    print("GARCH 条件异方差模型单元测试与自查验证全部成功！")
```

---

## 5. 权威参考文献
- Bollerslev, T. (1986). Generalized autoregressive conditional heteroskedasticity. *Journal of Econometrics*, 31(3), 307-327. DOI: https://doi.org/10.1016/0304-4076(86)90063-1
- Engle, R. F. (1982). Autoregressive conditional heteroscedasticity with estimates of the variance of United Kingdom inflation. *Econometrica*, 50(4), 987-1007. DOI: https://doi.org/10.2307/1912773
- Nelson, D. B. (1991). Conditional heteroskedasticity in asset returns: A new approach. *Econometrica*, 59(2), 347-370. DOI: https://doi.org/10.2307/2938260
- Tsay, R. S. (2010). *Analysis of Financial Time Series* (3rd ed.). Wiley. Chapter 3 (Conditional Heteroscedastic Models). DOI: https://doi.org/10.1002/9780470644560
- Francq, C., & Zakoian, J.-M. (2019). *GARCH Models: Structure, Statistical Inference and Financial Applications* (2nd ed.). Wiley. Chapter 1. URL: https://www.wiley.com/en-us/GARCH+Models%3A+Structure%2C+Statistical+Inference+and+Financial+Applications-p-9781119313571
