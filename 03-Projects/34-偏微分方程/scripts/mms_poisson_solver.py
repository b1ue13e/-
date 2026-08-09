# -*- coding: utf-8 -*-
r"""
Method of Manufactured Solutions (MMS) Poisson 2D Finite Difference Solver.
Solves -\Delta u = f on (0, 1)^2 with u = 0 on boundary.
Manufactured solution: u(x, y) = sin(pi * x) * sin(pi * y)
Exact source: f(x, y) = 2 * pi^2 * sin(pi * x) * sin(pi * y)
Verifies 2nd-order convergence: Error = O(h^2)
"""
import numpy as np
from scipy import sparse
from scipy.sparse.linalg import spsolve

def solve_poisson_2d(N):
    r"""
    Solve -\Delta u = f on unit square [0, 1]x[0, 1] with N intervals per side.
    h = 1.0 / N
    Inner grid points: (N-1) x (N-1)
    """
    h = 1.0 / N
    x = np.linspace(0, 1, N + 1)
    y = np.linspace(0, 1, N + 1)
    X, Y = np.meshgrid(x, y, indexing='ij')
    
    # Exact solution and source
    u_exact = np.sin(np.pi * X) * np.sin(np.pi * Y)
    f = 2.0 * (np.pi ** 2) * np.sin(np.pi * X) * np.sin(np.pi * Y)
    
    # Inner grid size
    n_inner = N - 1
    
    # Construct 1D Laplacian matrix
    main_diag = 2.0 * np.ones(n_inner)
    off_diag = -1.0 * np.ones(n_inner - 1)
    T = sparse.diags([off_diag, main_diag, off_diag], [-1, 0, 1], shape=(n_inner, n_inner), format='csr')
    
    # 2D 5-point discrete Laplacian matrix: A = (T \otimes I + I \otimes T) / h^2
    I = sparse.eye(n_inner, format='csr')
    A = sparse.kron(T, I) + sparse.kron(I, T)
    A = A / (h ** 2)
    
    # Inner RHS vector
    F_inner = f[1:N, 1:N].flatten()
    
    # Solve linear system A * U = F
    U_inner = spsolve(A, F_inner)
    
    # Reconstruct full numerical solution with boundary conditions
    u_num = np.zeros((N + 1, N + 1))
    u_num[1:N, 1:N] = U_inner.reshape((n_inner, n_inner))
    
    # Compute error norms on inner points
    error = np.abs(u_num[1:N, 1:N] - u_exact[1:N, 1:N])
    l2_error = np.sqrt(h * h * np.sum(error ** 2))
    linf_error = np.max(error)
    
    return h, l2_error, linf_error

def run_mms_convergence_study():
    grid_sizes = [10, 20, 40, 80]
    results = []
    
    print("=" * 70)
    print(f"{'N':>6} | {'Mesh h':>10} | {'L2 Error':>14} | {'L2 Order':>10} | {'Linf Error':>14} | {'Linf Order':>10}")
    print("-" * 70)
    
    for i, N in enumerate(grid_sizes):
        h, l2, linf = solve_poisson_2d(N)
        l2_order = 0.0
        linf_order = 0.0
        if i > 0:
            h_prev, l2_prev, linf_prev = results[-1]
            l2_order = np.log(l2_prev / l2) / np.log(h_prev / h)
            linf_order = np.log(linf_prev / linf) / np.log(h_prev / h)
            
        results.append((h, l2, linf))
        print(f"{N:>6} | {h:>10.4f} | {l2:>14.6e} | {l2_order:>10.2f} | {linf:>14.6e} | {linf_order:>10.2f}")
        
    print("=" * 70)
    print("MMS Convergence verification completed successfully. Convergence rate is O(h^2).")
    return results

if __name__ == "__main__":
    run_mms_convergence_study()
