---
type: stage
asset_eligibility: executable
topic: 板块 F：实战项目层
tags:
- 时间序列
- 实战
- 项目
- 教材外延
created: 2026-04-11
status: active
difficulty: advanced
concept:
- 项目复现
- 预测评估
- 模型比较
prerequisites:
- ARIMA模型
- GARCH模型
- 协整
- 时间序列交叉验证
related:
- 量化金融
- 能源预测
- 机器学习
phase: F
---

# 🚀 板块 F：实战项目层

> 本板块是 L00–L09 的结课出口：先完成 HW09 与经典基线，再决定是否叠加 ML/DL。项目资产统一存放在 `03-Projects/金融与时序/02-时间序列分析/`。

## 📊 板块进度

```dataviewjs
const projects = dv.pages('"03-Projects/金融与时序/02-时间序列分析"').where(p => p.type === "project" && p.kind === "project");
const total = projects.length;
const completed = projects.where(p => p.status === "completed").length;
const progress = total > 0 ? Math.round((completed / total) * 100) : 0;
dv.paragraph(`**学习者项目进度: ${progress}%** (${completed}/${total} 个真实实现项目完成)`);
dv.table(["项目", "状态", "进度"], projects.map(p => [p.file.link, p.status, p.progress ?? "未填写"]));
```

> 评分示例、答案册和 HW 不计入学习者项目完成率；只有 `kind: project` 的真实实现项目参与统计。

## 📚 项目基线与样例

- 最小交付：[[HW09-滚动预测与完整建模报告]]。
- 实现主项目：[[项目-时间序列预测与漂移监控]]。
- 评分参照：[[Capstone-评分示例与失败案例]]。
- 只有统计基线完成后，才引入树模型或深度模型比较。

## 📖 项目建议

| 项目方向 | 先做的教材基线 | 之后可扩展到 |
|:---|:---|:---|
| 单变量需求/销售预测 | [[时间序列结构-趋势季节噪声与ETS分解]] + [[L05-ARMA与ARIMA建模闭环]] | [[XGBoost时序预测]] |
| 金融收益率与波动率 | [[GARCH波动率建模]] | [[LSTM与GRU在时序中的应用]] |
| 多变量经济时序 | [[协整]] + [[误差修正模型]] | [[Transformer 时序预测]] |
| 能源负荷预测 | [[季节性与STL分解]] + [[L06-SARIMA与季节预测]] | [[N-BEATS与N-HiTS]] |

## ✅ 完成标准

- [ ] 每个项目都先给出一个清晰的教材基线模型
- [ ] 用滚动验证或时间序列交叉验证比较不同方法
- [ ] 记录“为什么复杂模型优于或不优于传统模型”
- [ ] 把实验结论沉淀回前面板块的概念笔记

## 🔗 板块导航

| ⬅️ 上一板块 | 📋 总览 |
|:---:|:---:|
| [[🤖 板块E：机器学习与深度学习进阶\|返回板块E]] | [[🗺️ 时间序列分析学习路径\|返回总览]] |


---

*板块更新：2026-04-16*
