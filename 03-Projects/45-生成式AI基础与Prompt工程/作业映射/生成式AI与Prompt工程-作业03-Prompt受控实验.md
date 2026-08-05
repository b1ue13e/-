---
type: project
topic: "Prompt受控实验"
created: 2026-08-05
status: active
progress: 0%
flow: project
kind: problem-type
tags: [项目, 45-生成式AI基础与Prompt工程, 作业映射, 实验]
source: "Stanford CS324 Project 1: Evaluating Large Language Models public reference"
---

# 作业 03：Prompt 工程受控实验

> 参考 [CS324 Project 1](https://stanford-cs324.github.io/winter2022/projects/CS324_P1.pdf) 的评测交付结构，只链接公开 PDF。

## 可执行任务包

在 `03-Projects/45-生成式AI基础与Prompt工程/starter/` 运行：

```powershell
python -m unittest -v
python course_lab.py 03 --adapter rule --output assignment03-offline.json
python course_lab.py 03 --adapter openai --model "模型ID" --output assignment03-live.json
```

runner 固定 20 条 test 的 ID 与执行顺序、同一 adapter、同一 parser；baseline/explicit rule 各运行一次，Few-shot 对同一组示例生成 5 个真实不同的排列。报告保存每个 Prompt 的 SHA-256 并写入 `controlled_variable: prompt_text_only`。离线 rule 对示例排列不敏感是夹具断言，不代表真实 LLM 也不敏感。

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
