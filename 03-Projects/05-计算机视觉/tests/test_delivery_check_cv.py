"""验证模型量化/模型剪枝卡增强示例（2026-08-06 交付检查）。"""
import numpy as np


def test_quantization_hand_example():
    """模型量化卡 3.3：对称量化（scale=x_max/127）误差 ≈ scale/2，int8 不溢出"""
    x = np.array([0.0, 0.5, 1.0, -1.0, 0.987])
    scale = 1.0 / 127.0
    q = np.round(x / scale).astype(np.int8)
    x_hat = q * scale
    err = np.abs(x - x_hat).max()
    assert err <= scale / 2 + 1e-9   # 最大绝对误差 ≤ 半个 scale
    assert q[0] == 0 and q[2] == 127  # x=1.0 → q=127（对称满量程，不溢出）


def test_pruning_parameter_calc():
    """模型剪枝卡 3.1：50% 通道剪枝 → 参数量减半"""
    c_in, c_out, k = 256, 256, 3
    base = c_in * c_out * k * k
    pruned = c_in * (c_out // 2) * k * k
    assert base == 589824 and pruned == 294912
    assert pruned / base == 0.5
    # FLOPs 检查：56x56 特征图
    flops_base = base * 56 * 56
    flops_pruned = pruned * 56 * 56
    assert abs(flops_base / 1e9 - 1.85) < 0.01   # ≈ 1.85 GMACs
    assert flops_pruned / flops_base == 0.5
