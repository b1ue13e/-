---
type: project
project_type: homework
topic: "带引用研究助手"
course: "AI Agent工程"
assignment_id: "AI-Agent工程-S03"
assignment_level: stage
assignment_format: project
stage_id: "03"
requires: ["[[AI-Agent-上下文工程-选择压缩隔离]]", "[[AI-Agent-记忆与检索增强生成]]", "[[AI-Agent-反思与元认知-校验修正停止]]", "[[AI-Agent-规划状态与工作流编排]]"]
source_type: local_integration_task
source: "课程原创任务；融合 Microsoft Agentic RAG/Context/Memory/Metacognition 与 Hello-Agents Deep Research 能力目标"
source_url: "https://github.com/datawhalechina/hello-agents/tree/main/docs/chapter14"
accessed: 2026-08-06
license: "任务文本原创；Microsoft MIT；Hello-Agents CC BY-NC-SA 4.0"
assignment_id: "AI-Agent工程-S03"
assignment_level: stage
assignment_format: project
stage_id: "03"
requires: ["[[AI-Agent-上下文工程-选择压缩隔离]]", "[[AI-Agent-记忆与检索增强生成]]", "[[AI-Agent-反思与元认知-校验修正停止]]", "[[AI-Agent-规划状态与工作流编排]]"]
source_type: local_integration_task
source: "课程原创任务；融合 Microsoft Agentic RAG/Context/Memory/Metacognition 与 Hello-Agents Deep Research 能力目标"
source_url: "https://github.com/datawhalechina/hello-agents/tree/main/docs/chapter14"
accessed: 2026-08-06
license: "任务文本原创；Microsoft MIT；Hello-Agents CC BY-NC-SA 4.0"
created: 2026-08-06
status: planned
flow: project
tags: [作业, 阶段作业, 46-AI Agent工程, 研究助手, 引用]
---

# AI Agent 工程阶段作业 03：带引用研究助手 (Deep Research)

## 🎯 学习目标

1. **多步骤规划与子任务分解**：掌握将复杂研究课题（如“如何判定一个 AI Agent 是否具备生产部署条件”）拆解为 DAG 有向无环图结构子问题的方法。
2. **离线检索与安全上下文装配**：实现只读本地 Markdown 文档切片检索与 Rank/Filtering 算法，在固定 Token 预算内排除恶意注入与过期数据。
3. **确定性引用校验与事实锚定**：对导出的研究报告实现 `Claim -> Source Chunk -> Direct Quote` 的逐句验证，确保每个断言均有真实证据支撑。
4. **有限修正与冲突降级**：实现限制在 2 轮以内的模型自反思机制；当证据冲突或缺乏支持时，自动降级并输出包含未决项（Unresolved Claims）的透明报告。

---

## 🚧 任务背景与边界

在实际 Agent 应用中，“Deep Research”（深层研究助手）必须能够综合多源信息并产出具备严肃引用出处的分析报告。本实验限定运行在**离线课程 Markdown 文档库**上。

**边界与假设**：
- **只读操作**：禁止发起真实 HTTP 网络连接，禁止写入或更改课程原文档。
- **抗注入性**：语料中混入了包含“忽略系统提示词”的注入文本。无论注入语句声称什么，绝对不能改变系统层面的只读与校验规则。
- **事实第一原则**：如果检索到的证据互相矛盾，报告中必须显式标注“证据冲突”而非由模型凭空凭感觉裁决。

---

## 📝 详细题目与里程碑

### 里程碑 1 (M1)：问题 DAG 规划与任务分解 (`src/research_planner.py`)
针对目标课题，自动生成 3~5 个有序子任务节点：
- Node 1：`"检查系统安全与受限循环设计"`
- Node 2：`"评估上下文 Token 预算与记忆衰减策略"`
- Node 3：`"核验部署门禁与审批签名机制"`
建立节点间的依赖关系 `depends_on: [Node 1, Node 2]`。

### 里程碑 2 (M2)：离线检索与安全过滤 (`src/retriever.py`)
从本地课程 Markdown 提取至少 8 份切片：
```python
@dataclass
class ResearchChunk:
    chunk_id: str
    doc_title: str
    text_content: str
    trust_level: float   # 1.0 (官方) ~ 0.5 (社区)
    is_malicious: bool
```
过滤逻辑必须自动抹除 `is_malicious=True` 的注入项，并限制装配在 1000 Token 预算内。

### 里程碑 3 (M3)：带引用的结构化报告生成 (`src/report_generator.py`)
生成格式规范的研究报告，每一段包含显式 Wikilink 引用：
> "Agent 在部署前必须经过硬性步数限制以防止无限循环 [[AI-Agent工程-课后作业-02-受限循环与工具契约]]。"

### 里程碑 4 (M4)：离线引用校验器与有限修正 (`src/verifier.py`)
遍历报告中的每一句断言：
1. 校验引用 WikiLink 是否存在于已检索切片列表中。
2. 计算断言与引用切片的重合度（Keyword Overlap Score）。
3. 重合度 $< 0.4$ 时触发至多 2 轮修正。若第 2 轮仍失败，标为 `[证据不足/争议]` 并保留降级输出。

---

## 🛠️ 环境与复现

- **运行环境**：Python 3.11+ 标准库，无需外部依赖。
- **测试命令**：
  ```bash
  python -m unittest discover -s tests -v
  ```
- **测试样本**：包含正常研究课题与带恶意注入语料的专门测试用例。

---

## 📦 提交产物清单

1. `src/research_planner.py`：子问题规划器。
2. `src/retriever.py`：本地检索与 Token 预算选择器。
3. `src/verifier.py`：引用校验与有限修正状态机。
4. `tests/test_research_assistant.py`：包含 10+ 个自动化测试用例。
5. `output/research_report.md`：导出的完整研究报告。
6. `output/verification_log.json`：引用校验与修正轨迹日志。

---

## 📏 验收标准与 Rubric

| 评估维度 | 分值 | 验收标准与扣分细则 |
| :--- | :---: | :--- |
| **问题规划与 DAG** | 15分 | 准确分解子问题且无环。缺少 DAG 关系扣 8 分。 |
| **来源检索与预算** | 25分 | 严格过滤注入切片且控制 Token 预算。预算越界扣 10 分。 |
| **引用支持准确性** | 25分 | 报告每个断言均有真实验收引用。存在无来源断言扣 15 分。 |
| **有限修正与降级** | 15分 | 限制 $\le 2$ 轮修正，支持降级标记。无限重试扣 15 分。 |
| **测试与可复现性** | 20分 | 测试覆盖注入防护、证据冲突与降级逻辑。缺测试扣 10 分。 |

---

## 💡 引导与自检

- **自检点 1**：检索器是否会误将恶意 Markdown 中的 Prompt 注入执行为系统指令？
- **自检点 2**：校验器在处理缺失引用的断言时，是否能够输出准确的行号与原因？
- **后续衔接**：通过本阶段项目后，请进入阶段四 [[🧭 阶段4-协作协议与环境]]。
