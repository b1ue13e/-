---
type: study
course: "05-计算机视觉"
topic: "DeiT 数据高效图像 Transformer"
created: 2026-08-06
updated: 2026-08-06
status: ongoing
difficulty: advanced
concept: ["DeiT", "知识蒸馏", "Vision Transformer", "数据高效训练"]
prerequisites: ["Transformer与自注意力", "ViT", "数据增强与正则化"]
upstream: ["[[ViT]]", "[[Transformer与自注意力]]", "[[数据增强与正则化]]"]
related: ["知识蒸馏", "SwinTransformer", "MAE"]
flow: knowledge
stage_moc: "[[🚀 第四阶段：前沿架构探索]]"
kind: concept
source: "Touvron et al. 2021, Training data-efficient image transformers & distillation through attention; arXiv:2012.12877"
tags: [学习, 计算机视觉, Transformer, DeiT, 知识蒸馏]
---

# DeiT：数据高效图像 Transformer

## 0. 先判断它值不值得深挖

- **值得**：它是"ViT 在小数据集上怎么训练起来"的官方答案；知识蒸馏 + 数据增强的组合思路在 CV 之外（多模态、推荐）也通用；DeiT 蒸馏 token 的设计是 2021 年后多种蒸馏架构（DeiT-III、DINO 蒸馏）的源头。
- **不值得**：如果你只做大规模预训练（几十亿数据）且不关心数据效率，DeiT 的蒸馏技巧收益有限；纯研究蒸馏算法的可以看更专门的蒸馏卡。

## 1. 这个知识点解决什么问题？

**问题**：ViT 需要 ImageNet-21k（1400 万张）或 JFT-300M 预训练才能在 ImageNet-1k 上超越 CNN（ResNet）。但绝大多数实验室/个人只有 ImageNet-1k（128 万张），直接训练 ViT 会过拟合、收敛慢。

**DeiT 的答案**：只用 ImageNet-1k，通过三个杠杆让 ViT 追平甚至超越 ResNet-50/152：
1. **强数据增强**（RegNet 时代的增强集：RandAugment、Mixup、CutMix、EMA）；
2. **知识蒸馏**（用预训练 CNN 当 teacher）；
3. **蒸馏 token**（`distillation token`），把蒸馏从"输出 logits 对齐"升级为"注意力监督"。

## 2. 为什么它重要？它有什么用？

- **降低 ViT 使用门槛**：从 1400 万张降到 128 万张即可训练，实验成本降低一个数量级。
- **蒸馏 token 是架构创新**：ViT 的 CLS token 只做分类，DeiT 加了 `distill token` 与 CLS token 并行，从 teacher 的注意力中蒸馏——这比纯 logit 蒸馏多了一条监督通道。
- **工业价值**：DeiT-S/Base 是小模型部署的常用 backbone；DeiT-III 的改进（更高 epoch、更强增强）至今仍是数据高效 Transformer 的基线。

## 3. 学它之前需要哪些前置知识？

1. **[[ViT|ViT 架构]]**：patch 化、位置编码、CLS token、Transformer encoder 层——DeiT 的所有改动都叠加在 ViT 上。
2. **[[Transformer与自注意力|自注意力机制]]**：Q/K/V 计算、多头、Softmax 加权——蒸馏 token 与 CLS token 的交互依赖它。
3. **[[数据增强与正则化|数据增强]]**：RandAugment/Mixup/CutMix 是 DeiT 训练配方的一半。

## 4. 用直觉语言解释它

想象一个"学生"（DeiT）和一个"老师"（ResNet-152）：
- 老师已经教了很多年（在 ImageNet 预训练好），知识很扎实。
- 学生不光自己刷题（真实标签），还模仿老师的解题过程（logits 对齐），甚至模仿老师"看题时关注哪里"（注意力图对齐）。
- 为了让学生不光学到答案还学到推理路径，DeiT 在 transformer 里多放了一个特殊的"小抄 token"（distillation token），专门承载"老师关注哪里"的信息。

## 5. 正式定义、核心公式、符号解释

**DeiT 的三个核心组件**：

1. **强数据增强配方**：RandAugment + Mixup + CutMix + EMA（指数移动平均），与 RegNet 训练配方一致。

2. **蒸馏 token（distillation token）**：
   - 输入序列变为 `[CLS, patch₁, ..., patchₙ, DIST]`，`DIST` 与 `CLS` 都是可学习向量，位置编码相同。
   - 前向时 CLS token 产生分类预测，DIST token 产生蒸馏预测（都接分类头）。

3. **蒸馏损失**——两种模式：

   **软蒸馏（soft distillation）**：
   $$
   \mathcal{L} = (1-\lambda)\,\mathcal{L}_{\text{CE}}(\psi(Z_s), y) + \lambda \tau^2 \,\mathcal{L}_{\text{KL}}(\psi(Z_s/\tau), \psi(Z_t/\tau))
   $$
   其中 $Z_s, Z_t$ 是学生/教师 logits，$\tau$ 是温度（默认 3.0），$\lambda$ 是蒸馏权重（默认 0.5），$\psi$ 是 softmax。

   **硬标签蒸馏（hard-label distillation）**：
   $$
   \mathcal{L} = \frac{1}{2}\,\mathcal{L}_{\text{CE}}(\psi(Z_s), y) + \frac{1}{2}\,\mathcal{L}_{\text{CE}}(\psi(Z_s), y_t)
   $$
   其中 $y_t = \arg\max_c\, Z_t^{(c)}$ 是教师预测的硬标签。硬蒸馏比软蒸馏更好（DeiT 实验：81.5% vs 81.4% 且实现更简单，因为不用温度缩放）。

   **关键设计**：CLS token 的损失只用真实标签 $y$（不蒸馏），DIST token 的损失只用教师标签 $y_t$（不真实标签）。两者互补，避免一条 token 被两个目标拉扯。

## 6. 推导思路和思想来源

1. **动机来源**：Touvron et al. 观察到 ViT 在 ImageNet-1k 上"欠训练"——缺归纳偏置，需要更多数据。他们的思路不是加卷积归纳偏置（那是 ConViT/CoAtNet 路线），而是"**给 ViT 一个老师**"，用 CNN 的归纳偏置"教"给 Transformer。
2. **为什么蒸馏 token 比只蒸馏 logits 好**：如果只把教师 logits 加到 CLS token 上，CLS 要同时拟合真实标签和教师分布，两个目标竞争。DeiT 把"学老师"和"学真相"拆成两个 token 并行，各自负责一路，最后分类时两个 token 的预测平均（或相加）——实验显示 DIST token 单独就达到 81.5%，CLS+DIST 平均到 82.0%。
3. **为什么硬蒸馏有效**：硬标签蒸馏等价于把教师当作一个"更强的标注器"，学生学的是教师已经"想清楚"的决策边界，而非模糊的概率分布；训练更稳定。

## 7. 例子：基础 → 中等 → 实际应用

**基础例子（蒸馏 token 的注意力交互）**：
输入一张猫图，patch 序列 `[CLS, p1..p14, DIST]`。经过一层 attention：
- CLS token 的注意力集中在"猫头" patches（负责真实分类）。
- DIST token 的注意力分布在"猫身、背景边缘" patches（因为教师 ResNet 关注这些，蒸馏信号把它们对齐）。
- 推理时 `pred = (head_cls(CLS) + head_dist(DIST)) / 2`。

**中等例子（训练配置对比）**：
| 配置 | ImageNet-1k top-1 |
|:---|:---:|
| ViT-Base（无增强/无蒸馏，1k 直接训） | ~77% |
| ViT-Base + 强增强（RandAug/Mixup/CutMix/EMA） | ~79.6% |
| DeiT-Base = ViT-Base + 强增强 + 蒸馏 token（teacher: RegNetY-16GF） | **81.8%** |
| DeiT-Base（teacher: ResNet-152） | 81.4% |

（数字为论文报告值，训练 300 epoch、ImageNet-1k only。）

**实际应用**：
- 用 DeiT-Small（21M 参数）替代 ResNet-50（25M）做骨干，在小样本迁移/检测分割任务中省预训练数据。
- DeiT-III（Touvron 2022）把训练配方推到 800 epoch + 更强增强，DeiT-S 在 ImageNet 达 81.4%，成为"数据高效 backbone"基线。

## 8. 常见误区和易混概念

| 误区 | 澄清 |
|:---|:---|
| "DeiT 就是 ViT + 蒸馏" | 不准确：还包括整套强增强配方（RandAug/Mixup/CutMix/EMA），蒸馏 token 只是其中一环；只加蒸馏不加增强效果有限 |
| "蒸馏 token 和 CLS token 一样" | 不同：CLS 只学真实标签，DIST 只学教师标签，两者损失分离；推理时平均 |
| "硬蒸馏就是 one-hot 标签" | 硬蒸馏的 $y_t$ 是教师 argmax 得到的，仍可能错（教师错时学生跟着错），但整体比软蒸馏稳 |
| 与 [[知识蒸馏]] 混淆 | 知识蒸馏是通用方法（teacher-student logits/特征对齐），DeiT 是它在 ViT 上的具体落地 + 蒸馏 token 创新；知识蒸馏卡讲通用框架 |

## 9. 相关知识点与 Obsidian 双链建议

- 上游：[[ViT]]、[[Transformer与自注意力]]、[[数据增强与正则化]]
- 下游：[[SwinTransformer]]（层次化替代）、[[MAE]]（自监督替代路线）
- 平行：[[Transformer与自注意力|Transformer]] 家族中的纯 CNN 路线（ConvNeXt）与 DeiT 形成"加归纳偏置 vs 教归纳偏置"对比

```dataview
LIST
FROM "02-Knowledge/🧠 学习系统"
WHERE contains(upstream, this.file.link)
SORT file.name ASC
```

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 10. 闭卷复现任务

1. 手写 DeiT 前向：输入 patch 序列，说明 CLS 与 DIST token 的初始化与位置编码处理（10 分钟）。
2. 写出硬标签蒸馏损失公式并解释为什么 $\lambda=0.5$ 时 CLS/DIST 各负责一个目标（5 分钟）。
3. 对比 ViT 与 DeiT 训练配方差异（增强集 + 蒸馏 token + EMA），说明各贡献约几个点（参考论文 Table 3）。

## 11. 自测题：5 道

- #自测题/基础 1. DeiT 相比 ViT 增加了哪两个组件？（蒸馏 token + 强增强配方）
- #自测题/基础 2. 硬标签蒸馏的 $y_t$ 是什么？（教师 logits 的 argmax）
- #自测题/中等 3. 为什么蒸馏 token 的损失只含教师标签、不含真实标签？（避免单 token 双目标竞争）
- #自测题/中等 4. 软蒸馏公式中温度 $\tau$ 的作用是什么？（软化教师分布，使小类概率不被淹没；反向传播时梯度缩放 $\tau^2$）
- #自测题/较难 5. 若 teacher 与 student 同架构（自蒸馏），DeiT 的蒸馏 token 设计还成立吗？为什么？（成立：DIST token 仍提供第二条监督通道；自蒸馏时 teacher 是 EMA 版本的自己）

## 12. 我的主动回忆区

> 填完并闭卷复述后打勾：
- [ ] 我能画出 DeiT 前向图（CLS + DIST 双 token）
- [ ] 我能默写硬/软蒸馏损失公式
- [ ] 我能解释"为什么只用 ImageNet-1k 就能训 ViT"

## 13. 给 Obsidian 的归档建议

- 与 [[ViT]] 放同一阶段目录；引用关系已建。
- 与 [[MAE]] 对比阅读：一个教归纳偏置（DeiT），一个自监督学表示（MAE）。

## 学完后可以完成

- 可作为 HW06 开放项目『DeiT 蒸馏训练实验』选题

> 该卡无直接课后/阶段作业：以卡内自测题与闭卷复现作为形成性验收；如需综合实践，可挂靠 HW06 开放课程项目或 CAP01。

## 🔗 知识图谱

```dataview
LIST
FROM "02-Knowledge/🧠 学习系统"
WHERE contains(upstream, this.file.link)
SORT file.name ASC
```
