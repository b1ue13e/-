---
type: alias
topic: "GARCH 模型导航"
canonical: "[[GARCH波动率建模]]"
created: 2026-04-16
updated: 2026-08-05
status: active
flow: knowledge
kind: moc
tags: [索引, 时间序列, GARCH, 波动率]
---

# GARCH 模型｜导航别名

> 权威主题卡为[[GARCH波动率建模]]；开放课程来源为 [Penn State STAT 510 Lesson 11.1](https://online.stat.psu.edu/stat510/Lesson11)。

GARCH(1,1)：$\sigma_t^2=\omega+\alpha\varepsilon_{t-1}^2+\beta\sigma_{t-1}^2$。常见协方差平稳条件为参数非负且 $\alpha+\beta<1$；贴近 1 表示波动冲击持久。模型是否改善风险区间必须用样本外覆盖和尾部表现验证。

**出口题**：为什么 $\alpha+\beta$ 接近 1 时不能只看样本内似然？

