---
type: study
topic: "第二阶段：传统统计NLP方法 (Traditional Statistical NLP)"
course: "08-NLP全栈"
created: 2026-08-06
status: active
flow: knowledge
kind: moc
tags: [学习, NLP, MOC, 传统NLP]
sources: ['Jurafsky, D., & Martin, J. H. (2024). Speech and Language Processing (3rd ed. draft).']
assessment_exempt: true
assessment_exempt_reason: 阶段 MOC 导航与学习目标总览页
---

# 🧭 08-NLP全栈 - 阶段 2：传统统计 NLP 方法

> ⏱ **预计完成耗时**：6 小时  
> 🎯 **阶段目标**：掌握文本预处理、向量空间模型 (TF-IDF/One-hot)、子词分词 (BPE)、隐马尔可夫模型 (HMM)/CRF 序列标注以及 LDA 主题模型。

---

## 🧭 为什么现在学 & 学习顺序

深度学习爆发前，传统统计 NLP 使用人工特征工程与概率图模型解决自然语言处理问题。理解传统方法有助于掌握基线设计与文本表征演进。
按以下顺序学习：
1. [[08-NLP全栈-文本预处理|文本预处理]]：正则化、停用词过滤与清洗
2. [[08-NLP全栈-文本表示方法|文本表示方法]]：One-hot, Bag-of-Words, TF-IDF
3. [[08-NLP全栈-子词分词|子词分词]]：BPE, WordPiece, Unigram 解决 OOV 问题
4. [[08-NLP全栈-统计机器学习|统计机器学习]]：朴素贝叶斯、SVM 文本分类
5. [[08-NLP全栈-序列标注|序列标注]]：HMM, CRF 词性标注与命名实体识别
6. [[08-NLP全栈-句法分析|句法分析]]：短语结构树与依存句法分析
7. [[08-NLP全栈-主题模型|主题模型]]：pLSA 与 LDA 文本隐主题挖掘

---

## 📚 本阶段有序知识卡清单

- 1️⃣ [[08-NLP全栈-文本预处理]]
- 2️⃣ [[08-NLP全栈-文本表示方法]]
- 3️⃣ [[08-NLP全栈-子词分词]]
- 4️⃣ [[08-NLP全栈-WordPiece与SentencePiece分词]]
- 5️⃣ [[08-NLP全栈-统计机器学习]]
- 6️⃣ [[08-NLP全栈-序列标注]]
- 7️⃣ [[08-NLP全栈-句法分析]]
- 8️⃣ [[08-NLP全栈-主题模型]]

---

## 🧪 阶段验收与作业

- **关联作业**：[[08-NLP全栈-课后作业-01-词向量与文本表征|课后作业-01-词向量与文本表征]]、[[08-NLP全栈-课后作业-05-传统NLP与序列标注实战|课后作业-05-传统NLP与序列标注实战]]
- **通过标准**：完成 TF-IDF 矩阵构建、WordPiece/BPE 字节对合并与 HMM Viterbi 序列标注代码编写。

```dataview
TABLE assignment_id AS "ID", assignment_level AS "层级", status AS "状态"
FROM "03-Projects/08-NLP全栈"
WHERE contains(requires, this.file.link) OR contains(requires, [[08-NLP全栈-文本表示方法]])
```

---

## 🔗 阶段导航

| ⬅️ 上一阶段 | 📋 课程主路径 | 下一阶段 ➡️ |
|:---:|:---:|:---:|
| [[01-基础准备/🧭 阶段1-基础准备\|阶段 1：基础准备]] | [[02-Knowledge/🧠 学习系统/08-NLP全栈/🗺️ 08-NLP全栈学习路径\|08-NLP全栈学习路径]] | [[03-深度学习NLP基础/🧭 阶段3-深度学习NLP基础\|阶段 3：深度学习NLP基础]] |
