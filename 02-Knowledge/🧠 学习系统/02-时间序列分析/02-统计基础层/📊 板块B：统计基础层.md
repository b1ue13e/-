---
type: stage
topic: 板块 B：统计基础层
tags:
- 时间序列
- 统计基础
- 教材主线
created: 2026-04-11
status: active
difficulty: intermediate
concept:
- 平稳性
- 自相关图
- 纯随机性检验
prerequisites:
- 时间序列的定义
related:
- ARMA模型
- 单位根检验
- 白噪声
phase: B
---

# 📊 板块 B：统计基础层

> 本板块是 L01–L02 的补充知识地图；必修仍按课程面板推进。

## 📊 板块进度

```dataviewjs
const topics = dv.pages('"02-Knowledge/🧠 学习系统/02-时间序列分析/02-统计基础层"').where(p => p.type === "study");
const total = topics.length;
const completed = topics.where(p => p.status === "completed").length;
const progress = total > 0 ? Math.round((completed / total) * 100) : 0;
dv.paragraph(`**板块进度: ${progress}%** (${completed}/${total} 模块)`);
```

## 📚 开放来源与主卡

- [FPP3 §9.1](https://otexts.com/fpp3/stationarity.html)：平稳与差分。
- [Penn State STAT 510 Lesson 1](https://online.stat.psu.edu/stat510/Lesson01)：平稳、ACF 与差分。
- 主卡：[[L01-平稳性与差分]]、[[L02-ACF-PACF与白噪声]]。

## 📖 学习清单

| 教材位置 | 重点 | 笔记入口 |
|:---|:---|:---|
| L01 | 定义、差分与单位根 | [[L01-平稳性与差分]] / [[单位根检验-ADF-KPSS]] |
| L02 | ACF、PACF 与白噪声 | [[L02-ACF-PACF与白噪声]] / [[自相关函数ACF]] |
| 诊断 | 纯随机性与白噪声检验 | [[纯随机性检验]] / [[白噪声]] |

## ✅ 完成标准

- [ ] 能解释“平稳”为什么是经典时序模型的前提
- [ ] 能从时序图和 ACF/PACF 图中读出最基本的结构信号
- [ ] 能把平稳性检验和纯随机性检验区分开
- [ ] 为进入 ARMA/ARIMA 建模准备好预处理判断流程

## 🔗 板块导航

| ⬅️ 上一板块 | 📋 总览 | 下一板块 ➡️ |
|:---:|:---:|:---:|
| [[🎯 板块A：基础认知层\|返回板块A]] | [[🗺️ 时间序列分析学习路径\|返回总览]] | [[📈 板块C：经典模型层\|进入板块C]] |


---

*板块更新：2026-04-16*
