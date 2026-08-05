---
tags: [时间序列, 基础认知, 教材主线]
created: 2026-04-11
status: active
phase: A
type: stage
topic: "板块 A：基础认知层"
difficulty: beginner
concept: ["时间序列", "描述性时序分析", "统计时序分析"]
prerequisites: []
related: ["平稳性", "时序图", "自相关图"]
---
# 🎯 板块 A：基础认知层

> 本板块是 L00 的补充知识地图；必修起点仍是[[L00-环境与时间索引]]。

## 📊 板块进度

```dataviewjs
const topics = dv.pages('"02-Knowledge/🧠 学习系统/02-时间序列分析/01-基础认知层"').where(p => p.type === "study");
const total = topics.length;
const completed = topics.where(p => p.status === "completed").length;
const progress = total > 0 ? Math.round((completed / total) * 100) : 0;
dv.paragraph(`**板块进度: ${progress}%** (${completed}/${total} 模块)`);
```

## 📚 开放来源与主卡

- [FPP3 Ch.2–3](https://otexts.com/fpp3/)：时间图、模式与变换。
- [pandas 时间序列指南](https://pandas.pydata.org/docs/user_guide/timeseries.html)：索引与频率。
- 主卡：[[L00-环境与时间索引]]、[[时间序列的定义]]、[[时间索引与频率]]。

## 📖 学习清单

| 教材位置 | 重点 | 笔记入口 |
|:---|:---|:---|
| L00 | 索引、频率、缺失、信息边界 | [[L00-环境与时间索引]] |
| 基础概念 | 时间序列、截面、面板与观测单位 | [[时间序列的定义]] |
| 图形描述 | 趋势、季节、异常、方差变化 | [[时间序列结构-趋势季节噪声与ETS分解]] |
| 执行闭环 | 建模、检验、预测、否决 | [[📚 时间序列课程学习面板]] |

## ✅ 完成标准

- [ ] 能说清时间序列和截面数据、面板数据的区别
- [ ] 能区分描述性时序分析与统计时序分析
- [ ] 能把“频率、趋势、季节、随机波动”四类词放回同一张图里理解
- [ ] 准备好后续预处理阶段需要使用的数据对象与基础工具

## 🔗 板块导航

| ⬅️ 上一板块 | 📋 总览 | 下一板块 ➡️ |
|:---:|:---:|:---:|
| - | [[🗺️ 时间序列分析学习路径\|返回总览]] | [[📊 板块B：统计基础层\|进入板块B]] |


---

*板块更新：2026-04-16*
