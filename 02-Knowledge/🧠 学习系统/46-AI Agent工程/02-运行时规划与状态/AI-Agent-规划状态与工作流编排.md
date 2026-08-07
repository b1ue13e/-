---
type: study
topic: "AI Agent规划状态与工作流编排"
course: "AI Agent工程"
tags: [学习, 46-AI Agent工程, AI-Agent, 工作流]
created: 2026-08-05
status: completed
difficulty: intermediate
concept: [任务规划, 状态机, 工作流编排]
prerequisites: [Agent循环, 工具调用]
related: [多智能体, 可观测性, 失败恢复]
stage_moc: "[[🧭 阶段2-运行时规划与状态]]"
upstream: ["[[AI-Agent-框架选型与最小运行时]]"]
flow: knowledge
kind: concept
assessment_exempt: false
source: "UC Berkeley CS 194/294-196 F24 StateFlow and Lab 01; Microsoft AI Agents for Beginners Lesson 7; Datawhale Hello-Agents Chapters 4.3 and 7"
source_urls: ["https://github.com/microsoft/ai-agents-for-beginners/tree/main/07-planning-design", "https://github.com/datawhalechina/hello-agents/tree/main/docs/chapter4", "https://github.com/datawhalechina/hello-agents/tree/main/docs/chapter7"]
accessed: 2026-08-06
license: "Microsoft MIT；Hello-Agents CC BY-NC-SA 4.0；Berkeley许可待核验；本卡为原创整合"
anki_deck: "46-AI Agent工程::04-规划编排"
anki_tags: [46-AI-Agent工程, 规划, 状态机]
---

# AI Agent：规划、状态与工作流编排

## 0. 学习边界

- **类别**：**A 类（核心概念，必须深挖）**
- **判断理由**：长任务最常见的问题不是模型“不会说”，而是漏步骤、状态丢失、重复副作用、错误后无法恢复。显式状态与转移把聊天轨迹变成可测试系统。

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦**：只靠对话历史隐式记住流程时，程序不知道当前完成了什么、下一步允许什么、失败后从哪里恢复。

本卡把任务表示为节点、依赖、状态、转移和不变量，并区分确定性编排与模型动态规划的边界。

## 2. 为什么它重要？它有什么用？

- **连接大图景**：工具是节点能力，Agent 是动态路由器，多智能体是不同执行者，评测基于状态与轨迹。
- **实际应用场景**：评论评分管线、审批、研究报告、代码修复和订单处理。
- **高频题型/任务**：任务分解、DAG 拓扑顺序、状态机转移、重试与补偿、终止条件。

## 3. 学它之前需要哪些前置知识？

1. **[[AI-Agent-边界与感知行动循环]]**：理解状态更新和终止。
2. **[[AI-Agent-工具调用与结构化契约]]**：每个工作节点要有明确输入输出。

## 4. 用直觉语言解释它

> “这东西其实就像机场转机：登机牌、安检和登机有固定先后；航班取消时走改签分支，而不是让旅客每次从记忆猜下一步。”

- **直觉类比**：计划是路线图，状态是“你现在在哪”，转移规则是“满足什么条件才能去下一站”。
- **为什么很自然**：长任务必须把已完成事实从自然语言中抽出来，才能恢复和审计。
- **一句话直觉本质**：把自由生成限制在需要判断的节点，把可确定的顺序交给状态机。

## 5. 正式定义、核心公式、符号解释

### 1. 最核心定义

工作流可表示为有向图 $G=(V,E)$。节点 $v\in V$ 是具有契约的任务，边表示依赖或条件转移；全局状态 $s$ 保存任务数据、节点状态、预算与错误。调度器只运行依赖满足且 guard 为真的节点。

### 2. 核心公式

$$Ready(v,s)=\bigwedge_{u\in pred(v)}Done(u,s)\land Guard_v(s)$$

$$s_{t+1}=\delta(s_t,v_t,result_t),\qquad v_t\in\{v:Ready(v,s_t)\}$$

### 3. 符号说明表

| 符号 | 含义 | 取值范围 / 量纲 | 备注 |
| :--- | :--- | :--- | :--- |
| $V,E$ | 节点与依赖边 | 有限集合 | 无循环时是 DAG |
| $s$ | 工作流状态 | 结构化对象 | 需可序列化 |
| $Guard_v$ | 节点前置条件 | 布尔谓词 | 权限也可作 guard |
| $\delta$ | 状态转移函数 | 旧状态×结果→新状态 | 应保持不变量 |

### 4. 常见变体与适用条件

- **DAG**：批处理依赖明确；**状态机**：有条件分支与循环；**Plan-and-Execute**：计划可动态修订。
- **限制条件**：模型生成的计划只是候选，必须校验依赖、预算、权限和不可逆动作。

## 6. 推导思路和思想来源

- **最初困难**：单个 prompt 同时负责分解、执行、记忆和判断，任何一处失败都难定位。
- **直接方法局限**：完整自由规划会生成不存在的工具或跳过关键步骤。
- **关键“转念”**：先把业务不变量和确定顺序固化，只让模型负责语义抽取、动态分支等不可预写部分。
- **推导主线与动机**：完成定义→节点契约→依赖→状态→转移→错误策略→验收。
- **为什么自然得到此结论**：可恢复系统必须知道已经提交的副作用和尚未完成的节点。

## 7. 例子：基础 → 中等 → 实际应用

### 例子 1：基础例子（可手算）

- **题目**：A 耗时 2，B 耗时 3，C 依赖 A 耗时 4，D 依赖 B/C 耗时 1。无限并行时最短完成时间？
- **解题思路与关键步骤**：A→C 长度 6；B 长度 3；D 要等两支都完成，再加 1。
- **最终答案**：$\max(6,3)+1=7$。
- **易错点**：把全部耗时直接相加成 10。
- **🤔 追问**：若只有一个执行器，顺序如何安排？

### 例子 2：中等例子（条件判断与多步推理）

餐厅管线固定为“查询→抽取→评分→聚合”，适合 DAG；当查询为空时应转入 `insufficient_evidence`，不能继续让评分 Agent 猜数字；抽取格式错可重试一次，聚合写入则需幂等。

### 例子 3：实际应用例子（真实场景/代码）

输入两条评论，按节点依赖执行；输出状态中包含 `score` 和完成轨迹。

```python
from dataclasses import dataclass, field
from typing import Callable

@dataclass
class State:
    data: dict[str, object]
    done: set[str] = field(default_factory=set)
    trace: list[str] = field(default_factory=list)

def extract(state: State) -> None:
    reviews = state.data["reviews"]
    state.data["ratings"] = [int(text.split(":")[-1]) for text in reviews]

def aggregate(state: State) -> None:
    ratings = state.data["ratings"]
    state.data["score"] = sum(ratings) / len(ratings)

NODES: dict[str, tuple[set[str], Callable[..., None]]] = {
    "extract": (set(), extract),
    "aggregate": ({"extract"}, aggregate),
}

def run(state: State) -> State:
    while len(state.done) < len(NODES):
        ready = [name for name, (deps, _) in NODES.items() if name not in state.done and deps <= state.done]
        if not ready:
            raise RuntimeError("workflow has unresolved dependencies")
        for name in ready:
            NODES[name][1](state)
            state.done.add(name)
            state.trace.append(name)
    return state

print(run(State({"reviews": ["food:5", "service:3"]})).data)
```

预期包含：`'score': 4.0`。

## 8. 常见误区和易混概念

### 误区 1：计划写出来就会被正确执行
- **错误直觉**：自然语言 checklist 足够表达状态。
- **为什么错**：它没有机器可判定的完成标记、依赖和不变量。
- **正确理解**：计划用于沟通，状态机用于执行与恢复。

### 误区 2：失败只需无限重试
- **错误直觉**：概率模型多试几次总会成功。
- **为什么错**：确定性错误不会消失，写操作还会重复副作用。
- **正确理解**：按错误分类决定重试、降级、补偿或人工介入。

### 概念对比表

| 概念 | 核心问题 | 关键区别 | 典型使用场景 |
| :--- | :--- | :--- | :--- |
| DAG | 哪些节点可并行？ | 依赖无环 | 数据管线 |
| 状态机 | 当前状态允许什么转移？ | 条件与循环显式 | 对话、审批 |
| 自由规划 | 模型建议哪些步骤？ | 适应性高、需校验 | 开放研究 |
| Checklist | 人要记住什么？ | 不直接执行 | 手工验收 |

## 9. 来源定位与关系

- 有向无环图与拓扑排序是工作流的语义补救主题；若不熟悉，先用本卡的最小例子完成闭卷复现，不伪造计划性链接。
- 直接知识依赖以 frontmatter `upstream` 为唯一事实源；直接后续由本文末 Dataview 反向派生。

## 10. 闭卷复现任务

- [ ] 1. 写出 Ready 公式。
- [ ] 2. 区分 DAG 与状态机。
- [ ] 3. 为四节点任务画依赖图。
- [ ] 4. 定义一个全局状态对象。
- [ ] 5. 写出空数据分支。
- [ ] 6. 区分瞬时错误与确定性错误。
- [ ] 7. 手算关键路径。
- [ ] 8. 说明写节点为何需要幂等。
- [ ] 9. 为动态计划写三条校验。
- [ ] 10. 说出恢复点需保存的字段。

## 11. 自测题：5 道

### 1. #自测题/基础
**题目**：节点何时 Ready？
> [!question]- 答案解析
> - **答案**：所有前驱完成且节点 guard 为真。
> - **解析**：仅“排在列表前面”不等于依赖满足。

### 2. #自测题/基础
**题目**：为什么状态应结构化且可序列化？
> [!question]- 答案解析
> - **答案**：便于持久化、恢复、测试、迁移和审计。
> - **解析**：只藏在对话文本里无法可靠判断节点完成。

### 3. #自测题/中等
**题目**：解析节点因 JSON 缺字段失败，应重试还是继续聚合？
> [!question]- 答案解析
> - **答案**：不应继续；可带明确格式反馈有限重试，仍失败则降级或终止。
> - **解析**：聚合依赖合法评分，跳过会破坏不变量。

### 4. #自测题/中等
**题目**：计划中出现未注册工具如何处理？
> [!question]- 答案解析
> - **答案**：计划校验失败，要求重新规划或人工选择，不能动态执行未知能力。
> - **解析**：计划不是授权。

### 5. #自测题/较难
**题目**：如何恢复“已扣款但确认消息发送失败”的流程？
> [!question]- 答案解析
> - **答案**：持久化扣款交易 ID 和节点完成状态；仅重试幂等的消息节点，不重复扣款；必要时走退款补偿并审计。
> - **解析**：恢复以已提交副作用为事实边界。

## 12. 我的主动回忆区

### 我的闭卷复述
> 解释为什么“确定流程 + 局部 Agent”常优于全自由 Agent：

### 我的推导复现
> 为 Lab01 画状态和错误分支：

### 我的错误与卡点
- 

### 下次复习日期
- [ ] 明天
- [ ] 3 天后
- [ ] 7 天后
- [ ] 14 天后

## 13. 给 Obsidian 的归档建议

- **适合文件夹**：`02-Knowledge/🧠 学习系统/46-AI Agent工程/`
- **关联已有笔记**：[[AI-Agent-工具调用与结构化契约]]、[[AI-Agent-多智能体协作与消息协议]]
- **建议标签**：`#学习` `#工作流` `#状态机`
- **拆分建议**：补偿事务形成多案例后拆为独立实践卡。

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

- 工作流节点 Ready 的条件是什么？::所有前驱节点完成，并且该节点的 guard 条件为真。
- 为什么模型生成的计划不能直接执行？::计划可能包含未知工具、非法依赖、越权动作或超预算步骤，必须经过结构、权限和可行性校验。
- 工作流恢复的事实边界是什么？::已持久化且确认提交的副作用与节点状态；恢复时不能仅凭模型记忆猜测是否执行过。

