---
type: study
topic: "AI Agent记忆与检索增强生成"
course: "AI Agent工程"
tags: [学习, 46-AI Agent工程, AI-Agent, RAG, 记忆]
created: 2026-08-05
status: completed
difficulty: intermediate
concept: [Agent记忆, RAG, 上下文管理]
prerequisites: [词向量相似度, AI-Agent-边界与感知行动循环]
related: [工具调用, 规划, 记忆污染]
stage_moc: "[[🧭 阶段3-上下文记忆与校验]]"
upstream: ["[[AI-Agent-上下文工程-选择压缩隔离]]"]
flow: knowledge
kind: concept
assessment_exempt: false
source: "UC Berkeley CS 194/294-196 F24 RAG; Stanford CS224V F25; Microsoft AI Agents for Beginners Lessons 5 and 13; Datawhale Hello-Agents Chapter 8; Hugging Face Agents Course Unit 3"
source_urls: ["https://github.com/microsoft/ai-agents-for-beginners/tree/main/05-agentic-rag", "https://github.com/microsoft/ai-agents-for-beginners/tree/main/13-agent-memory", "https://github.com/datawhalechina/hello-agents/tree/main/docs/chapter8"]
accessed: 2026-08-06
license: "Microsoft MIT；Hello-Agents CC BY-NC-SA 4.0；其他课程材料许可待核验；本卡为原创整合"
anki_deck: "46-AI Agent工程::05-记忆与RAG"
anki_tags: [46-AI-Agent工程, 记忆, RAG]
---

# AI Agent：记忆与检索增强生成

## 0. 学习边界

- **类别**：**A 类（核心概念，必须深挖）**
- **判断理由**：Agent 的上下文有限，参数知识会过期，工具轨迹会膨胀。记忆与 RAG 决定系统能否取得证据、保留必要状态，同时也是间接注入与隐私风险的主要入口。

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦**：把所有历史、文档和工具输出都塞进 prompt 会超窗、增噪、增成本；完全不保存又会重复工作和忘记约束。

本卡区分工作记忆、情节记忆、语义知识与外部检索，并建立“写入—索引—检索—验证—引用—淘汰”闭环。

## 2. 为什么它重要？它有什么用？

- **连接大图景**：记忆更新状态，RAG 是读取外部证据的工具，多 Agent 需共享经过治理的公共状态。
- **实际应用场景**：文档问答、长期任务、个性化、评论检索和研究助手。
- **高频题型/任务**：chunk、检索排序、引用、记忆写入策略、上下文预算和污染防护。

## 3. 学它之前需要哪些前置知识？

1. **[[AI-Agent-边界与感知行动循环]]**：检索结果是观察，摘要是状态压缩。
2. **[[08-NLP全栈/03-深度学习NLP基础/NLP全栈-词向量与Word2Vec|词向量与 Word2Vec]]**：理解向量检索只是候选生成，不等于事实正确。

## 4. 用直觉语言解释它

> “这东西其实就像做研究时的桌面、实验日志和图书馆：桌面放当前任务，日志记经历，图书馆按问题取证据；不能把整座图书馆搬上桌。”

- **直觉类比**：工作记忆短而活跃，长期记忆需索引，原始证据要保留来源。
- **为什么很自然**：有限上下文要求选择；选择必须围绕当前问题和可信度。
- **一句话直觉本质**：记住“未来会改变决策的最小信息”，按需取回可验证证据。

## 5. 正式定义、核心公式、符号解释

### 1. 最核心定义

给定查询 $q$ 和语料 $D$，检索器生成候选 $R_k(q)$，重排/过滤器选择上下文 $C$，生成器基于目标、当前状态和 $C$ 输出答案；记忆写入函数只保存满足价值、可信度和隐私策略的事件。

### 2. 核心公式

$$R_k(q)=\operatorname{TopK}_{d\in D} score(q,d)$$

$$C^*=\arg\max_{C\subseteq R_k(q)}\sum_{d\in C}Rel(q,d)-\alpha Redundancy(C)-\beta Risk(d)$$

### 3. 符号说明表

| 符号 | 含义 | 取值范围 / 量纲 | 备注 |
| :--- | :--- | :--- | :--- |
| $D$ | 文档/记忆库 | 带元数据条目 | 需来源与时间 |
| $score$ | 检索分数 | 实数 | 不等于真值概率 |
| $C$ | 注入上下文 | token 预算内集合 | 需要去重与排序 |
| $Risk$ | 污染/隐私风险 | 策略评分 | 高风险应隔离 |

### 4. 常见变体与适用条件

- **检索**：关键词、稠密向量、混合检索、图检索；**记忆**：窗口、摘要、事件、用户偏好。
- **限制条件**：高风险知识应使用授权数据源和确定性引用；用户偏好必须允许查看、更正和删除。

## 6. 推导思路和思想来源

- **最初困难**：模型参数不能覆盖私有、最新或任务现场信息。
- **直接方法局限**：长上下文并不自动解决检索，噪声和位置效应仍会损害回答。
- **关键“转念”**：先用便宜检索缩小候选，再验证、重排和引用；记忆写入也应有门槛。
- **推导主线与动机**：语料治理→切分→索引→候选→重排→上下文组装→引用评测。
- **为什么自然得到此结论**：Agent 需要的是与当前决策相关的证据，而不是最大量文本。

## 7. 例子：基础 → 中等 → 实际应用

### 例子 1：基础例子（可手算）

- **题目**：查询词集合 `{food, good}`。文档 A `{food, good, service}`，B `{food, slow}`。用 Jaccard 相似度排序。
- **解题思路与关键步骤**：A 交集 2、并集 3，$2/3$；B 交集 1、并集 3，$1/3$。
- **最终答案**：A 排在 B 前。
- **易错点**：把分数当成 A 必然真实或足以回答。
- **🤔 追问**：若 A 来源未知、B 来自官方数据库，如何加入可信度？

### 例子 2：中等例子（条件判断与多步推理）

对餐厅评分，应检索目标餐厅评论并保留评论 ID；若名称歧义先澄清；若只命中一条低置信评论，应报告证据不足。把另一餐厅的高相似评论注入会造成实体混淆。

### 例子 3：实际应用例子（真实场景/代码）

标准库词集检索；输入 `"good food"`，先返回带来源的 `r1`。

```python
import re

DOCS = [
    {"id": "r1", "text": "good food and friendly service", "source": "verified-review"},
    {"id": "r2", "text": "slow service but clean room", "source": "verified-review"},
]

def tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z]+", text.lower()))

def retrieve(query: str, top_k: int = 2) -> list[dict[str, object]]:
    query_tokens = tokens(query)
    ranked = []
    for document in DOCS:
        doc_tokens = tokens(document["text"])
        union = query_tokens | doc_tokens
        score = len(query_tokens & doc_tokens) / len(union) if union else 0.0
        ranked.append({**document, "score": round(score, 3)})
    return sorted(ranked, key=lambda item: item["score"], reverse=True)[:top_k]

print(retrieve("good food"))
```

## 8. 常见误区和易混概念

### 误区 1：RAG 会消除幻觉
- **错误直觉**：给了文档，模型就只能说文档内容。
- **为什么错**：检索可漏召回/错召回，生成可误读，文档可冲突或被注入。
- **正确理解**：分别评测检索、证据归因和最终答案，并允许“不知道”。

### 误区 2：所有对话都应写入长期记忆
- **错误直觉**：记得越多越个性化。
- **为什么错**：会积累错误、敏感信息和过期偏好。
- **正确理解**：写入需用途、可信度、保留期、用户控制和删除策略。

### 概念对比表

| 概念 | 核心问题 | 关键区别 | 典型使用场景 |
| :--- | :--- | :--- | :--- |
| 工作记忆 | 当前轮必须保留什么？ | 短期、容量小 | 工具轨迹 |
| 情节记忆 | 过去发生过什么？ | 带时间与结果 | 失败复盘 |
| 语义记忆 | 稳定事实是什么？ | 去情境化知识 | 用户偏好、领域知识 |
| RAG | 当前问题需取哪份外证？ | 按需检索并引用 | 文档问答 |

## 9. 来源定位与关系

- [[🗺️ 数据挖掘与信息检索学习路径|信息检索]]提供召回、排序和相关性评测基础。
- 直接知识依赖以 frontmatter `upstream` 为唯一事实源；直接后续由本文末 Dataview 反向派生。

## 10. 闭卷复现任务

- [ ] 1. 区分四类记忆。
- [ ] 2. 写出 Top-K 公式。
- [ ] 3. 手算 Jaccard。
- [ ] 4. 解释检索分数为何不是真值概率。
- [ ] 5. 写出记忆写入门槛。
- [ ] 6. 为上下文预算设计去重策略。
- [ ] 7. 说出 RAG 三层评测。
- [ ] 8. 给出证据不足的回答策略。
- [ ] 9. 说明间接注入入口。
- [ ] 10. 解释用户为何应能删除记忆。

## 11. 自测题：5 道

### 1. #自测题/基础
**题目**：RAG 的检索结果是什么性质？
> [!question]- 答案解析
> - **答案**：与查询相关的候选证据，不是自动可信的真相或指令。
> - **解析**：还需来源、时间、实体和内容验证。

### 2. #自测题/基础
**题目**：为什么要保存文档 ID/来源？
> [!question]- 答案解析
> - **答案**：支持引用、核验、去重、撤回和错误追踪。
> - **解析**：只保存摘要会失去证据链。

### 3. #自测题/中等
**题目**：Top-1 高分文档与问题实体不同，能用吗？
> [!question]- 答案解析
> - **答案**：不能直接用；实体约束优先，需过滤或重新查询。
> - **解析**：词面相似不能替代实体一致性。

### 4. #自测题/中等
**题目**：长期记忆中的用户偏好与本轮明确要求冲突，谁优先？
> [!question]- 答案解析
> - **答案**：本轮明确要求优先，并可询问是否更新过期偏好。
> - **解析**：记忆是辅助数据，不是不可覆盖指令。

### 5. #自测题/较难
**题目**：设计 RAG 的最小离线评测。
> [!question]- 答案解析
> - **答案**：带金标准证据与答案的数据集；测 recall@k/MRR、证据精确性与引用覆盖、答案正确性/拒答；分实体、时间和对抗文档切片。
> - **解析**：端到端分数无法定位检索还是生成失败。

## 12. 我的主动回忆区

### 我的闭卷复述
> 解释为什么“多上下文”不等于“好记忆”：

### 我的推导复现
> 为评论库设计条目元数据和淘汰规则：

### 我的错误与卡点
- 

### 下次复习日期
- [ ] 明天
- [ ] 3 天后
- [ ] 7 天后
- [ ] 14 天后

## 13. 给 Obsidian 的归档建议

- **适合文件夹**：`02-Knowledge/🧠 学习系统/46-AI Agent工程/`
- **关联已有笔记**：[[AI-Agent-ReAct推理行动范式]]、[[AI-Agent-安全威胁建模与系统评测]]
- **建议标签**：`#学习` `#RAG` `#Agent记忆`
- **拆分建议**：向量检索实现、GraphRAG 或长期记忆评测独立成实验时拆卡。

## 🔗 直接后续（派生）

```dataview
LIST
FROM "02-Knowledge/🧠 学习系统/46-AI Agent工程"
WHERE contains(upstream, this.file.link)
SORT file.name ASC
```

## 🧪 学完本节后可完成的作业

```dataview
LIST
FROM "03-Projects/46-AI Agent工程"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 🃏 Anki 卡片

- RAG 检索结果为何只是候选证据？::相关性分数衡量查询匹配，不保证来源可信、实体一致、内容新鲜或事实正确。
- Agent 记忆写入前应检查什么？::未来决策价值、来源可信度、隐私与授权、保留期限、可更正和可删除性。
- RAG 应分哪三层评测？::检索召回与排序、证据归因/引用质量、最终答案正确性与恰当拒答。

