---
type: study
topic: "Ljung-Box 检验"
course: "时间序列分析"
created: 2026-07-23
updated: 2026-08-07
status: ongoing
difficulty: intermediate
flow: knowledge
kind: derivation
aliases: ["Ljung-Box 检验（深挖笔记）", "Ljung-Box检验", "Ljung–Box 检验"]
concept: ["Portmanteau检验", "残差诊断", "白噪声"]
prerequisites: ["样本自相关", "卡方分布", "假设检验"]
related: ["Box-Pierce检验", "白噪声", "残差诊断"]
stage_moc: "[[🧭 阶段4-识别诊断与评估]]"
upstream: ["[[残差诊断与白噪声检验]]"]
sources:
  - title: "Forecasting: Principles and Practice (3rd ed.)"
    url: "https://otexts.com/fpp3/diagnostics.html"
    locator: "Section 5.4: residual diagnostics"
    source_type: open-textbook
    license: "link-only；本卡为原创释义，不复制教材正文或题目。"
    verified_at: 2026-08-07
  - title: "statsmodels acorr_ljungbox"
    url: "https://www.statsmodels.org/stable/generated/statsmodels.stats.diagnostic.acorr_ljungbox.html"
    locator: "Official API documentation"
    source_type: official-documentation
    license: "link-only"
    verified_at: 2026-08-07
tags: [学习, 时间序列分析, Ljung-Box, 残差诊断]
---

# Ljung–Box 检验

## 它检验什么

Ljung–Box 是 portmanteau 联合检验。给定最大滞后 $h$，它同时检查

$$
H_0:\rho_1=\rho_2=\cdots=\rho_h=0
$$

与

$$
H_1:\text{至少一个 }\rho_k\ne0.
$$

它回答的是“前 $h$ 阶是否还存在可检测的线性相关”，不是“序列是否独立”或“模型是否正确”。

## 统计量

样本长度为 $n$，样本自相关为 $r_k$，统计量为

$$
Q_{\mathrm{LB}}
=n(n+2)\sum_{k=1}^{h}\frac{r_k^2}{n-k}.
$$

在常规正则条件和大样本近似下，

$$
Q_{\mathrm{LB}}\overset{a}{\sim}\chi^2_{\nu}.
$$

- 对未经拟合的序列，常用 $\nu=h$。
- 对 ARMA 残差，常用 $\nu=h-p-q$，或在软件中传入已估计动态参数数目 model_df。
- 必须保证 $h-\text{model\_df}>0$；否则 p 值没有有效自由度。

趋势项、季节参数、外生回归项如何计入自由度依赖模型和软件约定，报告时必须写明。

## 手算例子

设 $n=100$，检查 $h=2$，且 $r_1=0.20,r_2=0.10$：

$$
Q_{\mathrm{LB}}
=100(102)\left(\frac{0.20^2}{99}+\frac{0.10^2}{98}\right)
\approx5.16.
$$

原序列检验使用 2 个自由度；若这是估计过一个动态参数的残差，常用自由度变为 $2-1=1$。同一个统计量会得到不同 p 值，这就是不能忽略 model_df 的原因。

## 滞后如何选择

滞后 $h$ 应在看 p 值前确定，并服务于具体风险：

- 覆盖业务上重要的短期记忆；
- 季节序列至少检查关键季节滞后；
- 样本短时避免把 $h$ 设得过大；
- 同时报告少量预注册滞后，而不是遍历到出现显著为止。

把 1 到 30 的每个滞后都试一遍，再挑最小 p 值报告，会造成选择偏差。

## 残差诊断协议

1. 确认残差按时间排序，且与拟合样本一一对齐。
2. 预注册 $h$ 和 model_df。
3. 查看残差图与 ACF，不只看 p 值。
4. 对原残差运行 Ljung–Box，检查遗漏的均值结构。
5. 对平方或绝对残差另做检查，识别波动聚集。
6. 结合参数根、收敛、滚动样本外误差和区间覆盖率判断模型。

大 p 值只表示当前样本未发现所检验滞后内的线性相关。小 p 值提示模型遗漏结构，但不能直接告诉你应增加哪个参数。

## 最小可运行验证

~~~python
import numpy as np
from statsmodels.stats.diagnostic import acorr_ljungbox

rng = np.random.default_rng(42)
residuals = rng.normal(size=500)

result = acorr_ljungbox(
    residuals,
    lags=[6, 12],
    model_df=0,
    return_df=True,
)
print(result)
~~~

若输入是 ARMA$(p,q)$ 残差，应把 model_df 设置为预先约定的动态参数数目，并在报告中保留该值。

## 与 Box–Pierce 的关系

Box–Pierce 使用

$$
Q_{\mathrm{BP}}=n\sum_{k=1}^{h}r_k^2.
$$

Ljung–Box 通过 $n(n+2)/(n-k)$ 权重进行有限样本修正。两者大样本下接近；当前课程以 Ljung–Box 作为主要诊断，Box–Pierce 只用于理解统计量来源。

## 常见错误

- 把大 p 值写成“残差已被证明是白噪声”。
- 忘记 residual test 的 model_df。
- 在看结果后不断更换 $h$。
- 只检验原残差，忽略平方残差。
- 把显著结果机械翻译为“再加一个 AR 项”。
- 残差顺序或样本窗口与拟合结果错位。

## 闭卷检索

1. 写出 $H_0$、$Q_{\mathrm{LB}}$ 和近似分布。
2. 解释原序列检验与拟合残差检验的自由度差异。
3. 手算 $n=100,h=2,r_1=0.2,r_2=0.1$ 的统计量。
4. 给出滞后预注册方案及其业务理由。
5. 说明 Ljung–Box 通过后仍需检查哪些证据。

**通过标准**：前三题公式和自由度正确；后两题包含预注册、平方残差、样本外误差和区间覆盖。

## 相关入口

- 诊断流程：[[L08-残差诊断与纯随机性检验]]
- 残差主题：[[残差诊断与白噪声检验]]
- 对比统计量：[[时间序列分析-Box-Pierce检验]]
- 波动诊断：[[GARCH波动率建模]]

## 学完后可以完成

### 下游知识

~~~dataview
LIST
FROM "02-Knowledge/🧠 学习系统"
WHERE contains(upstream, this.file.link)
SORT file.name ASC
~~~

### 可完成作业

~~~dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
~~~

