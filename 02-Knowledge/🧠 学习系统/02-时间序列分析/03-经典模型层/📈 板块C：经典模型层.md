---
type: stage
topic: 板块 C：经典模型层
tags:
- 时间序列
- 经典模型
- 教材主线
created: 2026-04-11
status: active
difficulty: intermediate
concept:
- ARMA
- ARIMA
- GARCH
prerequisites:
- 平稳时间序列
- 自相关函数ACF
related:
- 模型识别
- 预测与评估
- 条件异方差
phase: C
---

# 📈 板块 C：经典模型层

> 本板块是 L03–L08 的补充知识地图；不与 L00–L09 并行推进。

## 📊 板块进度

```dataviewjs
const topics = dv.pages('"02-Knowledge/🧠 学习系统/02-时间序列分析/03-经典模型层"').where(p => p.type === "study");
const total = topics.length;
const completed = topics.where(p => p.status === "completed").length;
const progress = total > 0 ? Math.round((completed / total) * 100) : 0;
dv.paragraph(`**板块进度: ${progress}%** (${completed}/${total} 模块)`);
```

## 📚 开放来源与主卡

- ARIMA：[FPP3 Ch.9](https://otexts.com/fpp3/arima.html)。
- ARCH/GARCH：[Penn State STAT 510 Lesson 11.1](https://online.stat.psu.edu/stat510/Lesson11)。
- 主课：[[L03-AR模型与均值回归]]至[[L08-残差诊断与纯随机性检验]]。

## 📖 学习清单

| 教材位置 | 重点 | 笔记入口 |
|:---|:---|:---|
| L03–L04 | AR、MA 与冲击传播 | [[L03-AR模型与均值回归]] / [[L04-MA模型与有限冲击]] |
| L05–L06 | ARIMA 与 SARIMA | [[L05-ARMA与ARIMA建模闭环]] / [[L06-SARIMA与季节预测]] |
| L07–L08 | 识别、估计与残差 | [[L07-模型识别与参数估计]] / [[L08-残差诊断与纯随机性检验]] |
| 扩展 | 条件异方差 | [[GARCH波动率建模]] |

## ✅ 完成标准

- [ ] 能根据平稳性和自相关结构区分 AR、MA、ARMA、ARIMA
- [ ] 能说清差分在非平稳序列建模中的作用
- [ ] 能把 GARCH 放回“条件异方差”这条统计主线里理解
- [ ] 至少完成一个从识别到预测的完整经典模型案例

## 🔗 板块导航

| ⬅️ 上一板块 | 📋 总览 | 下一板块 ➡️ |
|:---:|:---:|:---:|
| [[📊 板块B：统计基础层\|返回板块B]] | [[🗺️ 时间序列分析学习路径\|返回总览]] | [[🔍 板块D：建模与诊断层\|进入板块D]] |


---

*板块更新：2026-04-16*
