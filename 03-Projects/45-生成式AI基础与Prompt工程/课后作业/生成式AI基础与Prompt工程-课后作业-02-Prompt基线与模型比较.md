---
type: project
topic: "Prompt基线与模型比较"
project_type: homework
course: "生成式AI基础与Prompt工程"
assignment_id: "生成式AI基础与Prompt工程-02"
assignment_level: lesson
assignment_format: lab
stage_id: "03"
requires: ["[[Prompt工程-需求-任务规格与结构化输出]]", "[[Prompt评测-实验-指标数据集与误差分析]]", "[[Prompt工程-上下文学习-示例选择与提示敏感性]]"]
source_type: local_integration_task
created: 2026-08-05
status: planned
flow: project
tags: [作业, 45-生成式AI基础与Prompt工程, Prompt]
source: "Stanford CS324 Winter 2023 Intro Assignment public reference"
source_url: "https://stanford-cs324.github.io/winter2023/assignment/"
accessed: 2026-08-09
license: "[待验证]（本地任务原创；公开课程页仅作能力目标参考）"
---

# 作业 02：Prompt 基线与模型比较

> 使用 [CS324 Intro Assignment](https://stanford-cs324.github.io/winter2023/assignment/) 作为导航，仅链接原作业；本库不复制题面或答案。

## 可执行任务包

- 固定任务：40 条英文情感分类，`dev/test` 各 20 条且标签平衡、文本互斥。
- 文件：`scripts/course_lab.py`、`tests/test_course_lab.py`。
- 离线入口：`python scripts/course_lab.py 02 --adapter rule --output artifacts/assignment02-offline.json`。
- 真实模型入口：`python scripts/course_lab.py 02 --adapter openai --model "模型ID" --output artifacts/assignment02-模型ID.json`。
- `rule` 只验证 adapter、JSON schema、切分和评分协议；其准确率不得写成 LLM 能力结论。比较两个真实模型时分别运行两次，保持数据、Prompt、temperature=0 和 parser 完全相同。

| 子任务 | 对应笔记 | 输出 |
| :--- | :--- | :--- |
| 定义任务和 40 条固定样本 | [[Prompt工程-需求-任务规格与结构化输出]] | starter 内数据、标签与成功标准 |
| Zero/One/Few-shot | [[Prompt工程-上下文学习-示例选择与提示敏感性]] | 三组固定 Prompt |
| 比较基础模型与指令模型 | [[模型适配-对齐-SFT-RLHF与DPO]] | 同数据、同解码参数结果 |
| 报告准确率、失败和成本 | [[Prompt评测-实验-指标数据集与误差分析]] | 结果表与错误样本 |

## 学习目标

- 为 40 条固定分类样本写出标签定义、输入边界和严格 JSON 输出契约。
- 在同一模型与配置上建立 zero-shot 基线，再比较一个最小充分的 few-shot 方案。
- 比较两个真实模型时保持数据、Prompt、temperature 和 parser 不变，并保存模型标识与逐样本原始输出。

## 任务边界

`rule` adapter 只验证数据切分、schema、解析和报告协议，其准确率不是 LLM 证据。不得查看或修改 test 标签来优化 Prompt；没有 API Key 时可以完成离线 Gate，但不能声称完成真实模型比较。

## 提交产物

1. 离线协议报告和至少一份真实模型报告；无法运行真实模型时明确标记未验证。
2. Prompt 文本及 SHA-256、模型 ID、解码参数和逐样本 raw output。
3. dev/test 指标、非法输出率、成本/延迟记录和错误分类表。

## 验收标准

运行 `python scripts/course_lab.py 02 --adapter rule --output artifacts/assignment02-offline.json` 返回 0；dev/test 各 20 条且 ID 不重叠；所有输出经同一 parser；模型比较没有混杂变量；结论只覆盖实际运行的模型与数据。

## 引导自检

- [ ] 是否先固定任务规格，再写 Prompt？
- [ ] 是否把单个成功样例误写成总体提升？
- [ ] 若 dev 提升但 test 不提升，是否记录过拟合而不是继续改 test？
- [ ] 是否明确区分 rule fixture、真实模型和人工判断三类证据？

## 最小知识点集
- [ ] Prompt 规格、ICL、解码固定、数据隔离

## 全面知识点
- [ ] 示例顺序敏感性、置信区间、模型能力边界

## 验收

1. 在项目根目录运行 `python -m unittest discover -s tests -v`，固定数据、schema、切分和 RAG 回归测试必须全绿。
2. 不允许边看测试集边改 Prompt；只用 dev 选择 Prompt，测试集只做最后比较。
3. 每条输出必须是 `{"label":"positive|negative"}`；非法 JSON/越界标签计入 `invalid_rate`，不能静默修复。
4. 报告至少包含 accuracy、invalid rate、耗时、模型 ID、Prompt 原文和全部逐样本 raw output。
5. 两个模型若服务、解码或 Prompt 不同，比较无效；必须重新跑受控配置。

## 行为量规与失败反馈

| 维度 | 0 分 | 1 分 | 2 分 |
| :--- | :--- | :--- | :--- |
| 数据隔离 | 测试集调参 | 有切分但记录不全 | dev/test 固定、互斥、版本可查 |
| 输出契约 | 人工修答案 | 记录部分非法输出 | parser 失败关闭并报告 invalid rate |
| 模型对照 | 多变量同时变化 | 配置大体相同 | 仅模型 ID 变化且原始输出齐全 |
| 误差分析 | 只报均值 | 罗列样本 | 至少按否定范围/词汇/格式分组并提出回归样本 |

总分至少 7/8。`invalid_rate>0` 先修 schema；dev 提升而 test 下降先查过拟合；两个模型结果完全相同先核对 adapter/model ID 是否实际切换。
