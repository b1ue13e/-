---
type: study
topic: "PPO 近端策略优化"
course: "强化学习"
created: 2026-04-18
status: completed
stage_moc: "[[🧭 阶段7-PPO]]"
flow: knowledge
kind: concept
difficulty: intermediate
concept: ["PPO", "近端策略优化", "裁剪目标", "GAE"]
upstream: ["[[Actor-Critic 与 PPO]]", "[[TRPO-信任区域]]", "[[优势-定义]]"]
tags: [学习, 强化学习]
---
> 所属模块：[[🗺️ 强化学习学习路径|强化学习学习路径]]
> 主教材：`《Reinforcement Learning》`
> 对应阶段：[[🧭 阶段7-PPO|返回阶段页]]

# PPO 近端策略优化 (Proximal Policy Optimization)

## 1. PPO 近端策略优化的定义与核心动机

**PPO 近端策略优化 (Proximal Policy Optimization)** 的核心定义是：一种通过截断概率比率 (Clipped Probability Ratio) 约束新旧策略变化幅度、防止策略更新步长过大导致训练崩溃的**同策略 (On-Policy)** Actor-Critic 深度强化学习算法。由 Schulman 等人于 2017 年在 OpenAI 提出。

**基本性质**：PPO 近端策略优化具备 TRPO (Trust Region Policy Optimization) 保证单调提升的优良理论特性，同时将复杂的高阶 KL 散度 Hessian 约束简化为极易实现的**第一阶一元截断目标函数 (PPO-Clip)**，兼具算法简易性、样本效率与极高的工程鲁棒性，是 ChatGPT Reinforcement Learning from Human Feedback (RLHF) 微调的默认标准算法。

---

## 2. PPO-Clip 截断目标函数形式化推导

**概率比率定义**：
设新策略为 $\pi_\theta(a|s)$，旧采样策略为 $\pi_{\theta_{\text{old}}}(a|s)$，概率比率为：
$$r_t(\theta) = \frac{\pi_\theta(a_t|s_t)}{\pi_{\theta_{\text{old}}}(a_t|s_t)}, \quad \text{显然 } r_t(\theta_{\text{old}}) = 1$$

**广义优势估计 AEV (Advantage) 与 PPO-Clip 目标函数推导**：
1. 设 $A_t$ 为广义优势函数 (GAE) 估计值；
2. 基础策略梯度目标：$L^{\text{CPI}}(\theta) = \mathbb{E}_t \left[ r_t(\theta) A_t 
\right]$；
3. **PPO-Clip 截断目标**：为了限制 $r_t(\theta)$ 远离区间 $[1-\epsilon, 1+\epsilon]$（通常 $\epsilon=0.2$）：
$$L^{\text{CLIP}}(\theta) = \hat{\mathbb{E}}_t \left[ \min\left( r_t(\theta) A_t, \;\text{clip}(r_t(\theta), 1-\epsilon, 1+\epsilon) A_t 
\right) 
\right]$$
4. **悲观下界 (Pessimistic Bound) 推导**：取 $\min$ 确保了当优势 $A_t > 0$ 时，若 $r_t > 1+\epsilon$（策略改善过大），目标被封顶在 $(1+\epsilon) A_t$，梯度归零不给予额外奖励；当 $A_t < 0$ 时，若 $r_t < 1-\epsilon$，同样截断封顶。
5. **因此**，该下界悲观约束彻底阻止了策略发生破坏性的巨幅更新。

---

## 3. PPO-Clip 与 TRPO / 基础 Policy Gradient 的区别与对比

| 维度 | 基础策略梯度 (REINFORCE) | TRPO (置信域策略优化) | PPO 近端策略优化 (PPO-Clip) |
|:---|:---|:---|:---|
| **策略约束手段** | 无 (纯梯度下降) | **硬 KL 散度约束** $D_{\text{KL}} \le \delta$ | **软截断比例** $\text{clip}(r_t, 1\pm\epsilon)$ |
| **优化器与求解** | 标准 SGD / Adam | 需计算共轭梯度与 Hessian 向量积 | **标准一阶 Adam 优化器** |
| **代码实现难度** | 极简单 | 极度复杂 (计算图昂贵) | **极简 (仅需 3 行代码实现 clip)** |
| **多 Epoch 重复利用数据** | 否 (单次数据使用) | 否 (单步估计) | **是 (同一批数据可重复训练多 Epoch)** |
| **大模型 RLHF 适配度** | 差 (容易崩溃) | 差 (显存/内存开销过高) | **行业通用标准 (ChatGPT / LLM)** |

**局限（误区）**：PPO 近端策略优化依然属于 On-Policy 范畴，相较于 Off-Policy 算法（如 SAC、TD3），其样本利用率 (Sample Efficiency) 依然较低；另外优势函数 $A_t$ 的估计极度依赖 Critic 网络的准确度。

关联知识点推荐：[[Q-Learning算法]]、[[梯度下降与优化器|梯度下降与Adam优化器]]、[[信息论基础|交叉熵损失函数]]、[[Amdahl定律]]。

---

## 4. Python 核心 PPO-Clip 目标函数计算与梯度的自测断言

```python
import numpy as np

def ppo_clip_loss(pi_new_logits: np.ndarray, pi_old_logits: np.ndarray,
                  actions: np.ndarray, advantages: np.ndarray,
                  epsilon: float = 0.2) -> tuple:
    """
    PPO-Clip 损失函数与软截断梯度仿真
    假设: 离散动作空间，给定未归一化 logits
    推导: ratio = exp(log_pi_new - log_pi_old), L = min(ratio*A, clip(ratio, 1-eps, 1+eps)*A)
    """
    # 简化的 Softmax 概率提取
    def log_prob(logits, a):
        max_l = np.max(logits, axis=-1, keepdims=True)
        exp_l = np.exp(logits - max_l)
        probs = exp_l / np.sum(exp_l, axis=-1, keepdims=True)
        return np.log(probs[np.arange(len(a)), a] + 1e-10)

    log_pi_new = log_prob(pi_new_logits, actions)
    log_pi_old = log_prob(pi_old_logits, actions)

    ratio = np.exp(log_pi_new - log_pi_old)

    # 1. 计算未截断与截断项
    surr1 = ratio * advantages
    surr2 = np.clip(ratio, 1.0 - epsilon, 1.0 + epsilon) * advantages

    # 2. 取悲观下界 (取负数因为优化器做最小化)
    loss = -np.mean(np.minimum(surr1, surr2))

    return float(loss), ratio

if __name__ == "__main__":
    np.random.seed(42)
    # 2 个样本，旧策略 logits
    old_logits = np.array([[1.0, 2.0], [2.0, 1.0]])
    actions = np.array([1, 0])
    advantages = np.array([2.0, -1.5])  # 样本0优势正，样本1优势负

    # 情况 1: 新旧策略一致 (ratio = 1.0)
    loss_equal, ratio_equal = ppo_clip_loss(old_logits, old_logits, actions, advantages)
    # loss = -mean([1.0*2.0, 1.0*(-1.5)]) = -mean([2.0, -1.5]) = -0.25
    assert abs(loss_equal - (-0.25)) < 1e-5

    # 情况 2: 新策略变化过大 (ratio > 1 + epsilon, 触发正向截断)
    new_logits_large = np.array([[1.0, 5.0], [2.0, 1.0]])  # 动作 1 概率大幅上升
    loss_clip, ratio_clip = ppo_clip_loss(new_logits_large, old_logits, actions, advantages)
    assert ratio_clip[0] > 1.2
    # 截断后 surr2[0] = 1.2 * 2.0 = 2.4，min(surr1, surr2) = 2.4 限制增长
    print(f"PPO 采样比率 = {ratio_clip[0]:.2f} (成功触发 1.2 截断上限)")

    print(f"PPO-Clip 损失函数计算成功: 初始 Loss = {loss_equal:.4f}, 截断后 Loss = {loss_clip:.4f}")
    print("PPO 近端策略优化单元测试与自查验证全部成功！")
```

---

## 5. 权威参考文献
- Schulman, J., Wolski, F., Dhariwal, P., Radford, A., & Klimov, O. (2017). Proximal policy optimization algorithms. *arXiv preprint arXiv:1707.06347*. URL: https://arxiv.org/abs/1707.06347
- Schulman, J., Levine, S., Abbeel, P., Jordan, M., & Moritz, P. (2015). Trust region policy optimization. *International Conference on Machine Learning (ICML '15)*, 1889-1897. URL: https://arxiv.org/abs/1502.05477
- Ouyang, L., et al. (2022). Training language models to follow instructions with human feedback (InstructGPT / ChatGPT). *Advances in Neural Information Processing Systems (NeurIPS '22)*, 35, 27730-27744. URL: https://arxiv.org/abs/2203.02155

## 闭卷自测
1. PPO 裁剪目标如何限制单步更新步幅？
2. GAE 在 PPO 中承担什么角色？
3. PPO 相比 TRPO 为何更易实现且同样有效？

## 学完后可以完成

```dataview
TABLE assignment_level, source_type FROM "03-Projects"
WHERE contains(requires, this.file.link)
```

## 相关下游知识

```dataview
LIST FROM "02-Knowledge/🧠 学习系统"
WHERE contains(upstream, this.file.link)
```
