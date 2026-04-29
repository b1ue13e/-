---
type: stage
topic: 板块 E：机器学习与深度学习进阶
tags:
- 时间序列
- 机器学习
- 深度学习
- 教材外延
created: 2026-04-11
status: planned
difficulty: advanced
concept:
- 时序特征工程
- 时间序列交叉验证
- RNN
- Transformer
prerequisites:
- ARIMA模型
- 协整
- 预测与评估
related:
- 机器学习
- 深度学习
- 项目实战
phase: E
---

# 🤖 板块 E：机器学习与深度学习进阶

> 这个板块不直接来自王燕教材，而是建立在主教材读完之后，用现代机器学习方法扩展时间序列分析能力。

## 📊 板块进度

```dataviewjs
const total = dv.pages('"🧠 学习系统/02-时间序列分析/05-机器学习与深度学习进阶"').length - 1;
const completed = dv.pages('"🧠 学习系统/02-时间序列分析/05-机器学习与深度学习进阶"').where(p => p.status === "completed").length;
const progress = total > 0 ? Math.round((completed / total) * 100) : 0;
dv.paragraph(`**板块进度: ${progress}%** (${completed}/${total} 模块)`);
```

## 📚 与教材的关系

- 主教材前置：[[📚 书库/书籍笔记/时间序列分析基于R|时间序列分析基于R]]
- 推荐前提：至少完成教材第 1-6 章，再进入本板块。
- 这里的目标不是替代 ARIMA/GARCH，而是在经典统计基线之上比较树模型和神经网络。

## 📖 学习清单

| 扩展主题 | 重点 | 笔记入口 |
|:---|:---|:---|
| 特征工程 | 滞后特征、滚动统计、日历特征 | [[时序特征工程]] |
| 验证策略 | 滚动验证、时间序列交叉验证 | [[时间序列交叉验证]] |
| 树模型 | XGBoost/LightGBM 做时序预测 | [[XGBoost时序预测]] |
| RNN 家族 | RNN、LSTM、GRU 的时序建模思路 | [[RNN时序建模]] / [[LSTM与GRU]] |
| Transformer 家族 | Informer、Autoformer、N-BEATS/N-HiTS | [[Transformer时序]] / [[N-BEATS与N-HiTS]] |

## ✅ 完成标准

- [ ] 能把经典时序模型与树模型/深度模型做清晰对比
- [ ] 明白时序验证和普通随机交叉验证的区别
- [ ] 至少完成一次“统计模型基线 vs 机器学习模型”的实验对比
- [ ] 只在经典模型已经给不出满意结果时，再投入复杂深度模型

## 🔗 板块导航

| ⬅️ 上一板块 | 📋 总览 | 下一板块 ➡️ |
|:---:|:---:|:---:|
| [[🔍 板块D：建模与诊断层\|返回板块D]] | [[🗺️ 时间序列分析学习路径\|返回总览]] | [[🚀 板块F：实战项目层\|进入板块F]] |


---

*板块更新：2026-04-16*
