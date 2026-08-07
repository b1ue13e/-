---
type: project
kind: project
track: 机器学习与AI应用
project_type: homework
course: "08-NLP全栈"
assignment_id: "08-NLP全栈-HW04"
assignment_level: lesson
assignment_format: lab
stage_id: "05"
requires: ["[[08-NLP全栈-参数高效微调PEFT]]"]
source_type: open_source_project_task
source: "Hugging Face PEFT & Microsoft LoRA Official Paper Repo"
source_url: "https://github.com/microsoft/LoRA"
created: 2026-08-07
status: planned
flow: project
tags: [作业, NLP, PEFT, LoRA, 微调, LLM]
assessment_exempt: false
---

# 08-NLP全栈-课后作业-04-LoRA参数高效微调算子

> ⏱ **预计完成耗时**：2.5 小时  
> 🎯 **对应阶段**：阶段 5 - 大语言模型与前沿技术

---

## 🎯 学习目标

1. 掌握大模型高效微调（PEFT）代表算法 Low-Rank Adaptation (LoRA) 的数学原理与本真公式：
$$W = W_0 + \Delta W = W_0 + \frac{\alpha}{r} B A$$
2. 动手编写 PyTorch 自定义 `LoRALinear` 层，实现对现有 `nn.Linear` 权重的冻结与低秩旁路注入。
3. 掌握推理加速关键技术：在部署上线前将低秩矩阵 $B A$ 融合（Merge）进主权重 $W_0$，实现零额外延迟推理。

---

## 🚧 任务边界

- **包含**：使用 PyTorch 实现 `LoRALinear` 继承类、高斯初始化矩阵 $A \sim \mathcal{N}(0, \sigma^2)$、全零初始化矩阵 $B = 0$、缩放因子 $\frac{\alpha}{r}$ 计算、Merge/Unmerge 状态转换。
- **不包含**：QLoRA (4-bit NF4 量化矩阵微调)、AdaLoRA 动态秩调整、DoRA 权重方向归一化。

---

## 📋 详细题目与实施步骤

### 任务 1：`LoRALinear` 自定义层实现
实现兼容 `nn.Linear` 接口的 `LoRALinear` 模块：
1. 传入原始权重 $W_0 \in \mathbb{R}^{d_{out} \times d_{in}}$，设置 `requires_grad = False` 锁定更新。
2. 构造低秩旁路：
   - 矩阵 $A \in \mathbb{R}^{r \times d_{in}}$，使用 Kaiming / Normal 正态分布初始化。
   - 矩阵 $B \in \mathbb{R}^{d_{out} \times r}$，初始化为纯全零矩阵（确保初始状态下 $\Delta W = 0$，模型输出与原始 $W_0$ 严格一致）。
3. 定义缩放因子 `scaling = lora_alpha / r`。

### 任务 2：前向传播与梯度更新逻辑 (`forward`)
在前向传播中：
$$y = h W_0^\top + \text{scaling} \cdot (h A^\top B^\top) + b$$
验证在训练模式下，仅 $A$ 和 $B$ 的梯度被计算与反向传播，主权重 $W_0$ 的 `grad` 严格为 `None`。

### 任务 3：模型融合与解融机制 (`merge` / `unmerge`)
1. **`merge()`**：当 `merged = False` 时，计算 $W_{merged} = W_0 + \text{scaling} \cdot (B A)$，并更新 $W_0$ 的数据，释放旁路计算开销。
2. **`unmerge()`**：从 $W_{merged}$ 中扣除 $\text{scaling} \cdot (B A)$，恢复微调状态。

---

## 📦 提交产物

1. `scripts/lora_layer.py`：包含 `LoRALinear` 与 `inject_lora_to_model()` 替换函数的完整 PyTorch 代码。
2. `reports/hw04_lora_report.md`：参数量对比表格（原始参数 vs 可微调参数）及 Merge 前后输出 Consistency 验证日志。

---

## ⚖️ 验收标准 (Rubric)

| 评分项 | 权重 | 通过标准 |
| :--- | :--- | :--- |
| **低秩算子实现** | 40% | 初始状态 $\Delta W=0$，前向计算与 PyTorch 原生 Linear 兼容 |
| **Merge / Unmerge**| 30% | Merge 前后模型输出绝对误差 $< 10^{-6}$，主权重更新状态符合预期 |
| **单元测试** | 30% | 运行 `pytest 03-Projects/08-NLP全栈/tests/test_lora.py` 100% 通过 |

---

## 🔍 引导与自检

- [ ] 为何矩阵 $B$ 必须全零初始化，而矩阵 $A$ 不能全零初始化？
- [ ] 在使用 `merge()` 融合权重后，再次执行 `forward` 时是否避免了额外的 $A, B$ 矩阵相乘计算？
- [ ] 仅替换 Transformer 中的 $Q, V$ 投影矩阵与同时替换 $Q, K, V, O$ 矩阵对训练参数量和拟合能力的差异。

---

## 🧪 验证与测试

```bash
pytest 03-Projects/08-NLP全栈/tests/test_lora.py
```
