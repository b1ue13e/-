---
type: study
topic: "RNN 时序建模"
tags: [学习, 时间序列, RNN, 深度学习]
created: 2026-04-16
updated: 2026-08-05
status: completed
difficulty: intermediate
concept: ["循环神经网络", "隐藏状态", "截断反向传播"]
prerequisites: ["矩阵乘法", "神经网络", "滑动窗口"]
related: ["LSTM与GRU", "Transformer时序", "滚动回测"]
flow: knowledge
kind: concept
source: "PyTorch Sequence Models tutorial"
anki_deck: "时间序列分析::深度学习"
anki_tags: [时间序列, RNN, 隐藏状态]
---

# RNN 时序建模

## 0. 核心问题

普通前馈网络把每个样本视为固定向量。RNN 用共享递推状态压缩截至当前的历史：

$$h_t=\tanh(W_{xh}x_t+W_{hh}h_{t-1}+b_h),\qquad
\hat y_t=W_{hy}h_t+b_y.$$

同一组参数跨时间复用，因此能够处理可变长度序列。隐藏状态是历史的有损摘要，不是“完整记忆”。

## 1. 手算一次前向传播

标量模型 $h_t=\tanh(x_t+0.5h_{t-1})$，$h_0=0$，输入 `[1,0,-1]`：

$$h_1=\tanh(1)\approx0.762,$$
$$h_2=\tanh(0.381)\approx0.364,$$
$$h_3=\tanh(-1+0.182)\approx-0.674.$$

同一个输入 0 在不同历史状态下会产生不同输出，这就是递推上下文。

## 2. 为什么梯度会消失或爆炸

跨时间梯度包含许多 Jacobian 的乘积，简化看类似

$$\frac{\partial h_T}{\partial h_t}\approx\prod_{j=t+1}^T W_{hh}'\operatorname{diag}(1-h_j^2).$$

乘积的典型尺度长期小于 1 会衰减，大于 1 会爆炸。梯度裁剪主要控制爆炸，LSTM/GRU 的门控加法路径缓解衰减，但都不保证无限记忆。

## 3. 输入输出设计

| 任务 | 输入 | 输出 |
|---|---|---|
| one-to-one rolling | 历史窗口 | 下一期 |
| direct multi-horizon | 历史窗口 | 固定多个未来步 |
| sequence-to-sequence | 编码历史 | 逐步解码未来 |
| global model | 多条序列 + ID/静态特征 | 各序列未来 |

窗口长度、隐藏维度和 horizon 必须在滚动验证内选择。训练样本窗口可重叠，但验证/测试预测原点不能泄漏。

## 4. 可运行 PyTorch 例子

先安装：`python -m pip install torch`。

```python
import numpy as np
import torch
from torch import nn

torch.manual_seed(51)
np.random.seed(51)
t = np.arange(360)
y = np.sin(2 * np.pi * t / 20).astype("float32")

window = 30
X = np.stack([y[i:i + window] for i in range(len(y) - window)])
target = y[window:]
X = torch.tensor(X[:, :, None])       # batch, time, feature
target = torch.tensor(target[:, None])
split = 260

class SmallRNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.rnn = nn.RNN(1, 12, batch_first=True)
        self.head = nn.Linear(12, 1)
    def forward(self, x):
        out, _ = self.rnn(x)
        return self.head(out[:, -1])

model = SmallRNN()
optimizer = torch.optim.Adam(model.parameters(), lr=0.02)
loss_fn = nn.MSELoss()
for _ in range(120):
    optimizer.zero_grad()
    loss = loss_fn(model(X[:split]), target[:split])
    loss.backward()
    torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
    optimizer.step()

with torch.no_grad():
    pred = model(X[split:])
    mae = torch.mean(torch.abs(pred - target[split:])).item()
    naive = torch.mean(torch.abs(X[split:, -1, 0:1] - target[split:])).item()
print({"rnn_mae": round(mae, 4), "naive_mae": round(naive, 4)})
```

这是固定切分的教学 smoke test，不替代多个滚动起点。真实实验还要在每个训练窗口拟合缩放，并与 seasonal naïve 比较。

## 5. 常见误区

- 最后隐藏状态包含全部历史：它是有限维压缩，信息会丢失。
- 序列越长越好：长窗口增加优化难度和陈旧信息。
- 训练 loss 低即预测好：重叠窗口和一步任务会让 naïve 也很强。
- 隐藏状态可直接解释：状态坐标缺乏唯一业务含义。
- RNN 能替代信息边界：窗口构造仍可泄漏未来。

## 6. 闭卷验收与自测

1. 写出 RNN 状态更新式。`#自测题/基础`
2. 手算三步标量状态。`#自测题/基础`
3. 梯度为什么会消失/爆炸？`#自测题/中等`
4. 梯度裁剪解决哪一类问题？`#自测题/中等`
5. 如何公平比较 RNN 与 ARIMA/naïve？`#自测题/较难`

> [!answer]- 自测答案
> 1. 当前输入与上一隐藏状态经共享参数和非线性变换。  
> 2. 参见第 1 节。  
> 3. 跨时间 Jacobian 连乘长期收缩或放大。  
> 4. 主要限制梯度爆炸，不保证解决长期依赖。  
> 5. 同一预测原点、horizon、信息集和滚动指标，包含调参成本与基线。

## 7. 双链与来源

- 下游：[[LSTM与GRU在时序中的应用]]、[[Transformer 时序预测]]
- 评估：[[滚动回测与预测区间]]
- 实现来源：[PyTorch Sequence Models tutorial](https://pytorch.org/tutorials/beginner/nlp/sequence_models_tutorial.html)

## 🃏 Anki 卡片

### Card 1
Q: RNN 隐藏状态为什么不是完整历史？
A: 它用有限维向量递推压缩历史，容量、参数和优化都会导致信息丢失。
Tags: 时间序列 RNN

