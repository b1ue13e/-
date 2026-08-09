"""
07-最优化方法 · 阶段作业 04 算法实现脚本: FISTA 近端加速梯度求解器与软阈值算子
"""
import numpy as np

def soft_thresholding(x, tau):
    """软阈值近端算子 prox_{tau ||.||_1}(x) = sign(x) * max(|x| - tau, 0)"""
    return np.sign(x) * np.maximum(np.abs(x) - tau, 0.0)

def fista_lasso(X, y, lmbda, max_iters=200, L=None):
    """
    FISTA 求解 Lasso 目标: min 0.5/N ||X w - y||_2^2 + lmbda ||w||_1
    具备 O(1/k^2) 加速近端收敛性
    """
    N, d = X.shape
    if L is None:
        # Lipschitz 常数估计: L = ||X^T X||_2 / N
        eigvals = np.linalg.eigvalsh(X.T @ X)
        L = float(np.max(eigvals)) / N + 1e-6
    
    w = np.zeros(d)
    y_k = w.copy()
    t = 1.0
    history = []
    
    for _ in range(max_iters):
        # 梯度算子 (光滑项)
        grad = (1.0 / N) * X.T @ (X @ y_k - y)
        # 近端算子 (非光滑 L1 项)
        w_next = soft_thresholding(y_k - (1.0 / L) * grad, lmbda / L)
        
        # Nesterov 动量外推
        t_next = (1.0 + np.sqrt(1.0 + 4.0 * t**2)) / 2.0
        y_k = w_next + ((t - 1.0) / t_next) * (w_next - w)
        
        w = w_next
        t = t_next
        
        loss = 0.5 / N * np.sum((X @ w - y)**2) + lmbda * np.sum(np.abs(w))
        history.append(float(loss))
        
    return w, history
