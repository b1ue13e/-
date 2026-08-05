---
type: stage
topic: 板块 E：机器学习与深度学习进阶
tags:
- 时间序列
- 机器学习
- 深度学习
- 教材外延
created: 2026-04-11
status: active
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

> 本板块只在 L00–L09 和经典基线完成后进入，用现代机器学习扩展时间序列能力；它不是与必修课并行的第二条主线。

## 📊 板块进度

```dataviewjs
const required = [
  "时序特征工程与ML预测",
  "滚动回测与预测区间",
  "02-Knowledge/🧠 学习系统/02-时间序列分析/05-机器学习与深度学习进阶/XGBoost时序预测",
  "02-Knowledge/🧠 学习系统/02-时间序列分析/05-机器学习与深度学习进阶/RNN时序建模",
  "LSTM与GRU在时序中的应用",
  "Transformer 时序预测",
  "02-Knowledge/🧠 学习系统/02-时间序列分析/05-机器学习与深度学习进阶/N-BEATS与N-HiTS",
];
const topics = required.map(path => dv.page(path)).filter(Boolean);
const total = required.length;
const completed = topics.filter(p => Number(p.mastery ?? 0) >= 3).length;
const progress = total > 0 ? Math.round((completed / total) * 100) : 0;
dv.paragraph(`**学习者掌握进度: ${progress}%** (${completed}/${total} 主题达到 mastery 3)`);
dv.table(
  ["主题", "mastery", "状态"],
  topics.map(p => [p.file.link, Number(p.mastery ?? 0), Number(p.mastery ?? 0) >= 3 ? "已验收" : "待学习/待验收"]),
);
```

> `status: completed` 只表示笔记内容已经编写完成。只有完成无泄漏实现、统一滚动协议下的基线比较和错误解释，才把对应主题卡设置为 `mastery: 3`。

## 📚 进入条件与开放来源

- 必修前置：[[📚 时间序列课程学习面板|L00–L09]]，尤其是信息边界与滚动回测。
- 实现参考：[scikit-learn](https://scikit-learn.org/stable/)、[PyTorch](https://pytorch.org/tutorials/)、[Nixtla NeuralForecast](https://github.com/Nixtla/neuralforecast)。
- 目标不是替代 ARIMA/GARCH，而是在统一协议下检验树模型与神经网络是否产生增益。

## 📖 学习清单

| 扩展主题 | 重点 | 笔记入口 |
|:---|:---|:---|
| 特征工程 | 信息边界、滞后、滚动、日历特征 | [[时序特征工程与ML预测]] |
| 验证策略 | 滚动验证、逐 horizon 与区间 | [[滚动回测与预测区间]] |
| 树模型 | XGBoost/LightGBM 做时序预测 | [[XGBoost时序预测]] |
| RNN 家族 | 状态递推、梯度、门控边界 | [[RNN时序建模]] / [[LSTM与GRU在时序中的应用]] |
| 长 horizon 深度模型 | Transformer 与残差基展开 | [[Transformer 时序预测]] / [[N-BEATS与N-HiTS]] |

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
