---
type: study
topic: "AI Agent框架选型与最小运行时"
tags: [学习, 46-AI Agent工程, AI-Agent, 框架选型]
created: 2026-08-06
status: completed
difficulty: intermediate
concept: [Agent框架, Agent运行时, 框架选型]
prerequisites: ["AI-Agent-前置-消息JSON异常与单元测试", "AI-Agent-边界与感知行动循环", "AI-Agent-工具调用与结构化契约"]
related: ["AI-Agent-规划状态与工作流编排", "AI-Agent-框架-AutoGen官方Lab版本补丁", "AI-Agent-可观测性与生产运行-轨迹审批恢复"]
flow: knowledge
kind: concept
source: "Microsoft AI Agents for Beginners Lessons 2 and 14; Datawhale Hello-Agents Chapters 5-7 (repositories verified 2026-08-06)"
source_urls: ["https://github.com/microsoft/ai-agents-for-beginners/tree/main/02-explore-agentic-frameworks", "https://github.com/microsoft/ai-agents-for-beginners/tree/main/14-microsoft-agent-framework", "https://github.com/datawhalechina/hello-agents/tree/main/docs/chapter5", "https://github.com/datawhalechina/hello-agents/tree/main/docs/chapter6", "https://github.com/datawhalechina/hello-agents/tree/main/docs/chapter7"]
anki_deck: "46-AI Agent工程::框架与运行时"
anki_tags: [Agent框架, 运行时, 选型, 版本治理]
---

# AI Agent 框架选型与最小运行时

## 0. 先判断它值不值得深挖

- **类别**：**A 类（工程底座）**。
- **判断理由**：只会调用某个框架 API，会在版本漂移、故障定位和迁移时失去判断。先理解最小运行时，再按需求选择框架。

## 1. 这个知识点解决什么问题？

> **麻烦**：教程 Demo 经常把模型客户端、工具执行、状态、终止、记忆、追踪和部署封装在几行 API 后。小白能复制运行，却不知道失败发生在哪层，也无法判断是否需要框架。

本卡建立两种能力：

1. 能从零画出最小 Agent runtime 的控制流。
2. 能根据状态复杂度、可靠性、部署和团队约束选择，而不是按热度选框架。

## 2. 为什么它重要？它有什么用？

- 框架升级时能识别是 API 变了还是概念变了。
- 能为测试替换模型和工具，不把外部波动混入业务逻辑。
- 能判断低代码、代码框架、自研运行时和托管服务的边界。
- 能避免一开始就引入多 Agent、向量库和云服务。

## 3. 学它之前需要哪些前置知识？

1. Python 函数、类型、异常与单元测试。
2. [[AI-Agent-边界与感知行动循环]]。
3. [[AI-Agent-工具调用与结构化契约]]。

## 4. 用直觉语言解释它

> “框架是预制厨房，运行时是做菜流程。你可以租一间设备齐全的厨房，但仍要知道食材从哪里来、谁点火、何时关火、出错怎样清理。”

## 5. 最小运行时的七个部件

1. **Model adapter**：统一消息、结构化输出、超时和模型版本。
2. **Tool registry**：工具发现、schema、授权、执行与错误分类。
3. **State store**：当前步骤、artifact ID、预算和持久化状态。
4. **Orchestrator**：选择下一状态或 handoff。
5. **Termination policy**：成功、失败、轮数、成本、无进展和人工升级。
6. **Observability**：trace、span、请求 ID、成本与去敏记录。
7. **Evaluation hooks**：离线测试、回放、逐样本结果与上线 gate。

最小控制流：

```text
request -> validate -> model decision -> authorize tool -> execute
        -> record observation -> update state -> stop or continue
```

## 6. 框架选型决策

| 选择 | 适合 | 不适合 |
| :--- | :--- | :--- |
| 纯函数/自研最小 runtime | 教学、固定流程、强测试、少依赖 | 大量现成集成、复杂分布式部署 |
| 低代码平台 | 快速验证、业务人员参与、流程可视化 | 深度测试、细粒度版本控制、特殊运行时 |
| 代码 Agent 框架 | 状态图、多 Agent、记忆、追踪集成 | 一个 API 调用即可完成的任务 |
| 托管 Agent 服务 | 托管身份、部署、伸缩和运维 | 严格离线、本地隐私、供应商锁定敏感场景 |

### 选型评分表

先写需求，再比较候选：

- 状态是否跨步骤/跨会话持久化？
- 是否需要人工审批、暂停和恢复？
- 工具是否有副作用与细粒度权限？
- 是否需要多 Agent 或跨系统协议？
- 能否离线测试、回放轨迹、锁定版本？
- 部署位置、延迟、成本、隐私和团队语言是什么？

若前四项大多为“否”，通常先不用重框架。

## 7. 例子：基础 → 中等 → 实际应用

### 例子 1：是否需要框架

“把一段文本分类并返回 JSON”是单次受约束调用，不需要 Agent 框架。“检索多个来源、遇到冲突追问、调用工具、暂停审批并恢复”才需要显式 runtime 或框架。

### 例子 2：框架迁移

将 `ModelAdapter`、`ToolRegistry`、`State` 和 `TraceSink` 定义为本地接口。迁移 AutoGen/LangGraph/MAF 时只换适配层；业务测试继续使用 fake model/tool。

### 例子 3：可运行 Python 最小循环

```python
from dataclasses import dataclass, field
from typing import Callable

Tool = Callable[[dict], dict]

@dataclass
class State:
    step: int = 0
    done: bool = False
    trace: list[dict] = field(default_factory=list)

class Runtime:
    def __init__(self, tools: dict[str, Tool], max_steps: int = 3):
        self.tools = tools
        self.max_steps = max_steps

    def run(self, decision: dict) -> State:
        state = State()
        while not state.done and state.step < self.max_steps:
            name, args = decision["tool"], decision.get("args", {})
            if name not in self.tools:
                raise ValueError("unknown tool")
            result = self.tools[name](args)
            state.trace.append({"step": state.step, "tool": name, "result": result})
            state.step += 1
            state.done = bool(result.get("done"))
        if not state.done:
            raise RuntimeError("termination budget exhausted")
        return state

runtime = Runtime({"finish": lambda args: {"done": True, "answer": args["answer"]}})
print(runtime.run({"tool": "finish", "args": {"answer": 42}}).trace)
```

该例故意不调用真实模型：先验证控制流、未知工具和终止预算，再接模型适配器。

## 8. 常见误区和易混概念

### 误区 1：框架功能越多越适合

功能带来依赖、默认行为和升级面。需求未出现的能力不是收益。

### 误区 2：框架自带 trace 就等于可观测

还需业务阶段、输入输出摘要、错误分类、关联 ID、成本和隐私去敏。

### 误区 3：低代码适合小白，所以可跳过概念

低代码降低语法门槛，不消除状态、权限、终止、评测和成本问题。

| 概念 | 关注点 | 例子 |
| :--- | :--- | :--- |
| SDK | 调用某产品/API | 模型客户端 |
| Framework | 组织 Agent 组件与模式 | 状态图、多 Agent 抽象 |
| Runtime | 实际执行、状态与生命周期 | 调度、暂停、恢复、trace |
| Managed service | 托管部署与运营能力 | 身份、伸缩、监控 |

## 9. 双教材定位与 Obsidian 双链

- **Microsoft Lessons 2/14**：框架与托管服务的职责，以及 Microsoft Agent Framework 具体能力。
- **Hello-Agents Chapters 5-7**：低代码、AutoGen/AgentScope/LangGraph 对比与从零构建 HelloAgents。
- [[AI-Agent-框架-AutoGen官方Lab版本补丁]] 是一个特定历史版本的桥梁，不是通用框架主卡。
- 本库可运行参考：`03-Projects/46-AI Agent工程/local-acceptance/agent_runtime.py`。

## 10. 闭卷复现任务

- [ ] 默写最小 runtime 七部件。
- [ ] 给一个单次分类任务说明为何不需要 Agent。
- [ ] 用选型问题比较自研最小 runtime 与任一框架。
- [ ] 修改代码，加入超时错误或审批状态。
- [ ] 写一个 fake tool 测试未知工具与最大步数。

## 11. 自测题：5 道

### 1. #自测题/基础
SDK、framework、runtime 的最小区别是什么？
> [!question]- 答案解析
> SDK 提供 API 调用；framework 提供组织模式；runtime 负责真实执行、状态和生命周期。

### 2. #自测题/基础
为什么先用 fake model/tool？
> [!question]- 答案解析
> 隔离外部随机性、网络和费用，先验证控制流、契约、错误与终止。

### 3. #自测题/中等
何时状态图比自由循环更合适？
> [!question]- 答案解析
> 阶段、分支、失败、审批、恢复和终止可枚举且需审计时。

### 4. #自测题/中等
选型时为什么把暂停/恢复单独提问？
> [!question]- 答案解析
> 它要求持久状态、幂等、副作用治理和生命周期支持，显著影响 runtime 与托管方案。

### 5. #自测题/较难
设计一个避免框架锁定的边界。
> [!question]- 答案解析
> 本地定义模型、工具、状态、trace 和评测接口；框架对象仅存在于 adapter，业务状态与测试不依赖其私有类型。

## 12. 我的主动回忆区

### 我的闭卷复述
> 不看上文画出 request 到 termination 的控制流。

### 我的推导复现
> 为当前项目填写六个选型问题，写出“不选”的候选及理由。

### 我的错误与卡点
- 

### 下次复习日期
- [ ] 明天
- [ ] 3 天后
- [ ] 7 天后
- [ ] 14 天后

## 13. 给 Obsidian 的归档建议

- **适合文件夹**：`02-Knowledge/🧠 学习系统/46-AI Agent工程/`
- **建议标签**：`#学习` `#Agent框架` `#运行时`
- **拆分建议**：具体框架 API 独立做版本补丁卡，不污染稳定概念卡。

## 🃏 Anki 卡片

最小 Agent runtime 七部件是什么？::模型适配、工具注册、状态存储、编排、终止策略、可观测性、评测钩子。
何时通常不需要重 Agent 框架？::任务单步、无持久状态、无副作用工具、无审批恢复或多 Agent 需求时。
如何降低框架锁定？::用本地稳定接口隔离模型、工具、状态、trace 与评测，把框架类型限制在 adapter。
为什么低代码不能替代 Agent 工程知识？::它降低实现语法门槛，但状态、权限、终止、评测、成本与失败语义仍然存在。
