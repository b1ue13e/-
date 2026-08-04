---
type: index
cssclasses:
  - atlas-page
  - atlas-index
topic: "2026-Sprint1-时间序列分析冲刺计划"
created: 2026-07-25
updated: 2026-07-27
status: archived
flow: knowledge
sprint: archived
sprint_id: 2026-S01-timeseries-draft
source_of_truth: false
start: 2026-07-27
end: 2026-08-09
tags: [学习, 规划, 冲刺计划, 时间序列分析, PoW]
---

# 🎯 2026-Sprint 1：时间序列分析单主题冲刺计划

> [!warning] 已归档草案
> 当前唯一主攻已确定为量化金融。本页保留原始规划，不参与主页、周计划或日计划生成；未来重新主攻时间序列时再创建新的 Sprint。

> **冲刺周期**：2026-07-27 ~ 2026-08-09 (2 周 / 14 天)  
> **主攻目标**：全面攻克《02-时间序列分析》理论框架，并完成 PoW 里程碑项目。  
> **指南参考**：[[🚀 单主题冲刺与FSRS维护-执行指南|单主题冲刺与FSRS维护-执行指南]]

---

## 一、 核心课程路线与依赖

- 课程主页：[[🗺️ 时间序列分析学习路径|02-时间序列分析学习路径]]
- 前置知识：[[🗺️ 高等代数学习路径|高等代数]]、[[🗺️ 概率论与数理统计学习路径|概率论与数理统计]]

---

## 二、 PoW 里程碑项目 (Proof of Work)

* **项目名称**：`Time-Series-Forecasting-Engine (高频/长序列时间序列预测与回测引擎)`
* **技术栈**：Python, PyTorch, Statsmodels, Arch (GARCH模型)
* **核心交付物**：
  1. 经典统计模型模块：ARMA/ARIMA 建模、平稳性检验 (ADF)、ACF/PACF 谱分析、GARCH 波动率预测。
  2. 深度学习预测模块：LSTM / Informer 或 PatchTST 长序列预测模型实现。
  3. 可运行的 Jupyter Notebook 案例与完整测试结果对比报告。

---

## 三、 14 天冲刺分解表

### 📅 第一周：经典时间序列与平稳过程 (07-27 ~ 08-02)
- [ ] **Day 1 (07-27)**：时间序列概念、平稳性 (严平稳与宽平稳)、自相关函数 (ACF) 与偏自相关函数 (PACF)
- [ ] **Day 2 (07-28)**：AR(p) 模型推导、Yule-Walker 方程、MA(q) 模型与可逆性条件
- [ ] **Day 3 (07-29)**：ARMA(p,q) 建模、模型识别、AIC/BIC 准则与参数估计 (极大似然/最小二乘)
- [ ] **Day 4 (07-30)**：非平稳时间序列、单整过程、ARIMA(p,d,q) 模型与单位根检验 (ADF/KPSS)
- [ ] **Day 5 (07-31)**：ARCH 与 GARCH 条件异方差模型 (金融高频波动率建模)
- [ ] **Day 6 (08-01)**：VAR (向量自回归) 多维时间序列分析基础
- [ ] **Day 7 (08-02)**：阶段总结 + 第一周 FSRS 卡片包制作与整理

### 📅 第二周：深度时间序列与 PoW 里程碑项目攻坚 (08-03 ~ 08-09)
- [ ] **Day 8 (08-03)**：深度学习时间序列建模：RNN/LSTM/GRU 序列预测机制
- [ ] **Day 9 (08-04)**：前沿长序列 Transformer 模型架构 (Informer / PatchTST / N-BEATS)
- [ ] **Day 10 (08-05)**：PoW 项目搭建：构建数据流水线与经典 ARIMA-GARCH 预测基准
- [ ] **Day 11 (08-06)**：PoW 项目推进：实现 PyTorch 深度学习预测模型与损失函数
- [ ] **Day 12 (08-07)**：PoW 项目推进：模型对比评估 (MAE/RMSE/MAPE) 与回测可视化
- [ ] **Day 13 (08-08)**：PoW 项目收尾：编写 GitHub README 报告与使用说明
- [ ] **Day 14 (08-09)**：Sprint 1 结项答辩与全套知识卡归档挂载至 FSRS 库

---

## 四、 每日 20% FSRS 维护清单

在冲刺《时间序列分析》的同时，每天利用 30 分钟完成以下科目的 FSRS 提取维护：
- [ ] 07-最优化方法 (凸分析、梯度下降、KKT条件)
- [ ] 17-机器学习 (线性模型、SVM、决策树)
- [ ] 33-贝叶斯统计 (先验/后验、MCMC)
