---
type: study
topic: "AI Agent部署与本地运行：伸缩、路由与烟测"
course: "AI Agent工程"
tags: [学习, 46-AI Agent工程, AI-Agent, 部署, 本地运行]
created: 2026-08-06
status: completed
difficulty: advanced
concept: [Agent部署, 本地优先, 烟雾测试]
prerequisites: ["AI-Agent-框架选型与最小运行时", "AI-Agent-可观测性与生产运行-轨迹审批恢复"]
related: ["AI-Agent-环境交互-代码网页与沙箱执行", "AI-Agent-评测与基准-任务轨迹成本", "AI-Agent-安全审计-加密收据与审批绑定"]
stage_moc: "[[🧭 阶段6-部署审计与改进]]"
upstream: ["[[AI-Agent-可观测性与生产运行-轨迹审批恢复]]"]
flow: knowledge
kind: concept
source: "Microsoft AI Agents for Beginners Lessons 16 and 17 (verified 2026-08-06)"
source_urls: ["https://github.com/microsoft/ai-agents-for-beginners/tree/main/16-deploying-scalable-agents", "https://github.com/microsoft/ai-agents-for-beginners/tree/main/17-creating-local-ai-agents"]
accessed: 2026-08-08
license: "Microsoft AI Agents for Beginners MIT；本卡为原创整合"
anki_deck: "46-AI Agent工程::部署与本地运行"
anki_tags: [部署, 本地Agent, 路由, 烟测, 伸缩]
---

# AI Agent 部署与本地运行：伸缩、路由与烟测

## 0. 学习边界

- **类别**：**B 类（生产工程）**。
- **判断理由**：原型把状态放内存、串行调用工具、人工观察输出；部署后必须处理并发、持久状态、背压、路由、密钥、升级、成本和故障恢复。本地 Agent 还要面对模型能力、硬件和数据边界。

## 1. 这个知识点解决什么问题？

> **麻烦**：笔记本 Demo 成功，但第二个请求覆盖状态；worker 重启丢任务；高峰压垮模型；敏感数据被错误路由到云；部署“健康”却无法完成一次真实工具调用。

本卡回答：如何把 runtime 变成可伸缩服务，怎样在本地/云之间按策略路由，以及如何用 smoke test 在部署后快速发现接线错误。

## 2. 为什么它重要？它有什么用？

- 将进程内状态迁移为持久、可恢复、按 request 隔离的状态。
- 用队列、并发限制、超时、退避和幂等控制负载。
- 按隐私、能力、延迟、成本和可用性路由模型/工具。
- 区分 health check、smoke test、offline eval 和在线监控。

## 3. 学它之前需要哪些前置知识？

1. [[AI-Agent-框架选型与最小运行时]]：能拆出模型、工具、状态、编排、终止与 trace。
2. [[AI-Agent-可观测性与生产运行-轨迹审批恢复]]：请求关联、checkpoint、幂等和审批。
3. [[AI-Agent-评测与基准-任务轨迹成本]]：部署成功不代表任务质量通过。

## 4. 用直觉语言解释它

> “原型像一个人桌面上的待办纸；生产系统像有编号、排队、负责人、交接记录和应急出口的工单中心。”

本地/云路由像数据海关：先按数据等级与允许目的地检查，再考虑能力和成本。

## 5. 正式模型与架构

### 服务稳定性

到达率为 $\lambda$，每个 worker 服务率为 $\mu$，worker 数为 $c$：

$$
\rho = \frac{\lambda}{c\mu}
$$

长期 $\rho \ge 1$ 时队列会持续增长。实际系统还要为突发、长尾工具和模型限流留余量，不能把 100% 利用率当目标。

### 生产最小架构

```text
API/Auth -> Admission policy -> Queue -> Stateless workers
                    |              |          |
               rate limit      task state   model/tool adapters
                    |              |          |
                 audit        checkpoint    trace/eval hooks
```

### 本地优先路由

路由顺序不是“哪个模型更便宜”，而是：

1. 数据分类与合规是否允许离开设备/网络域？
2. 本地模型/工具是否具备任务所需能力？
3. 延迟、成本、容量和可用性是否满足 SLO？
4. 若降级/转云，是否需要去敏、审批和明确提示？

## 6. 从原型到部署的检查顺序

1. **冻结契约**：请求、消息、工具、状态、artifact 与错误 schema。
2. **外置状态**：worker 可重启；状态按 request/tenant 隔离并带版本。
3. **副作用幂等**：工具执行使用 idempotency key；重试不重复付款/发布。
4. **入口控制**：认证、配额、最大任务大小、超时和队列上限。
5. **背压与取消**：过载时拒绝/排队，不无限增加并发；传播取消信号。
6. **模型/工具路由**：按数据、能力、版本、预算和健康状态选择。
7. **逐步发布**：dev→staging→canary→production，保留快速回滚。
8. **部署后烟测**：最小真实链路回答、工具调用、状态写入、trace 和权限。
9. **离线评测门**：smoke 通过后仍需质量/安全/成本评测。

### 四种检查不要混淆

| 检查 | 回答什么 | 例子 |
| :--- | :--- | :--- |
| Liveness | 进程活着吗 | `/live` 返回 200 |
| Readiness | 依赖可用、能接请求吗 | 状态库/模型 endpoint 可达 |
| Smoke | 最小用户链路接通吗 | 一次只读工具任务完成且有 trace |
| Evaluation | 行为足够好吗 | 40 个分层样本通过门槛 |

## 7. 例子：基础 → 中等 → 实际应用

### 例子 1：手算容量

到达率 6 请求/秒，每个 worker 平均处理 2 请求/秒。3 个 worker 时 $\rho=1$，无突发余量；5 个 worker 时 $\rho=0.6$。但若 P95 工具调用远慢于平均值，还需队列与压测验证。

### 例子 2：本地/云混合

含个人病历的总结任务默认只在本地执行。本地模型无法处理图像时，不应自动上传；系统先请求用户批准，并仅发送经允许的去敏数据。公共技术文档总结可按成本/能力路由到云。

### 例子 3：可运行路由与烟测

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Request:
    data_class: str
    needs_large_model: bool

def route(req: Request, local_ready: bool, cloud_ready: bool) -> str:
    if req.data_class == "restricted":
        if not local_ready:
            raise RuntimeError("restricted request cannot leave local boundary")
        return "local"
    if req.needs_large_model and cloud_ready:
        return "cloud"
    if local_ready:
        return "local"
    raise RuntimeError("no allowed healthy route")

def smoke_test() -> None:
    assert route(Request("restricted", False), True, True) == "local"
    assert route(Request("public", True), True, True) == "cloud"
    try:
        route(Request("restricted", True), False, True)
    except RuntimeError as exc:
        assert "cannot leave" in str(exc)
    else:
        raise AssertionError("policy failure")

smoke_test()
print("smoke: ok")
```

这是路由策略微型实验，不是部署平台 SDK。真实 smoke test 还应验证一次模型调用、只读工具、状态、trace、认证与超时。

课程项目提供两个可执行门：`python -m scripts.readiness_smoke` 检查包导入、最小 runtime、内容绑定审批写入和 40 样本 eval Gate；`python -m pip wheel . --no-deps --no-build-isolation --wheel-dir artifacts/wheel` 验证项目可打包。两者都属于本地 readiness，不是云部署、canary 或真实模型 smoke；外部环境必须单独记录 endpoint、模型、认证、版本、费用和实际结果。

## 8. 常见误区和易混概念

### 误区 1：自动伸缩能修复所有过载

模型配额、数据库、工具 API 和队列可能是瓶颈；无背压只会把故障向下游扩散。

### 误区 2：本地模型等于数据绝不外流

遥测、崩溃报告、远程 MCP、更新服务和云工具仍可能出网；需数据流审计。

### 误区 3：smoke test 通过等于上线通过

Smoke 只证明最小链路接通，不能证明任务质量、安全和长尾成本。

| 概念 | 作用 |
| :--- | :--- |
| Scaling | 增减容量 |
| Load shedding | 过载时拒绝低优先级请求 |
| Backpressure | 让上游感知下游容量 |
| Routing | 按策略选择模型/工具/区域 |
| Canary | 让少量流量验证候选版本 |

## 9. 双教材定位与 Obsidian 双链

- [Microsoft Lesson 16 - Deploying Scalable Agents](https://github.com/microsoft/ai-agents-for-beginners/tree/main/16-deploying-scalable-agents)：部署模式、生命周期、伸缩、可观测、成本、企业考虑和 smoke test。
- [Microsoft Lesson 17 - Creating Local AI Agents](https://github.com/microsoft/ai-agents-for-beginners/tree/main/17-creating-local-ai-agents)：小模型、本地 RAG/MCP 与混合路由。
- 本卡抽取跨平台稳定机制；Foundry Local/Qwen 等具体 API 作为版本化选修，不进入核心定义。

## 10. 闭卷复现任务

- [ ] 画出 API、策略、队列、worker、状态、adapter 与 trace。
- [ ] 手算一个 $\rho$，说明为何等于 1 不安全。
- [ ] 区分 liveness/readiness/smoke/eval。
- [ ] 修改代码，加入 `confidential` 需去敏批准的分支。
- [ ] 为一个副作用工具写 idempotency key 和取消策略。
- [ ] 写 canary 的回滚触发指标。

## 11. 自测题：5 道

### 1. #自测题/基础
为什么生产 worker 应尽量无状态？
> [!question]- 答案解析
> 便于重启、横向扩展和故障转移；任务状态存入可版本化、可恢复的外部存储。

### 2. #自测题/基础
Readiness 与 smoke test 有什么区别？
> [!question]- 答案解析
> Readiness 检查依赖是否能接请求；smoke 执行最小真实用户链路，验证接线与权限。

### 3. #自测题/中等
为何重试副作用工具前必须有幂等？
> [!question]- 答案解析
> 超时可能发生在工具已成功但响应丢失之后；盲重试会重复付款、写入或发布。

### 4. #自测题/中等
本地模型不可用时，受限数据任务应怎样降级？
> [!question]- 答案解析
> 安全失败或等待本地恢复；除非策略和用户明确批准去敏后的特定云路径，不能自动外传。

### 5. #自测题/较难
Canary 版本任务成功率上升、P95 翻倍，是否推广？
> [!question]- 答案解析
> 取决于预设 SLO/预算；不能只看质量。若 P95 超门槛应停止推广，按 trace 定位并回滚或修复。

## 12. 我的主动回忆区

### 我的闭卷复述
> 不看上文，说出从原型到生产的九步检查顺序。

### 我的推导复现
> 为一个本地/云混合 Agent 写数据分类与路由决策表。

### 我的错误与卡点
- 

### 下次复习日期
- [ ] 明天
- [ ] 3 天后
- [ ] 7 天后
- [ ] 14 天后

## 13. 给 Obsidian 的归档建议

- **适合文件夹**：`02-Knowledge/🧠 学习系统/46-AI Agent工程/`
- **建议标签**：`#学习` `#Agent部署` `#本地Agent`
- **拆分建议**：具体平台配置、负载测试数据和运行手册放项目目录。

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

Liveness、Readiness、Smoke、Evaluation 分别回答什么？::进程活着吗、依赖可用能接请求吗、最小真实链路接通吗、行为质量/安全/成本足够好吗。
为什么本地优先路由先看数据分类？::数据是否允许离开设备/网络域是硬约束，能力、成本和延迟只能在允许路径中优化。
为什么副作用工具重试必须幂等？::超时不代表未执行，幂等键防止重试造成重复付款、写入或发布。
$\rho=\lambda/(c\mu)$ 表示什么？::平均到达负载与总服务能力之比；接近或超过 1 时队列缺乏稳定余量。

