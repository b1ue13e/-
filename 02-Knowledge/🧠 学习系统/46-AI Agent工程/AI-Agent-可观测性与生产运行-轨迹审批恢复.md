---
type: study
topic: "Agent 可观测性、人工审批与生产恢复"
tags: [学习, 46-AI Agent工程, 可观测性, HITL, 部署]
created: 2026-08-05
status: completed
mastery: not_started
difficulty: advanced
concept: ["轨迹可观测性", "人工审批", "故障恢复"]
prerequisites: ["AI-Agent-规划状态与工作流编排", "AI-Agent-安全威胁建模与系统评测"]
related: ["AI-Agent-工具调用与结构化契约", "AI-Agent-多智能体协作与消息协议"]
flow: knowledge
kind: concept
source: "UC Berkeley Agentic AI F25; Stanford CS224V F25; Microsoft AI Agents for Beginners Lessons 10, 16 and 18; Datawhale Hello-Agents Chapter 12; Hugging Face Agents Course observability"
source_urls: ["https://github.com/microsoft/ai-agents-for-beginners/tree/main/10-ai-agents-production", "https://github.com/microsoft/ai-agents-for-beginners/tree/main/16-deploying-scalable-agents", "https://github.com/microsoft/ai-agents-for-beginners/tree/main/18-securing-ai-agents", "https://github.com/datawhalechina/hello-agents/tree/main/docs/chapter12"]
anki_deck: "46-AI Agent工程::生产工程"
anki_tags: [可观测性, HITL, 重试, 幂等]
---

# AI Agent 可观测性与生产运行：轨迹、审批、恢复

## 0. 先判断它值不值得深挖

- **类别**：A 类（从演示走向可运营系统）。
- **判断理由**：最终答案正确并不能证明过程安全；生产系统还必须能暂停、审计、重放和恢复。

## 1. 这个知识点解决什么问题？

> Agent 重复下单、调用超时后状态不明、发生异常时只能看到最后一句文本，无法知道哪一步越权。

## 2. 为什么它重要？它有什么用？

- 轨迹日志支持定位模型、工具、编排、数据和权限层故障。
- HITL 在高风险动作前暂停并获得可审计批准。
- 幂等键、检查点和有限重试避免重复副作用。

## 3. 学它之前需要哪些前置知识？

1. [[AI-Agent-规划状态与工作流编排]]。
2. [[AI-Agent-安全威胁建模与系统评测]]。

## 4. 用直觉语言解释它

> “Agent 像自动驾驶：轨迹是行车记录仪，审批是接管请求，检查点是安全停车位，幂等键防止同一脚油门踩两次。”

## 5. 正式定义、核心公式、符号解释

端到端成功率：$R_{e2e}=N_{success}/N$；单步成功率不能相乘假定独立。一次事件至少记录：`trace_id, step_id, state, action, sanitized_input, outcome, latency_ms, cost, retry, policy_decision`。

| 机制 | 触发 | 结果 |
| :--- | :--- | :--- |
| 审批 | 金钱、删除、外发、权限提升 | pause/approve/reject |
| 重试 | 暂时性超时、限流 | 有上限、退避、抖动 |
| 幂等 | 可能重复的副作用 | 同一 key 只生效一次 |
| 检查点 | 每个可恢复状态 | 从已提交状态继续 |

## 6. 推导思路和思想来源

- 只记录自然语言不足以重放，必须记录状态与结构化动作。
- 重试会放大副作用，因此先判断动作是否幂等。
- 人工审批不是弹窗装饰，而是状态机中的持久化中断。

## 7. 例子：基础 → 中等 → 实际应用

### 例子 1：基础例子（可手算）

100 次任务中 80 次成功、10 次被安全拒绝、10 次故障。任务成功率 80%，安全决定覆盖率 100%；不能把合规拒绝算成系统崩溃。

### 例子 2：中等例子

支付请求超时并不代表未扣款。没有幂等键时自动重试可能重复支付；正确流程是查询已有结果或用相同键重试。

### 例子 3：实际应用例子（可运行 Python）

```python
# 输入：请求 ID 与金额；输出：幂等执行结果。
from dataclasses import dataclass, field

@dataclass
class PaymentStore:
    results: dict[str, str] = field(default_factory=dict)

    def charge(self, request_id: str, amount: int, approved: bool) -> str:
        if request_id in self.results:
            return self.results[request_id]
        if amount > 1000 and not approved:
            return "PAUSED_FOR_APPROVAL"
        result = f"CHARGED:{amount}"
        self.results[request_id] = result
        return result

store = PaymentStore()
assert store.charge("r1", 100, True) == "CHARGED:100"
assert store.charge("r1", 999, True) == "CHARGED:100"
assert store.charge("r2", 5000, False) == "PAUSED_FOR_APPROVAL"
```

### 本课程已实现的 trace 与 checkpoint

`03-Projects/46-AI Agent工程/local-acceptance/agent_runtime.py` 的 `ReviewAgentPipeline` 在每一步记录 `trace_id/step/stage/actor/action/outcome/tool/latency_ms/cost/retry/policy_decision`，在每次 handoff 记录 `sender/recipient/artifact`。`save_checkpoint()` 将 query、当前 stage、step、结构化证据 ID/分数、重试、消息和 trace 写入带 schema version 与 SHA-256 的 JSON envelope，并通过临时文件原子替换；`from_checkpoint()` 先验版本与完整性，再从暂停阶段继续。

自动测试执行“运行两步→暂停保存→新 runtime 加载→继续完成”，并将最终 score/evidence IDs 与不中断运行比较。故障注入连续超过 retry limit 时必须在 step budget 内进入 `failed`，不是靠最终文本猜测是否终止。

边界：当前 checkpoint 只覆盖标准库教学 runtime；AutoGen `initiate_chat` 的真实模型会话状态仍需在独立 0.2 环境验证，不能从本地测试外推。

## 8. 常见误区和易混概念

- **日志越多越好**是误区：不得记录密钥、完整隐私数据或未脱敏工具结果。
- **失败就重试**是误区：参数校验失败、权限拒绝不应重试。

| 概念 | 核心问题 | 区别 | 使用场景 |
| :--- | :--- | :--- | :--- |
| 日志 | 发生了什么 | 离散事件 | 调试 |
| 指标 | 整体是否退化 | 聚合统计 | 告警与比较 |
| 轨迹 | 一次任务如何流转 | 关联跨步骤事件 | 根因定位 |

## 9. 相关知识点与 Obsidian 双链建议

- 上游：[[AI-Agent-规划状态与工作流编排]]。
- 横向：[[AI-Agent-安全威胁建模与系统评测]]。
- 下游：课程结课项目的运行手册与事故复盘。
- 可运行实现：`03-Projects/46-AI Agent工程/local-acceptance/agent_runtime.py` 的 trace、有限重试和 JSON checkpoint。

## 10. 闭卷复现任务

- [ ] 写出最小轨迹字段。
- [ ] 区分可重试和不可重试错误。
- [ ] 为高风险工具设计审批状态。
- [ ] 解释幂等键如何防重复副作用。
- [ ] 设计从检查点恢复的测试。
- [ ] 区分日志、指标与轨迹。
- [ ] 说明哪些错误不应重试。
- [ ] 为一次高风险动作写审批摘要。
- [ ] 设计去敏日志规则。
- [ ] 说出一个幂等键的真实应用。

## 11. 自测题：5 道

1. 为什么只保存最终答案不够？ `#自测题/基础`
2. 参数越界应否重试？ `#自测题/基础`
3. 设计删除文件工具的审批条件。 `#自测题/中等`
4. 如何验证相同幂等键只执行一次？ `#自测题/中等`
5. 给出一个日志、指标、轨迹协同定位故障的案例。 `#自测题/较难`

> [!question]- 参考答案与评分点
> 1. 无法定位中间越权/错误。2. 否，应修正输入。3. 路径白名单、影响预览、人工批准、审计记录。4. 重复调用并断言副作用计数为 1。5. 需含告警指标→trace 定位→事件日志证据链。

## 12. 我的主动回忆区

- **轨迹字段默写**：
- **审批边界**：
- **恢复测试结果**：
- [ ] 明天  [ ] 3 天后  [ ] 7 天后  [ ] 14 天后

## 13. 给 Obsidian 的归档建议

- 当某一机制形成独立项目实现时，再拆“可观测性/HITL/恢复”子卡；入门阶段保留完整生产闭环。
- 结课项目必须附去敏 trace、SLO、重试矩阵和人工升级规则。

## 🃏 Anki 卡片

Q: 为什么副作用工具重试前必须考虑幂等？
A: 超时不代表动作未发生；非幂等重试可能重复支付、发送或删除。
