---
type: study
topic: "GCN归一化传播与谱近似"
course: "图神经网络"
created: 2026-08-08
status: planned
stage_moc: "[[🧭 阶段2-消息传递模型]]"
flow: knowledge
kind: derivation
difficulty: intermediate
concept: [GCN, 对称归一化, 谱近似]
upstream: ["[[图神经网络-消息传递统一框架]]", "[[图神经网络-图拉普拉斯与谱滤波直觉]]"]
related: [GraphSAGE, oversmoothing, self-loop]
source: "Kipf & Welling, Semi-Supervised Classification with GCNs; Hamilton GRL Ch.5"
source_url: "https://arxiv.org/abs/1609.02907"
accessed: 2026-08-08
license: "论文链接；本卡为本地原创解释"
tags: [学习, 图神经网络, GCN]
---

# 图神经网络-GCN归一化传播与谱近似

## 1. 问题动机

直接用 `A X W` 聚合会让高度节点的数值尺度随度数增长，并且没有保留节点自身特征。GCN 用自环和对称归一化把局部平滑写成一层可训练传播。

## 2. 核心公式

令 `\tilde A=A+I`，`\tilde D_{ii}=Σ_j\tilde A_{ij}`，则一层 GCN 为：

$$H^{(l+1)}=σ\left(\tilde D^{-1/2}\tilde A\tilde D^{-1/2}H^{(l)}W^{(l)}\right)$$

`H^(0)=X`；`W^(l)` 是共享于所有节点的可学习矩阵；`σ` 常用 ReLU。邻接传播和线性变换的次序要在代码中固定，不能把 `W` 随节点改变。

## 3. 一行手算

对路径 `0—1—2` 加自环后度为 `[2,3,2]`。节点 1 从自身和两个邻居接收的权重分别是 `1/3`、`1/√6`、`1/√6`；边界节点自身权重是 `1/2`。这说明对称归一化不是简单的“除以邻居数量”，而是发送端和接收端度数共同决定。

## 4. 与谱近似的关系

谱视角把滤波写成拉普拉斯多项式；一阶近似、限制参数并加入自环后得到局部传播。它的价值是解释归一化和平滑的来源，不应被写成“GCN 必须先完整特征分解”。实际实现直接做稀疏/稠密矩阵乘法。

## 5. 最小可运行传播检查

```python
import torch

A = torch.tensor([[0., 1., 0.], [1., 0., 1.], [0., 1., 0.]])
I = torch.eye(3)
At = A + I
degree = At.sum(dim=1)
D_inv_sqrt = torch.diag(degree.pow(-0.5))
S = D_inv_sqrt @ At @ D_inv_sqrt
X = torch.eye(3)
W = torch.ones(3, 1)
H = torch.relu(S @ X @ W)
assert H.shape == (3, 1)
assert torch.allclose(S, S.T)
print(H.squeeze().tolist())
```

这个检查验证自环、对称性和形状；它不是训练结果，也不能用于声称模型优于基线。

## 6. 适用条件与边界

- 对称归一化默认无向或已对称化的图；有向图要明确入/出边传播算子。
- 节点特征维度可不同于隐藏维度，`W` 负责变换；邻接矩阵不直接学习节点标签。
- 深度增加 receptive field，但也可能过平滑；残差、跳层、归一化和更好的图结构是后续设计，不是公式的隐含保证。
- 标准 GCN 的全图前向常用于 transductive 节点分类；大图需要采样或分区，见阶段 3。

## 7. 常见错误

1. 忘记把 `D` 按加自环后的 `\tilde A` 计算。
2. 使用 `D^{-1}A` 却在文字中称为 Kipf-Welling 对称归一化。
3. 训练/验证/测试划分后仍把测试边留在一个本应隐藏结构的链路预测传播图中。
4. 只展示一次前向输出，就称“模型学会了”；必须有 loss、梯度和冻结后的评估。

## 8. 检索练习与通过标准

- 写出任意 3 节点图的 `S`，检查它是否对称。
- 解释加入自环后为什么需要重新计算度矩阵。
- 从一阶谱近似说出 GCN 只使用多少跳邻域。

通过标准：手算一行权重无误；代码断言通过；能区分传播检查和训练闭环；能指出一个会导致泄漏的图切分场景。

## 9. 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

下一张：[[图神经网络-GraphSAGE采样与归纳学习]]。

