---
type: study
topic: "混合精度与ZeRO分布式优化"
course: "07-最优化方法"
created: 2026-08-08
status: completed
flow: knowledge
kind: concept
stage_moc: "[[🧭 阶段5-专题应用]]"
difficulty: advanced
upstream:
  - "[[最优化方法-分布式优化与对偶分解]]"
  - "[[最优化方法-Adam与自适应学习率]]"
  - "[[最优化方法-增广拉格朗日与ADMM]]"
---
# 最优化方法-混合精度与ZeRO分布式优化

## 1. 这个知识点解决什么问题？
> **我们遇到了什么麻烦**：
> 当模型参数量突破百亿到万亿级别时，单个 GPU 显存（如 80GB A100/H100）连模型参数和 Adam 优化器状态都无法装下。传统的纯数据并行（DDP）在每个 GPU 上完整复制一份参数、梯度和优化器状态（共需 $16\text{ Bytes}/\text{param}$ 显存），造成了极其严重的显存冗余（Memory Redundancy）；同时低精度格式（如 FP16）在梯度极小时会发生严重的数值下溢（Underflow）。
> **回答**：
> 1. **混合精度与动态损失缩放（Loss Scaling）**：用低精度（FP16/BF16/FP8）前向后向计算加速吞吐，用动态放大因子 $S$ 克服极小梯度的数值下溢，并在更新时维护高精度（FP32）主权重；
> 2. **ZeRO (Zero Redundancy Optimizer)**：将原本在所有显卡上完全重复冗余的优化器状态（ZeRO-1）、梯度（ZeRO-2）和模型参数（ZeRO-3）均匀切片分配到各个 GPU 上，以几乎不增加额外通信量（ZeRO-1/2 保持 $2\times$，ZeRO-3 仅增加 $50\%$ 到 $3\times$）的代价，将单卡显存需求降低达 $8\times \sim N\times$。

---
## 2. 为什么它重要？它有什么用？
- **连接大图景**：它是最优化理论在大规模工业级深度学习（DeepSpeed、Megatron-LM、PyTorch FSDP）中的终极工程落地。
- **实际应用场景**：
  - **LLaMA-3 405B / DeepSeek 等超大模型分布式预训练与微调**；
  - **单机多卡（8x H100）甚至多机集群全并行训练调度**。
- **核心计算与推导**：
  - 计算混合精度训练的标准显存占用：$4\Phi \text{ (参数)} + 4\Phi \text{ (梯度)} + 12\Phi \text{ (Adam状态)} = 16\Phi$ 字节；
  - 精确推导 ZeRO-1、ZeRO-2、ZeRO-3 在 AllReduce / ReduceScatter / AllGather 下的通信量。

---
## 3. 学它之前需要哪些前置知识？
1. **[[最优化方法-分布式优化与对偶分解]]**：理解分布式节点间的参数一致性与通信原语。
2. **[[最优化方法-Adam与自适应学习率]]**：掌握 AdamW 的一阶二阶矩存储机制。
3. **[[最优化方法-增广拉格朗日与ADMM]]**：理解块坐标切分与分布式同步思想。

---
## 4. 用直觉语言解释它
> «"传统的 DDP 就像 8 个厨师炒一桌大宴席，但每个人厨房里都必须买一整套昂贵的大锅、灶台和调料（完整模型与优化器），厨房瞬间挤爆；
> ZeRO-1 说：你们大家共用一套调料仓库（把 Adam 状态分给 8 个人分管）；
> ZeRO-2 说：大家连锅具也不用每人一套，各洗一部分（梯度切片）；
> ZeRO-3 说：每个人只要记住自己的拿手菜（参数切片），炒菜时向邻居大喊一声借过来（AllGather），炒完立刻还回去（释放显存）！"»

---
## 5. 正式定义、核心公式、符号解释

### 1. 混合精度训练的数学流程与损失缩放
设模型参数为 $\theta$，损失函数为 $\mathcal{L}(\theta)$，缩放因子为 $S_t > 0$：
1. **前向与后向计算（低精度 FP16）**：
   $$ \mathcal{L}_{\text{scaled}} = S_t \cdot \mathcal{L}(\theta_{\text{fp16}}) $$
   $$ g_{\text{scaled}} = \nabla_{\theta_{\text{fp16}}} \mathcal{L}_{\text{scaled}} = S_t \cdot \nabla_\theta \mathcal{L} $$
2. **非有限值（Inf/NaN）检测与解缩放**：
   $$ g_t = \frac{g_{\text{scaled}}}{S_t} $$
   - 若检测到 $\text{is\_inf\_or\_nan}(g_{\text{scaled}}) == \text{True}$：丢弃本次更新，缩放因子缩小 $S_{t+1} = \frac{1}{2} S_t$；
   - 若连续 $N_{\text{stable}}$ 步全为正常数值：$S_{t+1} = 2 S_t$。
3. **主权重更新（高精度 FP32）**：
   $$ \theta_{\text{fp32}}^{(t)} = \text{AdamW}(\theta_{\text{fp32}}^{(t-1)}, g_t) $$
   $$ \theta_{\text{fp16}}^{(t)} = \text{CastToFP16}(\theta_{\text{fp32}}^{(t)}) $$

---

### 2. ZeRO 阶段显存与通信量对比表
设模型参数量为 $\Phi$，GPU 节点数为 $N$：

| 机制 | 显存占用 (Bytes / param) | 前向通信量 | 后向通信量 | 优化器步通信量 | 总通信量 (相对传统 DDP) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **标准 DDP (FP16+Adam)** | $16\Phi$ | $0$ | $2\Phi$ (AllReduce) | $0$ | $2\Phi$ ($1.0\times$) |
| **ZeRO-1 (切分 $O_S$)** | $4\Phi + \frac{12\Phi}{N}$ | $0$ | $2\Phi$ (ReduceScatter + AllGather) | $0$ | $2\Phi$ ($1.0\times$) |
| **ZeRO-2 (切分 $O_S + G$)** | $2\Phi + \frac{14\Phi}{N}$ | $0$ | $\Phi$ (ReduceScatter) | $\Phi$ (AllGather) | $2\Phi$ ($1.0\times$) |
| **ZeRO-3 (切分 $O_S + G + P$)** | $\frac{16\Phi}{N}$ | $\Phi$ (AllGather) | $2\Phi$ (AllGather + ReduceScatter) | $0$ | $3\Phi$ ($1.5\times$) |

---

## 6. 推导思路与通信原语分析

### 为什么 ZeRO-2 相比传统 DDP 没有增加任何额外通信量？
在传统 DDP 中，后向传播结束后需要调用一次 **AllReduce** 将所有 GPU 上的梯度同步平均。根据环形通信（Ring-AllReduce）原理：
$$ \text{AllReduce通信量} = 2 \times \frac{N-1}{N} \Phi \approx 2\Phi $$
在 ZeRO-2 中，梯度的同步被拆解为两步：
1. 后向传播中进行 **ReduceScatter**，每个 GPU 仅保留属于自己负责切片范围内的聚合平均梯度：通信量为 $\frac{N-1}{N}\Phi \approx \Phi$；
2. 优化器利用局部梯度更新局部权重后，再执行一次 **AllGather** 广播更新后的权重切片：通信量为 $\frac{N-1}{N}\Phi \approx \Phi$。
总通信量恰好为 $\Phi + \Phi = 2\Phi$，与传统 AllReduce 严格相等！这就是 ZeRO 能够零通信开销节省巨大显存的根本原因。

---

## 7. 例子：Python/NumPy 动态损失缩放器模拟

```python
import numpy as np

class DynamicLossScaler:
    """工业级动态损失缩放器实现 (FP16 / BF16 数值稳定)"""
    def __init__(self, init_scale=65536.0, scale_factor=2.0, scale_window=2000):
        self.scale = init_scale
        self.scale_factor = scale_factor
        self.scale_window = scale_window
        self.stable_steps = 0

    def scale_loss(self, loss: float) -> float:
        return loss * self.scale

    def unscale_and_update(self, grads: list[np.ndarray]) -> tuple[list[np.ndarray], bool]:
        # 1. 检查梯度是否溢出 (Inf / NaN)
        has_overflow = any(not np.isfinite(g).all() for g in grads)
        
        if has_overflow:
            # 溢出：缩小 scale，重置稳定步数
            self.scale = max(1.0, self.scale / self.scale_factor)
            self.stable_steps = 0
            return grads, False
        else:
            # 正常：解缩放
            unscaled_grads = [g / self.scale for g in grads]
            self.stable_steps += 1
            if self.stable_steps >= self.scale_window:
                self.scale *= self.scale_factor
                self.stable_steps = 0
            return unscaled_grads, True
```

---

## 8. 常见误区与注意点
1. **误区：BF16 相比 FP16 精度更高**  
   - *纠错*：BF16 的尾数位（Mantissa）只有 7 位（低于 FP16 的 10 位），其数值精度实际上更低；但 BF16 的指数位（Exponent）有 8 位（与 FP32 相同），动态范围达到 $10^{\pm 38}$，因此通常**不需要动态损失缩放**即可避免下溢。
2. **误区：ZeRO-3 会导致训练速度下降数倍**  
   - *纠错*：ZeRO-3 的通信量仅从 $2\Phi$ 增加到 $3\Phi$（增加 $50\%$）。在具备高带宽互联（如 NVLink 900GB/s）的集群中，通过计算-通信异步重叠（Computation-Communication Overlapping），性能损耗通常低于 $10\%$。

---

## 9. 检索练习自测
1. **【计算题】** 训练一个 70B（700 亿参数）模型，使用 FP16 混合精度与 AdamW 优化器，至少需要多少 GB 显存来存储静态优化器状态与参数？
2. **【推导题】** 为什么 ZeRO-1 将优化器状态切分成 $N$ 份后，总通信量依然维持在 $2\Phi$？
3. **【应用题】** 简述 PyTorch FSDP (Fully Sharded Data Parallel) 与 ZeRO-3 的本质异同。

---

## 10. 🃏 Anki 卡片

```anki
deck: 07-最优化方法
tags: [最优化方法, 专题应用, ZeRO, 混合精度, 分布式优化]

# Card 1
Q: 混合精度训练中为什么需要 Dynamic Loss Scaling？其核心调整策略是什么？
A: 
1. **原因**：FP16 动态范围小，极小梯度会下溢为 0；
2. **策略**：用放大因子 $S$ 放大损失与梯度，检测到 Inf/NaN 时减半 $S$ 并跳过更新，连续稳定 $N$ 步时翻倍 $S$。
---
# Card 2
Q: 简述 ZeRO-1、ZeRO-2、ZeRO-3 分别对哪些显存组件进行了切片？
A: 
- **ZeRO-1**：切分优化器状态（Optimizer States $O_S$）；
- **ZeRO-2**：切分优化器状态 + 梯度（$O_S + G$）；
- **ZeRO-3**：切分优化器状态 + 梯度 + 模型参数（$O_S + G + P$）。
```

---

## 学完后可以完成

```dataview
LIST
FROM "03-Projects/07-最优化方法"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
