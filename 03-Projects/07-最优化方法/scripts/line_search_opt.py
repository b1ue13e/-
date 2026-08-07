"""
07-最优化方法 · 课后作业 04 算法实现脚本: 经典一阶与线搜索
"""
import numpy as np

def backtracking_armijo(f, grad_f, x, p, alpha0=1.0, c1=1e-4, rho=0.5):
    """Backtracking Armijo 线搜索"""
    alpha = alpha0
    fx = f(x)
    gx = grad_f(x)
    while f(x + alpha * p) > fx + c1 * alpha * np.dot(gx, p):
        alpha *= rho
        if alpha < 1e-12:
            break
    return alpha

def steepest_descent(f, grad_f, x0, tol=1e-6, max_iter=2000):
    """带 Armijo 线搜索的最速下降法"""
    x = np.array(x0, dtype=float)
    history = [x.copy()]
    for _ in range(max_iter):
        g = grad_f(x)
        if np.linalg.norm(g) < tol:
            break
        p = -g
        alpha = backtracking_armijo(f, grad_f, x, p)
        x = x + alpha * p
        history.append(x.copy())
    return x, history

def newton_method(f, grad_f, hess_f, x0, tol=1e-6, max_iter=100):
    """带线搜索的标准牛顿法"""
    x = np.array(x0, dtype=float)
    history = [x.copy()]
    for _ in range(max_iter):
        g = grad_f(x)
        if np.linalg.norm(g) < tol:
            break
        H = hess_f(x)
        p = - np.linalg.solve(H, g)
        alpha = backtracking_armijo(f, grad_f, x, p)
        x = x + alpha * p
        history.append(x.copy())
    return x, history

def linear_conjugate_gradient(A, b, x0, tol=1e-6):
    """线性共轭梯度法 (Linear Conjugate Gradient)"""
    x = np.array(x0, dtype=float)
    r = b - A @ x
    p = r.copy()
    rs_old = np.dot(r, r)
    
    for _ in range(len(b)):
        if np.sqrt(rs_old) < tol:
            break
        Ap = A @ p
        alpha = rs_old / np.dot(p, Ap)
        x = x + alpha * p
        r = r - alpha * Ap
        rs_new = np.dot(r, r)
        p = r + (rs_new / rs_old) * p
        rs_old = rs_new
    return x
