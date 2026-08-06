---
type: project
topic: "HW05 ARMA与ARIMA建模闭环"
course: "时间序列分析"
lesson: 5
created: 2026-08-02
status: active
progress: 0%
flow: project
kind: exercise
tags: [项目, 时间序列, 阶梯作业, ARIMA]
source_lesson: "[[L05-ARMA与ARIMA建模闭环]]"
---

# HW05｜ARMA 与 ARIMA 建模闭环阶梯作业

> **建议数据**：选择一个非季节、长度不少于 120 的公开时间序列。先保留最后 20% 作为测试段，在模型确定前不要查看测试结果。

## A｜差分与还原手算（15 分）

给定序列 `[100, 102, 105, 104, 108]`：

1. 计算一阶差分；
2. 若未来两期差分预测依次为 2 和 -1，递归还原两期水平预测；
3. 解释为什么两期预测不能都直接加在最后一个真实值 108 上。

## B｜模型翻译（15 分）

将 ARIMA(1,1,1)

$$
(1-\phi B)(1-B)y_t=c+(1+\theta B)\varepsilon_t
$$

分两步完成：

1. 令 $w_t=(1-B)y_t$，写出 $w_t$ 的 ARMA 方程；
2. 用文字分别解释 $\phi$、$\theta$、$d=1$ 控制什么。

## C｜人工候选台账（25 分）

对训练集完成：

1. 原序列和差分序列图；
2. 说明为何选择当前变换与 $d$；
3. 根据差分后 ACF/PACF 提出 3–5 个低阶候选；
4. 记录每个候选的阶数、趋势项、AICc、收敛状态、AR/MA 根和淘汰理由。

不得只提交软件摘要截图；每个候选必须有一句人类可读的判断。

## D｜自动选择与人工选择对照（15 分）

使用一种自动选模工具，并回答：

1. 它搜索了哪些 $p,d,q$ 和趋势设定？
2. 自动结果是否在你的人工候选中？
3. 若不同，差异来自搜索空间、信息准则还是约束？
4. 自动结果能否通过残差检查？

自动选模是对照实验，不是答案生成器。

## E｜滚动预测验收（20 分）

至少比较：

- naïve 基线；
- 你的最佳人工 ARIMA；
- 自动选择的 ARIMA。

使用 expanding-window 或 rolling-window 评估，分别报告 horizon 1 和更远 horizon 的 MAE/RMSE。说明模型排名是否随 horizon 改变。

## F｜迷你建模报告（10 分）

用 300–500 字回答：

1. 数据为何需要或不需要差分？
2. 最终模型为何胜出？
3. 残差还暴露了什么？
4. 与 naïve 相比，提升是否足以支持实际使用？
5. 模型在哪种条件变化下最可能失效？

## 验收标准

- [ ] 原序列、差分和逆差分逻辑一致
- [ ] 候选数量有限且有理论理由
- [ ] 不跨不同差分阶数机械比较 AICc
- [ ] 残差诊断包含图形与检验
- [ ] 样本外评估无数据泄漏且包含基线
- [ ] 结论说明限制，不把统计通过等同于业务有效

## 来源

- [FPP3 §9.5 Non-seasonal ARIMA models](https://otexts.com/fpp3/non-seasonal-arima.html)
- [FPP3 §9.7 ARIMA modelling](https://otexts.com/fpp3/arima-r.html)
- [FPP3 Chapter 9 Exercises](https://otexts.com/fpp3/arima-exercises.html)

