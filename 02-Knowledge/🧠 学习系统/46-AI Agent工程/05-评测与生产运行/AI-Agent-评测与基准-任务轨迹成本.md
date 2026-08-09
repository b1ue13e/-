---
type: study
topic: "AI Agent评测与基准：任务、轨迹与成本"
course: "AI Agent工程"
tags: [学习, 46-AI Agent工程, AI-Agent, 评测, 基准]
created: 2026-08-06
status: completed
difficulty: advanced
concept: [Agent评测, 轨迹评测, 基准测试]
prerequisites: ["AI-Agent-工具调用与结构化契约", "AI-Agent-规划状态与工作流编排"]
related: ["AI-Agent-反思与元认知-校验修正停止", "AI-Agent-Agentic-RL与自改进边界", "AI-Agent工程-大作业-受限可恢复Agent"]
stage_moc: "[[🧭 阶段5-评测与生产运行]]"
upstream: ["[[AI-Agent-环境交互-代码网页与沙箱执行]]", "[[AI-Agent-安全威胁建模与系统评测]]", "[[AI-Agent-规划状态与工作流编排]]"]
flow: knowledge
kind: concept
source: "Microsoft AI Agents for Beginners Lesson 10; Datawhale Hello-Agents Chapter 12; Berkeley Agentic AI F25 evaluation topics (verified 2026-08-06)"
source_urls: ["https://github.com/microsoft/ai-agents-for-beginners/tree/main/10-ai-agents-production", "https://github.com/datawhalechina/hello-agents/tree/main/docs/chapter12"]
accessed: 2026-08-08
license: "Microsoft MIT；Hello-Agents CC BY-NC-SA 4.0；Berkeley许可待核验；本卡为原创整合"
anki_deck: "46-AI Agent工程::评测"
anki_tags: [Agent评测, 轨迹, 基准, 成本]
---

# AI Agent 评测与基准：任务、轨迹与成本

## 0. 学习边界

- **类别**：**A 类（上线门禁）**。
- **判断理由**：Agent 的最终答案可能碰巧正确，但中途越权、使用错误证据、重复调用或成本失控。只做答案准确率会漏掉系统性失败。

## 1. 这个知识点解决什么问题？

> **麻烦**：Demo 成功无法回答“换任务还行吗、为什么成功、失败在哪层、成本多少、安全边界是否被突破”。

Agent 评测至少同时看：

1. **任务结果**：完成了吗？
2. **轨迹过程**：工具、证据、状态和权限是否正确？
3. **运行代价**：延迟、token、费用、步数与人工接管。
4. **安全性**：攻击成功、误拒、越权和敏感数据暴露。

## 2. 为什么它重要？它有什么用？

- 比较 Prompt、模型、工具、RAG、规划和框架版本。
- 通过 failure taxonomy 定位模型、工具、编排、数据、权限或环境层。
- 建立回归门，防止“修一个样例、破一类任务”。
- 为反思、自改进或 Agentic RL 提供可信信号。

## 3. 学它之前需要哪些前置知识？

1. 工具 schema 与成功/错误语义。
2. trace、span、artifact、checkpoint 与请求关联 ID。
3. 基本统计：比例、均值、分位数、置信区间与数据切片。

## 4. 用直觉语言解释它

> “评测 Agent 不只看送到终点没有，还要看走了哪条路、有没有闯红灯、花了多少油、遇到事故能否复现。”

## 5. 正式指标体系

### 任务层

$$TSR = \frac{\#\text{完成任务}}{N}$$

开放答案需明确判分器：精确匹配、单元测试、规则、人工 rubric 或经校准的 LLM judge。

### 工具/轨迹层

$$ToolAcc = \frac{\#\text{正确工具名且参数正确}}{\#\text{应调用工具的样本}}$$

还应报告非法工具率、无效重复调用率、证据引用正确率、平均步数、终止率和恢复成功率。

### 安全层

$$ASR=\frac{\#\text{攻击达到危险效果}}{\#\text{攻击样本}}, \quad FRR=\frac{\#\text{正常任务被误拒}}{\#\text{正常样本}}$$

### 运行层

报告 P50/P95 延迟、平均 token/费用、最大步数触发率、人工接管率；均值不能替代长尾。

## 6. 从任务到可信结论的流程

1. **定义任务分布**：真实用户意图、难度、工具组合、语言和风险层级。
2. **冻结样本与版本**：测试集、模型、Prompt、工具 schema、索引、随机种子和时间。
3. **定义逐样本预期**：答案、允许工具/参数、禁止动作、证据与停止条件。
4. **记录完整轨迹**：去敏输入输出、工具调用、状态转移、错误、成本。
5. **自动评分并抽样人工复核**：尤其校准 LLM judge。
6. **按切片和失败类型分析**：不只看总分。
7. **比较基线与候选**：同时检查质量、安全、成本和显著性。
8. **把失败样本加入回归集**：避免只改 Prompt 后丢失历史问题。

### 基准的正确用途

- **BFCL 类工具调用基准**：检查函数/工具选择与参数生成，不代表完整业务 Agent 可用。
- **GAIA 类综合任务基准**：检查推理、检索、工具与多步完成，不替代你的领域、权限和成本评测。
- 公共榜单用于定位能力，不是上线许可证。

## 7. 例子：基础 → 中等 → 实际应用

### 例子 1：手算

20 个正常任务成功 16 个，10 个攻击样本有 2 个达到危险效果，20 个正常任务有 1 个误拒：

- $TSR=16/20=0.80$
- $ASR=2/10=0.20$
- $FRR=1/20=0.05$

不能只报告“总体正确率 80%”，因为 20% 攻击成功可能直接阻止上线。

### 例子 2：答案对但轨迹错

Agent 最终给出正确汇率，却调用了未授权浏览器、访问了错误域名后又猜中。任务层通过，轨迹与安全层失败；应按失败分类修授权，而不是奖励最终答案。

### 例子 3：可运行 Python 指标聚合

```python
from statistics import median

rows = [
    {"normal": True, "success": True,  "attack_success": False, "latency_ms": 80},
    {"normal": True, "success": False, "attack_success": False, "latency_ms": 220},
    {"normal": False, "success": False, "attack_success": True, "latency_ms": 150},
]

normal = [r for r in rows if r["normal"]]
attacks = [r for r in rows if not r["normal"]]
tsr = sum(r["success"] for r in normal) / len(normal)
asr = sum(r["attack_success"] for r in attacks) / len(attacks)
latencies = sorted(r["latency_ms"] for r in rows)
p95_index = max(0, int(0.95 * len(latencies) + 0.9999) - 1)
print({"TSR": tsr, "ASR": asr, "P50_ms": median(latencies), "P95_ms": latencies[p95_index]})
```

输入是逐样本记录；输出包含任务、安全和延迟指标。真实报告还需样本数、置信区间、版本与切片。

本课程的固定回归集位于 `03-Projects/46-AI Agent工程/data/eval_cases.jsonl`，明确分成 20 条正常、10 条异常、10 条对抗样本。运行 `python -m scripts.run_eval` 会逐样本执行 runtime 和安全策略，输出状态、分数、工具轨迹、是否通过，并聚合 TSR、异常失败关闭率、ASR、ToolAcc、平均/P95 步数与成本代理到 `artifacts/eval/latest.json`。该结果只支持标准库离线控制面；真实模型仍须另建版本化在线 eval，不能把本地 `ASR=0` 外推到生产攻击面。

## 8. 常见误区和易混概念

### 误区 1：最终答案正确就通过

需要检查工具选择、参数、证据、权限、终止和成本。

### 误区 2：LLM judge 给分就是客观标准

judge 受提示、顺序、长度、模型与自偏好影响；需人工校准、盲评、规则交叉和版本固定。

### 误区 3：公共 benchmark 高分等于生产可用

公共分布通常不包含你的权限、数据质量、延迟预算、对抗输入和副作用。

| 概念 | 回答的问题 |
| :--- | :--- |
| Evaluation | 在定义分布与标准上表现怎样？ |
| Observability | 这次运行发生了什么？ |
| Monitoring | 上线后指标是否漂移或告警？ |
| Benchmark | 在共享任务集上怎样比较？ |

## 9. 双教材定位与 Obsidian 双链

- **Microsoft Lesson 10**：trace/span、生产指标、评测和成本。
- **Hello-Agents Chapter 12**：BFCL、GAIA、数据生成质量、LLM judge 与 win-rate 实践。
- [[AI-Agent-安全威胁建模与系统评测]] 负责威胁模型和安全指标；本卡补全任务、轨迹、成本、基准和实验设计。
- [[AI-Agent-反思与元认知-校验修正停止]] 使用单次反馈；本卡判断系统版本是否真的改进。

## 10. 闭卷复现任务

- [ ] 写出任务、轨迹、安全、运行四层指标。
- [ ] 手算 TSR、ASR、FRR。
- [ ] 为一个工具 Agent 写 5 条逐样本预期。
- [ ] 解释 P95 为什么不能由平均值替代。
- [ ] 设计一个 LLM judge 校准方案。
- [ ] 将一个失败归类到模型/工具/编排/数据/权限/环境层。

## 11. 自测题：5 道

### 1. #自测题/基础
为何 Agent 需要轨迹评测？
> [!question]- 答案解析
> 最终答案会掩盖错误工具、越权、错误证据、冗余步骤和碰巧成功。

### 2. #自测题/基础
ASR 和 FRR 分别衡量什么？
> [!question]- 答案解析
> ASR 衡量攻击达到危险效果的比例；FRR 衡量正常任务被安全机制误拒的比例。

### 3. #自测题/中等
BFCL 得分高仍需测什么？
> [!question]- 答案解析
> 领域任务成功、长程编排、真实工具错误、权限、安全、成本、延迟和恢复。

### 4. #自测题/中等
模型升级后总分上涨 2%，为什么不能马上替换？
> [!question]- 答案解析
> 需看样本量/波动、切片、ASR/FRR、成本/延迟、逐样本回归与版本可复现性。

### 5. #自测题/较难
怎样避免为 benchmark 过拟合？
> [!question]- 答案解析
> 分离开发/回归/盲测，保留真实流量切片和扰动样本，不针对公开答案写规则，周期更新并记录决策。

## 12. 我的主动回忆区

### 我的闭卷复述
> 不看上文，说出一个“答案正确但系统失败”的例子。

### 我的推导复现
> 为当前项目写一页 eval spec：任务分布、版本、逐样本预期、指标、门槛。

### 我的错误与卡点
- 

### 下次复习日期
- [ ] 明天
- [ ] 3 天后
- [ ] 7 天后
- [ ] 14 天后

## 13. 给 Obsidian 的归档建议

- **适合文件夹**：`02-Knowledge/🧠 学习系统/46-AI Agent工程/`
- **建议标签**：`#学习` `#Agent评测` `#基准`
- **拆分建议**：真实失败积累后，按 failure taxonomy 拆错题卡，不把逐样本日志塞进概念卡。

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

Agent 评测四层是什么？::任务结果、轨迹过程、安全边界、运行成本与延迟。
为什么最终答案正确不足以通过？::过程可能越权、用错工具/证据、重复调用或碰巧成功。
BFCL/GAIA 类基准不能替代什么？::你的领域分布、权限、安全、成本、延迟、故障与恢复评测。
LLM judge 至少怎样校准？::固定版本与 rubric，用人工盲评样本验证一致性，并与确定性规则/多个评审交叉。

