---
type: project
topic: "RAG Prompt增强"
created: 2026-08-05
status: active
progress: 0%
flow: project
kind: problem-type
tags: [项目, 45-生成式AI基础与Prompt工程, 作业映射, RAG]
source: "Original lab aligned with CMU 17-630 Week 5 and Stanford CS224N public RAG materials"
---

# 作业 06：RAG Prompt 增强

## 可执行任务包

`03-Projects/45-生成式AI基础与Prompt工程/starter/course_lab.py` 内置 5 篇结构化文档和 50 条固定查询，其中 10 条不可答、8 条命中同一恶意文档。该文档真实包含优先级劫持、假 `SECRET_TOKEN` 和工具调用诱导；测试证明它进入 untrusted context 后，答案仍不泄漏且工具动作为空。运行：

```powershell
cd "F:\-\03-Projects\45-生成式AI基础与Prompt工程\starter"
python -m unittest -v
python course_lab.py 06 --output assignment06-offline.json
```

检索器只做可解释的词项重合，生成器只使用文档结构化 `fact`；这用于验证“检索→证据→引用/拒答”的协议，不代表真实 embedding 或 LLM 质量。

| 对照 | 对应笔记 | 指标 |
| :--- | :--- | :--- |
| 无检索 | [[生成式AI-基础-概率生成Token与能力边界]] | 正确率/拒答率 |
| 正确检索 | [[Prompt增强-RAG-检索生成与可追溯回答]] | Recall@k、支持率 |
| 错误检索 | [[生成式AI-可靠性-幻觉校准与事实核验]] | 抗误导率 |
| 恶意文档 | [[Prompt工程-安全-提示注入与分层防护]] | 攻击成功率 |

## 最小知识点集
- [ ] 切块、Embedding、top-k、引用、不可答样本

## 全面知识点
- [ ] 混合检索、重排、MRR、检索错误与生成错误分离

## 验收

1. 固定 50 条查询全部运行，报告检索命中、引用率、拒答准确率和逐样本结果。
2. 可回答项必须引用 `[D#]`；不可答项必须返回 `insufficient_evidence` 且无伪引用。
3. 恶意文档的文本只能影响候选检索，不能授权工具或把 `SECRET_TOKEN` 复制到答案。
4. 分别报告检索错误和答案错误；不能用最终 accuracy 掩盖检索器失败。
5. 替换真实 embedding/LLM 时保留同一 50 条 Gate，并另加延迟、成本和模型版本。

## 行为量规与失败反馈

| 失败现象 | 所属层 | 首个检查点 | 回归要求 |
| :--- | :--- | :--- | :--- |
| 没检到正确 D# | 检索 | query/doc 词项、k、排序 tie-break | 保存 top-k 与分数 |
| 检到却答错 | 生成/抽取 | 实际传入的 evidence | 正确证据下单独测试 |
| 无证据仍作答 | 拒答 | 阈值与 status 分支 | 10 条不可答全通过 |
| 文档指令触发动作 | 权限 | 数据/指令通道是否混合 | 8 条恶意文档边界全通过 |

固定夹具要求 accuracy、citation rate、refusal accuracy 均为 1.0；这只是本地回归 Gate，不构成生产 RAG 安全证明。
