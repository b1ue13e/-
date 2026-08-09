"""
阶段作业 03: DPO (Direct Preference Optimization) 偏好对齐损失算法单元测试
"""
import pytest
import torch
import torch.nn.functional as F

def dpo_loss(
    policy_chosen_logps: torch.Tensor,
    policy_rejected_logps: torch.Tensor,
    reference_chosen_logps: torch.Tensor,
    reference_rejected_logps: torch.Tensor,
    beta: float = 0.1,
) -> torch.Tensor:
    """
    DPO Loss 表达公式:
    L_DPO = -E [ log sigmoid ( beta * ( (log p_pi(y_w|x) - log p_ref(y_w|x)) - (log p_pi(y_l|x) - log p_ref(y_l|x)) ) ) ]
    """
    pi_logratios = policy_chosen_logps - policy_rejected_logps
    ref_logratios = reference_chosen_logps - reference_rejected_logps
    logits = pi_logratios - ref_logratios
    losses = -F.logsigmoid(beta * logits)
    return losses.mean()

def test_dpo_loss_computation():
    batch_size = 4
    policy_chosen_logps = torch.tensor([-1.0, -1.2, -0.8, -1.5])
    policy_rejected_logps = torch.tensor([-2.5, -3.0, -2.8, -4.0])
    reference_chosen_logps = torch.tensor([-1.1, -1.3, -0.9, -1.6])
    reference_rejected_logps = torch.tensor([-2.0, -2.2, -2.1, -2.5])

    loss = dpo_loss(
        policy_chosen_logps,
        policy_rejected_logps,
        reference_chosen_logps,
        reference_rejected_logps,
        beta=0.1
    )

    assert isinstance(loss, torch.Tensor), "DPO loss 应该返回 PyTorch Tensor"
    assert loss.dim() == 0, "DPO loss 应该标量化 (mean)"
    assert loss.item() > 0, "DPO 损失标量值应大于 0"

def test_dpo_loss_preference_reward():
    # 当 Policy 模型极其偏好 chosen 且远胜 ref 时, logits > 0, loss 应该极小
    policy_chosen_logps = torch.tensor([0.0])
    policy_rejected_logps = torch.tensor([-10.0])
    reference_chosen_logps = torch.tensor([-5.0])
    reference_rejected_logps = torch.tensor([-5.0])

    loss = dpo_loss(
        policy_chosen_logps,
        policy_rejected_logps,
        reference_chosen_logps,
        reference_rejected_logps,
        beta=0.5
    )

    assert loss.item() < 0.05, f"当 Policy 极大偏好 chosen 样本时, DPO Loss 应该接近于 0, 实际为 {loss.item()}"
