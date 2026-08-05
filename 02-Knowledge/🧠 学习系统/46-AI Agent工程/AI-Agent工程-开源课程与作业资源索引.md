---
type: index
topic: "AI Agent工程公开课程资源"
tags: [索引, 学习, 46-AI Agent工程, 开源课程]
created: 2026-08-05
status: active
flow: knowledge
kind: moc
source: "各大学与课程项目官方页面"
---

# AI Agent 工程：开源课程与作业资源索引

## 1. 选源原则

1. 优先大学、课程团队或项目组织的官方一手页面。
2. “公开可访问”不自动等于“允许复制/改编”；无明确许可证时只做链接、事实摘要与原创知识映射。
3. 公开作业不复制答案；学校 Honor Code 与课程协作要求继续有效。
4. 依赖账号、API Key、Google Drive、Gradescope 或隐藏测试的内容，明确标记其复现边界。

## 2. 推荐主线

| 优先级 | 资源 | 可用内容 | 作业/实践 | 公开与许可判断 | 本课程用途 |
| :---: | :--- | :--- | :--- | :--- | :--- |
| A | [UC Berkeley CS 194/294-196 Large Language Model Agents, Fall 2024](https://rdi.berkeley.edu/llm-agents/f24) | 课程纲要、部分幻灯片、公开视频、论文阅读：reasoning、ReAct、框架、RAG、代码 Agent、多 Agent、安全 | Lab 01–03 与项目时间线 | 官方公开页面；页面未见课程内容的通用开放许可证，因此只链接和摘要 | 理论与官方 Lab 主线 |
| A | [Berkeley LLM Agents MOOC Lab 01–03 release](https://rdi.berkeley.edu/llm-agents-mooc/assets/instructions.pdf) | 三份 Lab 名称、目标、下载入口、协作与通过门槛 | Lab01 餐厅评论管线；Lab02 攻击；Lab03 防御 | 官方公开说明；starter code 通过 Drive 获取，具体文件许可证需下载后逐项核验 | 作业验收事实来源 |
| A | [UC Berkeley CS 194/294-196 Agentic AI, Fall 2025](https://rdi.berkeley.edu/agentic-ai/f25) | Agent overview、系统设计、后训练、评测、多 Agent、真实部署、安全 | Green Agent / White Agent 项目阶段 | 官方公开课程页；材料未统一声明开放许可证 | 评测与工程扩展 |
| A | [Berkeley Agentic AI MOOC, Fall 2025](https://agenticai-learning.org/f25) | 公开视频、幻灯片、每讲公开测验、补充阅读 | quizzes、Learning & Sharing、AgentX-AgentBeats | 公开访问；复用正文许可未统一声明 | 自测与前沿阅读 |
| A | [Stanford CS224V Conversational Virtual Assistants, Fall 2025](https://web.stanford.edu/class/cs224v/) | 可靠 Agent、知识整理、RAG、任务对话、结构化/非结构化查询、评测 | [HW1 Knowledge Curation](https://web.stanford.edu/class/cs224v/assignments/CS_224V_HW1.pdf)、[HW2 Task-Oriented Agents](https://web.stanford.edu/class/cs224v/assignments/CS_224V_HW2.pdf) | 官方公开 handout；课程要求成组提交且无统一内容许可证，只链接不复制答案 | 深度研究、RAG 与可靠对话扩展 |
| A | [Microsoft AI Agents for Beginners](https://github.com/microsoft/ai-agents-for-beginners) | 18 个当前 Lesson：边界、框架、工具、Agentic RAG、可信、规划、多 Agent、元认知、生产、协议、上下文、记忆、CUA、部署、本地 Agent、加密收据 | 每课 code sample/knowledge check，部分含 smoke test、assignment | 仓库 MIT；本次锁定 commit `15ad10c`（2026-07-29） | 生产能力检查表与国际化工程补充 |
| A | [Datawhale Hello-Agents](https://github.com/datawhalechina/hello-agents) | 16 章中文系统教材：范式、低代码/框架、自研 runtime、记忆、上下文、协议、Agentic RL、评测与三个项目 | 章末习题、配套代码、旅行/Deep Research/赛博小镇/毕业设计 | 仓库 `LICENSE.txt` 为 CC BY-NC-SA 4.0；本次锁定 commit `d4953e8`（2026-08-04） | 中文原理、从零实现与综合项目结构 |
| B | [Hugging Face Agents Course](https://huggingface.co/learn/agents-course/en/unit0/introduction) / [GitHub](https://github.com/huggingface/agents-course) | Agent 循环、tools、smolagents、LlamaIndex、LangGraph、Agentic RAG、可观测性 | Unit quizzes、use case、GAIA 子集最终项目 | 官方仓库明确 Apache-2.0；不是名校课程，作为开放工程教材补充 | 可运行实验与框架对照 |
| B | [Stanford DSPy](https://github.com/stanfordnlp/dspy) | typed signatures、modules、优化器、RAG 与 Agent 程序 | 官方 examples/tests；不是课程作业 | Stanford Future Data Systems 开源工程，仓库 MIT License | 名校开源工程补充；用于比较“声明式 LM 程序”与手写工作流 |
| B | [Stanford CS224N](https://web.stanford.edu/class/cs224n/) | Transformer、预训练、后训练、prompting/PEFT、Agents/Tool Use/RAG、评测 | A3 Self-Attention/Transformer；A4 LLM benchmark/evaluation；GPT-2 项目 | 官方明确欢迎使用公开 slides/assignments 并致谢；仍受 Honor Code 约束 | 补 LLM 前置与评测，不作为 Agent 作业主线 |
| C | [Stanford CS25 Transformers United](https://web.stanford.edu/class/cs25/) | 面向前沿研究的公开讲座与录像 | **无作业、无项目、无考试**，学分只看出勤 | 官方 FAQ 明确任何人可旁听；不能声称其提供 Agent 作业 | 前沿讲座选修，不作为作业来源 |

## 3. 公开但不纳入主线

### CMU 11-667 Large Language Models: Methods and Applications

- 官方课程与六份作业公开：<https://2024.cmu-llms.org/assignments/>
- Assignment 3 是 RAG 与 tool-use，可作为补充练习；其余覆盖数据、Transformer、prompt bias、效率和 mini-project。
- 课程面向已有 ML/NLP 基础的研究生，不适合直接作为本课程小白起点。
- 页面和作业下载文件未发现统一开放许可证；仅建立链接与知识映射，不复制题干或 starter code。

### Stanford CS224G

- [2025 课程页](https://web.stanford.edu/class/cs224g/2025/index.html) 证明其采用两周 sprint 项目制并涵盖 prompt、RAG、embedding、fine-tuning。
- 课程录像不可公开观看，slide 多在 Canvas，具体 sprint 作业也未完整公开；因此只能参考其项目节奏，不能宣称拥有公开作业包。

## 4. 许可证与访问风险表

| 风险 | 识别方式 | 本库处理 |
| :--- | :--- | :--- |
| 无明确许可证 | 页面公开但没有 LICENSE/CC 声明 | 只保存 URL、课程事实和原创摘要 |
| Honor Code | 明示不可查看他人实现/答案 | 不收集答案；映射页只列知识与自测 |
| 隐藏测试 | 官方只公开通过门槛 | 不猜测试输入，不反推判题器 |
| 登录/密钥依赖 | Gradescope、Canvas、API、HF account | 另做本地标准库微型实验，官方环境单独执行 |
| 活课程漂移 | 框架 API、链接与评分会变化 | 每次正式开做前重开官方页核验日期与版本 |

### 逐资源使用账本

| 资源 | 版本 | 明示许可 | 是否改编 | 本库用途 | 访问/Honor 风险 |
| :--- | :--- | :--- | :---: | :--- | :--- |
| UC Berkeley CS 194/294-196 LLM Agents | Fall 2024 | 课程材料未见统一开放许可 | 否 | 理论顺序、Lab 事实与链接 | starter 经 Drive 获取，逐文件核验；不复制答案/隐藏测试 |
| Berkeley LLM Agents MOOC instructions | Fall 2024 | 公开可访问，未见通用改编许可 | 否 | Lab 名称、目标、历史 Gate | 只摘要公开事实，历史 Gate 不冒充当前验收 |
| UC Berkeley Agentic AI | Fall 2025 | 未见统一开放许可 | 否 | 评测、部署、安全扩展 | 活课程漂移，使用前复核 |
| Stanford CS224V | Fall 2025 | handout 公开，许可不统一 | 否 | RAG、任务对话与可靠性扩展 | 只链接，不复制答案 |
| Microsoft AI Agents for Beginners | commit `15ad10c` | MIT | 是，注明来源 | 逐课能力映射、设计检查、生产/本地/部署扩展 | Azure/Foundry 示例可能需账号或密钥；稳定概念与产品 API 分开 |
| Datawhale Hello-Agents | commit `d4953e8` | CC BY-NC-SA 4.0 | 仅在许可范围内；本库主要做原创摘要与能力映射 | 中文原理路线、runtime 分解、上下文/协议/RL/评测和项目结构 | 长代码依赖与框架版本需按章核验；不复制习题答案 |
| Hugging Face Agents Course | 仓库当前版本 | Apache-2.0 | 是，注明来源 | 可运行工程补充与框架比较 | 非名校课程，不冒充主干来源 |
| Stanford DSPy | 仓库当前版本 | MIT License | 是，注明来源 | typed LM program 与 Agent/RAG 工程对照 | 开源软件而非 Stanford 官方课程作业 |
| Microsoft AutoGen 0.2 docs | 0.2 历史文档 | 官方文档，内容许可依站点 | 否，只做 API 导航 | Berkeley F24 版本桥梁 | 与当前稳定 API 不兼容，必须隔离环境 |

## 5. 引用格式

笔记 `source` 应写具体课程与年份；正文公式、结论或作业要求尽可能指向具体页面。若来源只支持“课程有该主题”，不得扩张成“官方给出了某个未公开的实现或答案”。

## 6. 两层来源结论

- **名校公开教学层**：Berkeley/Stanford 页面、handout 与 Lab 事实负责课程顺序和能力目标；因未见统一开放许可，只链接和原创摘要。
- **系统教材层**：Microsoft AI Agents for Beginners（MIT）负责生产能力广度，Hello-Agents（CC BY-NC-SA 4.0）负责中文原理与从零构建深度；逐章去向见 [[AI-Agent工程-双教材章节覆盖矩阵]]。
- **明确开源工程层**：Hugging Face Agents Course（Apache-2.0）、Stanford DSPy（MIT）及 AutoGen 开源软件负责可改编实现与测试。
- 因此本课程不会写成“所有名校作业均开源”。更准确的表述是：**公开名校课程与 Lab 事实 + 两套系统教材能力融合 + 逐项核验许可的原创工程实验层**。
