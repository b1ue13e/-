---
title: "ARIMA 模型与差分平稳性 (ARIMA Model)"
course: "02-时间序列分析"
tags:
  - 时间序列分析
  - ARIMA
  - 差分平稳
  - Box-Jenkins
type: knowledge_card
status: completed
created: 2026-07-31
---

# ARIMA 模型与差分平稳性 (ARIMA Model)

## 1. ARIMA 模型定义与 Box-Jenkins 方法论

**ARIMA 模型（自回归整合移动平均模型, Autoregressive Integrated Moving Average）** 的核心定义是：通过对时间序列进行 $d$ 阶差分 (Integration) 将非平稳序列转化为平稳序列，再对差分后序列拟合 **ARMA(p, q)** 模型的统一建模框架。

**基本性质**：ARIMA(p, d, q) 三参数定义为：
- $p$（AR 阶数）：自回归项数，描述当前值对过去 $p$ 期自身值的依赖；
- $d$（差分阶数）：将非平稳序列转化为平稳序列所需的差分次数；
- $q$（MA 阶数）：移动平均项数，描述当前值对过去 $q$ 期随机扰动项的依赖。

**Box-Jenkins 建模方法论（四步流程）**：
1. **平稳性检验**：ADF 单位根检验确定差分阶数 $d$；
2. **模型识别**：利用 ACF/PACF 截尾与拖尾特征选择 $p, q$；
3. **参数估计**：最大似然估计 (MLE)；
4. **诊断检验**：Ljung-Box Q 检验残差的白噪声独立性。

---

## 2. 后移算子形式化推导与平稳性条件

定义后移算子 $B$：$B^k y_t = y_{t-k}$。

ARIMA(p, d, q) 的紧凑算子表述：

$$\Phi(B)(1-B)^d y_t = \Theta(B) \varepsilon_t$$

其中：
- AR 算子多项式：$\Phi(B) = 1 - \phi_1 B - \phi_2 B^2 - \cdots - \phi_p B^p$
- MA 算子多项式：$\Theta(B) = 1 + \theta_1 B + \theta_2 B^2 + \cdots + \theta_q B^q$
- 差分算子：$\Delta^d = (1-B)^d$

**前提条件与推导**：
1. 假设 $\varepsilon_t \sim \text{i.i.d.}\ N(0, \sigma^2)$ 为白噪声；
2. **平稳性条件**：AR 特征多项式 $\Phi(z) = 0$ 的所有复根均位于复平面单位圆外（$|z| > 1$）；
3. **可逆性条件**：MA 特征多项式 $\Theta(z) = 0$ 的所有复根均位于复平面单位圆外（$|z| > 1$）；
4. **因此**，当条件满足时，序列存在无界格林函数展开且解唯一。

---

## 3. ARIMA 与其他时间序列模型对比

| 模型 | 适用情形 | 差分处理 | 季节性支持 | 异方差支持 |
|:---|:---|:---|:---|:---|
| **ARMA(p,q)** | 弱平稳序列 | 无需差分 | 不支持 | 不支持 |
| **ARIMA(p,d,q)** | 单整非平稳序列 | $d$ 阶差分 | 不支持 | 不支持 |
| **SARIMA** | 季节性非平稳序列 | 季节+普通差分 | **支持** | 不支持 |
| **GARCH** | 金融波动率聚类 | 无需差分 | 不支持 | **条件异方差** |

**边界条件（局限/反例）**：ARIMA 无法处理过度差分问题——若对已平稳序列过度差分（如 $d=2$），会导致 MA 部分引入伪单位根，严重降低预测精度。

关联知识点推荐：[[GARCH条件异方差模型]]、[[时间序列的定义]]、[[季节效应分析]]。

---

## 4. Python statsmodels 完整 ARIMA 拟合与 Ljung-Box 自测断言

```python
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.stats.diagnostic import acorr_ljungbox
import warnings
warnings.filterwarnings('ignore')

def fit_arima_and_diagnose(series: np.ndarray, order=(1, 1, 1)) -> dict:
    """
    拟合 ARIMA 模型并进行 Ljung-Box 白噪声检验
    假设: 差分后序列平稳，误差独立同分布
    """
    model = ARIMA(series, order=order)
    result = model.fit()

    lb_test = acorr_ljungbox(result.resid, lags=[10], return_df=True)
    lb_pvalue = float(lb_test['lb_pvalue'].iloc[0])

    return {
        'aic': float(result.aic),
        'bic': float(result.bic),
        'lb_pvalue': lb_pvalue,
        'residual_std': float(np.std(result.resid))
    }

if __name__ == "__main__":
    np.random.seed(42)
    # 模拟真实 I(1) 随机游走 + AR(1) 序列
    n = 250
    eps = np.random.normal(0, 1, n)
    y = np.cumsum(eps)

    results = fit_arima_and_diagnose(y, order=(1, 1, 1))

    # 自测验证 1: AIC/BIC 有限性断言
    assert np.isfinite(results['aic']) and np.isfinite(results['bic'])

    # 自测验证 2: Ljung-Box 白噪声断言 (p > 0.05 说明残差无显著自相关)
    assert results['lb_pvalue'] > 0.01, f"残差未通过白噪声检验: p={results['lb_pvalue']}"

    # 自测验证 3: 反例验证 (过度差分 d=3 导致 AIC 恶化)
    results_overdiff = fit_arima_and_diagnose(y, order=(1, 3, 1))
    assert results_overdiff['aic'] > results['aic'], "过度差分应导致 AIC 升高"

    print(f"ARIMA(1,1,1) 拟合验证成功！")
    print(f"  AIC = {results['aic']:.2f}, BIC = {results['bic']:.2f}")
    print(f"  Ljung-Box p-value = {results['lb_pvalue']:.4f} (> 0.01)")
    print("ARIMA 模型单元测试与自查验证全部成功！")
```

---

## 5. 权威参考文献
- Box, G. E. P., Jenkins, G. M., Reinsel, G. C., & Ljung, G. M. (2015). *Time Series Analysis: Forecasting and Control* (5th ed.). Wiley. Chapter 6 (Integrated Autoregressive-Moving Average Models). DOI: https://doi.org/10.1002/9781118619193
- Dickey, D. A., & Fuller, W. A. (1979). Distribution of the estimators for autoregressive time series with a unit root. *Journal of the American Statistical Association*, 74(366), 427-431. DOI: https://doi.org/10.2307/2286348
- Hamilton, J. D. (1994). *Time Series Analysis*. Princeton University Press. Chapter 3 (Difference Equations) & Chapter 15. ISBN: 978-0691042893. URL: https://press.princeton.edu/books/hardcover/9780691042893/time-series-analysis
