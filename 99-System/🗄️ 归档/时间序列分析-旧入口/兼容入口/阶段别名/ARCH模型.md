---
type: alias
topic: "ARCH 模型导航"
canonical: "[[GARCH波动率建模]]"
created: 2026-04-16
updated: 2026-08-05
status: active
flow: knowledge
kind: moc
tags: [索引, 时间序列, ARCH, 波动率]
---

# ARCH 模型｜导航别名

> ARCH/GARCH 的定义、诊断、代码和风险边界统一在[[GARCH波动率建模]]，补充卡为[[GARCH条件异方差模型]]。

ARCH(q) 用过去平方创新解释当前条件方差：$\sigma_t^2=\omega+\sum_{i=1}^q\alpha_i\varepsilon_{t-i}^2$。原残差 ACF 接近零不排除波动聚集，应检查平方/绝对残差和区间覆盖。

**出口题**：为什么原残差白噪声仍可能有可预测的条件方差？

