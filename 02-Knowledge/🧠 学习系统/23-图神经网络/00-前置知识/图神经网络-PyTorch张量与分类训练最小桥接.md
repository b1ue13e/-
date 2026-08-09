---
type: study
topic: "PyTorch张量与分类训练最小桥接"
course: "图神经网络"
created: 2026-08-08
status: planned
stage_moc: "[[🧭 图神经网络-前置知识]]"
flow: knowledge
kind: concept
difficulty: beginner
concept: [张量, 自动微分, 分类训练]
related: [Python, 线性代数, 交叉熵]
source: "PyTorch official tutorials; local GNN training bridge"
source_url: "https://pytorch.org/tutorials/beginner/basics/intro.html"
accessed: 2026-08-08
license: "官方教程链接；本卡为本地原创桥接"
tags: [学习, 图神经网络, 前置知识, PyTorch]
---

# 图神经网络-PyTorch张量与分类训练最小桥接

## 1. 这张卡解决什么问题

消息传递只负责产生表示，任务头和损失函数才把表示变成可优化目标。本卡只补 GNN 实验所需的张量形状、分类 logits、交叉熵和一次梯度更新，不展开完整深度学习课程。

## 2. 张量合同

对节点分类，约定：

- `X.shape == (num_nodes, num_features)`：每行是一个节点的输入特征；
- `logits.shape == (num_nodes, num_classes)`：每行是一个节点对各类别的未归一化分数；
- `y.shape == (num_nodes,)`：每个元素是整数类别编号 `0..num_classes-1`；
- `train_mask/val_mask/test_mask.shape == (num_nodes,)` 且互不重叠。

`softmax` 只把 logits 转成概率，训练时优先直接把 logits 交给 `CrossEntropyLoss`，避免先手动取 `log` 造成数值不稳定。

## 3. 交叉熵与参数更新

对样本 `i` 的真实类别 `y_i`：

$$\ell_i=-\log\frac{\exp(z_{i,y_i})}{\sum_c\exp(z_{i,c})}$$

训练步骤固定为：清空旧梯度 → 前向得到 logits → 只在训练掩码上计算损失 → `backward()` → `optimizer.step()`。验证和测试只前向，不更新参数，不选择“让测试分数最高”的超参数。

## 4. 最小可运行例子

```python
import torch

torch.manual_seed(0)
X = torch.tensor([[0.0, 0.0], [0.0, 1.0], [1.0, 0.0], [1.0, 1.0]])
y = torch.tensor([0, 1, 1, 0])
model = torch.nn.Linear(2, 2)
optimizer = torch.optim.SGD(model.parameters(), lr=0.5)
loss_fn = torch.nn.CrossEntropyLoss()

for _ in range(80):
    optimizer.zero_grad()
    logits = model(X)
    loss = loss_fn(logits, y)
    loss.backward()
    optimizer.step()

with torch.no_grad():
    predicted = model(X).argmax(dim=1)
    accuracy = (predicted == y).float().mean().item()
assert 0.0 <= accuracy <= 1.0
print(f"accuracy={accuracy:.2f}")
```

这里的网络没有图结构，故意作为任务头和训练循环的 oracle。GNN 只需把 `X` 换成消息传递后的 `H`，训练协议不应悄悄改变。

## 5. 最常见的形状错误

- 把 `y` 写成 one-hot 后仍传给默认 `CrossEntropyLoss`；本课程统一使用整数类别标签。
- 用 `softmax` 后再传给 `CrossEntropyLoss`，导致重复归一化。
- 把节点维和特征维颠倒，`Linear` 的 `in_features` 因此不匹配。
- 用全节点 loss 代替训练掩码 loss；这会把验证/测试标签参与参数更新。
- 在测试前根据测试指标调学习率、层数或隐藏维度；这让测试集变成验证集。

## 6. 检索练习

1. 给出 `logits.shape=(6,4)` 和 `y.shape=(6,)` 时，单个样本 loss 选择哪个 logit。
2. 说明 `model.eval()` 与 `torch.no_grad()` 分别解决什么问题；为什么两者不能互相替代。
3. 写出只在 `train_mask` 上计算交叉熵的 PyTorch 表达式。

通过标准：代码运行成功；能从张量形状定位一个维度错误；能解释为什么测试标签不能进入梯度图。

## 7. 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

下一步：[[图神经网络-图学习评估与无泄漏划分]]。

