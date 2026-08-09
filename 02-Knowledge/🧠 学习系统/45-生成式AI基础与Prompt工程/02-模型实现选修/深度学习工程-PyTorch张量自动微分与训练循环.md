---
type: study
topic: "PyTorch 张量、自动微分与训练循环"
course: "生成式AI基础与Prompt工程"
tags: [学习, 45-生成式AI基础与Prompt工程, PyTorch, 自动微分]
created: 2026-08-05
status: completed
mastery: not_started
difficulty: beginner
stage_moc: "[[🧭 阶段2-模型实现选修]]"
concept: ["张量形状", "自动微分", "训练循环"]
prerequisites: ["神经网络表达-ReLU分段线性逻辑门与泛化", "课程前置-神经网络数学-凸性几何链式法则与优化"]
related: ["训练优化-交叉熵AdamW调度梯度裁剪与检查点", "生成模型数学-高斯KL重参数化与扩散后验"]
upstream: ["[[神经网络表达-ReLU分段线性逻辑门与泛化]]", "[[课程前置-Python-JSON测试与实验复现]]"]
flow: knowledge
kind: concept
source: "MIT OCW 6.7960 Deep Learning Fall 2024 Homework 1 and 5; PyTorch official tutorials"
source_url: "https://ocw.mit.edu/courses/6-7960-deep-learning-fall-2024/"
accessed: 2026-08-09
license: "MIT OCW 为 CC BY-NC-SA 4.0；PyTorch 文档按其站点许可"
anki_deck: "45-生成式AI基础与Prompt工程::深度学习工程"
anki_tags: [PyTorch, Tensor, Autograd, 训练循环]
---

# 深度学习工程：PyTorch 张量、自动微分与训练循环

## 0. 学习边界

- **类别**：A 类（MIT HW1/HW5 和 CS336 A1 的代码先修）。
- **判断理由**：只懂公式仍会在 batch 维、梯度清零、训练/评估模式和 checkpoint 上失败。本卡给出从纯函数到 PyTorch 的最短工程链。

## 1. 这个知识点解决什么问题？

> 怎样把数学里的向量、函数和梯度变成可批处理、可求导、可优化、可复现的代码？

官方深度学习作业通常留下模块或 `FIXME`，要求学习者补前向、反向、训练和测试。完成这些任务需要理解每个 API 背后的状态，而不只是复制训练循环。

## 2. 为什么它重要？它有什么用？

- **张量形状**：多数实现错误不是公式错误，而是 batch、feature、sequence 维混淆。
- **自动微分**：计算图按链式法则累积梯度，支撑神经网络训练。
- **状态管理**：参数梯度、优化器状态、随机数和 train/eval 模式都会改变结果。
- **作业定位**：支撑 MIT HW1 Q8、Q10–Q12、Q14–Q15，MIT HW5 Q4–Q6/Q12–Q13，以及 CS336 A1 训练循环。

## 3. 学它之前需要哪些前置知识？

1. [[课程前置-神经网络数学-凸性几何链式法则与优化]]：理解局部导数与参数更新。
2. [[课程前置-Python-JSON测试与实验复现]]：函数、异常、断言、随机种子和测试。

## 4. 用直觉语言解释它

> “张量是带形状的数字容器；计算图是记录这些容器怎样产生的账本；`backward()` 从损失沿账本倒查每个参数的责任。”

- `forward` 产生预测和标量损失。
- `backward` 把梯度累积到叶子参数的 `.grad`。
- 优化器读取梯度更新参数；下一轮前必须清零旧梯度。
- 一句话本质：**训练循环是数据、模型、损失、梯度、更新、评估六个状态转换的闭环。**

## 5. 正式定义、核心公式、符号解释

对 batch $X\in\mathbb{R}^{B\times d}$、权重 $W\in\mathbb{R}^{m\times d}$、偏置 $b\in\mathbb{R}^{m}$：

$$Z=XW^T+b,\qquad \hat Y=f_\theta(X),\qquad
L(\theta)=\frac1B\sum_{i=1}^B\ell(\hat y_i,y_i).$$

梯度更新：

$$g_t=\nabla_\theta L_t,\qquad \theta_{t+1}=\theta_t-\eta g_t.$$

| 对象/API | 含义 | 关键约束 | 常见故障 |
| :--- | :--- | :--- | :--- |
| `Tensor` | 同类型多维数组 | 明确 shape/dtype/device | 广播掩盖维度错 |
| `requires_grad` | 是否追踪梯度 | 参数通常为 True | 误用 `detach` 断图 |
| `loss.backward()` | 反向累积梯度 | 损失通常为标量 | 重复反传、未清零 |
| `optimizer.step()` | 用梯度更新参数 | 必须在 backward 后 | eval 阶段误更新 |
| `model.train()/eval()` | 切换模块行为 | 影响 dropout/BN | 验证结果漂移 |
| `torch.no_grad()` | 禁止建反向图 | 评估/推理使用 | 训练时误包裹 |

### 最小 PyTorch 训练顺序

```text
model.train()
for x, y in loader:
    optimizer.zero_grad(set_to_none=True)
    prediction = model(x)
    loss = criterion(prediction, y)
    loss.backward()
    optimizer.step()
model.eval()
with torch.no_grad():
    validation_prediction = model(validation_x)
```

官方作业使用真实 PyTorch/Colab 环境；本库不宣称标准库示例可以替代官方 GPU 实验。

## 6. 推导思路和思想来源

1. **标量链式法则**：若 $L=(wx-y)^2/2$，则 $\partial L/\partial w=(wx-y)x$。
2. **计算图局部化**：每个运算保存输入与局部导数，反向时乘以上游梯度。
3. **向量化**：把样本循环折叠到 batch 维，保证第一维始终表示样本。
4. **状态分离**：训练允许求导和更新；验证冻结参数、关闭随机训练行为。
5. **工程闭环**：单 batch 过拟合 → 梯度检查 → 小数据训练 → 验证 → 保存/恢复，逐层扩大问题。

## 7. 例子：基础 → 中等 → 实际应用

### 例子 1：基础例子（可手算）

$x=2,w=1,y=5$，预测为 2，损失为 $(2-5)^2/2=4.5$，梯度 $(2-5)\times2=-6$。若学习率 0.1，新权重为 $1-0.1(-6)=1.6$，损失应下降。

### 例子 2：中等例子

若 logits shape 为 `[B, C]`，标签 shape 应为 `[B]` 的类别索引。把标签误做成 `[B,1]` 可能触发广播或 API 错误；先写 `assert logits.shape[0] == labels.shape[0]`，再检查类别维。

### 例子 3：实际应用例子（可运行 Python）

```python
# 输入：线性数据 y=2x+1；输出：手写自动微分训练后的 w、b。
class Value:
    def __init__(self, data, children=(), backward=lambda: None):
        self.data, self.grad = float(data), 0.0
        self.children, self._backward = children, backward

    def __add__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data + other.data, (self, other))
        def backward():
            self.grad += out.grad
            other.grad += out.grad
        out._backward = backward
        return out

    __radd__ = __add__

    def __mul__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data * other.data, (self, other))
        def backward():
            self.grad += other.data * out.grad
            other.grad += self.data * out.grad
        out._backward = backward
        return out

    __rmul__ = __mul__

    def __neg__(self):
        return self * -1

    def __sub__(self, other):
        return self + (-other)

    def backward(self):
        order, seen = [], set()
        def visit(node):
            if id(node) not in seen:
                seen.add(id(node))
                for child in node.children:
                    visit(child)
                order.append(node)
        visit(self)
        self.grad = 1.0
        for node in reversed(order):
            node._backward()

w, b = Value(0.0), Value(0.0)
data = [(0.0, 1.0), (1.0, 3.0), (2.0, 5.0)]
for _ in range(120):
    losses = []
    for x, y in data:
        error = w * x + b - y
        losses.append(error * error)
    loss = sum(losses, Value(0.0)) * (1 / len(losses))
    w.grad = b.grad = 0.0
    loss.backward()
    w.data -= 0.08 * w.grad
    b.data -= 0.08 * b.grad
print(round(w.data, 3), round(b.data, 3), round(loss.data, 6))
assert abs(w.data - 2.0) < 0.05 and abs(b.data - 1.0) < 0.05
```

### 例子 4：PyTorch CPU 对照（真实 API）

```python
# 依赖：PyTorch 2.x CPU；输入 y=2x+1；输出训练后的预测与 loss。
import torch
from torch import nn

torch.manual_seed(7)
x = torch.tensor([[0.0], [1.0], [2.0], [3.0]])
y = 2 * x + 1
model = nn.Sequential(nn.Linear(1, 8), nn.ReLU(), nn.Linear(8, 1))
optimizer = torch.optim.SGD(model.parameters(), lr=0.05)
criterion = nn.MSELoss()

model.train()
for _ in range(300):
    optimizer.zero_grad(set_to_none=True)
    prediction = model(x)
    loss = criterion(prediction, y)
    loss.backward()
    optimizer.step()

model.eval()
with torch.no_grad():
    final_loss = criterion(model(x), y).item()
print(round(final_loss, 6), tuple(model(x).shape))
assert final_loss < 1e-3
assert tuple(model(x).shape) == (4, 1)
```

若本机没有 PyTorch，应使用官方 Colab/仓库环境安装，而不是把该块改写成伪 API。标准库 `Value` 例子负责解释机制，PyTorch 例子负责验证真实训练状态，两者不能互相冒充。

## 8. 常见误区和易混概念

- **误区 1**：`backward()` 会覆盖梯度。PyTorch 默认累积，因此必须显式清零。
- **误区 2**：`model.eval()` 等于关闭梯度。它只改变部分模块行为；还需 `torch.no_grad()`。
- **误区 3**：loss 下降就证明实现正确。标签泄漏、错误切分或错误目标也能产生漂亮曲线。
- **误区 4**：CPU 微型实验复现了官方规模结果。它只验证接口、形状与逻辑。

| 概念 | 核心问题 | 关键区别 | 使用场景 |
| :--- | :--- | :--- | :--- |
| 自动微分 | 如何算导数 | 构建/遍历计算图 | `backward` |
| 优化器 | 如何更新参数 | 使用梯度和内部状态 | `step` |
| 训练模式 | 模块是否采用训练行为 | 影响 dropout/BN | 训练循环 |
| 无梯度上下文 | 是否记录计算图 | 影响内存和反传 | 验证/推理 |

## 9. 课程连接

- [[神经网络表达-ReLU分段线性逻辑门与泛化]] 提供可训练模块的最小对象，[[课程前置-Python-JSON测试与实验复现]] 提供断言与复现纪律。
- [[训练优化-交叉熵AdamW调度梯度裁剪与检查点]] 在此基础上加入优化器、调度与恢复状态。
- [[生成模型数学-高斯KL重参数化与扩散后验]] 和 Transformer 实现都会复用 shape、梯度与 train/eval 边界。

## 10. 闭卷复现任务

- [ ] 写出 batch 线性层的形状变化。
- [ ] 手算一个标量平方损失梯度。
- [ ] 解释梯度为什么会累积。
- [ ] 按正确顺序写出训练循环六步。
- [ ] 区分 `train/eval` 与 `no_grad`。
- [ ] 解释 `detach` 会怎样影响计算图。
- [ ] 设计单 batch 过拟合测试。
- [ ] 写出中心有限差分梯度检查。
- [ ] 列出 checkpoint 最少要保存的状态。
- [ ] 说明 CPU 微型验证与官方复现的边界。

## 11. 自测题：5 道

1. 为什么每轮更新前要清零梯度？ `#自测题/基础`
2. `[32, 128] @ [64, 128].T` 的输出形状是什么？ `#自测题/基础`
3. 验证阶段为什么同时需要 `eval()` 与 `no_grad()`？ `#自测题/中等`
4. 训练 loss 不下降时，按什么顺序检查数据、前向、损失、梯度与更新？ `#自测题/中等`
5. 设计一组测试证明“保存后恢复训练”等价于不中断训练，并列出需固定的随机状态。 `#自测题/较难`

> [!question]- 参考答案与评分点
> 1. 梯度默认累积，否则混入历史 batch。2. `[32,64]`。3. 前者切换模块行为，后者停止建图。4. 单样本与 shape → 前向数值 → 手算 loss → 梯度非空/有限 → 参数确实变化。5. 保存模型、优化器、步数、调度器与 Python/NumPy/PyTorch RNG，比较后续损失和参数。

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/45-生成式AI基础与Prompt工程"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

## 12. 我的主动回忆区

- **训练循环**：
- **shape 契约**：
- **调试顺序**：
- [ ] 明天  [ ] 3 天后  [ ] 7 天后  [ ] 14 天后

## 13. 给 Obsidian 的归档建议

- 本卡承担 PyTorch 工程主线；AdamW、学习率调度与 checkpoint 细节放入独立训练优化卡。
- 做官方作业时以官方环境和测试为准，记录本课删减规模，不把标准库演示冒充 PyTorch 结果。

## 🃏 Anki 卡片

Q: 一个最小训练 step 的顺序是什么？
A: 清梯度、前向、算损失、反向、参数更新；验证另行切换 eval 并关闭梯度。

Q: `model.eval()` 为什么不能替代 `torch.no_grad()`？
A: eval 只改变 dropout/BN 等模块行为，不会停止构建自动微分图。

