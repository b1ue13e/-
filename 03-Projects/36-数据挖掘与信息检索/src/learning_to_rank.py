"""
排序学习与链接分析模块：PageRank 幂迭代与纯 NumPy RankNet 神经网络
"""

import numpy as np
from typing import List, Tuple, Dict, Optional

class PageRank:
    """
    PageRank 链接分析引擎 (幂迭代算法)
    - 随机游走与阻尼因子 d (默认 0.85)
    - 严格处理悬空节点 (Dangling Nodes, 出度为 0 的节点平均重分配)
    - 随机跳转向量 (Teleportation): (1 - d) / N
    """
    def __init__(self, d: float = 0.85, max_iter: int = 200, tol: float = 1e-7):
        self.d = d
        self.max_iter = max_iter
        self.tol = tol

    def fit_predict(self, adj_matrix: np.ndarray) -> np.ndarray:
        N = adj_matrix.shape[0]
        assert adj_matrix.shape == (N, N), "邻接矩阵必须为 N x N 方阵"
        
        out_degree = np.sum(adj_matrix, axis=1)
        # 构造列随机转移矩阵 M_ij = A_ji / OutDeg(j)
        M = np.zeros((N, N), dtype=float)
        for j in range(N):
            if out_degree[j] > 0:
                M[:, j] = adj_matrix[j, :] / out_degree[j]
            else:
                M[:, j] = 1.0 / N  # 悬空节点平均分配
                
        r = np.full(N, 1.0 / N)
        teleport = np.full(N, (1.0 - self.d) / N)
        
        for _ in range(self.max_iter):
            r_next = self.d * np.dot(M, r) + teleport
            if np.sum(np.abs(r_next - r)) < self.tol:
                break
            r = r_next
            
        return r


class RankNetNumPy:
    """
    纯 NumPy 实现可训练的两层 RankNet 排序神经网络
    - 架构：Input (D) -> Dense (H, ReLU) -> Dense (1, Linear Score)
    - 目标：最小化 Pairwise 交叉熵损失
    - 概率建模：P_ij = sigmoid(s_i - s_j) = 1 / (1 + e^{-(s_i - s_j)})
    - 梯度传播：严格按链式法则更新两层权重与偏置
    """
    def __init__(self, input_dim: int, hidden_dim: int = 8, lr: float = 0.05, seed: int = 42):
        np.random.seed(seed)
        self.W1 = np.random.randn(input_dim, hidden_dim) * 0.1
        self.b1 = np.zeros(hidden_dim)
        self.W2 = np.random.randn(hidden_dim, 1) * 0.1
        self.b2 = np.zeros(1)
        self.lr = lr
        
        # 前向缓存
        self.z1: Optional[np.ndarray] = None
        self.a1: Optional[np.ndarray] = None
        self.score: Optional[np.ndarray] = None

    def forward(self, x: np.ndarray) -> np.ndarray:
        # x shape: (N, input_dim)
        self.z1 = np.dot(x, self.W1) + self.b1
        self.a1 = np.maximum(0, self.z1)  # ReLU
        self.score = np.dot(self.a1, self.W2) + self.b2
        return self.score.squeeze(-1)

    def train_step(self, x_i: np.ndarray, x_j: np.ndarray, target: float = 1.0) -> float:
        """
        单步 Pairwise 训练：文档 i 应当排在文档 j 之前 (target = 1.0)
        """
        s_i = self.forward(x_i)
        a1_i = self.a1.copy()
        s_j = self.forward(x_j)
        a1_j = self.a1.copy()

        diff = s_i - s_j
        # 数值稳定 sigmoid
        prob = 1.0 / (1.0 + np.exp(-np.clip(diff, -15.0, 15.0)))
        loss = -target * np.log(prob + 1e-12) - (1.0 - target) * np.log(1.0 - prob + 1e-12)

        # 梯度 dLoss / ds_i
        grad_si = prob - target
        grad_sj = -grad_si

        # 反向传播更新 W2, b2
        grad_W2 = np.dot(a1_i.T, grad_si[:, None]) + np.dot(a1_j.T, grad_sj[:, None])
        grad_b2 = np.sum(grad_si) + np.sum(grad_sj)

        # 隐藏层梯度
        grad_a1_i = np.dot(grad_si[:, None], self.W2.T) * (a1_i > 0)
        grad_a1_j = np.dot(grad_sj[:, None], self.W2.T) * (a1_j > 0)

        # 反向传播更新 W1, b1
        grad_W1 = np.dot(x_i.T, grad_a1_i) + np.dot(x_j.T, grad_a1_j)
        grad_b1 = np.sum(grad_a1_i, axis=0) + np.sum(grad_a1_j, axis=0)

        # 参数梯度下降
        self.W2 -= self.lr * grad_W2
        self.b2 -= self.lr * grad_b2
        self.W1 -= self.lr * grad_W1
        self.b1 -= self.lr * grad_b1

        return float(np.mean(loss))
