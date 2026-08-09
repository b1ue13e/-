"""
现代大模型优化器核心实现包
包含:
1. Lion (EvoLved Sign Momentum Optimizer)
2. Muon (Momentum Orthogonalized by Newton-Schulz)
3. Dynamic Loss Scaler (FP16 / BF16 混合精度数值稳定性组件)
"""

import numpy as np
from typing import List, Tuple, Optional


def newton_schulz_polar(G: np.ndarray, steps: int = 10, eps: float = 1e-7) -> np.ndarray:
    """
    Newton-Schulz 极分解正交化算法 (Muon 核心)
    目标: 将 2D 动量矩阵 G 投影至最近的正交/酉矩阵，拉平所有奇异值为 1。
    数学迭代: X_{k+1} = 1.5 * X_k - 0.5 * (X_k @ X_k^T) @ X_k
    """
    assert G.ndim == 2, "Muon 正交化算法仅适用于 2D 权重矩阵"
    transposed = False
    if G.shape[0] > G.shape[1]:
        G = G.T
        transposed = True

    d1, d2 = G.shape
    # 谱范数或二范数初值归一化，保证谱半径落在收敛域 (0, sqrt(3)) 内
    norm = np.linalg.norm(G, 2) + eps
    X = G / norm

    for _ in range(steps):
        # 极分解二次收敛 Newton-Schulz 迭代
        X = 1.5 * X - 0.5 * (X @ X.T) @ X

    return X.T if transposed else X


class Lion:
    """
    Lion (EvoLved Sign Momentum) 优化器
    每参数仅需 4 字节显存 (仅一阶动量)，更新步长模长有界。
    """
    def __init__(self, params: List[np.ndarray], lr: float = 1e-4, beta1: float = 0.9, beta2: float = 0.99, weight_decay: float = 0.0):
        self.params = params
        self.lr = lr
        self.beta1 = beta1
        self.beta2 = beta2
        self.wd = weight_decay
        self.exp_avg = [np.zeros_like(p) for p in self.params]

    def step(self, grads: List[np.ndarray]) -> None:
        for p, g, m in zip(self.params, grads, self.exp_avg):
            # 1. 解耦权重衰减
            if self.wd != 0:
                p -= self.lr * self.wd * p

            # 2. 插值方向并取符号 (刚性有界更新)
            c = self.beta1 * m + (1.0 - self.beta1) * g
            update = np.sign(c)

            # 3. 参数更新
            p -= self.lr * update

            # 4. 动量缓存累积
            m *= self.beta2
            m += (1.0 - self.beta2) * g


class Muon:
    """
    Muon 优化器 (用于 2D 线性层/注意力投影矩阵)
    结合 Polyak 动量与 Newton-Schulz 谱正交化。
    """
    def __init__(self, params: List[np.ndarray], lr: float = 0.02, momentum: float = 0.95, nesterov: bool = True, ns_steps: int = 8):
        self.params = params
        self.lr = lr
        self.momentum = momentum
        self.nesterov = nesterov
        self.ns_steps = ns_steps
        self.exp_avg = [np.zeros_like(p) for p in self.params]

    def step(self, grads: List[np.ndarray]) -> None:
        for p, g, m in zip(self.params, grads, self.exp_avg):
            m *= self.momentum
            m += g
            
            direction = (self.momentum * m + g) if self.nesterov else m
            if p.ndim == 2:
                u = newton_schulz_polar(direction, steps=self.ns_steps)
                # 动态 RMS 尺度缩放
                rms_p = max(float(np.mean(p ** 2) ** 0.5), 1e-4)
                rms_u = max(float(np.mean(u ** 2) ** 0.5), 1e-4)
                scale = rms_p / rms_u
                p -= self.lr * scale * u
            else:
                # 1D 参数退化为普通动量
                p -= self.lr * direction


class DynamicLossScaler:
    """
    工业级动态损失缩放器 (Dynamic Loss Scaler)
    用于混合精度训练中防止极小梯度下溢 (Underflow)。
    """
    def __init__(self, init_scale: float = 65536.0, scale_factor: float = 2.0, scale_window: int = 100):
        self.scale = init_scale
        self.scale_factor = scale_factor
        self.scale_window = scale_window
        self.stable_steps = 0

    def scale_loss(self, loss_val: float) -> float:
        return loss_val * self.scale

    def unscale_and_update(self, grads: List[np.ndarray]) -> Tuple[List[np.ndarray], bool]:
        has_overflow = any(not np.isfinite(g).all() for g in grads)

        if has_overflow:
            self.scale = max(1.0, self.scale / self.scale_factor)
            self.stable_steps = 0
            return grads, False
        else:
            unscaled = [g / self.scale for g in grads]
            self.stable_steps += 1
            if self.stable_steps >= self.scale_window:
                self.scale *= self.scale_factor
                self.stable_steps = 0
            return unscaled, True
