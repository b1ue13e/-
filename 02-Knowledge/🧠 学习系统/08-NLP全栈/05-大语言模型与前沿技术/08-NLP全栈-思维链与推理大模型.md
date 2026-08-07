---
sources: ['Wei, J., Wang, X., Schuurmans, D., Bosma, M., Chi, E., Le, Q., & Zhou, D. (2022). Chain-of-thought prompting elicits reasoning in large language models. NeurIPS 2022.', 'DeepSeek-AI (2025). DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning. arXiv:2501.12948.', 'OpenAI (2024). Learning to Reason with LLMs (OpenAI o1 Technical Report).']
course: "08-NLP全栈"
type: study
flow: knowledge
kind: concept
topic: "思维链与推理大模型"
created: 2026-08-07
status: completed
assessment_exempt: false
difficulty: advanced
stage_moc: "[[🧭 阶段5-大语言模型与前沿技术]]"
upstream: ["[[08-NLP全栈-提示工程]]", "[[08-NLP全栈-DPO直接偏好优化与RLHF对齐]]"]
tags: [学习, NLP, LLM, 思维链, CoT, 推理大模型, DeepSeek-R1, OpenAI-o1, PRM, GRPO]
---

# 08-NLP全栈-思维链与推理大模型

---

## 1. 这个知识点解决什么问题？

> **我们遇到了什么麻烦**：
> 传统大语言模型（如 GPT-3.5、LLaMA-2）在处理多步数学推导、复杂代码生成与逻辑推理任务时，往往因“快思考（System 1）”直觉输出而导致中间逻辑断裂或幻觉累积。如何让 LLM 具备类似人类“慢思考（System 2）”的反思、自我纠错与长链条逻辑推演能力，是生成式 AI 从普通对话向高阶专家推理跨越的核心难题。

---

## 2. 为什么它重要？它有什么用？

- **连接大图景**：思维链（Chain-of-Thought, CoT）与推理大模型（如 OpenAI o1/o3、DeepSeek-R1）代表了 2024-2026 年大模型发展的核心前沿——**测试时计算扩展律 (Test-Time Compute Scaling Law)**。
- **核心优势**：
  1. **复杂逻辑拆解**：将单步映射转换成多步中间推理轨迹 $z_1, z_2, \dots, z_K$，极大降低每一步的预测熵值。
  2. **推理预算扩展**：在推理阶段（Inference Time）通过增加 Token 思考长度或 MCTS 树搜索，按需换取更高准确率。
  3. **强化学习自主涌现**：通过纯 RL（如 GRPO）在不依赖大量人工 CoT 标注的情况下，自主涌现“自我顿悟 (Aha Moment)”与反思验证。

---

## 3. 数学推导与理论证明

### 1. 马尔可夫决策过程与思维轨迹分解

设输入提示为 $x$，最终答案为 $y$。传统生成建模直接预测 $P(y|x)$。
引入中间思维链 Token 序列 $Z = (z_1, z_2, \dots, z_K)$，联合概率分布分解为：

$$P(y, Z \mid x) = \prod_{k=1}^K P(z_k \mid x, z_{<k}) \cdot P(y \mid x, Z)$$

通过全概率公式，引入思维链后的边际概率为：

$$P(y \mid x) = \sum_{Z} P(y \mid x, Z) P(Z \mid x)$$

由于推理模型仅生成高边际似然的有效推理链 $Z^*$，边缘分布的峰值效应使得复杂答案 $y$ 的熵 $H(Y \mid X, Z^*) \ll H(Y \mid X)$。

### 2. 结果监督 (ORM) vs 过程监督 (PRM)

- **结果奖励模型 (Outcome-based Reward Model, ORM)**：对生成结果仅给予标量反馈 $R(x, y) \in \{0, 1\}$。
- **过程奖励模型 (Process-based Reward Model, PRM)**：对思维链的每一步 $z_k$ 分配逐步奖励 $r(x, z_1, \dots, z_k)$。

对 $K$ 步推理链，整体软最大化目标函数可表示为：

$$\max_{\theta} \mathbb{E}_{(x,y) \sim \mathcal{D}} \left[ \sum_{k=1}^K \gamma^k r_\psi(x, z_{\le k}) - \beta D_{\text{KL}}\left(\pi_\theta(z_k \mid x, z_{<k}) \parallel \pi_{\text{ref}}(z_k \mid x, z_{<k})\right) \right]$$

### 3. DeepSeek-R1 的 GRPO 目标函数

Group Relative Policy Optimization (GRPO) 抛弃了独立的 Critic 网络，通过对同一 Prompt $x$ 采样 $G$ 个推理输出 $\{y_1, y_2, \dots, y_G\}$ 归一化计算优势 $A_i$：

$$A_i = \frac{r_i - \text{mean}(\{r_1, \dots, r_G\})}{\text{std}(\{r_1, \dots, r_G\}) + \epsilon}$$

GRPO 优化目标为：

$$\mathcal{J}_{\text{GRPO}}(\theta) = \mathbb{E}\left[ \frac{1}{G} \sum_{i=1}^G \min\left( \frac{\pi_\theta(y_i \mid x)}{\pi_{\text{old}}(y_i \mid x)} A_i, \text{clip}\left(\frac{\pi_\theta(y_i \mid x)}{\pi_{\text{old}}(y_i \mid x)}, 1-\epsilon, 1+\epsilon\right) A_i \right) - \beta D_{\text{KL}}(\pi_\theta \parallel \pi_{\text{ref}}) \right]$$

---

## 4. PyTorch 最小代码实现 (Process Verification & CoT Scorer)

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class StepProcessRewardModel(nn.Module):
    """
    简易过程奖励模型 (PRM) 评分器：评估思维链每个推理步骤的正确概率
    """
    def __init__(self, hidden_dim: int = 128):
        super().__init__()
        self.step_encoder = nn.Linear(hidden_dim, hidden_dim)
        self.reward_head = nn.Linear(hidden_dim, 1)

    def forward(self, step_embeddings: torch.Tensor) -> torch.Tensor:
        # step_embeddings: [Batch, Num_Steps, Hidden_Dim]
        h = F.relu(self.step_encoder(step_embeddings))
        step_scores = torch.sigmoid(self.reward_head(h)).squeeze(-1) # [Batch, Num_Steps]
        return step_scores

def compute_grpo_advantages(rewards: torch.Tensor, eps: float = 1e-8) -> torch.Tensor:
    """
    根据 Group 组内奖励算子计算相对优势 Advantages
    rewards: [Batch_Size (Group_Size)]
    """
    mean_r = rewards.mean()
    std_r = rewards.std(unbiased=False)
    advantages = (rewards - mean_r) / (std_r + eps)
    return advantages

# 验证代码逻辑
group_size = 4
hidden_dim = 128
num_steps = 5

prm = StepProcessRewardModel(hidden_dim=hidden_dim)
dummy_steps = torch.randn(group_size, num_steps, hidden_dim)
step_probs = prm(dummy_steps)

# 模拟末端结果奖励 (1 代表计算正确, 0 代表错误)
dummy_rewards = torch.tensor([1.0, 0.0, 1.0, 0.0])
adv = compute_grpo_advantages(dummy_rewards)

assert step_probs.shape == (group_size, num_steps)
assert adv.shape == (group_size,)
print("CoT PRM & GRPO Advantage Computation Passed!")
print("Sample Advantages:", adv)
```

---

## 5. 常见误区与对比矩阵

| 评估维度 / 特性 | Zero-Shot CoT | Few-Shot CoT | 推理强化学习 (DeepSeek-R1 / o1) |
| :--- | :--- | :--- | :--- |
| **触发机制** | 提示词追加 `"Let's think step by step"` | 提供带完整推理步骤的示例 (Few-Shot Prompt) | 模型内部涌现 `<think> ... </think>` 思考块 |
| **泛化性与稳定度** | 依赖 Prompt 敏感，复杂题易崩溃 | 受限于 Context 长度与 Exemplar 偏差 | 极高，泛化至未见过的长链题型 |
| **训练依赖度** | 无需训练 | 无需训练 | 需高强度 RL (GRPO / PPO) 与过程监督 |
| **推理开销 (Latency)** | 增加 2x~3x Token | 增加 3x~5x Token | 根据难题程度动态膨胀 5x~20x Token |

---

## 6. 常见误区与易错点

### 误区：CoT 只是单纯在 Prompt 里加提示词
- **事实纠偏**：Prompt 级别的 CoT 仅为表层触发器。现代推理大模型（R1/o1）是在**预训练与 RL 阶段**通过自博弈（Self-Play）与规则奖励约束，将推理能力内化为模型的内隐式“慢思考”状态机。

---

## 🛠️ 学完后可以完成

### 派生作业与验收入口
```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```

### 关联下游知识点
```dataview
LIST
FROM "02-Knowledge/🧠 学习系统/08-NLP全栈"
WHERE contains(upstream, this.file.link)
SORT file.name ASC
```

---

## 7. 参考文献与延伸阅读

- Wei, J., et al. (2022). Chain-of-thought prompting elicits reasoning in large language models. *NeurIPS 2022*.
- Lightman, H., et al. (2023). Let's Verify Step by Step. *arXiv:2305.20050*.
- DeepSeek-AI (2025). DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning. *arXiv:2501.12948*.

---

## 🛠️ 我的主动回忆区 (Guided Recall)

- [ ] **问题 1**：请不看笔记，口述《思维链与推理大模型》的核心定义与求解动机。
- [ ] **问题 2**：算法或推导的核心计算公式是什么？其中关键变量代表什么物理含义？
- [ ] **问题 3**：在实际工程落地或模型训练中，该方法最常见的 2 个踩坑点或退化场景是什么？

---

## 🃏 闭卷提取练习 (Self-Quiz)

1. **概念自测**：对比结果监督 (ORM) 与过程监督 (PRM) 的本质区别，为什么 PRM 能有效抑制步骤幻觉？
2. **代数/代码自测**：写出 GRPO 组内优势归一化的计算公式，并说明为什么它无需 Critic 网络？
3. **防错自测**：在长链推理中，模型出现反复死循环重复解题时，应如何在 Reward 中加入长度惩罚或终止符约束？
