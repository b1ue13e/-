"""
07-最优化方法 · 阶段作业 04 算法实现脚本: FISTA 近端加速梯度求解器
"""
import numpy as np

def soft_thresholding(x, tau):
    """软阈值算子"""
    return np.sign(x) * np.maximum(np.abs(x) - tau, 0.0)

def fista_lasso(X, y, lmbda, max_iters=500, L=None):
    """FISTA 求解 Lasso"""
    N, d = X.shape
    if L is None:
        L = np.linalg.norm(X, ord=2)**2 / N
    
    w = np.zeros(d)
    y_k = w.copy()
    t = 1.0
    history = []
    
    for _ in range(max_iters):
        grad = (1.0 / N) * X.T @ (X @ y_k - y)
        w_next = soft_thresholding(y_k - (1.0 / L) * grad, lmbda / L)
        t_next = (1.0 + np.sqrt(1.0 + 4.0 * t**2)) / 2.0
        y_k = w_next + ((t - 1.0) / t_next) * (w_next - w)
        
        w = w_next
        t = t_next
        loss = 0.5 / N * np.sum((X @ w - y)**2) + lmbda * np.sum(np.abs(w))
        history.append(loss)
        
    return w, history
