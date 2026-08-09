---
type: study
course: "05-计算机视觉"
topic: "CLIP 对比语言-图像预训练"
created: 2026-08-06
updated: 2026-08-06
status: ongoing
difficulty: advanced
concept: ["CLIP", "对比学习", "多模态", "零样本分类", "图文对齐"]
prerequisites: ["Transformer与自注意力", "SimCLR与对比学习", "Softmax与SVM损失函数"]
upstream: ["[[Transformer与自注意力]]", "[[计算机视觉-SimCLR与对比学习]]", "[[Softmax与SVM损失函数]]"]
related: ["ViT", "DeiT", "生成模型GAN与Diffusion", "可解释性Saliency与CAM"]
flow: knowledge
stage_moc: "[[🧭 阶段4-前沿架构探索]]"
kind: concept
source: "Radford et al. 2021, Learning Transferable Visual Models From Natural Language Supervision; arXiv:2103.00020; OpenAI CLIP"
tags: [学习, 计算机视觉, 多模态, CLIP, 零样本]
---

# CLIP：对比语言-图像预训练

## 0. 学习边界

- **值得**：CLIP 是"视觉-语言对齐"的奠基工作，零样本分类、图文检索、可控生成（Stable Diffusion 的 text encoder 就是 CLIP）都建立在其上；工业界文本-图像模型的事实标准。
- **不值得**：如果你只做单模态纯视觉任务且无多模态需求，可只读 §5 损失与 §8 误区，不必深挖训练细节（WebImageText 数据集不可复现）。

## 1. 这个知识点解决什么问题？

**问题**：传统图像分类模型（ResNet、ViT）学到的标签空间是**固定的**（1000 类 ImageNet），换任务就要重新标注、重新训练。真实世界类别是开放的（"长颈鹿"、"赛博朋克风格的猫"），且很多类别没有标注数据。

**CLIP 的答案**：用**互联网图文对**（4 亿对）做对比预训练，让模型学会"图像与描述它的文本"对齐。训练后：
- **零样本分类**：无需微调，把类别名拼成文本模板（"a photo of a {class}"），算图像与每个类别文本的相似度即可分类；
- **检索**：文本搜图、图搜文本；
- **特征提取**：下游任务用它当 backbone。

## 2. 为什么它重要？它有什么用？

- **零样本能力**：ImageNet 零样本 top-1 ≈ 76.2%（ResNet-50 线性探测基线 76.2% 相当）——第一次让"没见过的类别"分类达到监督水平。
- **多模态对齐范式**：InfoNCE 对比损失成为图文对齐标准（后续 ALIGN、BLIP、LLaVA 都沿此思路）。
- **可控生成基础**：Stable Diffusion / DALL·E 2 用 CLIP text encoder 把文本语义注入生成过程。
- **评测与局限并存的教材**：CLIP 暴露了"捷径学习"（对文本的拼写/背景敏感）等短板，是研究分布偏移的经典案例。

## 3. 学它之前需要哪些前置知识？

1. **[[Transformer与自注意力|Transformer / 自注意力]]**：CLIP 的 text encoder 是 Transformer，image encoder 可以是 ResNet 或 ViT。
2. **[[计算机视觉-SimCLR与对比学习|对比学习]]**：InfoNCE 损失、正负样本构造——CLIP 把 SimCLR 的"图像-增强图像"对比扩展为"图像-文本"对比。
3. **[[Softmax与SVM损失函数|Softmax 与交叉熵]]**：对比损失的 softmax 归一化与温度缩放。

## 4. 用直觉语言解释它

CLIP 像给模型配了一本"图文词典"：
- 4 亿张图和它们的文字描述成对出现。
- 模型有两个编码器：图像编码器（看图）和文本编码器（读文字）。
- 训练目标：**让"猫的图片"与"a photo of a cat"的向量靠近，与其他文本远离**。
- 训练完，模型学会"图像和文字共享一个语义空间"。分类时不用标注，把候选类别写成句子，看哪个句子和图片最像。

## 5. 正式定义、核心公式、符号解释

**架构**：
- Image encoder $f: \mathbb{R}^{H\times W\times 3} \to \mathbb{R}^{d}$（ResNet-50 或 ViT-B/32，最终用 attention pooling 或 CLS token 输出）
- Text encoder $g: \text{tokens} \to \mathbb{R}^{d}$（Transformer，12 层，在 `[EOS]` token 输出处取向量）
- 两个编码器输出都 L2 归一化到单位超球面，投影到同一维度 $d$（默认 512）。

**InfoNCE 对比损失（batch size $N=32768$）**：
对 batch 内每个图像 $i$，正样本是配对的文本 $i$，负样本是 batch 内其余 $N-1$ 个文本：
$$
\mathcal{L} = -\frac{1}{N}\sum_{i=1}^{N} \log \frac{\exp(\text{sim}(I_i, T_i)/\tau)}{\sum_{j=1}^{N} \exp(\text{sim}(I_i, T_j)/\tau)}
$$
其中 $\text{sim}(I, T) = \frac{f(I) \cdot g(T)}{\lVert f(I)\rVert \lVert g(T)\rVert}$（余弦相似度），$\tau$ 是可学习的温度参数（初始 0.07）。

对称版本还加上文本侧的交叉熵（对文本 $i$，正样本是图像 $i$），两个方向各算一个损失取平均。

**零样本分类**：
对类别集合 $\mathcal{C} = \{c_1, ..., c_K\}$，构造文本模板 $t_k = \text{"a photo of a "} + c_k$，预测：
$$
\hat{y} = \arg\max_{k}\, \text{sim}(f(I), g(t_k))
$$
常用多模板集成（80 个模板取平均文本嵌入）提升鲁棒性。

## 6. 推导思路和思想来源

1. **来源**：Radford et al. 参考 SimCLR/CPC 的 InfoNCE，但把"正样本对"从"同一图像的不同增强"换成"图像-文本对"。监督信号从自监督的增强不变性变成**语言监督的语义对齐**。
2. **为什么用对比而非生成**：生成式（image captioning）损失计算量大且难优化；对比损失只要求"匹配对相似度高于不匹配对"，计算高效（batch 内即可构造负样本）。
3. **为什么大 batch**：InfoNCE 的负样本质量决定嵌入质量。CLIP 用 32768 的 batch（在 592 块 V100 上训练 18 天），保证每个图像有大量难负样本。
4. **为什么温度可学习**：固定温度 0.07 是 SimCLR 的经验值；CLIP 让它可学习，模型自动缩放 logits 尺度，稳定训练。

## 7. 例子：基础 → 中等 → 实际应用

**基础例子（零样本分类）**：
测试图片：一只金毛犬。
- 候选类：["cat", "dog", "car"]
- 文本模板：["a photo of a cat", "a photo of a dog", "a photo of a car"]
- 计算相似度：sim(图, "a photo of a dog") 最大 → 预测 "dog" ✅（无需任何标注训练）。

**中等例子（损失计算）**：
batch $N=4$，图像 $I_1..I_4$、文本 $T_1..T_4$ 配对。对 $I_1$：
- 正样本：$T_1$；负样本：$T_2, T_3, T_4$
- 相似度矩阵 $S \in \mathbb{R}^{4\times4}$，对角线是正
- 行 softmax 后取对角线交叉熵，加列方向交叉熵平均

**实际应用**：
- **Stable Diffusion**：text encoder 直接用 CLIP ViT-L/14，文本条件注入 latent diffusion。
- **检索系统**：商品图库建图像嵌入索引，用户输入"红色运动鞋"→ 文本嵌入 → 余弦检索 top-k。
- **检测/分割的开放词汇**：GLIP、Open-vocabulary 检测用 CLIP 文本分支做类别嵌入。

## 8. 常见误区和易混概念

| 误区 | 澄清 |
|:---|:---|
| "CLIP 是生成模型" | 不是：CLIP 是**判别式**对比模型（图文相似度），不生成图像/文本；生成是 Stable Diffusion 等下游利用它的 text encoder |
| "CLIP 零样本=万能" | 局限明显：细粒度/抽象类别（"真菌种类"）差、对文本拼写敏感（"penguin" vs "penguin" 变形）、数据集存在捷径（ImageNet 上可用背景猜类） |
| "CLIP 的 text encoder 是 BERT" | 不同：是 Transformer encoder，但用 `[SOS]/[EOS]` token，输出取 `[EOS]` 位置，词表 49408（BPE） |
| 与 [[02-Knowledge/🧠 学习系统/05-计算机视觉/04-前沿架构探索/计算机视觉-SimCLR与对比学习\|SimCLR]] 混淆 | SimCLR 是同模态（图-图）对比，CLIP 是跨模态（图-文）对比；损失同源（InfoNCE）但数据与正样本定义不同 |
| "CLIP 训练数据可复现" | 不可：WebImageText（4 亿对）未公开，官方只给权重；复现需自建图文对数据集 |

## 9. 相关知识点与 Obsidian 双链建议

- 上游：[[Transformer与自注意力]]、[[计算机视觉-SimCLR与对比学习|SimCLR 对比学习]]
- 平行：[[自监督学习SimCLR与CLIP|自监督学习总卡]]（CLIP 在其中的定位）
- 下游：[[生成模型GAN与Diffusion|生成模型]]（Stable Diffusion 用 CLIP 文本编码）、[[计算机视觉-DeiT]]（数据高效训练的另一种路线）

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

1. 手写 CLIP 对比损失（InfoNCE 单方向），说明温度 $\tau$ 的作用（10 分钟）。
2. 画出 CLIP 零样本分类流程：图像 → image encoder → 归一化嵌入；类别 → 模板 → text encoder → 嵌入；余弦相似度 argmax（5 分钟）。
3. 解释为什么大 batch 对 CLIP 重要（负样本质量），以及为什么温度可学习（5 分钟）。

## 11. 自测题：5 道

- #自测题/基础 1. CLIP 的两个编码器分别是什么？（图像编码器 + 文本编码器，输出同维归一化嵌入）
- #自测题/基础 2. CLIP 的训练损失属于什么类型？（对比学习 / InfoNCE，图-文跨模态）
- #自测题/中等 3. 零样本分类时，类别名要做什么处理？（拼成文本模板，如 "a photo of a {class}"，再编码）
- #自测题/中等 4. 温度 $\tau$ 为什么是可学习的？（自动缩放 logits 尺度，稳定训练；初始 0.07）
- #自测题/较难 5. CLIP 在 ImageNet 上能零样本达到监督水平，为什么在细粒度类别上差？（类别文本区分度低 + 预训练数据覆盖不足 + 捷径学习）

## 12. 我的主动回忆区

> 填完并闭卷复述后打勾：
- [ ] 我能默写 InfoNCE 对比损失公式
- [ ] 我能解释零样本分类流程
- [ ] 我能列举 CLIP 的两个已知局限

## 13. 给 Obsidian 的归档建议

- 与 [[计算机视觉-SimCLR与对比学习|SimCLR 卡]] 对比：同源损失、不同模态。
- 与 [[生成模型GAN与Diffusion|生成模型卡]] 关联：Stable Diffusion 的 text encoder 是 CLIP。

## 学完后可以完成

> 下列作业在 `requires` 中引用了本卡，由 Dataview 实时派生（非人工维护反向链接）：

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

本卡另以前置「🧪 自测题」与闭卷复现作为形成性验收。

## 🔗 知识图谱

```dataview
LIST
FROM "02-Knowledge/🧠 学习系统"
WHERE contains(upstream, this.file.link)
SORT file.name ASC
```

