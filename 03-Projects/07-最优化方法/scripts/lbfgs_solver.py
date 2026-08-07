"""
L-BFGS (Limited-memory BFGS) 求解器与双循环递归 (Two-Loop Recursion)
支持历史缓存 m、Backtracking Line Search 及收敛轨线追踪
"""
import numpy as np

def lbfgs_two_loop(g_k, s_history, y_history):
    """
    L-BFGS 双循环递归计算搜索方向 r = - H_k * g_k
    """
    m_count = len(s_history)
    if m_count == 0:
        return -g_k

    q = g_k.copy()
    alphas = []

    # 第一循环：逆序计算 alpha_i
    for i in reversed(range(m_count)):
        s_i = s_history[i]
        y_i = y_history[i]
        rho_i = 1.0 / (np.dot(y_i, s_i) + 1e-10)
        alpha_i = rho_i * np.dot(s_i, q)
        alphas.append(alpha_i)
        q = q - alpha_i * y_i

    alphas.reverse()

    # 基础 Hessian 缩放：H_0^k = (s_k^T y_k / y_k^T y_k) * I
    s_last = s_history[-1]
    y_last = y_history[-1]
    gamma = np.dot(s_last, y_last) / (np.dot(y_last, y_last) + 1e-10)
    r = gamma * q

    # 第二循环：顺序更新 r
    for i in range(m_count):
        s_i = s_history[i]
        y_i = y_history[i]
        rho_i = 1.0 / (np.dot(y_i, s_i) + 1e-10)
        beta = rho_i * np.dot(y_i, r)
        r = r + s_i * (alphas[i] - beta)

    return -r


def lbfgs_optimizer(f, grad_f, x0, m=10, max_iters=200, tol=1e-5):
    """
    L-BFGS 主优化函数
    返回：x_opt, convergence_history (含 (iter, f_val, ||grad||))
    """
    x = np.array(x0, dtype=float)
    s_history = []
    y_history = []
    history = []

    for k in range(max_iters):
        g = grad_f(x)
        g_norm = np.linalg.norm(g)
        history.append((k, f(x), g_norm))

        if g_norm < tol:
            break

        p = lbfgs_two_loop(g, s_history, y_history)

        # 回溯线搜索 (Armijo Line Search)
        alpha = 1.0
        c1 = 1e-4
        f_val = f(x)
        while f(x + alpha * p) > f_val + c1 * alpha * np.dot(g, p):
            alpha *= 0.5
            if alpha < 1e-12:
                break

        x_next = x + alpha * p
        g_next = grad_f(x_next)

        s_k = x_next - x
        y_k = g_next - g

        if np.dot(s_k, y_k) > 1e-10:
            if len(s_history) >= m:
                s_history.pop(0)
                y_history.pop(0)
            s_history.append(s_k)
            y_history.append(y_k)

        x = x_next

    return x, history
