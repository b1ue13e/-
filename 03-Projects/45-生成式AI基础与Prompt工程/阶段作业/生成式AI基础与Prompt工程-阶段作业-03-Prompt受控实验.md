---
type: project
topic: "Prompt受控实验"
project_type: homework
course: "生成式AI基础与Prompt工程"
assignment_id: "生成式AI基础与Prompt工程-03"
assignment_level: stage
assignment_format: lab
stage_id: "03"
requires: ["[[Prompt工程-需求-任务规格与结构化输出]]", "[[Prompt评测-实验-指标数据集与误差分析]]", "[[Prompt工程-方法-指令示例推理与约束]]", "[[Prompt工程-上下文学习-示例选择与提示敏感性]]"]
source_type: local_integration_task
created: 2026-08-05
status: planned
flow: project
tags: [作业, 45-生成式AI基础与Prompt工程, 实验]
source: "Stanford CS324 Project 1: Evaluating Large Language Models public reference"
source_url: "https://stanford-cs324.github.io/winter2022/assignments/project1.pdf"
accessed: 2026-08-09
license: "[待验证]（本地任务原创；公开课程 PDF 仅作交付结构参考）"
---

# 作业 03：Prompt 工程受控实验

> 参考 [CS324 Project 1](https://stanford-cs324.github.io/winter2022/assignments/project1.pdf) 的评测交付结构，只链接公开 PDF。

## 可执行任务包

在项目根目录运行：

```powershell
python -m unittest discover -s tests -v
python scripts/course_lab.py 03 --adapter rule --output artifacts/assignment03-offline.json
python scripts/course_lab.py 03 --adapter openai --model "模型ID" --output artifacts/assignment03-live.json
```

runner 固定 20 条 test 的 ID 与执行顺序、同一 adapter、同一 parser；baseline/explicit rule 各运行一次，Few-shot 对同一组示例生成 5 个真实不同的排列。报告保存每个 Prompt 的 SHA-256 并写入 `controlled_variable: prompt_text_only`。离线 rule 对示例排列不敏感是夹具断言，不代表真实 LLM 也不敏感。

## 学习目标

- 设计“每次只改一个变量”的 Prompt 实验并提前写出假设、主指标和护栏指标。
- 对同一组 few-shot 示例运行五种不同顺序，报告均值、方差与失败类型。
- 根据逐样本证据做保留、回退或继续实验的决策，而不是只选最高分 Prompt。

## 任务边界

固定数据、adapter、parser、模型和解码参数，唯一改变量为 Prompt 文本。离线 rule 结果只用于协议回归；真实模型实验必须单独保存服务端模型标识和 usage。不得删除失败样本或用 test 集选 Prompt。

## 提交产物

1. baseline、显式规则和五个示例顺序的 JSON 报告。
2. 实验注册表：假设、控制变量、Prompt hash、模型/adapter、seed 和时间。
3. 至少四类错误的逐样本表，以及最终保留/回退结论。
4. 一页限制说明，包括样本量、模型漂移、成本和未验证项。

## 验收标准

运行 `python scripts/course_lab.py 03 --adapter rule --output artifacts/assignment03-offline.json` 返回 0；报告的 `controlled_variable` 为 `prompt_text_only`；五种排列实际不同；test ID 与顺序一致；所有指标可由逐样本结果重算。

## 引导自检

- [ ] 除 Prompt 外是否误改了示例、parser、seed 数量或模型参数？
- [ ] 是否报告方差与最差情况，而非只报均值或最好结果？
- [ ] Prompt hash 是否能对应到原文？
- [ ] 证据不足时是否选择“保持基线/继续实验”，而不是强行宣称提升？

| 对照 | 唯一改变量 | 对应笔记 |
| :--- | :--- | :--- |
| 基线 vs 完整规格 | 需求字段 | [[Prompt工程-需求-任务规格与结构化输出]] |
| Zero-shot vs Few-shot | 示例 | [[Prompt工程-上下文学习-示例选择与提示敏感性]] |
| Direct vs 分解 | 推理流程 | [[Prompt工程-推理-任务分解自一致性与验证]] |
| greedy vs sampling | 解码 | [[生成控制-解码-温度Top-k与Top-p]] |

## 最小知识点集
- [ ] 固定数据、模型、解码和评分规则
- [ ] 每次只改变一个因素
- [ ] 报告均值、方差、失败类型、Token 与延迟

## 验收

- starter Gate：2 个固定对照 + 5 个 Few-shot 示例顺序 × 20 条冻结 test；测试样本顺序不变，全部条件保存 raw output。
- 独立迁移 Gate：将同一协议扩展到自己定义的 50 条冻结样本；不能复制 starter 文本凑数。
- 每个对照只改 Prompt 文本；模型、数据、parser、解码和运行环境固定。
- 对 5 个 seed 报告均值与离散程度，并保留逐样本 ID，不能只截一张汇总图。

## 行为量规与失败反馈

| Gate | 通过证据 | 失败时回退 |
| :--- | :--- | :--- |
| 单变量 | 报告中的 `fixed` 与 `controlled_variable` | 恢复固定配置，删掉混入的模型/温度变化 |
| 可重复 | 5 个 seed 均有记录 | 记录顺序、模型版本与原始输出 |
| 可诊断 | 至少 4 类失败及样本 ID | 先查 raw→parser→label，再改 Prompt |
| 可迁移 | 新任务 50 条冻结样本 | 回到 completion 层，只保留 adapter 接口和测试 |

任何通过改测试标签、删除失败样本或只选择最好 seed 得到的结果均判失败。
