---
type: study
topic: "图Transformer与结构编码"
course: "图神经网络"
created: 2026-08-08
status: planned
stage_moc: "[[🧭 阶段4-结构扩展与系统边界]]"
flow: knowledge
kind: concept
difficulty: advanced
concept: [图Transformer, 结构编码, 位置编码]
upstream: ["[[图神经网络-GAT图注意力与边特征]]", "[[图神经网络-图拉普拉斯与谱滤波直觉]]"]
related: [全局注意力, Laplacian PE, Graphormer]
source: "Stanford CS224W Homework 3; Ying et al. Do Transformers Really Perform Bad for Graph Representation?"
source_url: "https://web.stanford.edu/class/cs224w/homework/CS224W_Aut2526_Homework_3.pdf"
accessed: 2026-08-08
license: "官方课程题目 link-only；论文链接；本卡为本地原创解释"
tags: [学习, 图神经网络, 图Transformer]
---

# 图神经网络-图Transformer与结构编码

## 1. 问题动机

局部消息传递的感受野随层数增长，长程依赖可能过压缩；标准 Transformer 的全局 attention 能直接连接远处节点，但没有结构编码就会把节点集合当作无序 token。图 Transformer 的核心不是“把图喂给 Transformer”，而是同时设计 token、结构偏置和复杂度边界。

## 2. 全局与稀疏注意力

对节点 token `X∈R^{n×d}`：

$$Attention(X)=softmax\left(\frac{QK^T}{\sqrt d}+B\right)V$$

`B` 可以是邻接 mask、最短路距离 bias、边特征或位置编码作用。全局 attention 的注意力部分约为 `O(n^2d)`；只在边上注意的稀疏版本约随 `O(|E|d)`，但需要稀疏实现和连通性设计。

## 3. 结构编码选择

- Laplacian eigenvectors：提供全局结构方向，但有符号/重根等价性和跨图对齐问题；
- shortest-path/distance bias：直接进入 attention logits，保留距离但需要计算/存储距离；
- degree/centrality encodings：便宜但结构区分能力有限；
- relation/edge features：把边语义写入 bias 或 key/value，需明确缺失边如何处理。

位置编码不是免费的信息。若编码使用了测试图完整结构，却声称 inductive，协议需要重新审计。

## 4. 最小 masked attention 检查

```python
import torch

X = torch.eye(3)
Q = X
K = X
V = X
scores = Q @ K.T
mask = torch.tensor([[0., 0., -float("inf")], [0., 0., 0.], [-float("inf"), 0., 0.]])
attention = torch.softmax(scores + mask, dim=1)
assert torch.allclose(attention[0, 2], torch.tensor(0.0))
output = attention @ V
assert output.shape == X.shape
print(attention)
```

这验证 mask 只允许声明的邻居；真实模型还需处理 self-loop、边方向、batch padding 和结构编码的归一化。

## 5. 与 GAT 的区别

GAT 默认在局部邻域内学习 attention；图 Transformer 常允许更广甚至全局 token 交互，并额外注入位置/距离/边类型。两者都可能使用多头，但计算复杂度和结构先验不同。

## 6. 常见错误

1. 用 dense attention 处理大图后只报告模型分数，不报告 `n^2` 内存风险。
2. Laplacian eigenvector 的符号翻转导致预测变化，却没有做 sign-invariant 处理。
3. 用最短路 bias 却计算了跨时间未来边，造成结构泄漏。
4. 把“有位置编码”写成“理解了图结构”，没有和结构无编码基线比较。

## 7. 检索练习与通过标准

- 对 `n=1000,d=64,|E|=5000` 比较 dense 与 sparse attention 的主项复杂度。
- 说明 Laplacian PE 的一个强项、一个等价性问题和一个缓解办法。
- 设计一个只改变结构编码、不改变任务头和 split 的消融。

通过标准：能写出 attention 公式和 mask；能解释位置编码边界；报告含复杂度、稳定性和不使用结构编码的基线。

## 8. 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

下一张：[[图神经网络-大规模训练与线上评估边界]]。

