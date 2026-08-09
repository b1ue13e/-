---
type: study
topic: "宽度缩放、Weight Decay、卷积网络与受控比较"
course: "生成式AI基础与Prompt工程"
tags: [学习, 45-生成式AI基础与Prompt工程, 深度学习工程, CNN]
created: 2026-08-05
status: completed
mastery: not_started
difficulty: intermediate
stage_moc: "[[🧭 阶段2-模型实现选修]]"
concept: ["宽度参数化", "权重衰减", "卷积归纳偏置"]
prerequisites: ["深度学习工程-PyTorch张量自动微分与训练循环", "训练优化-交叉熵AdamW调度梯度裁剪与检查点"]
related: ["深度学习数学-对偶范数谱范数PowerIteration与最速下降", "图表示学习-不变聚合消息传递与手性边界"]
upstream: ["[[深度学习工程-PyTorch张量自动微分与训练循环]]", "[[训练优化-交叉熵AdamW调度梯度裁剪与检查点]]"]
flow: knowledge
kind: concept
source: "MIT OCW 6.7960 Deep Learning Fall 2024 Homework 2 Questions 9-14, CC BY-NC-SA 4.0"
source_url: "https://ocw.mit.edu/courses/6-7960-deep-learning-fall-2024/"
accessed: 2026-08-09
license: "CC BY-NC-SA 4.0"
anki_deck: "45-生成式AI基础与Prompt工程::深度学习工程"
anki_tags: [宽度缩放, WeightDecay, CNN, 受控实验]
---

# 深度学习工程：宽度缩放、Weight Decay、卷积与受控比较

## 0. 学习边界

- **类别**：A 类（MIT HW2 Q9–Q14 工程主卡）。
- **判断理由**：改变网络宽度会改变激活/梯度尺度；CNN 实现又涉及卷积 shape 和公平对照，不能用通用 Python 卡替代。

## 1. 这个知识点解决什么问题？

> 为什么同一学习率从窄网络搬到宽网络会失效？weight decay 实际改了什么？怎样实现 CNN，并证明性能差异来自归纳偏置而不是参数量、训练步数或数据泄漏？

## 2. 为什么它重要？它有什么用？

- 宽度参数化控制前向信号、反向梯度和超参数迁移。
- Weight decay 抑制参数无界增长，但 AdamW 与 L2 梯度并非总等价。
- 卷积通过局部连接与权重共享注入平移相关归纳偏置。
- 受控比较是把“模型 A 更好”变成可复核因果证据。

## 3. 学它之前需要哪些前置知识？

1. [[深度学习工程-PyTorch张量自动微分与训练循环]]。
2. [[训练优化-交叉熵AdamW调度梯度裁剪与检查点]]。

## 4. 用直觉语言解释它

> “网络加宽像让更多人同时发言：若每个人音量不缩放，总声压会随人数变；卷积则让同一个局部侦测器在整张图上巡逻。”

一句话本质：**参数化决定尺度，归纳偏置决定模型优先学哪类结构，实验控制决定比较是否可信。**

## 5. 正式定义、核心公式、符号解释

若 $h_j=\sum_{i=1}^{n}W_{ji}x_i$，且 $x_i,W_{ji}$ 独立零均值，则
$$\operatorname{Var}(h_j)=n\operatorname{Var}(W_{ji})\operatorname{Var}(x_i).$$
为保持宽度变化时激活方差 $O(1)$，常令 $\operatorname{Var}(W)=O(1/n)$（标准差 $O(1/\sqrt n)$）。学习率是否可跨宽度迁移还取决于输出层和参数化约定，不能只凭初始化判断。

解耦 weight decay：
$$\theta_{t+1}=(1-\eta_t\lambda)\theta_t-\eta_t\,\text{Update}(g_t).$$

二维卷积输出尺寸：
$$H_{out}=\left\lfloor\frac{H+2P-D(K-1)-1}{S}+1\right\rfloor,$$
$W_{out}$ 同理。参数量为 $C_{out}(C_{in}K_hK_w+1)$（含 bias）。

| 变量 | 含义 | 公平比较时是否固定 |
| :--- | :--- | :---: |
| width | 隐藏通道/神经元数 | 研究宽度时改变 |
| 参数化/初始化 | 权重尺度规则 | 必须记录 |
| optimizer/schedule | 更新动力学 | 固定或做独立消融 |
| train steps/data order | 训练预算 | 固定 |
| parameter/FLOP budget | 容量/计算 | 至少报告 |

## 6. 推导思路和思想来源

1. 用方差传播而非“经验感觉”确定初始化随 fan-in 缩放。
2. 宽度改变会同时改变参数数、NTK/feature-learning regime 和每层更新尺度，学习率迁移必须实验验证。
3. Weight decay 是更新规则的一部分；在自适应优化器中不要与 L2 惩罚混写。
4. CNN 将全连接的每位置独立参数改成共享 kernel，减少参数并编码局部性。
5. 架构比较至少固定数据切分、增强、优化器、步数和随机种子，并报告参数/FLOP 差异。

## 7. 例子：基础 → 中等 → 实际应用

### 例子 1：基础例子（可手算）

输入 `32×32`，kernel=3、padding=1、stride=2、dilation=1，则输出边长 $\lfloor(32+2-2-1)/2+1\rfloor=16$。

### 例子 2：中等例子

MLP 和 CNN 准确率不同，但 CNN 参数少 20 倍、增强不同，则不能单独归因于“卷积更好”。应先统一数据/训练，再分别做匹配参数量与匹配计算量比较。

### 例子 3：可运行 PyTorch CPU

```python
# 输入：4 张 1x8x8 图；输出：卷积 logits shape 与参数量。
import torch
from torch import nn

torch.manual_seed(3)
model = nn.Sequential(
    nn.Conv2d(1, 4, kernel_size=3, padding=1),
    nn.ReLU(),
    nn.MaxPool2d(2),
    nn.Flatten(),
    nn.Linear(4 * 4 * 4, 3),
)
inputs = torch.randn(4, 1, 8, 8)
logits = model(inputs)
parameter_count = sum(parameter.numel() for parameter in model.parameters())
print(tuple(logits.shape), parameter_count)
assert tuple(logits.shape) == (4, 3)
assert parameter_count == 235
```

## 8. 常见误区和易混概念

- 初始化方差缩放不自动保证最优学习率可跨宽度迁移。
- Weight decay 不是“每隔几步把小权重删掉”。
- CNN 并非完全平移不变；卷积更接近平移等变，pooling/读出和边界处理影响不变性。
- 只固定 seed 不等于受控实验；超参数、预算和数据处理也要固定。

| 概念 | 改变对象 | 主要效果 | 区别 |
| :--- | :--- | :--- | :--- |
| 初始化缩放 | 初始权重 | 稳定信号方差 | 不持续约束参数 |
| Weight decay | 每步参数 | 收缩参数 | 与梯度裁剪不同 |
| 梯度裁剪 | 当前梯度 | 限制突发更新 | 不直接正则参数 |
| 卷积共享 | 架构参数连接 | 局部/平移归纳偏置 | 不等于数据增强 |

## 9. 课程连接

- [[深度学习工程-PyTorch张量自动微分与训练循环]] 和 [[训练优化-交叉熵AdamW调度梯度裁剪与检查点]] 提供实现与优化状态。
- [[深度学习数学-对偶范数谱范数PowerIteration与最速下降]] 提供尺度分析；[[图表示学习-不变聚合消息传递与手性边界]] 对比另一类归纳偏置。
- 卷积专题的完整路线回到 [[🗺️ 计算机视觉学习路径|计算机视觉路径]]；本卡只保留 MIT HW2 所需的宽度、卷积和受控比较闭环。

## 10. 闭卷复现任务

- [ ] 推导 fan-in 方差缩放。
- [ ] 解释宽度为何影响学习率迁移。
- [ ] 写出 AdamW 衰减更新。
- [ ] 写出卷积输出尺寸公式。
- [ ] 计算卷积参数量。
- [ ] 区分平移等变与不变。
- [ ] 设计单 batch CNN 过拟合测试。
- [ ] 列出公平架构比较的固定项。
- [ ] 区分匹配参数与匹配 FLOP。
- [ ] 解释曲线差异不能单独证明归纳偏置。

## 11. 自测题：5 道

1. fan-in 从 100 增至 400 时权重标准差应约缩放多少？ `#自测题/基础`
2. `H=10,K=3,P=0,S=2` 的输出边长是多少？ `#自测题/基础`
3. `Conv2d(3,8,3,bias=True)` 参数量是多少？ `#自测题/中等`
4. 为什么 AdamW 衰减不等于对 Adam 梯度简单加 $\lambda\theta$？ `#自测题/中等`
5. 设计 MLP/CNN 的匹配参数、匹配 FLOP 两组实验与报告字段。 `#自测题/较难`

> [!question]- 参考答案与评分点
> 1. 标准差缩小到 1/2。2. 4。3. $8(3\cdot3\cdot3+1)=224$。4. 后者进入矩估计和自适应缩放。5. 固定数据/增强/步数/优化器，分别调宽度匹配参数或计算，报告曲线、参数、FLOP、方差与失败。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/45-生成式AI基础与Prompt工程"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 12. 我的主动回忆区

- **尺度推导**：
- **卷积 shape**：
- **公平比较清单**：
- [ ] 明天  [ ] 3 天后  [ ] 7 天后  [ ] 14 天后

## 13. 给 Obsidian 的归档建议

- 本卡负责 HW2 的宽度、优化与 CNN 工程闭环；图结构移到独立 GNN 卡。
- 官方实验须保存参数量、FLOP、seed 和全部曲线，不只截图最终准确率。

## 🃏 Anki 卡片

Q: 为什么常令权重方差与 fan-in 成反比？
A: 线性和的方差随 fan-in 累加，令 Var(W)=O(1/fan-in) 可保持激活方差为 O(1)。

Q: 卷积比较必须至少控制哪些因素？
A: 数据切分/增强、训练步数、优化器/调度、随机种子，并报告参数量和计算预算。

