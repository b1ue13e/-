"""
Polyak 重球法 (Heavy-Ball Momentum) 与 Nesterov 加速梯度 (Nesterov Accelerated Gradient, NAG)
提供病态二次型与非凸目标函数下的收敛性对比与迭代轨迹追踪
"""
import numpy as np

def polyak_heavy_ball(f, grad_f, x0, lr=0.01, beta=0.9, max_iters=200, tol=1e-5):
    """
    Polyak 重球法 (Heavy-Ball)
    更新规则:
      v_{k+1} = beta * v_k - lr * grad_f(x_k)
      x_{k+1} = x_k + v_{k+1}
    """
    x = np.array(x0, dtype=float)
    v = np.zeros_like(x)
    history = []

    for k in range(max_iters):
        g = grad_f(x)
        g_norm = np.linalg.norm(g)
        history.append((k, f(x), g_norm))

        if g_norm < tol:
            break

        v = beta * v - lr * g
        x = x + v

    return x, history


def nesterov_accelerated_gradient(f, grad_f, x0, lr=0.01, beta=0.9, max_iters=200, tol=1e-5):
    """
    Nesterov 加速梯度 (NAG)
    更新规则:
      x_lookahead = x_k + beta * v_k
      v_{k+1} = beta * v_k - lr * grad_f(x_lookahead)
      x_{k+1} = x_k + v_{k+1}
    """
    x = np.array(x0, dtype=float)
    v = np.zeros_like(x)
    history = []

    for k in range(max_iters):
        g = grad_f(x)
        g_norm = np.linalg.norm(g)
        history.append((k, f(x), g_norm))

        if g_norm < tol:
            break

        x_lookahead = x + beta * v
        g_lookahead = grad_f(x_lookahead)
        v = beta * v - lr * g_lookahead
        x = x + v

    return x, history
