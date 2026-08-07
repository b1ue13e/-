r"""
07-最优化方法 课后作业 06: 半定规划 (SDP) 与 Max-Cut 图最大割松弛求解器
基于 Goemans-Williamson (1995) 算法、Burer-Monteiro 黎曼流形投影法与 CVXPY/NumPy 备选
"""
import numpy as np

def maxcut_sdp_solver(W, max_iters=200):
    r"""
    求解 Max-Cut 问题半定规划松弛:
      max  1/4 * sum_{i,j} W_{ij} (1 - X_{ij})
      s.t. X_{ii} = 1, X \succeq 0
    优先使用 CVXPY；若未安装 cvxpy，自动降级至 Burer-Monteiro 黎曼流形投影算法 (纯 NumPy 实现)
    返回: X_opt, sdp_val
    """
    n = W.shape[0]

    try:
        import cvxpy as cp
        X = cp.Variable((n, n), PSD=True)
        cost = 0.25 * (np.sum(W) - cp.trace(W @ X))
        constraints = [cp.diag(X) == 1]
        prob = cp.Problem(cp.Maximize(cost), constraints)
        prob.solve(solver=cp.SCS, verbose=False)
        if X.value is not None:
            return X.value, prob.value
    except ModuleNotFoundError:
        pass

    # Burer-Monteiro (1999/2003) 黎曼流形求解器 (纯 NumPy 零依赖降级方案)
    # X = V V^T, V in R^{n x n}, 行范数 ||V_{i,:}|| = 1 (确保 X_{ii} = 1)
    np.random.seed(42)
    V = np.random.randn(n, n)
    V = V / np.linalg.norm(V, axis=1, keepdims=True)

    lr = 0.05
    for _ in range(max_iters):
        # 梯度 d/dV [ 1/4 (sum W - tr(W V V^T)) ] = -1/2 W V
        grad_V = -0.5 * (W @ V)
        # 上升方向 (最大化问题)
        V = V - lr * grad_V
        # 流形投影：归一化行范数
        norms = np.linalg.norm(V, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        V = V / norms

    X_opt = V @ V.T
    sdp_val = 0.25 * (np.sum(W) - np.trace(W @ X_opt))
    return X_opt, sdp_val


def random_hyperplane_rounding(X_opt, num_cuts=100):
    """
    Goemans-Williamson 随机超平面剪切算法:
      从 X_opt 提取 Cholesky/特征值因子 V (V V^T = X)，
      随机采样超平面法向量 r ~ N(0, I)，
      计算节点二值切割 sign(V r)。
    返回: best_cut (1/-1 向量)
    """
    n = X_opt.shape[0]
    
    # 特征值分解保证 PSD 因子分解
    eigvals, eigvecs = np.linalg.eigh(X_opt)
    eigvals = np.maximum(eigvals, 0)
    V = eigvecs @ np.diag(np.sqrt(eigvals)) # n x n
    
    best_cut = None
    best_val = -1.0

    for _ in range(num_cuts):
        r = np.random.randn(n)
        s = np.sign(V @ r)
        s[s == 0] = 1
        best_cut = s

    return best_cut
