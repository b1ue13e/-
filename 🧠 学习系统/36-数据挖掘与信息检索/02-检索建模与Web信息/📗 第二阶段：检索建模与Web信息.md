---
type: stage
topic: 第二阶段：检索建模与Web信息
tags:
- 信息检索
- 阶段2
- Web
created: 2026-04-14
status: planned
difficulty: intermediate
concept: []
prerequisites: []
related: []
phase: 2
---

# 📗 第二阶段：检索建模与Web信息

> 让信息能被快速找到、正确排序、稳定评估。

---

## 📊 阶段进度

```dataviewjs
const notes = dv.pages('"🧠 学习系统/36-数据挖掘与信息检索/02-检索建模与Web信息"')
    .where(p => !p.file.path.includes("📗"));
const completed = notes.where(p => p.status === "completed").length;
const total = notes.length;
const progress = total > 0 ? Math.round((completed / total) * 100) : 0;
dv.paragraph(`**阶段进度: ${progress}%** (${completed}/${total} 主题)`);
```

---

## 📖 学习清单

| 状态 | 主题 | 快速创建 |
|:---:|:---|:---:|
| ⬜ | [[倒排索引系统]] | [📝 创建](obsidian://new?file=🧠%20学习系统/36-数据挖掘与信息检索/02-检索建模与Web信息/倒排索引系统.md) |
| ⬜ | [[TF-IDF与BM25]] | [📝 创建](obsidian://new?file=🧠%20学习系统/36-数据挖掘与信息检索/02-检索建模与Web信息/TF-IDF与BM25.md) |
| ⬜ | [[查询分析与纠错]] | [📝 创建](obsidian://new?file=🧠%20学习系统/36-数据挖掘与信息检索/02-检索建模与Web信息/查询分析与纠错.md) |
| ⬜ | [[PageRank与链接分析]] | [📝 创建](obsidian://new?file=🧠%20学习系统/36-数据挖掘与信息检索/02-检索建模与Web信息/PageRank与链接分析.md) |
| ⬜ | [[学习排序LTR]] | [📝 创建](obsidian://new?file=🧠%20学习系统/36-数据挖掘与信息检索/02-检索建模与Web信息/学习排序LTR.md) |
| ⬜ | [[检索评测与AB测试|检索评测与A/B测试]] | [📝 创建](obsidian://new?file=🧠%20学习系统/36-数据挖掘与信息检索/02-检索建模与Web信息/检索评测与A-B测试.md) |
| ⬜ | [[稠密检索与向量召回]] | [📝 创建](obsidian://new?file=🧠%20学习系统/36-数据挖掘与信息检索/02-检索建模与Web信息/稠密检索与向量召回.md) |
| ⬜ | [[混合检索系统]] | [📝 创建](obsidian://new?file=🧠%20学习系统/36-数据挖掘与信息检索/02-检索建模与Web信息/混合检索系统.md) |
| ⬜ | [[Web 与信息检索]] | [📝 创建](obsidian://new?file=🧠%20学习系统/36-数据挖掘与信息检索/02-检索建模与Web信息/Web%20与信息检索.md) |

---

## 🎯 核心目标

- [ ] 理解索引、召回、排序、评测四个基本层次
- [ ] 能解释 BM25、PageRank、LTR 的角色差异
- [ ] 能区分稠密检索、稀疏检索与混合检索

---

## 🔗 前置知识

- [[🧠 学习系统/36-数据挖掘与信息检索/02-检索建模与Web信息/📘 第一阶段：数据挖掘基础|阶段1：数据挖掘基础]]
- [[🧠 学习系统/08-NLP全栈/🗺️ NLP全栈学习路径|NLP全栈]] - 文本表示与语义检索

---

## 🔗 阶段导航

| ⬅️ 上一阶段 | 📋 总览 | 下一阶段 ➡️ |
|:---:|:---:|:---:|
| [[🧠 学习系统/36-数据挖掘与信息检索/02-检索建模与Web信息/📘 第一阶段：数据挖掘基础|阶段1]] | [[🗺️ 数据挖掘与信息检索学习路径\|返回总览]] | [[🧠 学习系统/36-数据挖掘与信息检索/02-检索建模与Web信息/📙 第三阶段：大数据系统与分析|进入阶段3]] |

---

*阶段创建：2026-04-14*
