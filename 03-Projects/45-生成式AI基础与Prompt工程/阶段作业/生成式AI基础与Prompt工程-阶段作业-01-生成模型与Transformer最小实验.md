---
type: project
topic: "生成模型与Transformer实验"
project_type: homework
course: "生成式AI基础与Prompt工程"
assignment_id: "生成式AI基础与Prompt工程-01"
assignment_level: stage
assignment_format: lab
stage_id: "01"
requires: ["[[生成式AI-模型家族-VAE-GAN与扩散模型]]", "[[Transformer与大语言模型-架构-Transformer工作原理]]", "[[Transformer与大语言模型-训练-GPT与自回归语言模型]]", "[[生成控制-解码-温度Top-k与Top-p]]"]
source_type: local_integration_task
created: 2026-08-05
status: planned
flow: project
tags: [作业, 45-生成式AI基础与Prompt工程, Transformer]
source: "MIT OCW 6.7960 Fall 2024 Homework; Stanford CS336 Spring 2025 Assignment 1 (MIT License repositories)"
source_url: "https://ocw.mit.edu/courses/6-7960-deep-learning-fall-2024/"
accessed: 2026-08-09
license: "本地原创小规模实验；MIT OCW 来源为 CC BY-NC-SA 4.0，CS336 A1 仓库为 MIT License"
---

# 作业 01：生成模型与 Transformer 可解释实验

> 从 [MIT 6.7960 Homework](https://ocw.mit.edu/courses/6-7960-deep-learning-fall-2024/lists/homework/) 和 [CS336 A1](https://github.com/stanford-cs336/assignment1-basics) 进入官方材料。本作业只选小规模、CPU 可调试部分，不发布官方答案。

| 模块 | 知识点 | 对应笔记 | 验收 |
| :--- | :--- | :--- | :--- |
| 模型家族辨析 | VAE/GAN/扩散/自回归 | [[生成式AI-模型家族-VAE-GAN与扩散模型]] | 流程图与比较表 |
| Tokenizer 小实验 | Unicode、切分、词表 | [[生成式AI-基础-概率生成Token与能力边界]] | 往返编码测试 |
| Attention 手算 | Q/K/V、softmax、Mask | [[Transformer与大语言模型-架构-Transformer工作原理]] | 与程序结果一致 |
| 最小 LM | 交叉熵、训练/验证 | [[Transformer与大语言模型-训练-GPT与自回归语言模型]] | 过拟合小数据后验证 |
| 采样 | 温度、top-k/top-p | [[生成控制-解码-温度Top-k与Top-p]] | 固定种子对照表 |

## 完成本作业的最小知识点集
- [ ] 线性代数形状、softmax、交叉熵、梯度下降
- [ ] Python/PyTorch 基础与单元测试

## 学习目标

- 画出自回归生成循环并标出 tokenizer、因果 mask、logits、概率和解码位置。
- 用小矩阵手算一次 masked attention，程序结果与手算误差小于 $10^{-6}$。
- 在固定 logits 上比较 greedy、temperature 和 top-k 的输出差异，并解释变量边界。
- 区分 VAE/GAN/扩散/自回归的训练对象与采样过程，不把名称比较当实现证据。

## 任务边界

本作业是 CPU 可运行的解释性实验，不要求训练大模型，也不替代 MIT/CS336 官方作业。若选择 PyTorch 扩展，必须单独记录依赖、硬件、删减和未复现部分。

## 提交产物

1. `artifacts/assignment01-offline.json` 与运行日志。
2. 一张生成循环图和一张生成模型家族比较表。
3. attention 手算、因果 mask 和程序对照。
4. 固定种子的三种解码结果、参数与解释。

## 验收标准

运行 `python scripts/course_lab.py 01 --output artifacts/assignment01-offline.json` 返回 0；mask 后未来位置权重为 0；概率归一化；相同 seed 与配置复现；报告明确离线微型实验不等于官方规模结果。

## 引导自检

- [ ] Q/K/V 的形状、缩放因子和 softmax 轴是否写清？
- [ ] 是否区分模型分布变化与解码策略变化？
- [ ] 结果不一致时是否先检查 mask、shape 和 seed，而非直接改答案？
- [ ] 是否写出至少一个本实验无法支持的结论？

## 全面知识点
- [ ] RoPE、RMSNorm、SwiGLU、AdamW、梯度裁剪、资源核算

## 验收
- 先在 CPU 上通过单元测试；报告形状、loss 曲线、采样参数和失败样本。

