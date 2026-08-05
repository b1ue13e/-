---
type: project
topic: "MIT 6.7960 Homework 3 逐节知识点映射"
created: 2026-08-05
status: active
progress: 0%
tags: [项目, 45-生成式AI基础与Prompt工程, MIT-OCW, HW03, Transformer]
flow: project
kind: moc
source: "MIT OCW 6.7960 Deep Learning Fall 2024 Homework 3, CC BY-NC-SA 4.0"
---

# MIT 6.7960 Homework 3 逐节知识点映射

> [!info] [打开官方 HW3 PDF](https://ocw.mit.edu/courses/6-7960-deep-learning-fall-2024/mit6_7960_f24_hw3.pdf)。这是 45 课程模型基础的核心官方作业；按 Problem/子问导航，不提供实现答案。

| 官方部分 | 子问 | 作业必需知识 | 对应笔记 | 验收焦点 |
| :--- | :--- | :--- | :--- | :--- |
| Problem 1 RNN vs Transformer | a–d | 递归展开、长依赖、梯度/路径 | [[Transformer与大语言模型-架构-Transformer工作原理]] | 能比较串行递归与全局注意 |
| Problem 1 | e | 训练/推理复杂度与并行性 | 同上 | 变量、序列长度、维度写清 |
| Problem 1 | f | 长序列部署取舍 | [[生成控制-解码-温度Top-k与Top-p]] | 给出成本—能力理由 |
| Problem 2 Transformer | a | 单头注意、mask | [[Transformer与大语言模型-架构-Transformer工作原理]] | mask 后禁用权重为 0 |
| Problem 2 | b | 多头拼接与投影 | 同上 | 所有张量形状一致 |
| Problem 2 | c | FFN、残差、完整 block | 同上 | 模块组合与测试通过 |
| Problem 2 | d | 连续模态 tokenization | [[生成式AI-多模态-条件生成与基础模型]] | 音频/图像切分方案与限制 |
| Problem 3 ViT | a | patch embedding | [[生成式AI-多模态-条件生成与基础模型]] | patch 数与维度正确 |
| Problem 3 | b | 位置/类别嵌入 | [[Transformer与大语言模型-架构-Transformer工作原理]] | 解释长度限制 |
| Problem 3 | c | 训练 ViT | [[Prompt评测-实验-指标数据集与误差分析]] | 环境、曲线、指标可复现 |
| Problem 3 | d–e | 注意力图与 CNN 比较 | [[生成式AI-多模态-条件生成与基础模型]] | 可视化不等同因果解释 |
| Problem 4 DialogueGPT | a | tokenizer、special token | [[生成式AI-基础-概率生成Token与能力边界]] | encode/decode 测试 |
| Problem 4 | b | padding 与 input mask | [[Transformer与大语言模型-架构-Transformer工作原理]] | pad 不参与损失/注意 |
| Problem 4 | c | causal LM 与位置嵌入 | [[Transformer与大语言模型-训练-GPT与自回归语言模型]] | 因果 mask 无未来泄漏 |
| Problem 4 | d | next-token cross-entropy | [[生成式AI-基础-概率生成Token与能力边界]] | 标签移位与 pad 忽略 |
| Problem 4 | e | 自回归生成成本 | [[生成控制-解码-温度Top-k与Top-p]] | 解释训练并行/生成串行 |
| Problem 4 | f | 训练语言模型 | [[课程前置-Python-JSON测试与实验复现]] | 保存配置、曲线、checkpoint |
| Problem 4 | g | 生成、top-p、KV cache | [[生成控制-解码-温度Top-k与Top-p]] | 比较策略并记录失败 |

## 最小完成顺序

1. 先通过 [[课程前置-概率向量与Softmax最小补丁]] 自测。
2. 按 Problem 2a→2b→2c 做单元测试，再进入 Problem 4。
3. Problem 4 先测试 tokenizer/mask/loss，再训练；不得用最终生成文本代替组件测试。

