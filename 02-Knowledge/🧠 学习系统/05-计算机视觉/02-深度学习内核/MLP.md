---
type: study
course: "05-计算机视觉"
topic: "多层感知机 (MLP)"
created: 2026-08-06
status: planned
difficulty: intermediate
concept: ["MLP", "隐藏层", "万能近似定理", "非线性激活", "XOR"]
prerequisites: ["感知机", "激活函数详解"]
related: ["反向传播与计算图", "卷积神经网络CNN"]
upstream: ["[[感知机]]"]
flow: knowledge
stage_moc: "[[🧠 第二阶段：深度学习内核]]"
kind: concept
source: "D2L Ch.5; 《Deep Learning》 Ch.6"
tags: [学习, 计算机视觉, 深度学习, MLP]
---

# 多层感知机 (Multilayer Perceptron, MLP)

> 所属模块：[[🗺️ 计算机视觉学习路径|计算机视觉学习路径]]
> 对应阶段：[[🧠 第二阶段：深度学习内核|第二阶段]]
> 建议先看：[[感知机]]、[[激活函数详解]]

---

## 0. 类别：A 类核心概念

MLP 是从单层感知机到深度神经网络的关键跃迁。理解它 → 理解"为什么加深网络能表达更复杂的函数"。

---

## 1. 直觉：用隐藏层"折叠"空间

单层感知机的决策边界是一条直线。MLP 加了一个隐藏层后，隐藏层将输入空间**非线性变换**到一个新空间，使得原本不可分的数据在新空间中**线性可分**。

> **一句话**：隐藏层 = 空间变换器。它能把弯弯曲曲的决策边界"拉直"。

---

## 2. 正式定义

**两层 MLP**（一个隐藏层）：

$$\mathbf{h} = \sigma(\mathbf{W}_1 \mathbf{x} + \mathbf{b}_1)$$
$$\hat{\mathbf{y}} = \text{softmax}(\mathbf{W}_2 \mathbf{h} + \mathbf{b}_2)$$

| 组件 | 形状 | 含义 |
|:---|:---|:---|
| $\mathbf{x} \in \mathbb{R}^d$ | 输入 | d 维特征 |
| $\mathbf{W}_1 \in \mathbb{R}^{h \times d}$ | 隐藏层权重 | h 个隐藏神经元 |
| $\sigma$ | 激活函数 | 非线性（ReLU/Sigmoid/Tanh） |
| $\mathbf{W}_2 \in \mathbb{R}^{c \times h}$ | 输出层权重 | c 个类别 |

---

## 3. 为什么必须用非线性激活？

如果 $\sigma$ 是线性的（$\sigma(z) = z$）：

$$\hat{\mathbf{y}} = \mathbf{W}_2 (\mathbf{W}_1 \mathbf{x} + \mathbf{b}_1) + \mathbf{b}_2 = (\mathbf{W}_2\mathbf{W}_1)\mathbf{x} + (\mathbf{W}_2\mathbf{b}_1 + \mathbf{b}_2)$$

多层退化为**单层线性变换**！无论堆多少层，表达能力等同于一层。

```python
# 验证：两层线性网络 = 一层线性网络
import torch.nn as nn
linear_2layer = nn.Sequential(nn.Linear(10, 5), nn.Linear(5, 3))
linear_1layer = nn.Linear(10, 3)
# 对于任意输入 x，存在 W, b 使两者输出相等
```

> **非线性激活是深度网络"深度"的意义所在。**

---

## 4. 万能近似定理 (Universal Approximation Theorem)

**定理**：具有至少一个隐藏层、足够多隐藏神经元、非线性激活函数（如 Sigmoid）的 MLP，可以以任意精度逼近 $\mathbb{R}^n$ 的紧集上的任意连续函数。

| 条件 | 说明 |
|:---|:---|
| ✅ 隐藏层 ≥ 1 | 一层就够了（理论上） |
| ✅ 神经元足够多 | 可能需要指数级数量 |
| ✅ 非线性激活 | Sigmoid/Tanh/ReLU 都满足 |
| ❌ 线性激活 | 不满足 |

> **实际含义**：理论上 MLP 可以做任何事。实践中深度比宽度更高效（参数利用率更高）。

---

## 5. 代码示例：MLP 解 XOR

```python
import torch
import torch.nn as nn

class XOR_MLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(2, 4),    # 2输入 → 4隐藏神经元
            nn.ReLU(),
            nn.Linear(4, 1),    # → 1输出
            nn.Sigmoid()
        )
    
    def forward(self, x):
        return self.net(x)

model = XOR_MLP()
criterion = nn.BCELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.5)

X = torch.tensor([[0.,0.],[0.,1.],[1.,0.],[1.,1.]])
y = torch.tensor([[0.],[1.],[1.],[0.]])

for epoch in range(2000):
    optimizer.zero_grad()
    loss = criterion(model(X), y)
    loss.backward()
    optimizer.step()

# 预期：约 500-1000 epoch 收敛，loss→0
with torch.no_grad():
    preds = model(X).round()
    print(f"Predictions: {preds.flatten().tolist()}")  # [0, 1, 1, 0]
    print(f"Accuracy: {(preds == y).float().mean():.0%}")  # 100%
```

---

## 6. 设计选择与变体

| 选择 | 选项 | 建议 |
|:---|:---|:---|
| 隐藏层数 | 1-3（浅层 MLP）vs 10+（深层） | CV 中 CNN 取代 MLP；表格数据用 2-4 层 |
| 隐藏单元数 | 通常 $2^k$（64/128/256/512） | 从 128 开始，根据过拟合/欠拟合调 |
| 激活函数 | ReLU（默认）/ GELU（Transformer）/ Swish | ReLU 是安全选择 |

---

## 7. 常见误区

- ❌ "MLP 就是很多感知机堆叠" — 没有非线性激活的多层 = 单层
- ❌ "隐藏层越多越好" — 太多层导致梯度消失；ResNet 的残差连接部分解决了这个问题
- ❌ "万能近似 = 实际可行" — 理论保证需要指数级神经元，深度网络用深度换取参数效率

---

## 🧪 自测题

1. **(基础)** 两层线性变换等价于一层线性变换，为什么？
   <details><summary>💡 提示</summary>$\mathbf{W}_2(\mathbf{W}_1\mathbf{x}) = (\mathbf{W}_2\mathbf{W}_1)\mathbf{x}$，两个矩阵乘积仍是一个矩阵。</details>

2. **(中等)** 为什么 Sigmoid 在深层 MLP 中会导致梯度消失？
   <details><summary>💡 提示</summary>Sigmoid 导数最大 0.25，多层连乘后梯度指数衰减。ReLU 导数为 0 或 1，缓解了这个问题。</details>

3. **(较难)** 万能近似定理说一层隐藏层就够了。为什么实际中深层网络比浅层宽网络更好？
   <details><summary>💡 提示</summary>浅层宽网络需要指数级神经元才能达到深层网络的表达能力。深度 = 参数效率高 = 更好的归纳偏置。</details>

---
---

## 学完后可以完成

- [[05-计算机视觉-课后作业-02-两层网络与反向传播|HW02]]：实现两层全连接网络前向与反向

> 作业入口由 frontmatter `requires` 维护（唯一事实源），下方 Dataview 反向派生当前卡可完成的全部作业。
## 🔗 知识图谱

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
