---
type: study
topic: "消息、JSON、异常与单元测试"
course: "AI Agent工程"
tags: [学习, 46-AI Agent工程, Python, 测试]
created: 2026-08-05
status: completed
mastery: not_started
difficulty: beginner
concept: ["消息协议", "异常处理", "测试替身"]
prerequisites: ["Python函数与字典"]
related: ["AI-Agent-工具调用与结构化契约", "AI-Agent-多智能体协作与消息协议"]
stage_moc: "[[🧭 AI-Agent工程-前置知识]]"
flow: knowledge
kind: concept
assessment_exempt: false
source: "UC Berkeley CS 194/294-196 Fall 2024 Lab 01 public instructions; Python standard library documentation"
source_urls: ["https://rdi.berkeley.edu/llm-agents-mooc/assets/instructions.pdf", "https://docs.python.org/3/library/unittest.html", "https://docs.python.org/3/library/json.html"]
accessed: 2026-08-06
license: "Berkeley材料许可待逐文件核验；Python文档按PSF许可；本卡仅作原创摘要与示例"
anki_deck: "46-AI Agent工程::课程前置"
anki_tags: [消息, JSON, 异常, 测试]
---

# AI Agent 前置：消息、JSON、异常与单元测试

## 0. 学习边界

- **类别**：A 类。Lab 01 的 Agent、工具和编排都依赖它。
- **判断理由**：不会先验证普通 Python 函数，就会把解析错误、网络错误和框架错误全部误判为 Prompt 问题。

## 1. 这个知识点解决什么问题？

> Agent 收到缺字段消息后继续执行，直到很晚才失败；真实 API 波动又让测试无法定位。

## 2. 为什么它重要？它有什么用？

- 用 schema 区分 `user`、`assistant`、`tool` 消息。
- 用明确异常阻断越权或非法数据。
- 用 fake model/tool 在无网络、无密钥时测试核心流程。

## 3. 学它之前需要哪些前置知识？

1. Python 函数、字典、列表与 `try/except`。
2. 若不会 JSON 与断言，先读 [[课程前置-Python-JSON测试与实验复现|Python、JSON 与实验复现]]。

## 4. 用直觉语言解释它

> “消息是快递单，schema 是必填栏，异常是拒收原因，测试替身是假包裹演练。”

## 5. 正式定义、核心公式、符号解释

消息最小结构为 $m=(role,content,tool\_call\_id,metadata)$。协议校验函数 $V(m)$ 只返回有效消息，非法输入必须失败关闭。

| 字段 | 含义 | 必需性 | 约束 |
| :--- | :--- | :---: | :--- |
| `role` | 消息职责 | 是 | 白名单枚举 |
| `content` | 文本或结构数据 | 是 | 长度与类型限制 |
| `tool_call_id` | 调用关联键 | 工具结果必需 | 必须匹配待处理调用 |

## 6. 推导思路和思想来源

- 自然语言消息自由度高，执行系统需要收窄成契约。
- 外部依赖不可控，应依赖接口而非具体服务。
- 测试先覆盖解析与状态转移，再做真实模型集成。

## 7. 例子：基础 → 中等 → 实际应用

### 例子 1：基础例子（可手算）

消息 `{role: tool, content: 3}` 缺少调用 ID，应在边界拒绝，而不是猜它属于哪个调用。

### 例子 2：中等例子

工具超时、工具返回空列表、工具返回恶意文本是三种不同观察；状态机应分别重试、结束无证据、隔离为数据。

### 例子 3：实际应用例子（可运行 Python）

```python
# 输入：用户问题与可替换模型；输出：经协议校验的消息。
from dataclasses import dataclass
from typing import Protocol

class Model(Protocol):
    def reply(self, message: str) -> str: ...

@dataclass(frozen=True)
class FakeModel:
    answer: str
    def reply(self, message: str) -> str:
        return self.answer

def ask(model: Model, question: str) -> dict[str, str]:
    if not question.strip():
        raise ValueError("question 不能为空")
    answer = model.reply(question)
    if not answer.strip():
        raise RuntimeError("模型返回空内容")
    return {"role": "assistant", "content": answer}

assert ask(FakeModel("42"), "6*7?")["content"] == "42"
```

## 8. 常见误区和易混概念

- Fake 不是伪造真实效果，而是控制依赖以测试确定性逻辑。
- `except Exception: pass` 会吞掉故障证据，不是健壮性。

| 概念 | 核心问题 | 区别 | 场景 |
| :--- | :--- | :--- | :--- |
| Fake | 轻量可用实现 | 有简化行为 | 离线模型 |
| Stub | 固定返回 | 不验证交互 | 指定边界分支 |
| Mock | 是否按预期调用 | 强调交互断言 | 工具权限测试 |

## 9. 来源定位与关系

- 消息、异常和测试替身贯穿所有后续实现；直接后续与可完成作业由本文末 Dataview 根据权威字段派生。

## 10. 闭卷复现任务

- [ ] 写出消息最小 schema。
- [ ] 区分 ValueError、RuntimeError 与超时。
- [ ] 用 fake 替代一次模型调用。
- [ ] 为缺字段、空问题、空返回写测试。
- [ ] 解释为何工具输出按不可信数据处理。
- [ ] 区分 Fake、Stub 与 Mock。
- [ ] 为 tool_call_id 不匹配写失败条件。
- [ ] 说明为何不能吞掉所有异常。
- [ ] 设计一个超时测试替身。
- [ ] 说出一个消息协议的真实应用。

## 11. 自测题：5 道

1. `tool` 消息为何需要关联 ID？ `#自测题/基础`
2. 空用户问题应返回什么？ `#自测题/基础`
3. Fake 与 Mock 的主要差别是什么？ `#自测题/中等`
4. 设计超时后的有限重试状态。 `#自测题/中等`
5. 设计一个证明“恶意工具文本不会变系统指令”的测试。 `#自测题/较难`

> [!question]- 参考答案与评分点
> 1. 将结果绑定到唯一调用，避免串线。2. 在边界明确失败，不调用模型。3. Fake 提供简化实现，Mock 验证交互。4. 含最大次数、退避和终止状态。5. 需断言文本只进入数据字段且不改变权限/工具白名单。

## 12. 我的主动回忆区

- **闭卷 schema**：
- **失败分支测试**：
- **仍混淆的异常**：
- [ ] 明天  [ ] 3 天后  [ ] 7 天后  [ ] 14 天后

## 13. 给 Obsidian 的归档建议

- 本卡与 45 的 Python 前置互补；通过标准是 5 道自测 ≥4 且代码断言通过。
- 所有 Agent 项目先保留 fake 测试，再增加真实模型测试。

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

Q: 为什么 Agent 应使用模型测试替身？
A: 隔离网络、成本和非确定性，先验证协议、状态与确定性业务逻辑。

