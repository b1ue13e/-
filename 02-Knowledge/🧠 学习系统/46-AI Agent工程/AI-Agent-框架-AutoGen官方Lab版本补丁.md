---
type: study
topic: "AutoGen 0.2 官方 Lab 版本补丁"
tags: [学习, 46-AI Agent工程, AutoGen, Berkeley-Lab01]
created: 2026-08-05
status: completed
mastery: not_started
difficulty: intermediate
concept: ["AutoGen 0.2", "工具注册", "终止条件"]
prerequisites: ["AI-Agent-前置-消息JSON异常与单元测试", "AI-Agent-工具调用与结构化契约"]
related: ["AI-Agent-多智能体协作与消息协议", "AI-Agent-规划状态与工作流编排"]
flow: knowledge
kind: concept
source: "UC Berkeley LLM Agents MOOC F24 Lab 01; Microsoft AutoGen 0.2 docs; Microsoft AI Agents for Beginners Lessons 2 and 14; Datawhale Hello-Agents Chapter 6"
source_urls: ["https://github.com/microsoft/ai-agents-for-beginners/tree/main/02-explore-agentic-frameworks", "https://github.com/microsoft/ai-agents-for-beginners/tree/main/14-microsoft-agent-framework", "https://github.com/datawhalechina/hello-agents/tree/main/docs/chapter6"]
anki_deck: "46-AI Agent工程::框架桥梁"
anki_tags: [AutoGen, 工具注册, 终止, 版本锁定]
---

# AI Agent 框架：AutoGen 0.2 官方 Lab 版本补丁

## 0. 先判断它值不值得深挖

- **类别**：A 类（Berkeley Fall 2024 Lab 01 的框架桥梁）。
- **判断理由**：AutoGen 当前稳定 API 已与 0.2 时代显著不同；混用教程会造成导入、注册和终止错误。

## 1. 这个知识点解决什么问题？

> 课程 starter code 使用旧代 API，搜索结果却常显示新版 `autogen_agentchat`。照抄后类名、工具注册和运行入口对不上。

## 2. 为什么它重要？它有什么用？

- 识别作业环境到底属于 0.2 还是当前稳定版。
- 完成最小 Agent、工具注册、执行角色和终止条件。
- 用测试替身先验收业务逻辑，再接模型与框架。

## 3. 学它之前需要哪些前置知识？

1. [[AI-Agent-前置-消息JSON异常与单元测试]]。
2. [[AI-Agent-工具调用与结构化契约]]。
3. 能读取 starter code 的 `requirements.txt`、导入语句和测试命令。

## 4. 用直觉语言解释它

> “框架版本像插座规格：业务流程没变，但插头、接线和开关位置变了。先认规格，再接线。”

## 5. 正式定义、核心公式、符号解释

Fall 2024 兼容线使用官方 0.2 文档接口：`ConversableAgent`、`register_for_llm`、`register_for_execution`、`initiate_chat`。安装基线为：

`python -m venv .venv` → 激活环境 → `pip install "autogen-agentchat==0.2.40"`。

> [!warning] 不要直接使用 `~=0.2`
> 按 PEP 440，`~=0.2` 的兼容上界是 `<1.0`；2026-08-05 实测会解析到 `0.7.5`，该版本没有旧教程的 `autogen.ConversableAgent` 命名空间。本课程烟测固定 `0.2.40`；若 Berkeley starter 声明另一精确 0.2.x，以 starter 为准并单独锁定。

最终仍应以官方 starter code 内依赖声明为准，并运行 `pip freeze > environment-lock.txt` 保存实际解析版本。

| 角色 | 职责 | 0.2 API |
| :--- | :--- | :--- |
| caller | 决定调用哪个工具及参数 | `register_for_llm` |
| executor | 执行白名单函数 | `register_for_execution` |
| termination | 阻止无限对话 | `is_termination_msg` / 最大轮数 |

## 6. 推导思路和思想来源

- 工具“可见”与“可执行”必须分离：模型只获 schema，执行者持有函数权限。
- 终止不能只靠模型自觉输出，应同时设置消息条件和轮数上限。
- 框架层应薄，解析、评分、聚合保留为纯函数，便于离线测试。

## 7. 例子：基础 → 中等 → 实际应用

### 例子 1：基础例子（可手算）

只有 `register_for_llm` 时模型知道工具但无人执行；只有 `register_for_execution` 时执行者有函数但模型不知道何时、怎样调用。两端缺一不可。

### 例子 2：中等例子

最小 0.2 无密钥烟测已写入 `03-Projects/46-AI Agent工程/local-acceptance/autogen02_smoke.py`。它不发起模型调用，但真实验证导入、Agent 构造、caller/executor 双注册、工具执行与终止谓词：

```powershell
python -m venv .venv-autogen02
.\.venv-autogen02\Scripts\python -m pip install -r requirements-autogen02.txt
.\.venv-autogen02\Scripts\python autogen02_smoke.py
```

预期输出：`AutoGen 0.2 smoke test passed without an API call.`。真实 `initiate_chat` 集成仍需用户自己的模型配置和密钥，因此与无密钥烟测分开。

### 例子 3：实际应用例子（可运行 Python，无 API）

```python
# 输入：工具名与参数；输出：注册表执行结果；模拟框架边界。
from collections.abc import Callable

TOOLS: dict[str, Callable[..., float]] = {}

def register(name: str, function: Callable[..., float]) -> None:
    if name in TOOLS:
        raise ValueError("工具名重复")
    TOOLS[name] = function

def score(values: list[float]) -> float:
    if not values:
        raise ValueError("values 不能为空")
    return sum(values) / len(values)

register("score", score)
assert TOOLS["score"]([4.0, 2.0]) == 3.0
try:
    register("score", score)
except ValueError as error:
    print(type(error).__name__, str(error))
```

## 8. 常见误区和易混概念

- **误区**：`pyautogen`、`autogen-agentchat 0.2` 与当前稳定版教程可以随意混装。必须隔离环境并锁定。
- **误区**：让模型输出 `TERMINATE` 就不会死循环。还需要硬轮数/超时上限。

| 概念 | 0.2 教学线 | 当前稳定线 | 是否混用 |
| :--- | :--- | :--- | :---: |
| Agent 导入 | `from autogen import ...` | `autogen_agentchat.agents` | 否 |
| 工具注册 | caller/executor 双注册 | Workbench/AgentChat 新接口 | 否 |
| 迁移策略 | 完成官方旧 Lab | 新项目单独建环境 | 分仓或分虚拟环境 |

## 9. 相关知识点与 Obsidian 双链建议

- 上游：[[AI-Agent-工具调用与结构化契约]]。
- 下游：[[AI-Agent-多智能体协作与消息协议]]、[[AI-Agent-规划状态与工作流编排]]。
- 作业：[[Berkeley-Lab01-Restaurant-Review-Pipeline-知识点映射]]。

## 10. 闭卷复现任务

- [ ] 说出识别 0.2 项目的三条证据。
- [ ] 写出虚拟环境与安装命令。
- [ ] 解释 caller/executor 双注册。
- [ ] 同时设置软终止与硬上限。
- [ ] 用 fake model 跑通业务纯函数测试。
- [ ] 解释 `~=0.2` 为何不能锁在 0.2.x。
- [ ] 核验实际安装版本为 0.2.40 或 starter 指定版本。
- [ ] 运行无密钥双注册烟测。
- [ ] 区分烟测与真实模型集成测试。
- [ ] 说明升级到稳定新 API 时为何要另建环境。

## 11. 自测题：5 道

1. `register_for_llm` 给谁什么信息？ `#自测题/基础`
2. 为什么 executor 可以设置 `llm_config=False`？ `#自测题/基础`
3. 只有 `TERMINATE` 文本有哪些风险？ `#自测题/中等`
4. 如何避免旧 Lab 与新项目依赖冲突？ `#自测题/中等`
5. 设计一个不用真实模型也能验证餐厅评分管线的测试层次。 `#自测题/较难`

> [!question]- 参考答案与评分点
> 1. 给调用者工具 schema。2. 执行者只运行白名单函数，无需模型。3. 模型可能漏写或工具循环，应设轮数/超时。4. 独立虚拟环境并保存锁文件。5. 纯函数→工具注册表→消息/状态→真实模型逐层集成。

## 12. 我的主动回忆区

- **版本识别证据**：
- **最小接线图**：
- **终止测试**：
- [ ] 明天  [ ] 3 天后  [ ] 7 天后  [ ] 14 天后

## 13. 给 Obsidian 的归档建议

- 本卡只服务官方 Fall 2024 兼容线；新项目应查当前官方稳定文档，不把旧 API 当长期最佳实践。
- starter code 若给出不同依赖，以 starter 为准并在作业报告记录差异。

## 🃏 Anki 卡片

Q: AutoGen 0.2 工具为什么要分别注册给 caller 与 executor？
A: caller 需要 schema 来提出调用，executor 需要函数对象来真正执行，权限与决策分离。

Q: Agent 终止为何需要双保险？
A: 模型终止文本可能失败，所以还需最大轮数、超时或预算等硬上限。
