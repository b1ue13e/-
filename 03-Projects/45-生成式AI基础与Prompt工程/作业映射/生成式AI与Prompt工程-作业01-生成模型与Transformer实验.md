---
type: project
topic: "生成模型与Transformer实验"
created: 2026-08-05
status: active
progress: 0%
flow: project
kind: problem-type
tags: [项目, 45-生成式AI基础与Prompt工程, 作业映射, Transformer]
source: "MIT OCW 6.7960 Fall 2024 Homework; Stanford CS336 Spring 2025 Assignment 1 (MIT License repositories)"
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

## 全面知识点
- [ ] RoPE、RMSNorm、SwiGLU、AdamW、梯度裁剪、资源核算

## 验收
- 先在 CPU 上通过单元测试；报告形状、loss 曲线、采样参数和失败样本。

