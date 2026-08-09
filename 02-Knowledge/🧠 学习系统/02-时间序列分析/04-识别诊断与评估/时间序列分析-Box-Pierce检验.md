---
type: study
topic: "Box-Pierce 检验"
course: "时间序列分析"
created: 2026-07-23
updated: 2026-08-07
status: ongoing
difficulty: intermediate
flow: knowledge
kind: derivation
aliases: ["Box-Pierce 检验（深挖笔记）", "Box-Pierce检验", "Box–Pierce 检验"]
concept: ["Portmanteau检验", "样本自相关", "卡方近似"]
prerequisites: ["Ljung-Box检验", "样本自相关"]
related: ["Ljung-Box检验", "白噪声", "残差诊断"]
stage_moc: "[[🧭 阶段4-识别诊断与评估]]"
upstream: ["[[时间序列分析-Ljung-Box检验]]"]
sources:
  - title: "Forecasting: Principles and Practice (3rd ed.)"
    url: "https://otexts.com/fpp3/diagnostics.html"
    locator: "Section 5.4: residual diagnostics"
    source_type: open-textbook
    license: "link-only；本卡为原创对比推导。"
    verified_at: 2026-08-07
  - title: "statsmodels acorr_ljungbox"
    url: "https://www.statsmodels.org/stable/generated/statsmodels.stats.diagnostic.acorr_ljungbox.html"
    locator: "boxpierce option"
    source_type: official-documentation
    license: "link-only"
    verified_at: 2026-08-07
tags: [学习, 时间序列分析, Box-Pierce, Portmanteau]
---

# Box–Pierce 检验

## 在课程中的角色

Box–Pierce 是 portmanteau 检验的较早形式。本卡只保留统计量来源和与 Ljung–Box 的差异；实际残差诊断以[[时间序列分析-Ljung-Box检验|Ljung–Box]]为主，避免维护两套重复流程。

## 统计量

检验原假设

$$
H_0:\rho_1=\cdots=\rho_h=0
$$

时，Box–Pierce 统计量为

$$
Q_{\mathrm{BP}}=n\sum_{k=1}^{h}r_k^2.
$$

大样本下常使用

$$
Q_{\mathrm{BP}}\overset{a}{\sim}\chi^2_{\nu}.
$$

原序列常用 $\nu=h$；拟合残差需按模型参数调整自由度。该近似在小样本和较大滞后下可能偏差明显。

## 为什么是平方和

若每个 $r_k$ 都接近 0，则平方和很小。任意滞后的正或负相关都会通过 $r_k^2$ 增加统计量，所以一次检验可汇总前 $h$ 阶的偏离。

平方和不保留相关方向，也不能指出是哪一个滞后或哪种模型结构造成拒绝。拒绝后仍需返回残差图、ACF 和模型设定定位问题。

## 与 Ljung–Box 的差异

Ljung–Box 统计量为

$$
Q_{\mathrm{LB}}
=n(n+2)\sum_{k=1}^{h}\frac{r_k^2}{n-k}.
$$

对每一阶 $k$，对应权重之比为

$$
\frac{n(n+2)/(n-k)}{n}
=\frac{n+2}{n-k}.
$$

有限 $n$ 下该比值大于 1，并随 $k$ 增大；当 $n$ 很大且 $h$ 相对较小时，比值趋近 1，两种统计量逐渐接近。

### 同一组数字

若 $n=100,h=2,r_1=0.20,r_2=0.10$：

$$
Q_{\mathrm{BP}}
=100(0.20^2+0.10^2)=5.00,
$$

而

$$
Q_{\mathrm{LB}}\approx5.16.
$$

差异来自有限样本权重，不表示两种检验拥有不同原假设。

## 最小可运行对比

~~~python
import numpy as np
from statsmodels.stats.diagnostic import acorr_ljungbox

rng = np.random.default_rng(42)
series = rng.normal(size=300)

result = acorr_ljungbox(
    series,
    lags=[6, 12],
    boxpierce=True,
    return_df=True,
)
print(result)
~~~

输出会同时包含 Ljung–Box 与 Box–Pierce 的统计量和 p 值。不要挑选更符合预期的一列作为最终结论。

## 使用边界

- 小样本优先使用 Ljung–Box 的有限样本修正。
- 两种检验都只检查所选滞后内的线性相关。
- 自由度、滞后预注册和残差对齐问题完全相同。
- 检验结果不能替代参数根、收敛、样本外误差和区间覆盖。

## 闭卷检索

1. 写出 $Q_{\mathrm{BP}}$ 和 $Q_{\mathrm{LB}}$。
2. 推导两者逐滞后权重的比值。
3. 计算给定手算例子中的两个统计量。
4. 解释为什么本课程不维护两套并行诊断流程。
5. 写出两种检验共同无法回答的三个问题。

**通过标准**：前三题计算正确；后两题明确主流程使用 Ljung–Box，并列出非线性依赖、结构定位和样本外性能边界。

## 相关入口

- 主诊断卡：[[时间序列分析-Ljung-Box检验]]
- 样本 ACF：[[自相关函数ACF]]
- 白噪声：[[白噪声]]
- 残差诊断：[[残差诊断与白噪声检验]]

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

