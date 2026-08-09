#!/usr/bin/env python3
"""
Numerical Analysis Core Algorithms and Benchmarks
Covers:
- HW01: Floating point arithmetic, catastrophic cancellation, Kahan summation
- HW02: LU factorization with partial pivoting, solver, Wilkinson growth factor
- HW03: Householder QR decomposition, least squares
- HW04: Chebyshev nodes, Barycentric Lagrange Form II interpolation
- HW05: Golub-Welsch Gauss-Legendre quadrature
- HW06: Multidimensional Newton-Raphson with Armijo line search
- HW07: Runge-Kutta 4 (RK4) IVP solver and convergence analysis
- HW08: 2D Poisson equation finite difference CSR solver
- Capstone: 2D Poisson / Manufactured Solutions (MMS) spatial convergence verification
"""

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla


# ============================================================================
# HW01: Floating Point, Epsilon, Kahan Summation
# ============================================================================
def measure_machine_epsilon() -> float:
    """Measure machine epsilon without calling np.finfo."""
    eps = 1.0
    while (1.0 + eps / 2.0) != 1.0:
        eps /= 2.0
    return eps


def stable_cancellation_demo(x: float) -> tuple[float, float]:
    """
    Compare (1 - cos(x)) / x^2 directly vs using 2*sin^2(x/2) / x^2.
    Returns (direct_val, stable_val).
    """
    direct = (1.0 - np.cos(x)) / (x**2) if x != 0 else 0.5
    stable = 2.0 * (np.sin(x / 2.0) ** 2) / (x**2) if x != 0 else 0.5
    return direct, stable


def kahan_sum(arr: np.ndarray) -> np.float32:
    """Kahan compensated summation algorithm in single precision."""
    s = np.float32(0.0)
    c = np.float32(0.0)
    for x in arr:
        y = np.float32(x) - c
        t = s + y
        c = (t - s) - y
        s = t
    return s


# ============================================================================
# HW02: LU Factorization with Partial Pivoting & Solver
# ============================================================================
def lu_factor_pivot(A_in: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Compute PA = LU with partial pivoting.
    Returns (piv_indices, L, U).
    """
    A = A_in.copy().astype(np.float64)
    n = A.shape[0]
    piv = np.arange(n)

    for k in range(n - 1):
        p = np.argmax(np.abs(A[k:, k])) + k
        if p != k:
            A[[k, p], :] = A[[p, k], :]
            piv[[k, p]] = piv[[p, k]]

        if abs(A[k, k]) < 1e-15:
            raise ValueError("Matrix is numerically singular.")

        A[k + 1 :, k] /= A[k, k]
        A[k + 1 :, k + 1 :] -= np.outer(A[k + 1 :, k], A[k, k + 1 :])

    L = np.tril(A, -1) + np.eye(n)
    U = np.triu(A)
    return piv, L, U


def lu_solve_pivot(piv: np.ndarray, L: np.ndarray, U: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Solve Ax = b using LU factors with partial pivoting."""
    n = len(b)
    # Permute b
    b_perm = b[piv]

    # Forward solve L y = b_perm
    y = np.zeros(n, dtype=np.float64)
    for i in range(n):
        y[i] = b_perm[i] - np.dot(L[i, :i], y[:i])

    # Backward solve U x = y
    x = np.zeros(n, dtype=np.float64)
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - np.dot(U[i, i + 1 :], x[i + 1 :])) / U[i, i]

    return x


# ============================================================================
# HW03: Householder QR Decomposition & Least Squares
# ============================================================================
def householder_qr(A_in: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
    Compute QR decomposition A = Q R (m x n, m >= n) using Householder reflections.
    Returns (Q, R).
    """
    A = A_in.copy().astype(np.float64)
    m, n = A.shape
    Q = np.eye(m)

    for k in range(min(m, n)):
        x = A[k:, k]
        norm_x = np.linalg.norm(x)
        if norm_x > 1e-15:
            alpha = -np.sign(x[0]) * norm_x if x[0] != 0 else -norm_x
            v = x.copy()
            v[0] -= alpha
            v_norm = np.linalg.norm(v)
            if v_norm > 1e-15:
                v /= v_norm
                A[k:, k:] -= 2.0 * np.outer(v, np.dot(v, A[k:, k:]))
                Q[:, k:] -= 2.0 * (Q[:, k:] @ v[:, None]) @ v[None, :]

    R = np.triu(A[:n, :])
    return Q[:, :n], R


def qr_least_squares(A: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Solve min ||Ax - b||_2 using Householder QR."""
    Q, R = householder_qr(A)
    c = Q.T @ b
    # Solve R x = c
    n = R.shape[1]
    x = np.zeros(n, dtype=np.float64)
    for i in range(n - 1, -1, -1):
        x[i] = (c[i] - np.dot(R[i, i + 1 :], x[i + 1 :])) / R[i, i]
    return x


# ============================================================================
# HW04: Barycentric Chebyshev Interpolation (Form II)
# ============================================================================
class BarycentricChebyshevInterpolator:
    """Barycentric Lagrange Form II Interpolator on 1st-kind Chebyshev roots."""

    def __init__(self, f_func, n_points: int):
        self.n = n_points
        k = np.arange(self.n)
        self.xk = np.cos((2 * k + 1) / (2 * self.n) * np.pi)
        self.fk = f_func(self.xk)
        self.wk = ((-1.0) ** k) * np.sin((2 * k + 1) / (2 * self.n) * np.pi)

    def evaluate(self, x_eval: np.ndarray | float) -> np.ndarray:
        x = np.atleast_1d(np.asarray(x_eval, dtype=np.float64))
        exact_match = x[:, None] == self.xk[None, :]
        has_match = np.any(exact_match, axis=1)

        diff = x[:, None] - self.xk[None, :]
        with np.errstate(divide="ignore", invalid="ignore"):
            term = self.wk[None, :] / diff
            numer = np.sum(term * self.fk[None, :], axis=1)
            denom = np.sum(term, axis=1)
            result = numer / denom

        if np.any(has_match):
            for i in np.where(has_match)[0]:
                col = np.where(exact_match[i])[0][0]
                result[i] = self.fk[col]

        return result if len(result) > 1 else result[0]


# ============================================================================
# HW05: Golub-Welsch Gauss-Legendre Quadrature
# ============================================================================
def golub_welsch_gauss_legendre(n: int) -> tuple[np.ndarray, np.ndarray]:
    """Compute n-point Gauss-Legendre nodes and weights on [-1, 1]."""
    k = np.arange(1, n)
    beta = k / np.sqrt(4.0 * (k**2) - 1.0)
    J = np.diag(beta, -1) + np.diag(beta, 1)
    eigenvalues, eigenvectors = np.linalg.eigh(J)
    nodes = eigenvalues
    weights = 2.0 * (eigenvectors[0, :] ** 2)
    return nodes, weights


def gauss_legendre_integrate(f, a: float, b: float, n: int = 10) -> float:
    """Integrate f(x) over [a, b] using n-point Gauss-Legendre quadrature."""
    nodes, weights = golub_welsch_gauss_legendre(n)
    mid = 0.5 * (a + b)
    scale = 0.5 * (b - a)
    mapped_nodes = scale * nodes + mid
    return scale * float(np.sum(weights * f(mapped_nodes)))


# ============================================================================
# HW06: Multidimensional Newton-Raphson with Armijo Line Search
# ============================================================================
def newton_raphson_nd(
    F_func,
    J_func,
    x0: np.ndarray,
    tol: float = 1e-12,
    max_iter: int = 50,
) -> tuple[np.ndarray, int, bool]:
    """Solve F(x) = 0 with analytic Jacobian J and Armijo backtracking."""
    x = x0.copy().astype(np.float64)
    for it in range(max_iter):
        F_val = F_func(x)
        norm_F = np.linalg.norm(F_val)
        if norm_F < tol:
            return x, it, True

        J_val = J_func(x)
        delta_x = np.linalg.solve(J_val, -F_val)

        # Armijo backtracking line search
        alpha = 1.0
        c_armijo = 1e-4
        while alpha > 1e-6:
            x_candidate = x + alpha * delta_x
            if np.linalg.norm(F_func(x_candidate)) < (1.0 - c_armijo * alpha) * norm_F:
                break
            alpha *= 0.5

        x = x + alpha * delta_x

    return x, max_iter, np.linalg.norm(F_func(x)) < tol


# ============================================================================
# HW07: Runge-Kutta 4 (RK4) IVP Solver
# ============================================================================
def rk4_solve(f_ode, y0: np.ndarray | float, t_span: tuple[float, float], n_steps: int):
    """Solve y' = f(t, y) from t0 to T using classical RK4."""
    t0, tf = t_span
    h = (tf - t0) / n_steps
    t_grid = np.linspace(t0, tf, n_steps + 1)

    y_shape = np.atleast_1d(y0).shape
    Y = np.zeros((n_steps + 1, *y_shape), dtype=np.float64)
    Y[0] = y0

    for i in range(n_steps):
        t = t_grid[i]
        y = Y[i]
        k1 = f_ode(t, y)
        k2 = f_ode(t + 0.5 * h, y + 0.5 * h * k1)
        k3 = f_ode(t + 0.5 * h, y + 0.5 * h * k2)
        k4 = f_ode(t + h, y + h * k3)
        Y[i + 1] = y + (h / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)

    return t_grid, Y


# ============================================================================
# HW08 & Capstone: 2D Poisson & Manufactured Solutions (MMS)
# ============================================================================
def solve_poisson_2d(f_src, g_bc, N: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Solve -Laplace(u) = f in (0, 1)^2 with Dirichlet boundary g using CSR 5-point stencil.
    """
    h = 1.0 / N
    x = np.linspace(0, 1, N + 1)
    y = np.linspace(0, 1, N + 1)
    X, Y = np.meshgrid(x, y)

    n_in = N - 1
    T1 = sp.diags([-1.0, 2.0, -1.0], [-1, 0, 1], shape=(n_in, n_in), format="csr")
    I = sp.eye(n_in, format="csr")
    A = (sp.kron(I, T1) + sp.kron(T1, I)) / (h**2)
    A = A.tocsr()

    F = f_src(X[1:-1, 1:-1], Y[1:-1, 1:-1])
    b_mat = F.copy()

    # Absorb Dirichlet boundaries
    b_mat[0, :] += g_bc(x[1:-1], 0.0) / (h**2)
    b_mat[-1, :] += g_bc(x[1:-1], 1.0) / (h**2)
    b_mat[:, 0] += g_bc(0.0, y[1:-1]) / (h**2)
    b_mat[:, -1] += g_bc(1.0, y[1:-1]) / (h**2)

    b = b_mat.flatten()
    u_in = spla.spsolve(A, b)

    U = np.zeros((N + 1, N + 1), dtype=np.float64)
    U[1:-1, 1:-1] = u_in.reshape((n_in, n_in))
    U[0, :] = g_bc(x, 0.0)
    U[-1, :] = g_bc(x, 1.0)
    U[:, 0] = g_bc(0.0, y)
    U[:, -1] = g_bc(1.0, y)

    return X, Y, U
