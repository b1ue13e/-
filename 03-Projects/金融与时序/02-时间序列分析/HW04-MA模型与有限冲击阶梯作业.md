---
type: project
topic: "HW04 MA模型与有限冲击"
course: "时间序列分析"
lesson: 4
created: 2026-08-02
status: active
progress: 0%
flow: project
kind: exercise
tags: [项目, 时间序列, 阶梯作业, MA模型]
source_lesson: "[[L04-MA模型与有限冲击]]"
---

# HW04｜MA 模型与有限冲击阶梯作业

## A｜生成过程手算（25 分）

对 (y_t=1+\varepsilon_t-0.4\varepsilon_{t-1})，给定创新 `2, 0, -1, 3, 0`：

1. 计算五个 (y_t)；
2. 标出大小为 3 的冲击影响了哪些观测；
3. 解释常数 1 与序列均值的关系。

## B｜理论推导（20 分）

推导 MA(1) 的方差、lag-1 协方差和一阶 ACF，并说明为何更高阶协方差为零。

## C｜等价参数实验（20 分）

比较 θ=0.5 与 θ=2：

1. 计算理论一阶 ACF；
2. 分别模拟并比较样本 ACF；
3. 解释为什么需要可逆性约束。

## D｜模型比较（20 分）

对同一模拟 MA(2) 数据拟合 AR(1)、MA(2)、ARMA(1,1)，提交 AICc、残差检验和滚动预测。不能只凭生成模型已知就宣布 MA(2) 胜出。

## E｜费曼解释（15 分）

用“不超过三天的天气意外”类比，在 150 字内解释有限冲击响应，以及它和 AR 记忆的区别。

## 验收标准

- [ ] 手算能从创新重建观测
- [ ] 推导说明共同创新来自哪里
- [ ] 模拟前先写 ACF 预期
- [ ] 使用至少三类证据比较模型
- [ ] 不混淆 MA 模型与平滑

## 来源

- [FPP3 §9.4 Moving average models](https://otexts.com/fpp3/MA.html)
- [FPP3 Chapter 9 Exercises](https://otexts.com/fpp3/arima-exercises.html)
