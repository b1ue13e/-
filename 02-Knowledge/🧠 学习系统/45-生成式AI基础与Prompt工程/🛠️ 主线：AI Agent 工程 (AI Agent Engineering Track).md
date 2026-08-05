---
title: "主线-AI Agent工程"
type: moc
kind: moc
flow: knowledge
track: "AI Agent工程"
status: active
created: 2026-07-30
updated: 2026-07-30
tags:
  - MOC
  - 主线
  - AIAgent
  - 智能体
  - 架构设计
  - 知识网络
---

# 🛠️ 主线：AI Agent 工程 (AI Agent Engineering Track)

> 🧭 **主线宗旨**：收拢 Datawhale Hello-Agents、微软 18 课、Hugging Face Agents、LangGraph、MCP 协议、OpenAI SDK、GenAI 基础等 8 大 AI Agent 开源课程。严格遵循 `AGENTS.md` **全库唯一主卡** 规则，消除概念重复，构建从 Prompt/RAG 到手撕 Agent、状态机工作流、MCP 服务编排与企业级 Guardrails 的高能工程主线。
>
> 🗺️ **融合主视图**：详见全库 8 大开源课程无冗余融合主路线图 —— [[🗺️ AI Agent终极融合修炼路线]]。

---

## 🗺️ 8 门 AI Agent 子线路径 5 层递进图

```mermaid
flowchart TD
    L0["Layer 0: 前置基石 (Foundations)<br/>[[🗺️ 生成式AI基础与Prompt工程学习路径\|45-生成式AI基础与Prompt工程]]<br/>(LLM, Token, Embedding, Vector Search, Basic RAG)"]
    L0 --> L1["Layer 1: 原理与零依赖手撕主线 (Core Implementation)<br/>[[🗺️ HelloAgents从零构建智能体学习路径\|39-HelloAgents]] & [[🗺️ AI Agent设计与工程实践学习路径\|38-AI Agent设计与工程]]<br/>(纯 Python 手撕 Agent, GRPO, Deep Research, 理论全景)"]
    L1 --> L2["Layer 2: 复杂工作流与生态框架 (Workflows & Ecosystem)<br/>[[🗺️ LangGraph复杂工作流与状态机学习路径\|42-LangGraph]] & [[🗺️ HuggingFace-Agents开源框架与实战学习路径\|41-HuggingFace]]<br/>(StateGraph 状态机, HITL, smolagents, FC SFT 微调)"]
    L2 --> L3["Layer 3: 专项协议与现代 SDK 范式 (Protocols & SDKs)<br/>[[🗺️ MCP协议与智能体服务编排学习路径\|43-MCP协议]] & [[🗺️ OpenAI-Agents-SDK架构与设计模式学习路径\|44-OpenAI SDK]]<br/>(Model Context Protocol JSON-RPC, Agent-as-Tool 嵌套)"]
    L3 --> L4["Layer 4: 企业工程、安全与全景评测 (Enterprise & Security)<br/>[[🗺️ 微软AI-Agents入门与工程实践学习路径\|40-微软AI-Agents]] & [[项目-AI Agent核心组件与多智能体系统搭建]]<br/>(Guardrails 攻击拦截, Router/Orchestrator, SWE-bench 评测)"]
```

---

## 🔑 全库唯一 Master 概念卡 (Single Source of Truth)

所有 8 门 Agent 课程的核心理论统一收拢至以下 6 张 Master 概念卡：

1. **ReAct 与 Agent 核心**：[[ReAct范式与Agent核心公式]] ($\text{Agent} = \text{LLM} + \text{Context} + \text{Tools}$)
2. **上下文与记忆系统**：[[Agent记忆系统与向量检索]] (Working vs Episodic Memory, Cosine + Decay)
3. **工具调用与安全沙箱**：[[ToolUse与FunctionCalling]] (JSON Schema, Code-as-Action, AST Sandbox)
4. **高级规划与 Coding Agent**：[[CodingAgent原理与实践]] (Tree of Thoughts, Reflexion, SWE-bench)
5. **多模态与多智能体**：[[MultiAgent多智能体协作机制]] (SOP Protocol, MetaGPT/AutoGen Topologies, GUI ReAct)
6. **评测对齐与自进化**：[[Agent评测对齐与自进化]] (Agent SFT/DPO Loss, Dynamic Tool Evolution)

---

## 📊 包含子路径看板 (Dataview)

```dataview
TABLE course AS "课程名称", status AS "状态", importance AS "优先级", updated AS "最近更新"
FROM "02-Knowledge/🧠 学习系统"
WHERE type = "index" AND track = "AI Agent工程"
SORT file.name ASC
```

---

*主线更新时间：2026-07-30 | 状态：active*
