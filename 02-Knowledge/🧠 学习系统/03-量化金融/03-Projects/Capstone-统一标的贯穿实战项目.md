---
title: "Capstone-统一标的贯穿实战项目"
type: project
topic: "贯穿式实战"
created: "2026-08-04"
status: active
tags: [项目, 实战]
---

# 🏆 Capstone Project：死磕苹果 (Project AAPL)

## 项目背景
为了防止知识点散落如盘沙，我们设定一个贯穿整个量化学习周期的 Capstone 终极主线任务。
从第一天到最后一天，我们将使用**同一个标的（苹果公司 AAPL）**，随着你技能的升级，对它进行层层解剖。

## 任务里程碑 (Milestones)

### Phase 1: 夯实基础 (Pandas 与直觉)
- [ ] 提取 AAPL 过去 10 年的前复权收盘价。
- [ ] 在 AAPL 上手写双均线交叉策略，算出累积收益率和最大回撤。

### Phase 2: 量化核心技能 (统计与波动率)
- [ ] 用 GARCH(1,1) 模型去拟合 AAPL 的日收益率序列，预测它明天的真实波动率。
- [ ] 用 CAPM 算出 AAPL 相对纳斯达克指数 (QQQ) 的 $\beta$ 旋钮到底是多少。

### Phase 3: 深入精通 (随机微积分与衍生品)
- [ ] 根据前面算出的 AAPL 波动率 $\sigma$，用蒙特卡洛模拟 (Monte Carlo) 画出 AAPL 未来一年的 10000 种可能价格路径。
- [ ] 给 AAPL 的看涨期权用 Black-Scholes 公式进行精准定价。

### Phase 4: 高频与微观
- [ ] (可选) 获取 AAPL 的逐笔订单簿数据 (LOB)，观测它的买卖价差与订单不平衡 (Order Imbalance)。
