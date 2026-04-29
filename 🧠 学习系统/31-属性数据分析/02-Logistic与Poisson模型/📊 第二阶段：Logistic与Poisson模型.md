---
tags: ["属性数据分析", "阶段2", "Logistic与Poisson模型"]
created: 2026-04-12
status: ongoing
difficulty: intermediate
phase: 2
type: stage
topic: "第2阶段：Logistic与Poisson模型"
concept: ["Logistic 回归", "模型诊断", "Poisson 回归", "对数线性模型"]
prerequisites: ["列联表与二分类", "概率统计与回归分析基础"]
related: ["应用回归分析", "多元统计"]
---
# 📊 第2阶段：Logistic与Poisson模型

> 这一阶段聚焦：掌握最常用的离散响应广义线性模型。

## 📈 阶段进度

```dataviewjs
const notes = dv.pages('"🧠 学习系统/31-属性数据分析/02-Logistic与Poisson模型"').where(p => !p.file.path.endsWith("📊 第二阶段：Logistic与Poisson模型.md"));
const completed = notes.where(p => p.status === "completed").length;
const total = notes.length;
const progress = total > 0 ? Math.round((completed / total) * 100) : 0;
dv.paragraph(`**阶段进度: ${progress}%** (${completed}/${total} 主题)`);
```

## 📌 阶段定位
- 这一阶段要解决的问题：掌握最常用的离散响应广义线性模型。
- 推荐前置：列联表与二分类
- 学完后通向：多分类与相关响应
- 建议周期：4-6周

## ❓ 本阶段要回答的问题
- Logistic 回归 和 模型诊断 之间是什么关系？
- Poisson 回归 在这一阶段里解决什么核心痛点？
- 在进入下一阶段前，为什么必须先把 对数线性模型 讲清楚？

## 🧩 建议拆卡清单
| 模块 | 你要掌握什么 | 建议拆卡方向 |
|:---|:---|:---|
| Logistic 回归 | logit 链接、系数解释、预测概率与边际效应 | 最大似然、优势比、交互项 |
| 模型诊断 | 偏差、残差、拟合优度与分离问题 | deviance、Hosmer-Lemeshow、完全分离 |
| Poisson 回归 | 计数响应、对数链接和 offset | 暴露量、过度离散、率模型 |
| 对数线性模型 | 多维列联表建模与交互结构 | 主效应、交互、独立结构比较 |


## 🗂️ 建议原子笔记清单
| 模块 | 建议原子笔记题目 |
|:---|:---|
| Logistic 回归 | Logistic与Poisson模型-Logistic 回归-最大似然<br>Logistic与Poisson模型-Logistic 回归-优势比<br>Logistic与Poisson模型-Logistic 回归-交互项 |
| 模型诊断 | Logistic与Poisson模型-模型诊断-deviance<br>Logistic与Poisson模型-模型诊断-Hosmer-Lemeshow<br>Logistic与Poisson模型-模型诊断-完全分离 |
| Poisson 回归 | Logistic与Poisson模型-Poisson 回归-暴露量<br>Logistic与Poisson模型-Poisson 回归-过度离散<br>Logistic与Poisson模型-Poisson 回归-率模型 |
| 对数线性模型 | Logistic与Poisson模型-对数线性模型-主效应<br>Logistic与Poisson模型-对数线性模型-交互<br>Logistic与Poisson模型-对数线性模型-独立结构比较 |

## ✅ 完成标准
- [ ] 能用自己的话解释：掌握最常用的离散响应广义线性模型。
- [ ] 能区分并串联：Logistic 回归、模型诊断、Poisson 回归
- [ ] 能围绕 对数线性模型 至少拆出 6-10 条原子笔记并完成一轮整理
- [ ] 能把本阶段内容和 多分类与相关响应 接上

## 🔗 阶段导航
| ⬅️ 上一阶段 | 🧭 总览 | 下一阶段 ➡️ |
|:---:|:---:|:---:|
| [[🧠 学习系统/31-属性数据分析/01-列联表与二分类/📋 第一阶段：列联表与二分类\|进入上一阶段]] | [[🧠 学习系统/31-属性数据分析/🗺️ 属性数据分析学习路径\|返回总览]] | [[🧠 学习系统/31-属性数据分析/03-多分类与相关响应/🔗 第三阶段：多分类与相关响应\|进入下一阶段]] |

*阶段更新：2026-04-17*
