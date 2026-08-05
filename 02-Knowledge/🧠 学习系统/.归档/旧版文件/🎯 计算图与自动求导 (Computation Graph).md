---
type: study
topic: "计算图与自动求导 (Computation Graph)"
created: 2026-08-05
status: ongoing
difficulty: intermediate
concept:
  - 计算图
  - 自动求导
  - PyTorch Autograd
  - 动态图
prerequisites:
  - 反向传播
  - 链式法则
related:
  - 反向传播算法
  - PyTorch框架
flow: knowledge
kind: concept
source: "D2L Ch.5; CS231n A1"
anki_deck: "05-计算机视觉::02-深度学习内核"
anki_tags:
  - 学习
  - 深度学习
  - 计算机视觉
  - 计算图
  - 自动求导
  - Autograd
tags:
  - 学习
  - 深度学习
  - 计算机视觉
  - 计算图
  - 自动求导
  - Autograd
---

# 🎯 计算图与自动求导 (Computation Graph)

---

## 0. 先判断它值不值得深挖

- **类别**：**A 类（核心概念，必须深挖）**
- **判断理由**：计算图（Computational Graph）是所有现代化深度学习框架（PyTorch、TensorFlow、JAX）实现**通用自动微分（Autograd）**的基础设施。它将复杂的神经网络数学表达式抽象为一个**有向无环图 (DAG)**，把求导过程转化为图上的节点拓扑遍历与局部导数乘积。彻底搞懂计算图，才能明白 PyTorch 中 `requires_grad=True`、`grad_fn`、动态图与静态图的区别，以及如何正确编写自定义算子。

---

## 1. 这个知识点解决什么问题？

> **We Encountered a Problem (我们遇到了什么麻烦)**：
> 在没有计算图之前，要训练一个新的神经网络架构（例如 ResNet 或 Transformer），算法工程师必须用纸笔手动推导每个参数的偏导数公式，然后再手写 C++/Python 梯度代码。只要网络结构稍微改变一处（比如增加一个 Residual 连接或改变损失函数），整套求导公式就得**从头重推重新硬编码**！
> 这种手动硬编码极易出错且开发效率低下。我们需要一种机制，让计算机能够**自动记录任意复杂运算的执行轨迹，并自动推导出精确梯度**。

---

## 2. 为什么它重要？它有什么用？

- **连接大图景**：计算图是反向传播算法在现代软件工程中的通用数据结构载体。不理解计算图，就无法理解框架内存占用（为何前向传播需要保存中间 Tensor 激活值）、无法排查“尝试对释放的计算图再次求导”的 RuntimeError，也无法做模型导出与推理优化（ONNX/TensorRT 图优化）。
- **实际应用场景**：动态计算图构造（PyTorch）、静态图编译优化（TensorFlow Graph/TorchScript）、高阶导数计算（如 GAN 中的梯度惩罚 GP）。
- **高频考点/任务**：手画复杂公式的计算图、动态图 vs 静态图对比、计算图前向/反向拓扑排序手推、PyTorch 计算图内存释放机制。

---

## 3. 学它之前需要哪些前置知识？

最小必要背景：

1. **[[02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/链式法则|链式法则]]**：标量复合函数偏导数的连乘规则，计算图反向遍历时沿边传递的就是局部导数（Local Gradients）。
2. **[[10-数据结构与算法/01-图论基础/有向无环图|有向无环图 (DAG) 与拓扑排序]]**：无环的有向图，节点代表变量或算子，边代表数据依赖关系。

---

## 4. 用直觉语言解释它

> «“这东西其实就像……”»

- **直觉类比**：计算图就像一张**极度详尽的工厂工程施工流水图**：
  - **前向传播**：原材料输入（Tensor）经过一个个加工车间（加法、乘法、ReLU算子），产生中间零部件并最终装配成成品（Loss 标量）。施工图把每一步谁依赖谁记录得清清楚楚；
  - **反向传播**：质量检查员拿这张施工图逆向倒流，每个车间根据自己车间的加工规则（局部导数 `vjp`），把上游传过来的质量隐患（梯度）乘上自己的加工系数，精确传回给上一级零件供应商。
- **为什么很自然**：任何复杂的数学表达式，本质上都可以分解为基础算子（加、减、乘、除、Sin、Exp）的复合，只要框架知道每个基础算子的导数，按施工图逆向相乘即可！
- **一句话直觉本质**：用有向图记录运算轨迹，把复杂求导分解为基础算子局部导数的逆向拓扑累乘。

---

## 5. 正式定义、核心公式、符号解释

### 1. 核心定义
计算图是一个由节点集合 $V$ 和有向边集合 $E$ 组成的有向无环图 $\mathcal{G} = (V, E)$：
- **节点 $v \in V$**：代表变量（张量 Tensor）或操作符（算子 Operation）；
- **有向边 $(u, v) \in E$**：表示节点 $v$ 的计算依赖于节点 $u$ 的输出。

### 2. 计算图上的反向传播公式
对于图中任意节点 $u$，设其所有直接后继节点集合为 $\text{Children}(u)$，最终标量目标为 $L$（Loss），则 $L$ 对节点 $u$ 的梯度为：
$$\frac{\partial L}{\partial u} = \sum_{v \in \text{Children}(u)} \frac{\partial L}{\partial v} \cdot \frac{\partial v}{\partial u}$$

### 3. 符号说明表

| 符号 | 含义 | 取值范围 / 量纲 | 备注 |
| :--- | :--- | :--- | :--- |
| $\mathcal{G}$ | 计算图 (DAG) | N/A | 图结构数据 |
| $v$ | 图节点 (Node) | Tensor / Operation | 变量或运算符 |
| $\frac{\partial v}{\partial u}$ | 局部导数 (Local Gradient) | 依赖算子定义 | 算子自身求导法则 |
| $\text{grad\_fn}$ | 反向函数指针 | PyTorch Node 引用 | 指向创建该 Tensor 的算子 |
| `requires_grad` | 是否追踪梯度标志 | Boolean | True 时建图 |

---

## 6. 推导思路和思想来源

- **最初困难**：直接符号求导（Symbolic Differentiation）会导致“表达式膨胀”（例如对 $\sin(x \cdot e^x)$ 迭代求导，公式长度呈指数级暴增）；数值求导又不够精准且极慢。
- **关键转念**：结合代码执行过程！在代码运行的同时构建图结构，求导时**只传递数值梯度，不生成符号公式**。
- **推导与构建主线**：
  1. **前向拓扑遍历**：按照数据依赖次序计算每个节点的值 $v_i = f_i(\text{Parents}(v_i))$，并保存需要的中间激活值；
  2. **反向拓扑遍历**：从损失节点 $L$ 出发，令 $\frac{\partial L}{\partial L} = 1$；
  3. 按照反向拓扑顺序，每个节点 $u$ 收集所有后继节点传回的 $\frac{\partial L}{\partial v} \frac{\partial v}{\partial u}$ 并累加（多元链式法则求和）；
  4. 遍历到叶子节点（Leaf Tensors, 即权重参数），完成梯度积累。

---

## 7. 例子：基础 → 中等 → 实际应用

### 例子 1：基础例子（标量算子手绘与求导）
- **题目**：设表达式 $e = (a + b) \cdot (b + 1)$，其中 $a=2, b=1$。构建计算图并求 $\frac{\partial e}{\partial a}$ 和 $\frac{\partial e}{\partial b}$。
- **解答过程**：
  1. 引入中间节点：$c = a + b$, $d = b + 1$, 最终输出 $e = c \cdot d$。
  2. 前向计算：
     - $a=2, b=1$
     - $c = 2 + 1 = 3$
     - $d = 1 + 1 = 2$
     - $e = 3 \times 2 = 6$
  3. 反向传播（设起点 $\frac{\partial e}{\partial e} = 1$）：
     - 对 $c$：$\frac{\partial e}{\partial c} = d = 2$
     - 对 $d$：$\frac{\partial e}{\partial d} = c = 3$
     - 对 $a$：$\frac{\partial e}{\partial a} = \frac{\partial e}{\partial c} \frac{\partial c}{\partial a} = 2 \times 1 = 2$
     - 对 $b$（两条路径汇合）：$\frac{\partial e}{\partial b} = \frac{\partial e}{\partial c} \frac{\partial c}{\partial b} + \frac{\partial e}{\partial d} \frac{\partial d}{\partial b} = 2 \times 1 + 3 \times 1 = 5$。
- **🤔 追问**：为什么 $b$ 的梯度是两条路径的乘积之和？
  - *答*：因为 $b$ 在计算图中同时影响了 $c$ 和 $d$，根据全微分定理，其对最终输出 $e$ 的总贡献是所有依赖路径偏导的累加！

### 例子 2：中等例子（PyTorch 动态图构建过程解析）
分析以下 PyTorch 代码的计算图结构与节点引用关系：

```python
import torch

x = torch.tensor(2.0, requires_grad=True) # 叶子节点 Leaf Node
w = torch.tensor(3.0, requires_grad=True) # 叶子节点 Leaf Node
b = torch.tensor(1.0, requires_grad=True) # 叶子节点 Leaf Node

y = w * x # 产生中间节点 y, grad_fn=<MulBackward0>
z = y + b # 产生最终节点 z, grad_fn=<AddBackward0>

z.backward()
print(x.grad, w.grad, b.grad) # tensor(3.), tensor(2.), tensor(1.)
```

- **图结构**：
  `x, w` $\to$ `MulBackward0` $\to$ `y` $\to$ `AddBackward0` $\to$ `z` $\leftarrow$ `b`
- **内存生命周期**：当 `z.backward()` 执行完毕后，中间节点 `y` 的梯度被释放；再次调用 `z.backward()` 会报 `RuntimeError: Trying to backward through the graph a second time`。

### 例子 3：实际应用（利用计算图实现二阶导数 / 梯度惩罚）
在 WGAN-GP 等前沿模型中，需要对“梯度的范数”再次求导（二阶求导）。动态计算图天然支持这种高阶求导：

```python
import torch

x = torch.randn(4, 3, requires_grad=True)
y = (x ** 3).sum()

# 第一次求导：计算一阶梯度 grad_x
grad_x = torch.autograd.grad(outputs=y, inputs=x, create_graph=True)[0]

# create_graph=True 意味着求导过程本身也被构建成新的计算图！
# 对一阶梯度的范数再次求导（二阶导）
penalty = ((grad_x.norm(2, dim=1) - 1) ** 2).mean()
penalty.backward() # 顺畅完成二阶导数反向传播！
```

---

## 8. 常见误区和易混概念

### 误区 1：原地方向操作（In-place Operation）不影响计算图求导
- **错误直觉**：“在 PyTorch 中使用 `x += 1` 或 `x.add_(1)` 只是节省了显存，对反向传播没影响。”
- **为什么错**：计算图反向传播时，很多算子（如 Sigmoid、乘法）需要用到**前向传播保存的原始输入 Tensor 值**。如果你用 in-place 操作原地修改了该 Tensor，反向传播时导数计算将获取到错误的被修改值，PyTorch 会直接报错拦截 `RuntimeError: a view of a leaf Variable that requires grad is being modified in-place`。

### 概念对比表

| 概念 | 核心机制 | 优缺点 | 代表框架 / 场景 |
| :--- | :--- | :--- | :--- |
| **动态计算图 (Define-by-Run)** | 边执行代码边实时建图，每次前向传播重新建图 | 极其灵活，支持 Python 原生循环与分支，易调试 | PyTorch, JAX |
| **静态计算图 (Define-and-Run)** | 先定义图结构编译优化，再送入数据反复执行 | 无法使用 Python 自由控制流，调试困难，但推理部署性能极强 | TensorFlow 1.x, Caffe, TensorRT |

---

## 9. 相关知识点与 Obsidian 双链建议

### 上游依赖
- [[02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/链式法则|链式法则]]：计算图节点间传递梯度的数学基础。
- [[10-数据结构与算法/01-图论基础/有向无环图|有向无环图]]：计算图的数据结构原型。

### 下游延伸
- [[02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/PyTorchModule|PyTorchModule]]：利用计算图自动追踪模型内所有层参数。
- [[02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/自定义算子|自定义算子]]：手动编写拓展计算图节点的 `Function`。

### 横向关联
- [[02-Knowledge/🧠 学习系统/17-机器学习/03-正则优化/反向传播算法|反向传播算法]] ↔ [[02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/计算图|计算图]]：BP 是算法逻辑，计算图是工程实现结构。

---

## 10. 闭卷复现任务

- [ ] 1. 用一句话说清楚计算图解决什么问题（自动化通用高效求导）。
- [ ] 2. 用直觉语言解释它（«“这东西其实就像工程施工图……”»）。
- [ ] 3. 画出标量表达式的计算图并执行前反向计算。
- [ ] 4. 写出计算图节点梯度累加的求和公式。
- [ ] 5. 解释 PyTorch 中 `requires_grad` 和 `grad_fn` 的作用。
- [ ] 6. 讲出为什么 In-place 操作会导致 Autograd 报错。
- [ ] 7. 解释动态计算图与静态计算图的关键区别。
- [ ] 8. 说明什么情况下需要设置 `create_graph=True`。
- [ ] 9. 手绘 $e = (a+b)(b+1)$ 的计算图并推导分支路径梯度的累加。
- [ ] 10. 写出包含静态方法 `forward` 与 `backward` 的自定义算子伪代码。

---

## 11. 自测题：5 道

| 题号 | 类型 | 难度 | 考查点 |
| :--- | :--- | :--- | :--- |
| 1 | 概念辨析 | 基础 | 动态图与静态图的区别 |
| 2 | 编码实践 | 基础 | PyTorch `detach()` 割断计算图 |
| 3 | 规则判断 | 中等 | In-place 操作在 Autograd 中的限制 |
| 4 | 变式/综合 | 中等 | 计算图分支节点梯度的聚合方式 |
| 5 | 开放/架构 | 较难 | 计算图显存优化的重计算 (Checkpointing) 机制 |

### 题目与解析

#### 1. 关于 PyTorch 动态计算图的描述，错误的是？
- A. 每次调用 `forward()` 时都会重新构建一张新的计算图
- B. 叶子节点 (Leaf Tensor) 的 `grad_fn` 属性通常为 `None`
- C. 在使用 `with torch.no_grad():` 的上下文内部，操作依然会被记录到计算图中
- D. 计算图反向传播完成后，中间非叶子节点的梯度默认会被释放以节省内存

> [!question]- 答案解析
> - **答案**：C
> - **解析**：`with torch.no_grad():` 上下文会显式禁用 Autograd 引擎，在此区域内的所有 Tensor 操作都不会被构建入计算图，从而大幅节省显存和计算开销。
> - **对应误区**：误区 1。

#### 2. 在 PyTorch 中，如果对某个中间变量调用了 `.detach()`，计算图会发生什么变化？
> [!question]- 答案解析
> - **答案**：将该变量从当前计算图中断开，使其变为一个新的叶子节点 (`requires_grad=False`)。
> - **解析**：反向传播传播到该节点时会停止向后传递，常用于 GAN 训练中交替固定生成器或判别器参数。

#### 3. 为什么在计算图中，如果一个节点被多个后继节点依赖，它的梯度必须是各个后继节点传回梯度的“加和”而非“乘积”？
> [!question]- 答案解析
> - **答案**：由多元微积分的全微分定理与链式法则决定。
> - **解析**：若 $z = f(x, y)$ 且 $x = g(u), y = h(u)$，则 $u$ 的微小变化 $\Delta u$ 会同时通过 $x$ 和 $y$ 两条路径独立引发 $z$ 的变化。总变化量为 $\Delta z \approx \frac{\partial z}{\partial x} \Delta x + \frac{\partial z}{\partial y} \Delta y$。因此 $\frac{d z}{d u} = \frac{\partial z}{\partial x} \frac{d x}{d u} + \frac{\partial z}{\partial y} \frac{d y}{d u}$，即分支梯度必须加和。

#### 4. 在运行极深网络（如 1000 层 Transformer）时，前向传播保存所有中间激活值会导致显存爆炸。计算图如何解决这一痛点？
> [!question]- 答案解析
> - **答案**：梯度 checkpointing（激活重计算，Activation Recomputation）。
> - **解析**：在前向传播时不保存中间大部分激活值，只保留少数关键 checkpoint 节点；在反向传播需要某个区域的激活值时，临时重新跑一小段前向传播计算出来。用时间（额外计算）换取大幅显存节省！

#### 5. 【代码诊所】以下代码在运行 `loss.backward()` 时报错，请指出错误原因并修改：
```python
x = torch.tensor([2.0], requires_grad=True)
y = x * 2
y.add_(1) # 修改这一行
loss = y.sum()
loss.backward()
```
> [!question]- 答案解析
> - **答案**：`y.add_(1)` 是 in-place 原地修改操作，破坏了计算图节点的原始历史状态。
> - **修改方法**：改为非 inplace 操作 `y = y + 1`，PyTorch 将创建新的计算图节点，Autograd 正常运行。

---

## 12. 我的主动回忆区

### 我的闭卷复述
> 不看上文，用自己的话解释这个知识点：

### 我的推导复现
> 不看上文，尝试写出核心公式或推导主线：

### 我的错误与卡点
- 

### 下次复习日期
- [ ] 明天
- [ ] 3 天后
- [ ] 7 天后
- [ ] 14 天后

---

## 13. 给 Obsidian 的归档建议

- **归档目录**：`02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/`
- **建议双链**：
  - [[02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/🧠 第二阶段：深度学习内核|第二阶段：深度学习内核]]
  - [[02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/链式法则|链式法则]]
  - [[02-Knowledge/🧠 学习系统/17-机器学习/03-正则优化/反向传播算法|反向传播算法]]
  - [[02-Knowledge/🧠 学习系统/05-计算机视觉/02-深度学习内核/PyTorchModule|PyTorchModule]]
- **建议标签**：`#学习` `#深度学习` `#计算图` `#Autograd` `#PyTorch` `#动态图` `#拓扑排序`
