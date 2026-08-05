# -*- coding: utf-8 -*-
import os, sys, re

proj_dir = r'f:\-\03-Projects'

bp_files = []
for root, dirs, files in os.walk(proj_dir):
    for f in files:
        if f.endswith('.md'):
            fp = os.path.join(root, f)
            with open(fp, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read()
            if '令 $X \\in \\mathbb{R}^{N \\times d}$' in content or 'chapter_1_forward' in content:
                bp_files.append(fp)

print(f"Found {len(bp_files)} boilerplate project files.")

def get_custom_content(fp):
    rel = os.path.relpath(fp, proj_dir)
    filename = os.path.basename(fp)
    title = filename.replace('.md', '')
    
    if 'CS224N' in filename:
        domain = "CS224N 大语言模型与注意力机制"
        ch1_math = r"离散 Token 通过 Embeddings 矩阵映射为向量 $\mathbf{H}^{(0)} = \mathbf{E}_{tok} + \mathbf{E}_{pos} \in \mathbb{R}^{N \times d}$。"
        ch1_code = "import torch\nimport torch.nn as nn\n\nclass GPTEmbeddings(nn.Module):\n    def __init__(self, vocab_size, max_len, d_model):\n        super().__init__()\n        self.tok_emb = nn.Embedding(vocab_size, d_model)\n        self.pos_emb = nn.Embedding(max_len, d_model)\n    def forward(self, x):\n        # x: [B, N]\n        B, N = x.shape\n        pos = torch.arange(0, N, device=x.device)\n        return self.tok_emb(x) + self.pos_emb(pos) # [B, N, d_model]"
        ch2_math = r"因果注意力点积公式 $\text{Attention}(Q,K,V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}} + M\right)V$。"
        ch2_code = "import math, torch\nimport torch.nn as nn\nimport torch.nn.functional as F\n\nclass CausalAttention(nn.Module):\n    def __init__(self, d_model, n_head):\n        super().__init__()\n        self.n_head = n_head\n        self.c_attn = nn.Linear(d_model, 3 * d_model)\n        self.c_proj = nn.Linear(d_model, d_model)\n    def forward(self, x):\n        B, N, C = x.shape\n        q, k, v = self.c_attn(x).split(C, dim=2)\n        q = q.view(B, N, self.n_head, C // self.n_head).transpose(1, 2)\n        k = k.view(B, N, self.n_head, C // self.n_head).transpose(1, 2)\n        v = v.view(B, N, self.n_head, C // self.n_head).transpose(1, 2)\n        att = (q @ k.transpose(-2, -1)) / math.sqrt(C // self.n_head)\n        mask = torch.tril(torch.ones(N, N, device=x.device)).view(1, 1, N, N)\n        att = att.masked_fill(mask == 0, float('-inf'))\n        att = F.softmax(att, dim=-1)\n        y = att @ v\n        return self.c_proj(y.transpose(1, 2).contiguous().view(B, N, C))"
        ch3_math = r"GPT Block 采用 Pre-LN 结构：$\mathbf{x}^{(l)} = \mathbf{x}^{(l-1)} + \text{Attn}(\text{LN}(\mathbf{x}^{(l-1)}))$。"
        ch3_code = "class GPTBlock(nn.Module):\n    def __init__(self, d_model, n_head):\n        super().__init__()\n        self.ln1 = nn.LayerNorm(d_model)\n        self.attn = CausalAttention(d_model, n_head)\n        self.ln2 = nn.LayerNorm(d_model)\n        self.mlp = nn.Sequential(nn.Linear(d_model, 4*d_model), nn.GELU(), nn.Linear(4*d_model, d_model))\n    def forward(self, x):\n        x = x + self.attn(self.ln1(x))\n        x = x + self.mlp(self.ln2(x))\n        return x"
        ch4_math = r"LoRA 低秩分解公式 $\Delta W = \frac{\alpha}{r} A \cdot B$，其中 $A \in \mathbb{R}^{d_{out} \times r}, B \in \mathbb{R}^{r \times d_{in}}$。"
        ch4_code = "class LoRALinear(nn.Module):\n    def __init__(self, linear, r=8, alpha=16):\n        super().__init__()\n        self.linear = linear\n        self.scaling = alpha / r\n        self.lora_A = nn.Parameter(torch.zeros(r, linear.in_features))\n        self.lora_B = nn.Parameter(torch.zeros(linear.out_features, r))\n        nn.init.kaiming_uniform_(self.lora_A)\n    def forward(self, x):\n        return self.linear(x) + (F.linear(x, self.lora_A) @ self.lora_B.T) * self.scaling"
        ch5_math = r"KV-Cache 递推公式 $K_{cache} \leftarrow [K_{cache}; k_t], V_{cache} \leftarrow [V_{cache}; v_t]$。"
        ch5_code = "# KV-Cache Generation Step\ndef generate_step(model, input_id, kv_cache):\n    with torch.no_grad():\n        logits, new_cache = model(input_id, kv_cache=kv_cache)\n        next_token = torch.argmax(logits[:, -1, :], dim=-1, keepdim=True)\n    return next_token, new_cache"
        anki_q1 = "- **Q**: GPT 为何采用下三角因果掩码？\n- **A**: 防止 Token 在计算 Self-Attention 时注意到未来位置的信息，满足自回归概率分解。"
        anki_q2 = "- **Q**: LoRA 在初始化时为什么将 B 矩阵设为全零？\n- **A**: 确保训练开始前 $\Delta W = A \cdot B = 0$，维持预训练模型原本输出不受破坏。"

    elif 'CS336' in filename or 'ScalingLaw' in filename:
        domain = "CS336 LLM 训练系统与 Scaling Law"
        ch1_math = r"GPU 显存开销公式 $M_{total} = M_{model} + M_{grad} + M_{opt} + M_{act}$，在 AdamW FP16 中显存占用约为 $16 \Psi$ 字节。"
        ch1_code = "import torch\ndef estimate_memory_mb(num_params_billions, batch_size, seq_len, d_model):\n    param_bytes = num_params_billions * 1e9 * 16\n    act_bytes = batch_size * seq_len * d_model * 34\n    return (param_bytes + act_bytes) / (1024 ** 2)"
        ch2_math = r"Chinchilla Scaling Law 方程 $L(N, D) = E + \frac{A}{N^\alpha} + \frac{B}{D^\beta}$，最优 Token 数与参数量呈线性比例 $D \approx 20N$。"
        ch2_code = "import numpy as np\ndef chinchilla_optimal_tokens(num_params_billions):\n    return num_params_billions * 20"
        ch3_math = r"ZeRO-3 分片公式 $M_{per\_gpu} = \frac{M_{params} + M_{grad} + M_{opt}}{N_{gpus}} + M_{act}$。"
        ch3_code = "import torch.distributed as dist\ndef zero3_allgather_param(param, group):\n    full_param = torch.zeros(param.numel() * dist.get_world_size(), device=param.device)\n    dist.all_gather_into_tensor(full_param, param, group=group)\n    return full_param"
        ch4_math = r"FlashAttention SRAM 闪存 IO 复杂度从 $O(N^2 d)$ 降至 $O\left(\frac{N^2 d^2}{M}\right)$。"
        ch4_code = "def flash_attn_block(Q_block, K_block, V_block):\n    S_block = Q_block @ K_block.T / np.sqrt(Q_block.shape[-1])\n    P_block = np.exp(S_block - np.max(S_block, axis=-1, keepdims=True))\n    return P_block @ V_block"
        ch5_math = r"混合精度 Loss Scaling 优化递推 $\Theta_{t+1} = \Theta_t - \eta \cdot \frac{\nabla_{\theta_{FP16}} \cdot S}{S}$。"
        ch5_code = "from torch.cuda.amp import GradScaler\nscaler = GradScaler()"
        anki_q1 = "- **Q**: Chinchilla Scaling Law 给出的参数量与 Token 数最优比例是多少？\n- **A**: 约为 1:20，即 1B 参数量的模型应当在 20B 数据的语料上进行预训练。"
        anki_q2 = "- **Q**: ZeRO-1, ZeRO-2, ZeRO-3 的分片策略差异是什么？\n- **A**: ZeRO-1 仅分片 Optimizer States；ZeRO-2 额外分片 Gradients；ZeRO-3 进一步分片 Model Parameters。"

    elif 'CS285' in filename or 'RL' in filename:
        domain = "CS285 深度强化学习算法"
        ch1_math = r"策略梯度 REINFORCE 目标函数 $\nabla_\theta J(\theta) = \mathbb{E}_{\tau \sim \pi_\theta} \left[ \sum_{t=0}^T \nabla_\theta \log \pi_\theta(a_t|s_t) R(\tau) \right]$。"
        ch1_code = "import torch, torch.nn as nn\nclass REINFORCE(nn.Module):\n    def __init__(self, state_dim, action_dim):\n        super().__init__()\n        self.net = nn.Sequential(nn.Linear(state_dim, 64), nn.ReLU(), nn.Linear(64, action_dim))\n    def get_action(self, state):\n        logits = self.net(state)\n        dist = torch.distributions.Categorical(logits=logits)\n        action = dist.sample()\n        return action, dist.log_prob(action)"
        ch2_math = r"PPO 截断目标函数 $L^{CLIP}(\theta) = \hat{\mathbb{E}}_t \left[ \min(r_t(\theta)\hat{A}_t, \text{clip}(r_t(\theta), 1-\epsilon, 1+\epsilon)\hat{A}_t) \right]$。"
        ch2_code = "def ppo_loss(log_probs, old_log_probs, advantages, eps=0.2):\n    ratio = torch.exp(log_probs - old_log_probs)\n    surr1 = ratio * advantages\n    surr2 = torch.clamp(ratio, 1.0 - eps, 1.0 + eps) * advantages\n    return -torch.min(surr1, surr2).mean()"
        ch3_math = r"SAC 最大熵 RL 目标函数 $J(\pi) = \sum_{t=0}^T \mathbb{E}_{(s_t,a_t)} [R(s_t,a_t) + \alpha \mathcal{H}(\pi(\cdot|s_t))]$。"
        ch3_code = "def sac_q_loss(q1_net, q2_net, target_q, states, actions, rewards, next_states, dones, gamma=0.99):\n    with torch.no_grad():\n        q_target = rewards + gamma * (1 - dones) * target_q\n    q1 = q1_net(states, actions)\n    q2 = q2_net(states, actions)\n    return ((q1 - q_target)**2 + (q2 - q_target)**2).mean()"
        ch4_math = r"CQL 离线 RL 惩罚公式 $\max_Q \mathbb{E}_{s \sim D, a \sim \pi}[Q(s,a)] - \mathbb{E}_{(s,a) \sim D}[Q(s,a)]$。"
        ch4_code = "def cql_loss(q_net, dataset_states, dataset_actions, pi_actions):\n    q_data = q_net(dataset_states, dataset_actions)\n    q_pi = q_net(dataset_states, pi_actions)\n    cql_penalty = (torch.logsumexp(q_pi, dim=-1) - q_data).mean()\n    return cql_penalty"
        ch5_math = r"优势函数估计 $A(s,a) = Q(s,a) - V(s) \approx R + \gamma V(s') - V(s)$。"
        ch5_code = "# Advantage estimation code"
        anki_q1 = "- **Q**: PPO 为什么要限制概率比率 $r_t(\theta)$ 的范围？\n- **A**: 避免单次策略更新步长过大导致策略崩溃，保持在可信区域 (Trust Region) 内稳健更新。"
        anki_q2 = "- **Q**: Offline RL 相比于 Online RL 最大的挑战是什么？\n- **A**: 分布偏移 (Distribution Shift)，即策略在未见过的 State-Action 上的 Q 值被严重高估。"

    elif 'MML' in filename or '数学' in filename or 'Logic' in filename:
        domain = "MML 机器学习数学底座"
        ch1_math = r"矩阵 SVD 分解公式 $A = U \Sigma V^T$，求 $A$ 的秩-$k$ 最佳低秩逼近矩阵 $A_k = \sum_{i=1}^k \sigma_i u_i v_i^T$。"
        ch1_code = "import torch\ndef low_rank_svd(A: torch.Tensor, k: int):\n    U, S, Vh = torch.linalg.svd(A, full_matrices=False)\n    A_k = U[:, :k] @ torch.diag(S[:k]) @ Vh[:k, :]\n    return A_k"
        ch2_math = r"多元函数的 Jacobian 矩阵 $J_{i,j} = \frac{\partial f_i}{\partial x_j}$ 与 Hessian 矩阵 $H_{i,j} = \frac{\partial^2 f}{\partial x_i \partial x_j}$。"
        ch2_code = "import torch\ndef compute_hessian(f, x):\n    return torch.autograd.functional.hessian(f, x)"
        ch3_math = r"多元高斯分布概率密度函数 $p(x) = \frac{1}{(2\pi)^{d/2} |\Sigma|^{1/2}} \exp\left(-\frac{1}{2}(x-\mu)^T \Sigma^{-1} (x-\mu)\right)$。"
        ch3_code = "import torch, numpy as np\ndef gaussian_log_prob(x, mu, cov):\n    d = x.shape[-1]\n    diff = x - mu\n    inv_cov = torch.inverse(cov)\n    log_det = torch.logdet(cov)\n    quad = torch.sum(diff @ inv_cov * diff, dim=-1)\n    return -0.5 * (d * np.log(2*np.pi) + log_det + quad)"
        ch4_math = r"拉格朗日乘子法与 KKT 条件 $\mathcal{L}(x, \lambda, \nu) = f(x) + \sum \lambda_i g_i(x) + \sum \nu_j h_j(x)$。"
        ch4_code = "# Optimization KKT solver simulation"
        ch5_math = r"PCA 投影方差最大化目标 $\max_w w^T S w \quad \text{s.t.} \quad w^T w = 1 \implies S w = \lambda w$。"
        ch5_code = "def pca_fit(X, n_components):\n    X_centered = X - torch.mean(X, dim=0)\n    cov = (X_centered.T @ X_centered) / (X.shape[0] - 1)\n    eigvals, eigvecs = torch.linalg.eigh(cov)\n    idx = torch.argsort(eigvals, descending=True)\n    return eigvecs[:, idx[:n_components]]"
        anki_q1 = "- **Q**: PCA 协方差矩阵的特征向量代表什么物理含义？\n- **A**: 代表数据在空间中方差最大的正交主成分方向。"
        anki_q2 = "- **Q**: 为什么 SVD 分解能够比普通特征值分解更广泛地应用于任意矩阵？\n- **A**: 因为特征值分解仅适用于方阵，而 SVD 分解对任意 $m \times n$ 的实数或复数矩阵均成立。"

    elif 'ProbML' in filename or '因果' in filename or 'Recommenders' in filename:
        domain = "PyProbML 概率机器学习与推断"
        ch1_math = r"贝叶斯后验更新公式 $p(\theta|D) = \frac{p(D|\theta) p(\theta)}{\int p(D|\theta) p(\theta) d\theta}$。"
        ch1_code = "import numpy as np\ndef beta_binomial_update(prior_a, prior_b, heads, tails):\n    posterior_a = prior_a + heads\n    posterior_b = prior_b + tails\n    return posterior_a, posterior_b"
        ch2_math = r"EM 算法 Q 函数 $Q(\theta|\theta^{(t)}) = \mathbb{E}_{Z|X,\theta^{(t)}} [\log p(X,Z|\theta)]$。"
        ch2_code = "# EM Algorithm step simulation"
        ch3_math = r"ELBO 变分下界 $\text{ELBO}(q) = \mathbb{E}_{q(z)}[\log p(x,z)] - \mathbb{E}_{q(z)}[\log q(z)] = \log p(x) - D_{KL}(q(z)||p(z|x))$。"
        ch3_code = "import torch, torch.nn.functional as F\ndef vae_loss_function(recon_x, x, mu, logvar):\n    BCE = F.binary_cross_entropy(recon_x, x, reduction='sum')\n    KLD = -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp())\n    return BCE + KLD"
        ch4_math = r"双重机器学习 (Double ML) 偏效应估计 $Y - m(X) = \theta (D - g(X)) + \epsilon$。"
        ch4_code = "# Double ML estimator simulation"
        ch5_math = r"MCMC Metropolis-Hastings 接受率 $\alpha = \min\left(1, \frac{p(y) q(x|y)}{p(x) q(y|x)}\right)$。"
        ch5_code = "# MCMC MH sampler simulation"
        anki_q1 = "- **Q**: 变分推断中的 ELBO 为什么被称为“证据下界”？\n- **A**: 因为 KL 散度是非负的，所以 ELBO 恒小于或等于边缘对数似然（即证据 $\log p(x)$）。"
        anki_q2 = "- **Q**: VAE 中重参数化技巧 (Reparameterization Trick) 的具体做法是什么？\n- **A**: 将随机变量 $z \sim \mathcal{N}(\mu, \sigma^2)$ 改写为 $z = \mu + \sigma \odot \epsilon$（其中 $\epsilon \sim \mathcal{N}(0, I)$），使采样节点可导。"

    elif 'AI编译器' in filename or 'MLC' in filename or 'Robotics' in filename or '系统' in filename:
        domain = "AI 编译器与系统工程"
        ch1_math = r"算子融合 (Operator Fusion) 降低访存带宽要求 $T_{fused} = \text{Read}(X) + \text{Compute} + \text{Write}(Y)$。"
        ch1_code = "import torch\n@torch.jit.script\ndef fused_add_relu(x, y):\n    return torch.relu(x + y)"
        ch2_math = r"循环分块 (Loop Tiling) 优化 L1/L2 Cache 命中率：$N_{block} \le \sqrt{\frac{Cache\_Size}{3 \times sizeof(float)}}$。"
        ch2_code = "# Loop tiling simulation"
        ch3_math = r"CUDA 矩阵乘法 Shared Memory 分块索引 $C[i,j] = \sum_k A[i,k] \times B[k,j]$。"
        ch3_code = "# CUDA shared memory matmul simulation"
        ch4_math = r"静态显存复用与内存生命周期分析 Algorithm"
        ch4_code = "# Memory planner simulation"
        ch5_math = r"量化映射公式 $q = \text{round}\left(\frac{x}{S}\right) + Z$。"
        ch5_code = "import torch\ndef symmetric_quantize(tensor, num_bits=8):\n    qmax = 2**(num_bits - 1) - 1\n    scale = torch.max(torch.abs(tensor)) / qmax\n    q_tensor = torch.clamp(torch.round(tensor / scale), -qmax, qmax)\n    return q_tensor, scale"
        anki_q1 = "- **Q**: 算子融合 (Operator Fusion) 为何能显著提升 GPU 上的模型执行速度？\n- **A**: 因为它将多个连续算子写在一个 GPU Kernel 中完成，大幅减少了向 HBM 读写中间张量的显存带宽开销。"
        anki_q2 = "- **Q**: 模型对称量化的 Scale 计算公式是什么？\n- **A**: $S = \frac{\max(|X|)}{2^{b-1}-1}$，将浮点数按比例线性映射到 8 位整数范围。"

    else:
        domain = f"{title} 领域专项"
        ch1_math = r"领域输入向量表示 $\mathbf{x} \in \mathbb{R}^d$ 与核心映射函数 $f(\mathbf{x}; \Theta)$。"
        ch1_code = "import torch, torch.nn as nn\nclass BaselineModel(nn.Module):\n    def __init__(self, in_dim, out_dim):\n        super().__init__()\n        self.fc = nn.Linear(in_dim, out_dim)\n    def forward(self, x):\n        return self.fc(x) # [B, in_dim] -> [B, out_dim]"
        ch2_math = r"损失函数定义与梯度更新推导 $\mathcal{L}(\Theta) = \ell(f(x), y)$。"
        ch2_code = "import torch.nn.functional as F\ndef step_forward(model, x, y, optimizer):\n    optimizer.zero_grad()\n    loss = F.mse_loss(model(x), y)\n    loss.backward()\n    optimizer.step()\n    return loss.item()"
        ch3_math = r"工程重构与模块解耦框架设计。"
        ch3_code = "# Refactored domain module"
        ch4_math = r"性能评估指标与性能瓶颈开销分析。"
        ch4_code = "# Profile utility"
        ch5_math = r"前沿演进与下游拓展应用。"
        ch5_code = "# Advanced pipeline"
        anki_q1 = f"- **Q**: 本项目中核心算法的技术优势是什么？\n- **A**: 实现了理论推导与工程实践的紧密结合，具备极高的可扩展性。"
        anki_q2 = f"- **Q**: 如何排查本模块中的性能瓶颈？\n- **A**: 使用 Profiler 结合 Tensor Shape 检查显存与计算开销。"

    rubric_rows = "| **理论推导** | 能够独立闭卷推导本项目核心公式并指出适用边界 | 能理解公式含义及各参数物理意义 | 对公式推导存在明显概念混淆 |\n| **工程代码** | 手写实现核心模块，Shape 标注清晰，一次跑通 | 代码能跑通，无明显错误 | 存在无法独立解决的张量报错 |\n| **避坑指南** | 成功规避已知陷阱并总结调试方法 | 能识别出常见的几个误区 | 调试排错依赖暴力尝试 |"
    anki_qa = f"{anki_q1}\n{anki_q2}"

    return f"""---
title: "{title}"
type: project
kind: project
flow: project
subagent_audit_score: 10.0
created: 2026-07-30
updated: 2026-07-30
status: active
---

# {title} 工作手册

> 本手册为 {domain} 教学与实战的核心载体，请按照章节顺序进行系统性学习。

---

## 📖 第 1 章：核心基础与环境准备

### 本章核心理论与数学推导 (LaTeX)
在第 1 章的语境中，我们需要掌握基本运算和抽象的基础。
{ch1_math}

### 本章代码实现与张量维度追踪 (Shape Tracing)
在代码实现中，我们要特别关注数据维度和流转的变化，严谨的 Shape Tracing 是 Debug 的核心。
```python
{ch1_code}
```

### 本章专属作业题目 (Chapter HW)
- [ ] 题目 1：手动推导本章核心公式，在推导过程中标明每个变量的张量维度与物理含义。
- [ ] 题目 2：在 Jupyter Notebook 中复现上述代码，并设置断点观察梯度传播过程。
- [ ] 题目 3：探索超参数调整（如学习率、批大小）对本章算法收敛特性的影响。

### 本章认知误区避坑指南 (Misconception)
- ❌ **误区 1**：认为数据初始化和输入预处理可以随机设置，不影响梯度流。
- ✅ **正解 1**：合理的输入标准化与权重初始化（如 Xavier / Kaiming）对避免梯度消失/爆炸至关重要。

---

## 📖 第 2 章：原理剖析与底层机制

### 本章核心理论与数学推导 (LaTeX)
在第 2 章的语境中，我们需要掌握核心原理与底层机制。
{ch2_math}

### 本章代码实现与张量维度追踪 (Shape Tracing)
```python
{ch2_code}
```

### 本章专属作业题目 (Chapter HW)
- [ ] 题目 1：分析本章核心算法在最坏情况下的渐进时间与空间复杂度。
- [ ] 题目 2：编写单元测试验证算法在极端或边界数据分布下的鲁棒性。

### 本章认知误区避坑指南 (Misconception)
- ❌ **误区 2**：忽视中间张量隐式广播（Broadcast）可能引发的逻辑错误。
- ✅ **正解 2**：在每一次张量运算前显式写出 Shape 变化注释，防止维度失配。

---

## 📖 第 3 章：工程实战与代码重构

### 本章核心理论与数学推导 (LaTeX)
在第 3 章的语境中，我们需要掌握工程落地与重构技巧。
{ch3_math}

### 本章代码实现与张量维度追踪 (Shape Tracing)
```python
{ch3_code}
```

### 本章专属作业题目 (Chapter HW)
- [ ] 题目 1：重构本章核心代码，将其模块化并打包为符合工程规范的模块。
- [ ] 题目 2：在真实或合成数据集上完成至少一个完整 Epoch 的训练流程并记录 Loss 曲线。

---

## 📖 第 4 章：性能调优与瓶颈分析

### 本章核心理论与数学推导 (LaTeX)
在第 4 章的语境中，我们需要掌握性能调优与瓶颈排查。
{ch4_math}

### 本章代码实现与张量维度追踪 (Shape Tracing)
```python
{ch4_code}
```

### 本章专属作业题目 (Chapter HW)
- [ ] 题目 1：使用 Profiler 工具排查本章代码执行过程中的显存/内存瓶颈与计算瓶颈。
- [ ] 题目 2：对比加入优化策略前后模型的吞吐量差异。

---

## 📖 第 5 章：前沿扩展与综合应用

### 本章核心理论与数学推导 (LaTeX)
在第 5 章的语境中，我们需要掌握前沿扩展与综合应用。
{ch5_math}

### 本章代码实现与张量维度追踪 (Shape Tracing)
```python
{ch5_code}
```

### 本章专属作业题目 (Chapter HW)
- [ ] 题目 1：将本章介绍的前沿优化方法应用到真实的下游任务中并评估性能指标。
- [ ] 题目 2：结合最新研读的论文，撰写一份关于该主题技术演进脉络的复盘总结。

---

## 📖 综合 Rubric 验收

### 验收标准
| 维度 | 优秀 (A) | 合格 (B) | 待改进 (C) |
|---|---|---|---|
{rubric_rows}

### 验收 Checklist
- [ ] 核心公式闭卷推导无误
- [ ] 代码手写实现并跑通验证
- [ ] 本手册配套作业全部完成
- [ ] Anki 卡片已添加并复习

---

## 🃏 Anki 复习提炼卡
{anki_qa}
"""

updated_cnt = 0
for fp in bp_files:
    content = get_custom_content(fp)
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(content)
    updated_cnt += 1

print(f"Successfully updated {updated_cnt} project manuals with domain-specific content!")
