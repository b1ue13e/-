---
title: "机器学习 4-Tier 阶梯作业全景规范说明书"
type: project
topic: "机器学习 4-Tier 阶梯作业规范"
course: "机器学习"
created: 2026-08-02
updated: 2026-08-02
status: active
flow: project
kind: moc
tags: [机器学习, 4Tier作业, 阶梯作业, 编程实战, PyTest]
---

# 🤖 机器学习 4-Tier 阶梯作业全景规范说明书 (李宏毅 ML2021 范式)

> 本说明书为 **17-机器学习** 路径下 HW01 ~ HW15 阶梯作业提供严格的 **4-Tier Baseline** 划分标准与测试校验 Harness 规范。

---

## 🧭 4-Tier Baseline 梯队划分原则

```
🟢 L1 - Simple Baseline   │ API/模型调用 / 跑通 Sample Pipeline / 基础手算
🟡 L2 - Medium Baseline   │ 特征选择 / 调参 / 验证集交叉验证 / 正则化
🔴 L3 - Strong Baseline   │ [核心] 不调库，从零手撕核心模型 (手撕 Gradient Boosting / Transformer / GAN / BERT)
👑 L4 - Boss Baseline     │ Kaggle/Top 竞赛冲榜 / 极致模型压缩 / 蒸馏 / 形式化收敛证明
```

---

## 🎯 HW01 ~ HW15 机器学习阶梯作业 4-Tier 细化规格

### 1. HW01 - COVID-19 阳性率回归预测 (Regression)
- 🟢 **L1**: 使用 PyTorch/scikit-learn 线性回归模型跑通训练与测试流程。
- 🟡 **L2**: 加入 L1/L2 正则化 (Ridge/Lasso) 与 5-Fold Cross Validation。
- 🔴 **L3 (手撕核心)**：**从零手撕带 Momentum 与 Adam 优化器的多项式回归模型**（仅允许使用 NumPy）。
- 👑 **L4**: Kaggle 冲榜，实现特征工程与自动搜索最佳超参数。

### 2. HW02 - 音帧分类 (Classification & Phoneme Recognition)
- 🟢 **L1**: 使用多层感知机 (MLP) 对 MFCC 音频特征进行多分类。
- 🟡 **L2**: 引入 Dropout、Batch Normalization 与 Kaiming 初始化。
- 🔴 **L3 (手撕核心)**：**从零手撕 MLP 前向传播与反向传播 (Backpropagation) 矩阵梯度推导**。
- 👑 **L4**: 结合 Conformer / CTC 损失函数实现时序音频分类。

### 3. HW03 - 图像分类 (CNN & Data Augmentation)
- 🟢 **L1**: 使用 torchvision 标准 ResNet-18 跑通图像分类。
- 🟡 **L2**: 数据增强 (CutMix/Mixup) 与 Cosine Annealing 学习率调度。
- 🔴 **L3 (手撕核心)**：**从零手撕卷积 (Conv2d) 与 Max Pooling 算子**（基于 NumPy im2col 实现）。
- 👑 **L4**: 模型轻量化剪枝与量化 (Quantization & Pruning)。

### 4. HW04 - 说话人识别 (Self-Attention & Transformer Encoder)
- 🟢 **L1**: 调用 HuggingFace / PyTorch `nn.TransformerEncoder` 进行说话人分类。
- 🟡 **L2**: 加入 Positional Encoding 与 Multi-Head Attention 调参。
- 🔴 **L3 (手撕核心)**：**从零手撕 Multi-Head Self-Attention 核心矩阵计算**：
  $$ \text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V $$
- 👑 **L4**: 实现 Linear Attention / FlashAttention 降低二次复杂度。

### 5. HW05 - 机器翻译 (Transformer Seq2Seq & Beam Search)
- 🟢 **L1**: 使用 Seq2Seq Encoder-Decoder 结构完成英中翻译。
- 🟡 **L2**: 使用 Greedy Search 与 Teacher Forcing 衰减训练。
- 🔴 **L3 (手撕核心)**：**手撕 Beam Search 解码器算法与 BLEU 指标评估器**。
- 👑 **L4**: 实现 Non-Autoregressive Transformer 并行解码。

### 6. HW06 - 动漫头像生成 (GAN & StyleGAN)
- 🟢 **L1**: 使用 DCGAN 跑通生成器与判别器交叉训练。
- 🟡 **L2**: 引入 WGAN-GP (Wasserstein GAN with Gradient Penalty) 解决梯度消失。
- 🔴 **L3 (手撕核心)**：**手写判别器梯度惩罚 (Gradient Penalty) 损失推导与计算**。
- 👑 **L4**: 实现 StyleGAN2 结构与 FID (Fréchet Inception Distance) 评估。

### 7. HW07 - 问答系统 (BERT & Question Answering)
- 🟢 **L1**: 微调 `bert-base-chinese` 完成抽取式问答。
- 🟡 **L2**: 动态掩码 (Dynamic Masking) 与 Sliding Window 处理长文本。
- 🔴 **L3 (手撕核心)**：**手写 BERT Token / Segment / Position Embedding 融合与 Masked LM 损失计算**。
- 👑 **L4**: 模型蒸馏 (DistilBERT / TinyBERT)。

### 8. HW08 - 异常检测与自编码器 (Autoencoder & Anomaly Detection)
- 🟢 **L1**: 使用 Simple Autoencoder 跑通重构误差计算。
- 🟡 **L2**: 使用 VAE (Variational Autoencoder) 与 KL 散度约束。
- 🔴 **L3 (手撕核心)**：**手写 VAE 重构损失与 KL 散度损失推导**（Reparameterization Trick）。
- 👑 **L4**: 结合 Normalizing Flows 估算精确概率密度。

### 9. HW09 - 模型可解释性 (Explainable AI / Saliency Maps)
- 🟢 **L1**: 生成 Saliency Maps 凸显输入特征贡献。
- 🟡 **L2**: 实现 Integrated Gradients 与 SmoothGrad 消除噪声。
- 🔴 **L3 (手撕核心)**：**手撕 Lime / Grad-CAM 图像特征映射归因算法**。
- 👑 **L4**: 对比 Transformer 中的 Attention Weight 与 Integrated Gradients 的一致性。

### 10. HW10 - 对抗攻击 (Adversarial Attack & Defense)
- 🟢 **L1**: 使用 FGSM (Fast Gradient Sign Method) 生成对抗样本。
- 🟡 **L2**: 实现 PGD (Projected Gradient Descent) 多步强攻击。
- 🔴 **L3 (手撕核心)**：**手撕 PGD 约束投影算法**（控制 $L_\infty$ 范数在 $\epsilon$ 范围内）。
- 👑 **L4**: 对抗训练 (Adversarial Training) 提升模型鲁棒性。

### 11. HW11 - 域适应与迁移学习 (Domain Adaptation)
- 🟢 **L1**: 基于 DANN (Domain-Adversarial Neural Network) 迁移。
- 🟡 **L2**: 加入 Gradient Reversal Layer (GRL) 对抗训练。
- 🔴 **L3 (手撕核心)**：**手写 GRL 前向为 Identity、反向乘以 $-\lambda$ 的自定义 PyTorch Autograd 算子**。
- 👑 **L4**: 实现 Optimal Transport / MMD (Maximum Mean Discrepancy) 域匹配。

### 12. HW12 - 强化学习 (Policy Gradient & Actor-Critic)
- 🟢 **L1**: 在 CartPole 环境使用 Policy Gradient (REINFORCE) 跑通。
- 🟡 **L2**: 加入 Baseline 扣除期望以降低方差。
- 🔴 **L3 (手撕核心)**：**手撕 Actor-Critic (A2C) 优势函数评估与策略梯度推导**。
- 👑 **L4**: 实现 PPO (Proximal Policy Optimization) 截断目标函数。

### 13. HW13 - 终身学习与持续学习 (Continual Learning)
- 🟢 **L1**: 在 Split-MNIST 上观察灾难性遗忘 (Catastrophic Forgetting)。
- 🟡 **L2**: 使用 EWC (Elastic Weight Consolidation) 保护重要权重。
- 🔴 **L3 (手撕核心)**：**手写 Fisher 信息矩阵 (Fisher Information Matrix) 估计器**。
- 👑 **L4**: 实现 Replay-Buffer 与 Memory Vector 联合方法。

### 14. HW14 - 压缩与量化 (Model Compression & Pruning)
- 🟢 **L1**: 使用 Weight Magnitude Pruning 剪枝 30% 参数。
- 🟡 **L2**: 实现 Knowledge Distillation (蒸馏) 训练小模型。
- 🔴 **L3 (手撕核心)**：**手写 8-bit 量化 (Int8 Quantization) scale/zero_point 映射算子**。
- 👑 **L4**: 实现 QAT (Quantization-Aware Training) 虚假量化节点。

### 15. HW15 - 结构化预测与 CRF (Structured Prediction & CRF)
- 🟢 **L1**: 使用 BiLSTM 进行命名实体识别 (NER)。
- 🟡 **L2**: 引入 Conditional Random Field (CRF) 标签转移矩阵。
- 🔴 **L3 (手撕核心)**：**手撕 Viterbi 解码算法求最优标签路径**。
- 👑 **L4**: 结构化 SVM / Margin-based 损失函数导出。

---

## 🧪 测试校验 Harness 规范 (`pytest`)

在 `03-Projects/projects-ml/tests/` 目录下运行单元测试：

```bash
pytest 03-Projects/projects-ml/tests/test_hw01_regression.py
pytest 03-Projects/projects-ml/tests/test_hw04_attention.py
pytest 03-Projects/projects-ml/tests/test_hw07_bert.py
```
