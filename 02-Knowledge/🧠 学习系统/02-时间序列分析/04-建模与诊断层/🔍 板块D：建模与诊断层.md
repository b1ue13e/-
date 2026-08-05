---
type: stage
topic: 板块 D：建模与诊断层
tags:
- 时间序列
- 建模诊断
- 教材主线
created: 2026-04-11
status: active
difficulty: intermediate
concept:
- 时间序列分解
- 协整
- 误差修正模型
prerequisites:
- ARIMA模型
- 预测与评估
related:
- 趋势分析
- 季节效应分析
- 单位根检验
phase: D
---

# 🔍 板块 D：建模与诊断层

> 本板块是 L00–L09 结课后的专题支线，解决分解、变换、非平稳回归、协整和误差修正。它不是第二套并行必修课程。

## 📊 板块进度

```dataviewjs
const required = [
  "时间序列结构-趋势季节噪声与ETS分解",
  "季节性与STL分解",
  "02-Knowledge/🧠 学习系统/02-时间序列分析/04-建模与诊断层/方差齐性变换",
  "动态回归与ARIMAX",
  "残差诊断与白噪声检验",
  "单位根检验-ADF-KPSS",
  "02-Knowledge/🧠 学习系统/02-时间序列分析/04-建模与诊断层/虚假回归",
  "02-Knowledge/🧠 学习系统/02-时间序列分析/04-建模与诊断层/协整",
  "02-Knowledge/🧠 学习系统/02-时间序列分析/04-建模与诊断层/误差修正模型",
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

> `status: completed` 只表示笔记内容已经编写完成，不代表你已经掌握。完成闭卷复述、练习与迁移后，在对应主题卡设置 `mastery: 3`。

## 📚 开放来源

- 分解与变换：[FPP3 Ch.3](https://otexts.com/fpp3/)
- 回归误差与 ARCH/GARCH：[Penn State STAT 510](https://online.stat.psu.edu/stat510/)
- 单位根、结构突变与协整：[MIT OCW 14.384 Lectures 17–20](https://ocw.mit.edu/courses/14-384-time-series-analysis-fall-2013/pages/lecture-notes/)

## 📖 学习清单

| 教材位置 | 重点 | 笔记入口 |
|:---|:---|:---|
| FPP3 Ch.3 | 分解、趋势、季节性 | [[时间序列结构-趋势季节噪声与ETS分解]] / [[季节性与STL分解]] |
| FPP3 §3.1 | 方差稳定与逆变换 | [[方差齐性变换]] |
| STAT 510 | 回归误差和诊断 | [[动态回归与ARIMAX]] / [[残差诊断与白噪声检验]] |
| MIT 14.384 L17–20 | 单位根、虚假回归、协整、ECM | [[单位根检验-ADF-KPSS]] / [[虚假回归]] / [[协整]] / [[误差修正模型]] |

## ✅ 完成标准

- [ ] 能区分“确定性非平稳”和“随机非平稳”
- [ ] 能把趋势、季节、差分和协整放进同一条分析链路里
- [ ] 能理解为什么多元时间序列会出现虚假回归
- [ ] 至少完成一个协整或误差修正模型的整理笔记

## 🔗 板块导航

| ⬅️ 上一板块 | 📋 总览 | 下一板块 ➡️ |
|:---:|:---:|:---:|
| [[📈 板块C：经典模型层\|返回板块C]] | [[🗺️ 时间序列分析学习路径\|返回总览]] | [[🤖 板块E：机器学习与深度学习进阶\|进入板块E]] |


---

*板块更新：2026-04-16*
