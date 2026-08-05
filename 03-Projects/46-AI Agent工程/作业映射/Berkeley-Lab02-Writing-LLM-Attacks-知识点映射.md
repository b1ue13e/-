---
type: project
topic: "Berkeley Lab02 Writing LLM Attacks"
created: 2026-08-05
status: active
progress: 0%
tags: [项目, 46-AI Agent工程, Berkeley, Lab02, 安全]
flow: project
kind: moc
source: "Berkeley LLM Agents MOOC public Lab 01–03 release instructions"
---

# Berkeley Lab 02 — Writing LLM Attacks 知识点映射

> [!danger] 授权边界
> 只在 Berkeley 课程提供的环境、自己的本地靶场或书面授权系统中测试。本文不提供可直接迁移到真实系统的攻击载荷，也不复制官方隐藏测试或答案。

## 1. 官方事实

- **官方名称**：Lab 02, Writing LLM Attacks
- **公开目标**：编写攻击 prompts；课程公开说明将其定位为 LLM security prompt engineering。
- **官方验收事实**：至少通过 1/2 隐藏测试；公开说明称第一项隐藏测试与 `Instructions.md` 中 OpenAI Playground 图片的 mock system message 本质相同。
- **官方说明**：<https://rdi.berkeley.edu/llm-agents-mooc/assets/instructions.pdf>

## 2. 作业目标—知识点映射

| 工作阶段 | 完成所需知识 | 对应笔记 | 层级 | 自检证据 |
| :--- | :--- | :--- | :---: | :--- |
| 明确授权目标 | 测试范围、资产、禁区和停止条件 | [[AI-Agent-安全威胁建模与系统评测]] | P0 | 一页 scope 声明 |
| 理解 system/user/data 边界 | 指令层级、输入来源、信任边界 | [[AI-Agent-边界与感知行动循环]] | P0 | 标出攻击输入进入哪一层 |
| 定义攻击成功 | 可观察判据、不是主观“看起来越狱” | [[AI-Agent-安全威胁建模与系统评测]] | P0 | 每类攻击有 success predicate |
| 建立攻击类别 | 直接注入、角色冲突、上下文操纵、编码/混淆等 | [[AI-Agent-安全威胁建模与系统评测]] | P0/P1 | 类别矩阵而非单字符串 |
| 观察响应并迭代 | 轨迹、失败分类、有限预算 | [[AI-Agent-ReAct推理行动范式]] | P1 | 每轮假设与观察摘要 |
| 防止越权副作用 | 工具权限、sandbox、禁止真实目标 | [[AI-Agent-工具调用与结构化契约]] | P0 | 靶场无真实写权限 |
| 衡量攻击覆盖 | ASR、按类别切片、迁移性 | [[AI-Agent-安全威胁建模与系统评测]] | P1 | 结果表与失败样例 |

## 3. 完成本作业的最小知识点集

- [ ] 能区分 prompt injection 与 jailbreak。
- [ ] 能写出资产、攻击者、入口、成功条件和授权范围。
- [ ] 能将尝试按攻击机制分组，而不是堆同义句。
- [ ] 能记录模型版本、参数、提示、响应摘要与是否成功。
- [ ] 理解隐藏测试要求泛化，禁止为猜测字符串硬编码。

## 4. 全面掌握扩展知识

- [ ] 直接 vs 间接注入；单轮 vs 多轮；内容层 vs 工具层攻击。
- [ ] 按模型/温度/上下文长度测迁移性和方差。
- [ ] 同时记录攻击成本、查询次数和速率限制。
- [ ] 用去敏语料管理攻击用例，避免把危险内容传播到知识库正文。
- [ ] 把失败攻击也作为边界证据，而不是只保留成功样例。

## 5. 官方验收与自建验收分离

### 官方验收

- [ ] 从官方 Drive 下载当前 Lab02 包。
- [ ] 阅读 `Instructions.md` 和 mock system message。
- [ ] 在规定环境完成自己的攻击 prompts。
- [ ] 达到至少 1/2 隐藏测试的官方门槛并按官方表单提交。

### 本库自建验收（非 Berkeley 原题）

- [ ] 攻击类别至少覆盖 4 个机制，每类有假设而非只换措辞。
- [ ] 每个尝试有授权范围、成功判据和安全停止条件。
- [ ] 对同一类别至少记录一个失败样例及原因。
- [ ] 靶场不连接邮件、付款、删除等真实副作用工具。
- [ ] 攻击记录去除密钥、个人数据与可滥用真实目标信息。
- [ ] 运行 `local-acceptance` 的安全测试，确认不可信内容只进入数据层。

执行命令：

```powershell
cd "F:\-\03-Projects\46-AI Agent工程\local-acceptance"
python -m unittest -v
```

重点观察 `test_malicious_review_is_never_promoted_to_instruction`、不同措辞的 adversarial text 测试和故障终止测试。安全 harness 不按 `ignore/reveal/run` 等关键词判定成败，而按 typed source、requested action 与“危险动作是否被真正放行”计算 ASR。

> [!important] 历史 Gate 与当前学习 Gate 分离
> “隐藏测试至少 1/2”是 Fall 2024 的历史官方门槛，本库既无法也不会复刻隐藏测试。当前 Gate 是：4 类机制、每类至少 2 个安全靶场变体、明确成功判据、至少 1 个失败样例，以及本地策略测试全绿。

## 6. 受控实验记录模板

| ID | 机制类别 | 假设 | 授权靶场 | 成功判据 | 结果 | 失败解释 |
| :--- | :--- | :--- | :--- | :--- | :---: | :--- |
| A-01 | | | | | | |

> [!note] 不在此表写可复用攻击全文
> 完整实验输入只保存于作业自己的受控目录；知识库记录机制、结果和防御启示。

## 7. 复盘问题

1. 成功是模型内容层失守，还是应用层实际执行越权动作？
2. 攻击依赖具体字符串，还是利用稳定的信任边界缺陷？
3. 结果对模型和采样参数是否稳定？
4. 哪个模型外控制可以让同一攻击即使“说服模型”也不产生后果？

## 8. 交付证据

- [ ] 自己的攻击设计（受控保存）
- [ ] 类别与假设矩阵
- [ ] 结果与失败分类
- [ ] 查询预算和环境版本
- [ ] 合法授权与无真实副作用确认
- [ ] 对 Lab03 的防御需求清单
