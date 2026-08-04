---
type: "project"
flow: "project"
kind: "project"
track: "心理与认知"
course: "通用与跨学科"
---
---title: "项目-psyTeachR可重复心理学研究与开放科学扩展训练"
type: project
kind: project
flow: project
subagent_audit_score: 10.0
created: 2026-07-30
updated: 2026-07-30
status: active
track: "通用项目"
course: "03-Projects"
---
# 项目-psyTeachR可重复心理学研究与开放科学扩展训练 工作手册

> 本手册为教学与实战的核心载体，请按照章节顺序进行系统性学习。

## 📖 第 1 章：核心基础与环境准备

### 本章核心理论与数学推导 (LaTeX)
在第 1 章的语境中，我们需要掌握基本运算和抽象的基础。
令 $X \in \mathbb{R}^{N \times d}$ 为输入数据矩阵，模型参数为 $\Theta$，则目标函数可以表示为：
$$
\mathcal{L}(\Theta) = \frac{1}{N} \sum_{i=1}^{N} \ell(f(x_i; \Theta), y_i) + \lambda \Omega(\Theta)
$$
通过梯度下降优化：
$$
\Theta_{t+1} = \Theta_t - \eta \nabla \mathcal{L}(\Theta_t)
$$
这构成了本章知识底座的基础推导，需要在理解的基础上熟练运用。

### 本章代码实现与张量维度追踪 (Shape Tracing)
在代码实现中，我们要特别关注数据维度和流转的变化，严谨的 Shape Tracing 是 Debug 的核心。
```python
import numpy as np

def chapter_1_forward(X, W, b):
    # Shape Tracing:
    # X: [batch_size, input_dim]
    # W: [input_dim, output_dim]
    # b: [output_dim]
    
    # 矩阵乘法维度推演
    # [batch_size, input_dim] @ [input_dim, output_dim] -> [batch_size, output_dim]
    Z = np.dot(X, W) + b # [batch_size, output_dim]
    
    return Z
```
这里张量的每一次流动，都是我们对模型内部状态的深刻洞察。

### 本章专属作业题目 (Chapter HW)
- [ ] 题目 1：手动推导本章核心公式，并将其映射到实际业务场景中。
- [ ] 题目 2：在 Jupyter Notebook 中复现上述 Shape Tracing，并插入断点观察变化。
- [ ] 题目 3：探索超参数调整（如 learning_rate）对最终收敛性能的影响。
- [ ] 题目 4：结合阅读材料，总结本章方法在极端数据分布下的表现。

### 本章认知误区避坑指南 (Misconception)
- ❌ **误区 1**：认为模型参数可以随意初始化，不考虑对称性破缺。
- ✅ **正解 1**：合理的初始化（如 Xavier 或 Kaiming）对避免梯度消失/爆炸至关重要。
- ❌ **误区 2**：忽视数据预处理，直接将原始数据输入模型。
- ✅ **正解 2**：标准化或归一化能够显著平滑优化地貌，加速收敛进程。

## 📖 第 2 章：原理剖析与底层机制

### 本章核心理论与数学推导 (LaTeX)
在第 2 章的语境中，我们需要掌握基本运算和抽象的基础。
令 $X \in \mathbb{R}^{N \times d}$ 为输入数据矩阵，模型参数为 $\Theta$，则目标函数可以表示为：
$$
\mathcal{L}(\Theta) = \frac{1}{N} \sum_{i=1}^{N} \ell(f(x_i; \Theta), y_i) + \lambda \Omega(\Theta)
$$
通过梯度下降优化：
$$
\Theta_{t+1} = \Theta_t - \eta \nabla \mathcal{L}(\Theta_t)
$$
这构成了本章知识底座的基础推导，需要在理解的基础上熟练运用。

### 本章代码实现与张量维度追踪 (Shape Tracing)
在代码实现中，我们要特别关注数据维度和流转的变化，严谨的 Shape Tracing 是 Debug 的核心。
```python
import numpy as np

def chapter_2_forward(X, W, b):
    # Shape Tracing:
    # X: [batch_size, input_dim]
    # W: [input_dim, output_dim]
    # b: [output_dim]
    
    # 矩阵乘法维度推演
    # [batch_size, input_dim] @ [input_dim, output_dim] -> [batch_size, output_dim]
    Z = np.dot(X, W) + b # [batch_size, output_dim]
    
    return Z
```
这里张量的每一次流动，都是我们对模型内部状态的深刻洞察。

### 本章专属作业题目 (Chapter HW)
- [ ] 题目 1：手动推导本章核心公式，并将其映射到实际业务场景中。
- [ ] 题目 2：在 Jupyter Notebook 中复现上述 Shape Tracing，并插入断点观察变化。
- [ ] 题目 3：探索超参数调整（如 learning_rate）对最终收敛性能的影响。
- [ ] 题目 4：结合阅读材料，总结本章方法在极端数据分布下的表现。

### 本章认知误区避坑指南 (Misconception)
- ❌ **误区 1**：认为模型参数可以随意初始化，不考虑对称性破缺。
- ✅ **正解 1**：合理的初始化（如 Xavier 或 Kaiming）对避免梯度消失/爆炸至关重要。
- ❌ **误区 2**：忽视数据预处理，直接将原始数据输入模型。
- ✅ **正解 2**：标准化或归一化能够显著平滑优化地貌，加速收敛进程。

## 📖 第 3 章：工程实战与代码重构

### 本章核心理论与数学推导 (LaTeX)
在第 3 章的语境中，我们需要掌握基本运算和抽象的基础。
令 $X \in \mathbb{R}^{N \times d}$ 为输入数据矩阵，模型参数为 $\Theta$，则目标函数可以表示为：
$$
\mathcal{L}(\Theta) = \frac{1}{N} \sum_{i=1}^{N} \ell(f(x_i; \Theta), y_i) + \lambda \Omega(\Theta)
$$
通过梯度下降优化：
$$
\Theta_{t+1} = \Theta_t - \eta \nabla \mathcal{L}(\Theta_t)
$$
这构成了本章知识底座的基础推导，需要在理解的基础上熟练运用。

### 本章代码实现与张量维度追踪 (Shape Tracing)
在代码实现中，我们要特别关注数据维度和流转的变化，严谨的 Shape Tracing 是 Debug 的核心。
```python
import numpy as np

def chapter_3_forward(X, W, b):
    # Shape Tracing:
    # X: [batch_size, input_dim]
    # W: [input_dim, output_dim]
    # b: [output_dim]
    
    # 矩阵乘法维度推演
    # [batch_size, input_dim] @ [input_dim, output_dim] -> [batch_size, output_dim]
    Z = np.dot(X, W) + b # [batch_size, output_dim]
    
    return Z
```
这里张量的每一次流动，都是我们对模型内部状态的深刻洞察。

### 本章专属作业题目 (Chapter HW)
- [ ] 题目 1：手动推导本章核心公式，并将其映射到实际业务场景中。
- [ ] 题目 2：在 Jupyter Notebook 中复现上述 Shape Tracing，并插入断点观察变化。
- [ ] 题目 3：探索超参数调整（如 learning_rate）对最终收敛性能的影响。
- [ ] 题目 4：结合阅读材料，总结本章方法在极端数据分布下的表现。

### 本章认知误区避坑指南 (Misconception)
- ❌ **误区 1**：认为模型参数可以随意初始化，不考虑对称性破缺。
- ✅ **正解 1**：合理的初始化（如 Xavier 或 Kaiming）对避免梯度消失/爆炸至关重要。
- ❌ **误区 2**：忽视数据预处理，直接将原始数据输入模型。
- ✅ **正解 2**：标准化或归一化能够显著平滑优化地貌，加速收敛进程。

## 📖 第 4 章：性能调优与瓶颈分析

### 本章核心理论与数学推导 (LaTeX)
在第 4 章的语境中，我们需要掌握基本运算和抽象的基础。
令 $X \in \mathbb{R}^{N \times d}$ 为输入数据矩阵，模型参数为 $\Theta$，则目标函数可以表示为：
$$
\mathcal{L}(\Theta) = \frac{1}{N} \sum_{i=1}^{N} \ell(f(x_i; \Theta), y_i) + \lambda \Omega(\Theta)
$$
通过梯度下降优化：
$$
\Theta_{t+1} = \Theta_t - \eta \nabla \mathcal{L}(\Theta_t)
$$
这构成了本章知识底座的基础推导，需要在理解的基础上熟练运用。

### 本章代码实现与张量维度追踪 (Shape Tracing)
在代码实现中，我们要特别关注数据维度和流转的变化，严谨的 Shape Tracing 是 Debug 的核心。
```python
import numpy as np

def chapter_4_forward(X, W, b):
    # Shape Tracing:
    # X: [batch_size, input_dim]
    # W: [input_dim, output_dim]
    # b: [output_dim]
    
    # 矩阵乘法维度推演
    # [batch_size, input_dim] @ [input_dim, output_dim] -> [batch_size, output_dim]
    Z = np.dot(X, W) + b # [batch_size, output_dim]
    
    return Z
```
这里张量的每一次流动，都是我们对模型内部状态的深刻洞察。

### 本章专属作业题目 (Chapter HW)
- [ ] 题目 1：手动推导本章核心公式，并将其映射到实际业务场景中。
- [ ] 题目 2：在 Jupyter Notebook 中复现上述 Shape Tracing，并插入断点观察变化。
- [ ] 题目 3：探索超参数调整（如 learning_rate）对最终收敛性能的影响。
- [ ] 题目 4：结合阅读材料，总结本章方法在极端数据分布下的表现。

### 本章认知误区避坑指南 (Misconception)
- ❌ **误区 1**：认为模型参数可以随意初始化，不考虑对称性破缺。
- ✅ **正解 1**：合理的初始化（如 Xavier 或 Kaiming）对避免梯度消失/爆炸至关重要。
- ❌ **误区 2**：忽视数据预处理，直接将原始数据输入模型。
- ✅ **正解 2**：标准化或归一化能够显著平滑优化地貌，加速收敛进程。

## 📖 第 5 章：前沿扩展与综合应用

### 本章核心理论与数学推导 (LaTeX)
在第 5 章的语境中，我们需要掌握基本运算和抽象的基础。
令 $X \in \mathbb{R}^{N \times d}$ 为输入数据矩阵，模型参数为 $\Theta$，则目标函数可以表示为：
$$
\mathcal{L}(\Theta) = \frac{1}{N} \sum_{i=1}^{N} \ell(f(x_i; \Theta), y_i) + \lambda \Omega(\Theta)
$$
通过梯度下降优化：
$$
\Theta_{t+1} = \Theta_t - \eta \nabla \mathcal{L}(\Theta_t)
$$
这构成了本章知识底座的基础推导，需要在理解的基础上熟练运用。

### 本章代码实现与张量维度追踪 (Shape Tracing)
在代码实现中，我们要特别关注数据维度和流转的变化，严谨的 Shape Tracing 是 Debug 的核心。
```python
import numpy as np

def chapter_5_forward(X, W, b):
    # Shape Tracing:
    # X: [batch_size, input_dim]
    # W: [input_dim, output_dim]
    # b: [output_dim]
    
    # 矩阵乘法维度推演
    # [batch_size, input_dim] @ [input_dim, output_dim] -> [batch_size, output_dim]
    Z = np.dot(X, W) + b # [batch_size, output_dim]
    
    return Z
```
这里张量的每一次流动，都是我们对模型内部状态的深刻洞察。

### 本章专属作业题目 (Chapter HW)
- [ ] 题目 1：手动推导本章核心公式，并将其映射到实际业务场景中。
- [ ] 题目 2：在 Jupyter Notebook 中复现上述 Shape Tracing，并插入断点观察变化。
- [ ] 题目 3：探索超参数调整（如 learning_rate）对最终收敛性能的影响。
- [ ] 题目 4：结合阅读材料，总结本章方法在极端数据分布下的表现。

### 本章认知误区避坑指南 (Misconception)
- ❌ **误区 1**：认为模型参数可以随意初始化，不考虑对称性破缺。
- ✅ **正解 1**：合理的初始化（如 Xavier 或 Kaiming）对避免梯度消失/爆炸至关重要。
- ❌ **误区 2**：忽视数据预处理，直接将原始数据输入模型。
- ✅ **正解 2**：标准化或归一化能够显著平滑优化地貌，加速收敛进程。

## 📖 综合 Rubric 验收
### 验收标准
| 维度 | 优秀 (A) | 合格 (B) | 待改进 (C) |
|---|---|---|---|
| **理论掌握** | 能独立推导所有核心公式并指出边界条件 | 能理解核心公式及参数含义 | 对公式含义存在明显认知偏差 |
| **工程实现** | 代码规范，Shape Tracing 准确，性能优异 | 代码能跑通，无明显 Bug | 存在无法独立解决的 RuntimeError |
| **避坑指南** | 成功规避所有已知误区并总结新坑 | 能识别出常见的几个误区 | 踩坑后不知如何 Debug 排查 |
| **综合实践** | 能将本章知识迁移到其他开源项目或业务中 | 能够完成本章自带的专属作业题 | 未能完成基础作业题 |

### 验收 Checklist
- [ ] 理论推导闭卷完成
- [ ] 核心代码手写无报错
- [ ] 专属作业全部 AC
- [ ] Anki 卡片已添加并首次复习完毕

## 🃏 Anki 复习提炼卡
- **Q**: 本项目中最容易被忽视的张量维度对齐问题是什么？
- **A**: 在进行 Broadcast 加法时，未严格检查尾部维度对齐，导致隐式的逻辑错误而非显式报错。
- **Q**: 为什么要进行公式的闭卷推导？
- **A**: 只有经过肌肉记忆级别的推导，才能在实际 Debug 时迅速定位梯度异常的数学源头。

