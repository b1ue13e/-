"""
信赖域 Dogleg 方法 (Powell Dogleg Trust Region Method)
实现柯西点 (Cauchy Point) 与牛顿步 (Newton Step) 的折线折衷
支持信赖域半径 Delta_k 的自适应更新与收敛指标追踪
"""
import numpy as np

def dogleg_step(g, B, delta):
    """
    计算 Powell Dogleg 步 p_dogleg，满足 ||p|| <= delta
    """
    # 1. 柯西点方向与步长
    g_g = np.dot(g, g)
    g_Bg = np.dot(g, B @ g)
    if g_Bg <= 0:
        alpha = 1.0
    else:
        alpha = g_g / g_Bg

    p_C = -alpha * g
    norm_p_C = np.linalg.norm(p_C)

    if norm_p_C >= delta:
        return (delta / norm_p_C) * p_C

    # 2. 未约束牛顿步
    try:
        p_N = -np.linalg.solve(B, g)
    except np.linalg.LinAlgError:
        p_N = -g

    norm_p_N = np.linalg.norm(p_N)
    if norm_p_N <= delta:
        return p_N

    # 3. 折线 Dogleg 步: p(tau) = p_C + (tau - 1) * (p_N - p_C), 1 <= tau <= 2
    v = p_N - p_C
    v_v = np.dot(v, v)
    p_C_v = np.dot(p_C, v)
    p_C_p_C = np.dot(p_C, p_C)

    # 求解 ||p_C + (tau - 1) v||^2 = delta^2
    # a * t^2 + b * t + c = 0, t = tau - 1
    a = v_v
    b = 2 * p_C_v
    c = p_C_p_C - delta**2

    discriminant = b**2 - 4*a*c
    if discriminant < 0:
        t = 0.0
    else:
        t = (-b + np.sqrt(discriminant)) / (2*a)

    return p_C + t * v


def trust_region_dogleg(f, grad_f, hess_f, x0, delta0=1.0, max_delta=10.0, eta=0.15, max_iters=100, tol=1e-5):
    """
    信赖域 Dogleg 算法主流程
    返回: x_opt, history (含 (k, f_val, ||grad||, delta_k))
    """
    x = np.array(x0, dtype=float)
    delta = float(delta0)
    history = []

    for k in range(max_iters):
        g = grad_f(x)
        B = hess_f(x)
        g_norm = np.linalg.norm(g)
        history.append((k, f(x), g_norm, delta))

        if g_norm < tol:
            break

        p = dogleg_step(g, B, delta)

        # 实际下降 vs 预测下降
        actual_red = f(x) - f(x + p)
        pred_red = -(np.dot(g, p) + 0.5 * np.dot(p, B @ p))

        rho = actual_red / (pred_red + 1e-12)

        # 更新半径 delta
        if rho < 0.25:
            delta = 0.25 * delta
        else:
            if rho > 0.75 and np.abs(np.linalg.norm(p) - delta) < 1e-4:
                delta = min(2.0 * delta, max_delta)

        # 更新位置 x
        if rho > eta:
            x = x + p

    return x, history
