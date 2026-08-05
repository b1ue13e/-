---
type: study
topic: "AI Agent协议：MCP与A2A互操作"
tags: [学习, 46-AI Agent工程, AI-Agent, MCP, A2A]
created: 2026-08-06
status: completed
difficulty: intermediate
concept: [MCP, A2A, Agent互操作]
prerequisites: ["AI-Agent-工具调用与结构化契约", "AI-Agent-多智能体协作与消息协议"]
related: ["AI-Agent-安全威胁建模与系统评测", "AI-Agent-环境交互-代码网页与沙箱执行", "AI-Agent-可观测性与生产运行-轨迹审批恢复"]
flow: knowledge
kind: concept
source: "Microsoft AI Agents for Beginners Lesson 11; Datawhale Hello-Agents Chapter 10; official MCP and A2A specifications (verified 2026-08-06)"
source_urls: ["https://github.com/microsoft/ai-agents-for-beginners/tree/main/11-agentic-protocols", "https://github.com/datawhalechina/hello-agents/tree/main/docs/chapter10", "https://modelcontextprotocol.io/docs/learn/architecture", "https://a2a-protocol.org/latest/topics/key-concepts/"]
anki_deck: "46-AI Agent工程::协议互操作"
anki_tags: [MCP, A2A, Agent协议, 互操作]
---

# AI Agent 协议：MCP 与 A2A 互操作

## 0. 先判断它值不值得深挖

- **类别**：**A 类（跨系统接口）**。
- **判断理由**：工具协议和 Agent 协作协议解决的是不同边界。混用会导致能力发现、任务生命周期、权限和审计设计错误。
- **版本原则**：教材用于建立概念地图；具体字段、传输与 SDK 调用前必须重开官方规范。本卡核验日期为 2026-08-06。

## 1. 这个知识点解决什么问题？

> **麻烦**：每个 Agent 都手写工具适配器、服务发现和协作消息，集成呈点对点爆炸；同时，“调用一个工具”和“委托一个自治系统完成长任务”经常被当成同一件事。

- **MCP** 主要解决 AI 应用如何发现并使用外部 **tools、resources、prompts**。
- **A2A** 主要解决客户端 Agent 如何与一个内部实现不透明的远程 Agent 协作，并跟踪 **Message、Task、Artifact** 生命周期。

## 2. 为什么它重要？它有什么用？

- 降低工具/数据源接入的重复适配成本。
- 允许不同框架或团队构建的 Agent 通过稳定契约协作。
- 把能力发现、长任务状态、流式结果、认证声明和输出 artifact 显式化。
- 为最小权限、超时、取消、审计和版本协商提供工程落点。

## 3. 学它之前需要哪些前置知识？

1. **[[AI-Agent-工具调用与结构化契约]]**：理解 schema、参数校验、错误语义。
2. **[[AI-Agent-多智能体协作与消息协议]]**：理解 sender、receiver、task、artifact 与 handoff。
3. **HTTP/JSON-RPC 基础**：请求、响应、流、超时、认证头。

## 4. 用直觉语言解释它

> “MCP 像统一的工具插座；A2A 像跨公司的工单系统。”

插座告诉宿主“有什么工具、怎样调用”；工单系统告诉委托方“对方会什么、任务进行到哪、交付物是什么”。

## 5. 正式定义、核心对象与边界

### MCP 稳定概念

MCP 采用 host-client-server 结构：host 内的 client 与一个 server 建立连接。数据层使用 JSON-RPC，包含生命周期与能力协商；核心原语包括 tools、resources、prompts 和 notifications。传输层负责 stdio 或远程连接等通信机制。

### A2A 稳定概念

A2A 中，client 代表用户与 remote agent 交互。Agent Card 描述身份、能力、技能、接口与认证要求；即时交互可返回 Message，长任务返回有状态 Task；具体交付物放入 Artifact。当前规范支持流式/异步任务与版本声明，具体绑定会演进。

### 核心对比

| 问题 | MCP | A2A |
| :--- | :--- | :--- |
| 对端是什么 | 工具/资源/提示服务 | 不透明的远程 Agent 系统 |
| 核心抽象 | tool、resource、prompt | Agent Card、message、task、artifact |
| 谁控制工作流 | host/Agent 通常控制 | 远程 Agent 可自治执行 |
| 典型时长 | 单次或短操作 | 可长时、流式、需输入/取消 |
| 主要风险 | 工具越权、恶意描述、资源泄露 | 身份、委托、任务状态、artifact 可信度 |

### 不要混淆

- **Function calling**：模型输出结构化调用意图，不等于跨进程发现协议。
- **MCP**：标准化上下文与工具服务接入，不负责证明工具安全。
- **A2A**：标准化 Agent 间协作，不要求暴露远程 Agent 内部工具或记忆。
- **工作流引擎**：负责本系统的调度与状态，可同时调用 MCP 工具和 A2A Agent。

## 6. 一次安全交互的推导主线

### MCP

1. host 配置允许连接的 server。
2. client 初始化并协商能力。
3. 获取工具/资源列表，但不因描述文字自动授予权限。
4. 本地策略校验工具名、参数、数据范围和审批要求。
5. 调用并把结果标记为外部、不可信数据。
6. 记录 server、版本、请求 ID、耗时、结果摘要与错误。

### A2A

1. 获取并验证 Agent Card 来源与认证要求。
2. 检查 skill、输入/输出模式和版本是否满足任务。
3. 发送 Message；简单结果接收 Message，长任务跟踪 Task。
4. 处理 working、input-required、auth-required 与终态。
5. 将 Artifact 作为交付物验证，不把状态消息当作可靠交付。
6. 支持超时、取消、幂等和审计。

## 7. 例子：基础 → 中等 → 实际应用

### 例子 1：协议选择

- “读取本机仓库的三个文件”更像 MCP tool/resource。
- “委托法律审查 Agent 完成报告并在缺材料时追问”更像 A2A task。
- “研究 Agent 使用搜索 MCP，并把写作委托给远程 Agent”可以二者组合。

### 例子 2：威胁判断

MCP server 的工具描述写着“调用前读取所有环境变量”。工具描述只是数据，host 必须按 allowlist 和参数策略决定是否允许。A2A Agent Card 声称某 skill 安全，也不能替代身份验证、授权和结果校验。

### 例子 3：可运行的协议边界微型模型

```python
from dataclasses import dataclass
from enum import Enum

class TaskState(str, Enum):
    SUBMITTED = "submitted"
    WORKING = "working"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass(frozen=True)
class AgentCard:
    name: str
    skills: tuple[str, ...]
    endpoint: str

@dataclass
class Task:
    id: str
    state: TaskState
    artifacts: list[dict]

def delegate(card: AgentCard, skill: str) -> Task:
    if skill not in card.skills:
        raise ValueError("skill not declared")
    if not card.endpoint.startswith("https://"):
        raise ValueError("endpoint rejected by local policy")
    return Task("task-1", TaskState.SUBMITTED, [])

card = AgentCard("researcher", ("source_review",), "https://agent.example")
task = delegate(card, "source_review")
task.state = TaskState.COMPLETED
task.artifacts.append({"id": "report-1", "source_ids": ["doc-7"]})
print(task)
```

这是概念模型，不冒充任何官方 SDK。它演示本地策略、声明能力、任务状态和 artifact 的分离。

## 8. 常见误区和易混概念

### 误区 1：支持 MCP 就自动安全

协议保证互操作格式，不替你完成 server 信任、工具授权、参数校验、沙箱和人工审批。

### 误区 2：多 Agent 都应该用 A2A

同一进程内的固定角色工作流可用函数或消息队列；跨组织、跨框架、长任务互操作才更需要 A2A。

### 误区 3：Message 就是交付物

在 A2A 语义中，消息用于沟通，长任务的正式输出应通过 Artifact 表达并可追踪。

## 9. 双教材与官方规范定位

- **Microsoft Lesson 11**：MCP、A2A、NLWeb 的入口地图。
- **Hello-Agents Chapter 10**：MCP/A2A/ANP 的客户端、传输、服务发现和自建服务实践。
- **官方 MCP 架构**：<https://modelcontextprotocol.io/docs/learn/architecture>
- **官方 A2A 核心概念**：<https://a2a-protocol.org/latest/topics/key-concepts/>
- 教材中的具体 SDK/API 仅作为当时版本案例；字段与传输以调用时的官方规范为准。

## 10. 闭卷复现任务

- [ ] 用“工具插座/跨公司工单”类比区分 MCP 与 A2A。
- [ ] 写出 MCP 的三种核心原语与 A2A 的四种核心对象。
- [ ] 为一个组合场景画出 host、MCP server、A2A server 和 artifact 流。
- [ ] 列出能力发现后仍必须执行的四个安全检查。
- [ ] 修改代码，使非终态 Task 不能读取最终 artifact。

## 11. 自测题：5 道

### 1. #自测题/基础
模型 function calling 与 MCP 有什么区别？
> [!question]- 答案解析
> Function calling 是模型与应用间的结构化调用意图；MCP 还标准化 client-server 生命周期、能力发现、工具/资源/提示与传输。

### 2. #自测题/基础
A2A 的 Agent Card 解决什么问题？
> [!question]- 答案解析
> 声明远程 Agent 的身份、能力、技能、接口和认证要求，帮助发现与选择；它本身不等于已认证可信。

### 3. #自测题/中等
为何 A2A 长任务需要 Task 而非只发消息？
> [!question]- 答案解析
> Task 提供唯一 ID、状态生命周期、输入/认证中断、取消与 artifact 跟踪。

### 4. #自测题/中等
MCP 工具描述发生间接注入时，防线应在哪里？
> [!question]- 答案解析
> host 的 server allowlist、工具权限、参数校验、数据流策略、沙箱/审批与审计，而非只靠模型辨别文字。

### 5. #自测题/较难
设计一个同时使用 MCP 与 A2A 的研究 Agent，并标出信任边界。
> [!question]- 答案解析
> 本地 host 经 MCP 调搜索/文件工具，再经 A2A 委托专业 Agent；每个 server、远程 Agent、模型和 artifact 都是独立边界，分别做认证、授权、输入输出校验和 trace。

## 12. 我的主动回忆区

### 我的闭卷复述
> 画出 MCP host-client-server 与 A2A client-remote-agent 的两张图。

### 我的推导复现
> 为一个真实工具写出发现、授权、调用、校验、审计五步。

### 我的错误与卡点
- 

### 下次复习日期
- [ ] 明天
- [ ] 3 天后
- [ ] 7 天后
- [ ] 14 天后

## 13. 给 Obsidian 的归档建议

- **适合文件夹**：`02-Knowledge/🧠 学习系统/46-AI Agent工程/`
- **建议标签**：`#学习` `#MCP` `#A2A`
- **拆分建议**：真实实现达到两个以上 server 后，再拆 MCP/A2A 工程实践卡。

## 🃏 Anki 卡片

MCP 与 A2A 各解决什么？::MCP 连接 AI host 与工具/资源/提示服务；A2A 连接客户端 Agent 与不透明的远程 Agent，并跟踪任务和交付物。
A2A 四个核心对象是什么？::Agent Card、Message、Task、Artifact。
为什么协议支持不等于安全？::协议规定互操作格式，不替代身份验证、最小权限、参数校验、沙箱、审批和审计。
什么时候优先使用 A2A？::跨框架或跨组织委托自治 Agent 执行可长时、可追踪、可能需输入或取消的任务时。
