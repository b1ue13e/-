---
type: stage
cssclasses:
  - atlas-page
  - atlas-stage
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
const total = dv.pages('"02-Knowledge/🧠 学习系统/02-时间序列分析/05-机器学习与深度学习进阶"').length - 1;
const completed = dv.pages('"02-Knowledge/🧠 学习系统/02-时间序列分析/05-机器学习与深度学习进阶"').where(p => p.status === "completed").length;
const progress = total > 0 ? Math.round((completed / total) * 100) : 0;
dv.paragraph(`**板块进度: ${progress}%** (${completed}/${total} 模块)`);
```

## 📚 与教材的关系

- 主教材前置：[[时间序列分析基于R]]
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
| [[🔍 板块D：建模与诊断层|返回板块D]] | [[🗺️ 时间序列分析学习路径|返回总览]] | [[🚀 板块F：实战项目层|进入板块F]] |


---

*板块更新：2026-04-16*

<!-- curriculum-repair:start -->
## 🧩 教材对齐索引

| 模块 | 要解决的问题 | 教材定位 | 原子卡片 | 完成标准 |
|:---|:---|:---|:---|:---|
| 📚 与教材的关系 | 理解“📚 与教材的关系”中的“时序特征工程”，并能说明它在“🤖 板块 E：机器学习与深度学习进阶”中的作用。 | 按阶段教材挂载页优先阅读 | [[时序特征工程]]<br>[[时间序列交叉验证]]<br>[[XGBoost时序预测]]<br>[[RNN时序建模]]<br>[[LSTM与GRU]]<br>[[Transformer时序]]<br>[[N-BEATS与N-HiTS]] | 能用自己的话解释“时序特征工程”，给出一个最小例子，并说明它与本模块相邻概念的关系。 |

<!-- curriculum-repair:end -->

---

## 🃏 间隔复习卡片

> 用 **Spaced Repetition** 插件复习。
> 格式：单行卡 `问题 :: 答案`；多行卡：问题 → 空行 → `?` → 空行 → 答案。
> 写卡原则：用自己的话，答案不超过 3 句，每张卡只考一件事。

#flashcard

这个概念解决的核心问题是什么？ :: （填写）

最关键的公式/定义是什么？ :: （填写）

最容易混淆的概念是什
