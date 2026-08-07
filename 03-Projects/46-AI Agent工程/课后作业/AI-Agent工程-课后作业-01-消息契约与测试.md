---
type: project
project_type: homework
topic: "消息契约与测试"
course: "AI Agent工程"
assignment_id: "AI-Agent工程-L01"
assignment_level: lesson
assignment_format: lab
stage_id: "00"
requires: ["[[AI-Agent-前置-消息JSON异常与单元测试]]"]
source_type: local_integration_task
source: "课程原创任务；参考 Python unittest/json 官方文档与 Berkeley F24 Lab 的工程前置目标"
source_url: "https://docs.python.org/3/library/unittest.html"
accessed: 2026-08-06
license: "任务文本原创；Python文档按PSF许可；不复制Berkeley starter"
created: 2026-08-06
status: planned
flow: project
tags: [作业, 46-AI Agent工程, 消息, 测试]
---

# AI Agent 工程课后作业 01：消息契约与测试

## 学习目标

实现一个不依赖模型 API 的消息解析边界，证明正常输入、缺字段、类型错误和非法 JSON 都有确定结果。

## 任务背景与边界

输入是 UTF-8 JSON 字符串，目标结构包含 `role`、`content`、`request_id`。只允许 `system/user/tool/assistant` 角色；不得用 `eval`，不得把解析失败吞成空字符串。

## 详细题目

1. **题 1 · 契约**：写出输入、成功返回与至少四类错误返回的 schema；说明错误码与异常的关系。
2. **题 2 · 实现**：实现 `parse_message(raw: str) -> dict`，验证必需字段、类型、角色枚举和非空 `request_id`。
3. **题 3 · 测试**：为正常、空字符串、畸形 JSON、缺字段、错误类型、未知角色各写测试。
4. **题 4 · 测试替身**：写一个根据 `request_id` 返回预制决策的 fake model，证明测试无网络也可复现。

## 环境与复现

- Python 3.11+，仅使用标准库；固定 UTF-8。
- 建议目录：`src/message_contract.py`、`tests/test_message_contract.py`。
- 运行：`python -m unittest -v`；预计小于 1 秒，无 GPU、无密钥。

## 提交产物

- `src/message_contract.py`
- `tests/test_message_contract.py`
- `README.md`：契约、命令、实际输出和一条失败复盘

## 验收标准与 Rubric

| 维度 | 分值 | 标准 |
| :--- | ---: | :--- |
| 契约正确 | 35 | 字段、类型、枚举和失败语义完整 |
| 测试覆盖 | 35 | 六类测试独立断言错误类别 |
| 可复现 | 20 | 无网络全绿，命令与版本齐全 |
| 解释质量 | 10 | 能说明为何不能静默修复畸形输入 |

总分 ≥85；任一畸形输入被当成成功则不通过。

## 引导、自检与后续

- 先写测试再实现；不要只断言“抛异常”，同时断言错误类别。
- 常见失败：把 `None` 转成字符串、捕获所有异常、不同错误返回同一模糊文本。
- 完成后进入 [[🧭 阶段1-Agent基础与受限循环]]。

