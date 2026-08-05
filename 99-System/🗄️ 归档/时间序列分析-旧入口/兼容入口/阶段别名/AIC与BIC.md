---
type: alias
topic: "AIC、AICc 与 BIC 导航"
canonical: "[[L07-模型识别与参数估计]]"
created: 2026-04-16
updated: 2026-08-05
status: active
flow: knowledge
kind: moc
tags: [索引, 时间序列, 信息准则]
---

# AIC、AICc 与 BIC｜导航别名

> 公式、手算、候选台账与边界统一在[[L07-模型识别与参数估计]]；作业见[[HW07-模型识别与参数估计阶梯作业]]。

$$AIC=-2\ell+2k,\qquad AICc=AIC+\frac{2k(k+1)}{T-k-1},\qquad BIC=-2\ell+k\log T.$$

只能在响应、变换、有效样本和似然口径一致的候选间比较。信息准则用于候选排序，不检查根、残差、稳定性或样本外价值。

**出口题**：为什么 AICc 最低的近单位根模型仍可能被淘汰？

