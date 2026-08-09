---
type: project
topic: "环境与数学诊断"
project_type: homework
course: "生成式AI基础与Prompt工程"
assignment_id: "生成式AI基础与Prompt工程-00"
assignment_level: lesson
assignment_format: problem-set
stage_id: "00"
requires: ["[[课程前置-Python-JSON测试与实验复现]]", "[[课程前置-概率向量与Softmax最小补丁]]"]
source_type: local_integration_task
created: 2026-08-05
status: planned
flow: project
tags: [作业, 45-生成式AI基础与Prompt工程, 前置诊断]
source: "Original diagnostic aligned with MIT 6.7960 and Stanford CS336 prerequisites"
source_url: "https://cs336.stanford.edu/spring2025/"
accessed: 2026-08-09
license: "本地原创作业；仅引用公开课程的先修能力描述"
---

# 作业 00：环境与数学诊断

| 题目 | 考查知识点 | 对应笔记 | 通过条件 |
| :--- | :--- | :--- | :--- |
| 手算 softmax | 指数归一化 | [[生成式AI-基础-概率生成Token与能力边界]] | 误差小于 $10^{-3}$ |
| 三 Token 概率 | 链式法则 | [[Transformer与大语言模型-训练-GPT与自回归语言模型]] | 写出全部条件项 |
| 固定随机实验 | 随机种子与复现 | [[Prompt评测-实验-指标数据集与误差分析]] | 两次结果相同 |
| JSON 校验 | 数据类型与异常 | [[Prompt工程-需求-任务规格与结构化输出]] | 正常/缺字段均有测试 |

## 最小知识点集
- [ ] Python 函数、列表、字典、异常处理
- [ ] 概率、对数、均值和标准差
- [ ] 训练/验证/测试集的区别

## 验收
- 一份可运行脚本、4 个断言、README 中记录 Python 版本与运行命令。

## 学习目标

- 独立运行 Python 命令并把版本、退出码和输出保存为证据。
- 实现数值稳定的 softmax、条件概率连乘和严格 JSON 字段校验。
- 证明固定随机种子能复现实验，同时说明“固定种子”不等于结果正确。

## 任务边界

只使用 Python 标准库，不调用在线模型，不安装深度学习框架。非法 JSON、概率和不完整字段必须明确失败，不能静默补默认值。离线 Gate 只证明前置工具链可运行。

## 提交产物

1. `artifacts/assignment00-offline.json`。
2. 运行命令、Python 版本与测试退出码。
3. softmax 手算、程序结果和误差对照。
4. 一条故意构造的失败输入及其错误信息。

## 验收标准

运行 `python scripts/course_lab.py 00 --output artifacts/assignment00-offline.json` 返回 0；全部断言通过；概率和为 1；两次同种子输出一致；缺字段与错误类型均失败关闭。

## 引导自检

- [ ] 是否先减去最大 logit，避免指数溢出？
- [ ] 是否把随机性、环境和输入同时记录，而不是只写一个 seed？
- [ ] JSON 解析失败时是否停止流程，而不是把原始文本当成功输出？
- [ ] 能否在不看笔记时解释每个断言对应的风险？

