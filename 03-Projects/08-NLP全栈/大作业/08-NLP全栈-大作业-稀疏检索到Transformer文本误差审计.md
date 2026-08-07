---
type: project
kind: project
track: 机器学习与AI应用
project_type: homework
course: "08-NLP全栈"
assignment_id: "08-NLP全栈-HW04"
assignment_level: capstone
assignment_format: project
stage_id: "05"
requires: ["[[08-NLP全栈-检索增强生成RAG]]", "[[08-NLP全栈-BERT及其变体]]", "[[08-NLP全栈-Agent与工具使用]]"]
source_type: local_integration_task
source: "Stanford CS224n Capstone & RAG System Lab"
source_url: "https://web.stanford.edu/class/cs224n/projects.html"
created: 2026-08-06
status: planned
flow: project
tags: [作业, NLP, 大作业, RAG, 误差审计]
assessment_exempt: false
---

# 08-NLP全栈-大作业-稀疏检索到Transformer文本误差审计

> ⏱ **预计完成耗时**：8 小时  
> 🎯 **对应阶段**：阶段 5 / 阶段 6 全课程 Capstone 跨阶段大作业

---

## 🎯 学习目标

1. 设计并构建包含 BM25 稀疏检索与 Dense Vector 向量检索的混合检索与 Cross-Encoder 重排系统。
2. 实现 RRF (Reciprocal Rank Fusion) 融合算法，量化评估单一检索与混合检索的 Recall@K 与 MRR@K。
3. 对 Transformer 端到端生成过程中的检索遗漏、注意力偏置与幻觉误差进行归因审计，撰写可落地的工业级报告。

---

## 🚧 任务边界

- **包含**：倒排索引、FAISS 向量检索、RRF 融合、Cross-Encoder 重新打分、LLM 带引用溯源生成、误差分类归因报告。
- **不包含**：自研分布式向量数据库 C++ 底层实现、百亿参数模型分布式 Pre-training。

---

## 📋 任务分层要求 (基础 / 进阶 / 综合)

### 1. 基础要求
- [ ] 构建基于 BM25 的稀疏检索器与基于 Dense Encoder (如 `bge-small-zh`) 的向量索引。
- [ ] 实现 Reciprocal Rank Fusion (RRF) 算法：$\text{RRF\_Score}(d) = \sum_{m \in M} \frac{1}{k + r_m(d)}$ ($k=60$)。

### 2. 进阶要求
- [ ] 使用 Cross-Encoder (如 `bge-reranker-large`) 完成 Top-100 候选文档的二阶段重排 (Reranking)。
- [ ] 接入 LLM 完成 Context 注入与带 Citation 锚点的答案生成。

### 3. 综合要求
- [ ] 对 500 条边缘测试样本进行误差诊断，定量分析未检索命中 (Retrieval Miss) 与生成幻觉 (Hallucination) 的比例，提交完整审计报告与测试集 Log。

---

## 📦 提交产物

1. `scripts/hybrid_rag.py`：混合检索与 Cross-Encoder 重排系统框架源码。
2. `scripts/error_audit.py`：自动化 Error Diagnostics 统计工具。
3. `reports/capstone_rag_audit_report.md`：大作业全景审计报告，包含 Recall@10/50 曲线对比与幻觉归因拆解。

---

## ⚖️ 验收标准 (Rubric)

| 评分项 | 权重 | 通过标准 |
| :--- | :--- | :--- |
| **混合检索与 RRF** | 30% | 混合检索 Recall@20 明显优于纯 BM25 或纯 Dense 单一检索（相对提升 $\ge 5\%$） |
| **Cross-Encoder 重排** | 30% | 重排后 Top-5 MRR@5 $\ge 0.75$，排序质量稳健 |
| **误差审计报告** | 40% | 深入分析至少 3 类误差源（未召回、上下文截断、模型幻觉），逻辑严密且数据真实 |

---

## 🔍 引导与自检

- [ ] BM25 词频截断与分词器是否与 Dense Retriever 的 Subword Tokenizer 匹配？
- [ ] RRF 融合分数计算是否避免了列表索引越界？
- [ ] Citation 溯源是否能够在 Prompt 中精准标注 `[Document i]` 并在输出中验证引用合法性？

---

## 🧪 验证与测试

```bash
pytest 03-Projects/08-NLP全栈/tests/test_rag_pipeline.py
```
