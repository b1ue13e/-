---
type: study
topic: "阶段2-检索建模与Web信息"
course: "数据挖掘与信息检索"
created: 2026-08-07
status: completed
stage_moc: "[[🧭 阶段2-检索建模与Web信息]]"
flow: knowledge
kind: moc
tags: [学习, 数据挖掘与信息检索]
---
## 🎯 阶段目标

1. 掌握倒排索引构建、Variable Byte 及 Gamma 编码压缩算法。
2. 掌握 TF-IDF 模型与 BM25 概率检索模型参数调优与基线对拍。
3. 掌握 PageRank 幂迭代收敛过程与链接结构分析。
4. 掌握稠密向量召回（FAISS / ANN）与 Pairwise Learning-to-Rank (LTR) 重排序架构。

---

## 📚 本阶段知识卡清单

- [[Web 与信息检索]] — 信息检索体系概述与网络爬虫结构
- [[倒排索引系统]] — 词项-文档倒排表构建与布尔检索
- [[倒排索引压缩与VB-Gamma编码]] — Variable Byte 与 Elias Gamma 变长编码
- [[TF-IDF与BM25]] — 向量空间模型、TF-IDF 加权与 BM25 算法
- [[检索语言模型与平滑技术]] — Jelinek-Mercer 与 Dirichlet 语言模型平滑
- [[PageRank与链接分析]] — PageRank 幂迭代算法与 HITS 随机游走
- [[稠密检索与向量召回]] — 双塔向量表示、余弦距离与 FAISS 索引
- [[学习排序LTR]] — Pointwise, Pairwise 与 Listwise 学习排序框架
- [[检索评测与AB测试]] — MAP, MRR, NDCG 评估指标与在线 A/B 测试
- [[查询分析与纠错]] — 查询分词、拼写纠错与意图识别
- [[查询扩展与伪相关反馈]] — Rocchio 算法与伪相关反馈 (PRF)
- [[混合检索系统]] — 稀疏 BM25 与稠密 Vector 倒排融合 (RRF)

---

## 🏁 阶段验收与作业

```dataview
LIST
FROM "03-Projects/36-数据挖掘与信息检索"
WHERE stage_id = "02"
SORT assignment_level ASC, file.name ASC
```