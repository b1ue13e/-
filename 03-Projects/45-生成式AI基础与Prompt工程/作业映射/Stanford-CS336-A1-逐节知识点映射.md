---
type: project
topic: "Stanford CS336 Spring 2025 Assignment 1 逐节知识点映射"
created: 2026-08-05
status: active
progress: 0%
tags: [项目, 45-生成式AI基础与Prompt工程, Stanford-CS336, Assignment1]
flow: project
kind: moc
source: "Stanford CS336 Spring 2025 assignment1-basics repository, MIT License"
---

# Stanford CS336 A1 逐节知识点映射

> [!info] [官方仓库与 handout](https://github.com/stanford-cs336/assignment1-basics) 采用 MIT License。以下按 handout 的 Section 与 Problem ID 导航；不提供实现答案。官方完整作业面向有系统/ML 基础的学习者，本课小白只要求 CPU 微型变体。

| Section | 官方 Problem ID | 作业必需知识 | 对应笔记 | 本课取舍 |
| :--- | :--- | :--- | :--- | :--- |
| §2 Tokenizer | `unicode1`, `unicode2` | code point、UTF-8 bytes、边界字符 | [[Tokenizer工程-Unicode字节与BPE训练]] | 必做概念与可逆测试 |
| §2 | `train_bpe`, `train_bpe_tinystories`, `train_bpe_expts_owt` | pair 计数、确定合并、性能、语料差异 | [[Tokenizer工程-Unicode字节与BPE训练]] | CPU 小语料必做；大语料可选 |
| §2 | `tokenizer`, `tokenizer_experiments` | encode/decode、special token、merge rank、比较 | [[Tokenizer工程-Unicode字节与BPE训练]] | 必做中文/emoji/特殊 token 边界 |
| §3 Transformer | `linear`, `embedding`, `rmsnorm` | 线性层、嵌入、RMSNorm | [[Transformer与大语言模型-架构-Transformer工作原理]]、[[Transformer工程-RMSNorm-SwiGLU-RoPE与资源核算]] | 必做单元测试与均方根检查 |
| §3 | `positionwise_feedforward`, `rope` | SwiGLU/FFN、旋转位置编码 | [[Transformer工程-RMSNorm-SwiGLU-RoPE与资源核算]] | 必做公式、shape 与旋转范数测试 |
| §3 | `softmax`, `scaled_dot_product_attention` | 数值稳定、注意力 | [[课程前置-概率向量与Softmax最小补丁]]、[[Transformer与大语言模型-架构-Transformer工作原理]] | 必做 |
| §3 | `multihead_self_attention`, `transformer_block`, `transformer_lm` | 因果多头、block、LM | [[Transformer与大语言模型-架构-Transformer工作原理]]、[[Transformer与大语言模型-训练-GPT与自回归语言模型]] | 必做核心 |
| §3 | `transformer_accounting` | 参数/激活/优化器状态/FLOPs | [[Transformer工程-RMSNorm-SwiGLU-RoPE与资源核算]] | 必做分项核算 |
| §4 Optimizer | `cross_entropy`, `learning_rate_tuning` | 稳定 CE、学习率 | [[训练优化-交叉熵AdamW调度梯度裁剪与检查点]] | 必做小规模与极大 logits 测试 |
| §4 | `adamw`, `adamw_accounting` | AdamW、偏置修正、状态内存 | [[训练优化-交叉熵AdamW调度梯度裁剪与检查点]] | 必做标量更新；大模型记账进阶 |
| §4 | `learning_rate_schedule`, `gradient_clipping` | warmup/cosine、全局范数裁剪 | [[训练优化-交叉熵AdamW调度梯度裁剪与检查点]] | 必做边界 step 与范数测试 |
| §5 Training | `data_loading`, `checkpointing`, `training_together` | 批采样、保存/恢复、训练循环 | [[深度学习工程-PyTorch张量自动微分与训练循环]]、[[训练优化-交叉熵AdamW调度梯度裁剪与检查点]] | CPU 小数据必做；恢复等价测试 |
| §5 | `decoding`, `generate` | 采样、生成 | [[生成控制-解码-温度Top-k与Top-p]] | 必做 |
| §5 | `experiment_log`, `learning_rate`, `batch_size_experiment` | 日志、受控实验 | [[Prompt评测-实验-指标数据集与误差分析]] | 日志必做；算力实验缩小 |
| §5 Ablations | `layer_norm_ablation`, `pre_norm_ablation`, `no_pos_emb`, `swiglu_ablation` | 消融与架构因果 | [[Prompt评测-实验-指标数据集与误差分析]] | 选 2 个 CPU 小实验 |
| §5 Scaling | `main_experiment`, `leaderboard` | OWT 训练、规模与资源 | [[Transformer与大语言模型-训练-GPT与自回归语言模型]] | 阅读/可选，不作为小白 Gate |

## 环境与验收

1. 克隆官方仓库后用其 `uv` 配置；先运行 `uv run pytest` 观察预期未实现失败。
2. 通过 `tests/adapters.py` 连接自己的实现，按 Problem ID 逐组测试。
3. 本课默认 CPU 与小语料，不宣称复现 B200 小时实验；报告删减项、原因与替代证据。
4. 保留官方 LICENSE 与归属；自己的改动单独记录。

## 补救分支

- `unicode*` 或 round-trip 失败：先在 [[Tokenizer工程-Unicode字节与BPE训练]] 的 byte 级参考实现复现，再检查 normalization、special token 与 merge 顺序。
- `adamw` 或调度失败：先手算一次标量更新和边界 step，不在完整 LM 中猜超参数。
- `training_together` 失败：按“单 batch 过拟合 → 梯度有限 → 参数变化 → checkpoint 恢复”等四个 Gate 定位。
