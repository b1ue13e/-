---
type: stage
topic: 板块 C：经典模型层
tags:
- 时间序列
- 经典模型
- 教材主线
created: 2026-04-11
status: planned
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

> 这个板块把王燕教材第 3 章和第 5 章里的经典模型主干合并起来，先做 ARMA，再走 ARIMA 与 GARCH。

## 📊 板块进度

```dataviewjs
const total = dv.pages('"🧠 学习系统/02-时间序列分析/03-经典模型层"').length - 1;
const completed = dv.pages('"🧠 学习系统/02-时间序列分析/03-经典模型层"').where(p => p.status === "completed").length;
const progress = total > 0 ? Math.round((completed / total) * 100) : 0;
dv.paragraph(`**板块进度: ${progress}%** (${completed}/${total} 模块)`);
```

## 📚 对应教材

- 主教材：[[📚 书库/书籍笔记/时间序列分析基于R|时间序列分析基于R]]
- 对应章节：第 3 章《平稳时间序列分析》 + 第 5 章中的 `差分运算`、`ARIMA 模型`、`条件异方差模型`

## 📖 学习清单

| 教材位置 | 重点 | 笔记入口 |
|:---|:---|:---|
| 3.1-3.2 | AR、MA、ARMA 的定义与性质 | [[AR模型]] / [[MA模型]] / [[ARMA模型]] |
| 3.3 | 平稳序列建模：识别、估计、定阶 | [[模型识别]] / [[参数估计]] / [[AIC与BIC]] |
| 3.4 | 基于经典模型做预测 | [[预测与评估]] |
| 5.1-5.2 | 差分运算与 ARIMA 建模 | [[差分运算]] / [[🧠 学习系统/02-时间序列分析/03-经典模型层/ARIMA模型|ARIMA模型]] / [[SARIMA模型]] |
| 5.6 | ARCH/GARCH 族模型 | [[ARCH模型]] / [[🧠 学习系统/02-时间序列分析/03-经典模型层/GARCH模型|GARCH模型]] |

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
