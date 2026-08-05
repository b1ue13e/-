---
type: project
topic: "Berkeley Lab01 Restaurant Review Pipeline"
created: 2026-08-05
status: active
progress: 0%
tags: [项目, 46-AI Agent工程, Berkeley, Lab01]
flow: project
kind: moc
source: "Berkeley LLM Agents MOOC public Lab 01–03 release instructions"
---

# Berkeley Lab 01 — Restaurant Review Pipeline 知识点映射

> [!warning] 合规边界
> 这是**官方作业的原创知识映射**，不是题目副本或答案。请从官方入口下载当前 starter code 与 `Instructions.md`，遵守课程协作规则；不要搜索、保存或提交他人的实现。

## 1. 官方事实

- **官方名称**：Lab 01, Restaurant Review Pipeline
- **公开目标**：使用 AutoGen 构建分析餐厅评论并给餐厅评分的管线。
- **官方验收事实**：starter code 内提供 `test.py` 公共测试；公开说明称通过其中 3/4 是完成指标。
- **官方说明**：<https://rdi.berkeley.edu/llm-agents-mooc/assets/instructions.pdf>
- **源码访问**：官方说明中的 Google Drive 链接；下载后先检查具体文件的许可证与版本。

## 2. 题目阶段—知识点映射

| 作业阶段（按公开目标重述） | 完成所需知识 | 对应笔记 | 层级 | 自检证据 |
| :--- | :--- | :--- | :---: | :--- |
| 接收自然语言查询 | 实体/餐厅名抽取、输入清洗、失败返回 | [[AI-Agent-工具调用与结构化契约]] | P0 | 空输入、未知餐厅、大小写测试 |
| 获取目标评论 | 工具白名单、参数校验、证据边界 | [[AI-Agent-工具调用与结构化契约]]、[[AI-Agent-记忆与检索增强生成]] | P0/P1 | 只返回目标实体评论与来源 |
| 从评论抽取评分 | Prompt 约束、结构化输出、范围校验 | [[AI-Agent-工具调用与结构化契约]] | P0 | 1–5 边界、格式错误测试 |
| 组织多个处理角色 | 角色职责、消息 schema、handoff | [[AI-Agent-多智能体协作与消息协议]] | P0 | 每条消息有发送者/接收者/工件 |
| 控制执行顺序 | DAG/状态机、终止、错误分支 | [[AI-Agent-规划状态与工作流编排]] | P0 | 查询为空不进入评分；失败有限重试 |
| 使用模型反馈修正 | 观察驱动下一动作 | [[AI-Agent-ReAct推理行动范式]] | P1 | 解析失败后有明确修正或终止 |
| 计算最终分数 | 确定性数学、数值范围、可复现 | [[AI-Agent-工具调用与结构化契约]] | P0 | 手算样例与代码结果一致 |
| 运行公共测试 | Python 环境、依赖版本、测试定位 | [[AI-Agent工程-作业必需与全面知识清单]] | P0 | `test.py` 结果与失败日志 |

## 2.1 AutoGen 0.2 桥梁

- 先完成 [[AI-Agent-前置-消息JSON异常与单元测试]]，再完成 [[AI-Agent-框架-AutoGen官方Lab版本补丁]]。
- Fall 2024 兼容线按本课已验证烟测固定 `autogen-agentchat==0.2.40`；若 starter code 声明不同精确 0.2.x，以 starter 为准。不要用会解析到新 API 的宽泛 `~=0.2`。
- 工具解析、评分和聚合保持为纯函数；框架只负责消息、注册与编排。
- 保存 `python --version`、`pip freeze`、starter commit/下载日期，禁止把当前稳定版 API 混入旧 Lab 环境。

## 3. 完成本作业的最小知识点集

- [ ] [[AI-Agent-边界与感知行动循环]]
- [ ] [[AI-Agent-工具调用与结构化契约]]
- [ ] [[AI-Agent-规划状态与工作流编排]]
- [ ] [[AI-Agent-多智能体协作与消息协议]]
- [ ] 能从官方 starter code 识别当前 AutoGen 版本与已有函数，不凭旧教程猜 API。
- [ ] 能用纯 Python 单独验证解析与聚合，不依赖模型碰运气。

## 4. 全面掌握扩展知识

- [ ] [[AI-Agent-ReAct推理行动范式]]：只在观察会改变动作时使用模型循环。
- [ ] [[AI-Agent-记忆与检索增强生成]]：评论是证据，不是高优先级指令。
- [ ] [[AI-Agent-安全威胁建模与系统评测]]：恶意评论可能注入评分角色。
- [ ] 为模型层做 fake/stub，使核心管线测试不需要联网和付费。
- [ ] 记录模型名、参数、依赖、耗时、token/费用、重试和失败类型。

## 5. 官方验收与自建验收分离

### 官方验收

- [ ] 按官方 `Instructions.md` 配置环境。
- [ ] 运行官方 `test.py`，至少通过公开说明要求的 3/4。
- [ ] 仅通过官方表单提交自己的实现。

### 本库自建验收（非 Berkeley 原题）

- [ ] 未知餐厅返回“无证据”，不虚构评论。
- [ ] 空评论列表不除零、不继续评分。
- [ ] 评分越界、缺字段、文本夹带指令时被拒绝或隔离。
- [ ] 同一输入在确定性聚合层结果一致。
- [ ] 多 Agent 对话在步数上限内终止。
- [ ] 去掉任一必要阶段时，测试能检测到失败。
- [ ] 运行 `cd "F:\-\03-Projects\46-AI Agent工程\local-acceptance"; python -m unittest -v`，全量离线测试通过。
- [ ] 确认 `agent_runtime.py` 实际调用已注册工具，而不只是直接调用餐厅纯函数。
- [ ] trace 含 stage/tool/outcome；handoff 含 sender/recipient/artifact；持久状态不保存评论指令文本。
- [ ] 注入故障后有限重试并终止；暂停 checkpoint 后恢复结果与不中断运行一致。

> [!important] 历史 Gate 与当前学习 Gate 分离
> “公共测试至少 3/4”只是 Fall 2024 官方公开说明中的历史课程门槛，可能依赖旧 starter、API Key 或已变化的提交入口。本课程当前 Gate 是本地全量测试全绿 + 官方环境可用时再记录官方测试结果；不能把本地测试冒充 Berkeley 成绩。

## 6. 调试顺序

1. 先让纯函数解析、校验、聚合通过自建测试。
2. 再验证单个工具调用与返回 schema。
3. 再验证每次 handoff 的发送者、接收者和 payload。
4. 最后连接真实模型与 AutoGen，避免把所有错误都归因于 prompt。
5. 公共测试失败时，按“输入→工具→消息→状态→数值→终止”定位，不针对测试字符串硬编码。

## 7. 复盘记录

| 失败样例 | 层级 | 根因 | 修复 | 回归测试 |
| :--- | :--- | :--- | :--- | :--- |
| | 模型/工具/协议/编排/数值 | | | |

## 8. 交付证据

- [ ] 自己的代码与 README
- [ ] 依赖/环境版本
- [ ] 公共测试结果摘要
- [ ] 自建边界测试
- [ ] 去敏运行轨迹
- [ ] 设计与失败复盘（不包含隐藏测试猜测）
