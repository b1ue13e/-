"""
07-最优化方法 · 课后作业 05 算法实现脚本: BFGS 拟牛顿法
"""
import numpy as np

def armijo_line_search(f, grad_f, x, d, c1=1e-4, rho=0.5):
    """Armijo 回溯线搜索"""
    alpha = 1.0
    fx = f(x)
    gx = grad_f(x)
    while f(x + alpha * d) > fx + c1 * alpha * np.dot(gx, d):
        alpha *= rho
        if alpha < 1e-12:
            break
    return alpha

def bfgs_optimizer(f, grad_f, x0, max_iters=200, tol=1e-6):
    """手撕 BFGS 拟牛顿法"""
    x = np.array(x0, dtype=float)
    n = len(x)
    H = np.eye(n)
    history = [x.copy()]
    
    for _ in range(max_iters):
        g = grad_f(x)
        if np.linalg.norm(g) < tol:
            break
        d = - H @ g
        alpha = armijo_line_search(f, grad_f, x, d)
        x_next = x + alpha * d
        g_next = grad_f(x_next)
        
        s = x_next - x
        y = g_next - g
        ys = np.dot(y, s)
        if ys > 1e-10:
            rho = 1.0 / ys
            I = np.eye(n)
            H = (I - rho * np.outer(s, y)) @ H @ (I - rho * np.outer(y, s)) + rho * np.outer(s, s)
            
        x = x_next
        history.append(x.copy())
        
    return x, history
