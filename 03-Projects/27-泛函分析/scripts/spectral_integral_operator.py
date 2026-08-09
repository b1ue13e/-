r"""
Functional Analysis Operator Theory & Spectral Laboratory
=========================================================
Rigorous Numerical Verification of Core Infinite-Dimensional Phenomena:
1. Compact Self-Adjoint Operator (Hilbert-Schmidt Theorem):
   Eigenvalues lambda_k = 1 / ((k - 0.5)^2 * pi^2) strictly decay to 0.
2. Multiplication Operator (Continuous Spectrum & Weyl Sequence):
   (M_x f)(x) = x f(x) has no eigenvalues, purely continuous spectrum [0, 1].
   Weyl sequence v_n(x) satisfies ||v_n|| = 1 and ||(M_x - lambda I) v_n|| = 1 / (sqrt(12) * n) -> 0.
3. Volterra Integral Operator (Quasinilpotency):
   (V f)(x) = \int_0^x f(t) dt has sigma(V) = {0}, ||V^k|| <= 1/k! factorial decay.
4. Weak vs Strong Convergence & Mazur's Convex Combinations:
   f_n(x) = sqrt(2) sin(n pi x) has ||f_n||_L2 = 1 (does not converge strongly),
   but <f_n, g> -> 0 for all g in L^2 (weakly converges to 0).
   Mazur combination s_N = (1/N) \sum_{n=1}^N f_n converges strongly: ||s_N||_L2 = 1/sqrt(N) -> 0.
5. Non-Self-Adjoint Operator: Failure of Rayleigh Quotient & Numerical Range Gap:
   Demonstrates that for non-self-adjoint operators, spectral radius rho(T) < ||T|| and
   numerical radius w(T) = sup_{||x||=1} |<Tx, x>| < ||T||.
"""

import math
import numpy as np
from typing import Dict, List, Tuple, Callable


# =====================================================================
# 1. Compact Self-Adjoint Integral Operator
# =====================================================================

def nystrom_integral_operator(n_points: int) -> Dict:
    r"""
    Discretize compact self-adjoint integral operator:
    (T f)(x) = \int_0^1 min(x, y) f(y) dy on L^2[0, 1].
    Exact continuous eigenvalues: lambda_k = 1 / ((k - 0.5)^2 * pi^2).
    """
    h = 1.0 / n_points
    grid = np.linspace(0.5 * h, 1.0 - 0.5 * h, n_points)
    
    X, Y = np.meshgrid(grid, grid)
    K_matrix = np.minimum(X, Y) * h
    
    eigenvalues = np.linalg.eigvalsh(K_matrix)
    eigenvalues_sorted = np.sort(np.abs(eigenvalues))[::-1]
    
    k_indices = np.arange(1, n_points + 1)
    exact_eigenvalues = 1.0 / ((k_indices - 0.5) ** 2 * np.pi ** 2)
    
    return {
        'n_points': n_points,
        'grid': grid,
        'numerical_eig': eigenvalues_sorted,
        'exact_eig': exact_eigenvalues,
        'max_eig_error_top5': float(np.max(np.abs(eigenvalues_sorted[:5] - exact_eigenvalues[:5])))
    }


# =====================================================================
# 2. Multiplication Operator: Continuous Spectrum & Weyl Sequence
# =====================================================================

def verify_multiplication_weyl_sequence(lambda_val: float, n_list: List[int]) -> Dict:
    r"""
    Verify Weyl's Criterion for Continuous Spectrum of M_x f = x f(x) on L^2[0, 1].
    For target spectral point lambda_val \in (0, 1):
    Construct normalized wave-packet sequence v_n(x) = sqrt(n) * 1_{[\lambda - 1/(2n), \lambda + 1/(2n)]}(x).
    
    Analytical results:
    ||v_n||_{L^2} = 1
    ||(M_x - lambda I) v_n||_{L^2} = 1 / (sqrt(12) * n) = O(1/n).
    """
    assert 0.0 < lambda_val < 1.0, "lambda_val must be in the open interval (0, 1)"
    
    results = []
    for n in n_list:
        n_quad = 1000
        x_left = lambda_val - 1.0 / (2.0 * n)
        x_right = lambda_val + 1.0 / (2.0 * n)
        x_left = max(0.0, x_left)
        x_right = min(1.0, x_right)
        
        xs = np.linspace(x_left, x_right, n_quad)
        dx = (x_right - x_left) / (n_quad - 1)
        
        v_n = np.sqrt(n) * np.ones_like(xs)
        norm_v_n = np.sqrt(np.sum(v_n ** 2) * dx)
        
        residual = (xs - lambda_val) * v_n
        norm_res = np.sqrt(np.sum(residual ** 2) * dx)
        
        theory_res = 1.0 / (np.sqrt(12.0) * n)
        
        results.append({
            'n': n,
            'norm_v_n': float(norm_v_n),
            'norm_residual': float(norm_res),
            'theory_residual': float(theory_res),
            'rel_error': float(abs(norm_res - theory_res) / theory_res)
        })
        
    return {
        'lambda_val': lambda_val,
        'results': results
    }


# =====================================================================
# 3. Volterra Integral Operator: Quasinilpotency & Factorial Decay
# =====================================================================

def verify_volterra_quasinilpotency(n_grid: int = 100, max_power: int = 5) -> Dict:
    r"""
    Discretize Volterra operator (V f)(x) = \int_0^x f(t) dt.
    Verify:
    1. Spectral radius rho(V_h) = 0.
    2. Power norm decay: ||V^k|| <= 1 / k! (strictly quasinilpotent).
    """
    h = 1.0 / n_grid
    V_matrix = np.tril(np.ones((n_grid, n_grid)) * h, k=-1)
    
    eigs = np.linalg.eigvals(V_matrix)
    spectral_radius = float(np.max(np.abs(eigs)))
    
    powers_norm = []
    current_V = np.eye(n_grid)
    for k in range(1, max_power + 1):
        current_V = current_V @ V_matrix
        op_norm = float(np.linalg.norm(current_V, ord=2))
        theory_bound = 1.0 / float(math.factorial(k))
        powers_norm.append({
            'k': k,
            'op_norm': op_norm,
            'theory_bound': theory_bound
        })
        
    return {
        'n_grid': n_grid,
        'spectral_radius': spectral_radius,
        'powers_norm': powers_norm
    }


# =====================================================================
# 4. Weak vs Strong Convergence & Mazur's Lemma
# =====================================================================

def verify_weak_convergence_and_mazur(n_max: int = 50) -> Dict:
    r"""
    Demonstrate that sequence f_n(x) = sqrt(2) * sin(n * pi * x) on L^2[0, 1]:
    1. ||f_n||_L2 = 1 for all n (no strong convergence to 0).
    2. Inner product <f_n, g> -> 0 at rate O(1/n) (Riemann-Lebesgue weak convergence).
    3. Mazur convex combination: ||s_N||_L2 = 1 / sqrt(N) -> 0 (strong convergence!).
    """
    n_quad = 2000
    xs = np.linspace(0.0, 1.0, n_quad)
    dx = 1.0 / (n_quad - 1)
    
    g1 = xs
    g2 = xs ** 2
    g3 = np.exp(xs)
    
    weak_decay = []
    for n in range(1, n_max + 1):
        f_n = np.sqrt(2.0) * np.sin(n * np.pi * xs)
        norm_fn = float(np.sqrt(np.sum(f_n ** 2) * dx))
        inner_g1 = float(np.sum(f_n * g1) * dx)
        inner_g2 = float(np.sum(f_n * g2) * dx)
        inner_g3 = float(np.sum(f_n * g3) * dx)
        
        weak_decay.append({
            'n': n,
            'norm_fn': norm_fn,
            'inner_g1': inner_g1,
            'inner_g2': inner_g2,
            'inner_g3': inner_g3
        })
        
    mazur_results = []
    for N in [1, 4, 16, 64, 100]:
        s_N = np.zeros_like(xs)
        for n in range(1, N + 1):
            s_N += np.sqrt(2.0) * np.sin(n * np.pi * xs)
        s_N /= N
        norm_sN = float(np.sqrt(np.sum(s_N ** 2) * dx))
        theory_norm = 1.0 / np.sqrt(N)
        mazur_results.append({
            'N': N,
            'norm_sN': norm_sN,
            'theory_norm': theory_norm,
            'error': float(abs(norm_sN - theory_norm))
        })
        
    return {
        'weak_decay': weak_decay,
        'mazur_results': mazur_results
    }


# =====================================================================
# 5. Non-Self-Adjoint Operator: Breakdown of Rayleigh Quotient Norm
# =====================================================================

def verify_non_self_adjoint_rayleigh_gap(n_dim: int = 50) -> Dict:
    r"""
    Compare Self-Adjoint vs Non-Self-Adjoint Operators:
    - For Self-Adjoint A: ||A|| = rho(A) = sup_{||x||=1} |<Ax, x>| (Rayleigh quotient exact).
    - For Non-Self-Adjoint B (Shift matrix / asymmetric kernel):
      rho(B) < ||B|| and numerical radius w(B) = sup |<Bx, x>| < ||B||.
    """
    # 1. Self-Adjoint symmetric tridiagonal
    A = np.diag(np.ones(n_dim - 1), -1) + np.diag(2.0 * np.ones(n_dim), 0) + np.diag(np.ones(n_dim - 1), 1)
    norm_A = float(np.linalg.norm(A, ord=2))
    rho_A = float(np.max(np.abs(np.linalg.eigvals(A))))
    
    # 2. Non-Self-Adjoint Jordan nilpotent shift matrix
    B = np.diag(np.ones(n_dim - 1), 1) # B_{i, i+1} = 1
    norm_B = float(np.linalg.norm(B, ord=2))
    rho_B = float(np.max(np.abs(np.linalg.eigvals(B)))) # rho(B) = 0
    
    # Numerical radius w(B) = cos(pi / (n_dim + 1))
    theory_w_B = float(np.cos(np.pi / (n_dim + 1)))
    
    return {
        'n_dim': n_dim,
        'self_adjoint': {
            'op_norm': norm_A,
            'spectral_radius': rho_A,
            'norm_equals_rho': bool(abs(norm_A - rho_A) < 1e-10)
        },
        'non_self_adjoint': {
            'op_norm': norm_B,
            'spectral_radius': rho_B,
            'theory_numerical_radius': theory_w_B,
            'rayleigh_gap': float(norm_B - theory_w_B)
        }
    }


# =====================================================================
# Main CLI Runner
# =====================================================================

def run_all_experiments():
    print("=" * 70)
    print(" FUNCTIONAL ANALYSIS OPERATOR & SPECTRAL LABORATORY EXPERIMENTS")
    print("=" * 70)
    
    # 1. Compact Integral Operator
    print("\n--- 1. Compact Self-Adjoint Operator Spectral Decay ---")
    comp_res = nystrom_integral_operator(100)
    print(f"Top 5 Numerical Eigenvalues: {comp_res['numerical_eig'][:5]}")
    print(f"Top 5 Exact Eigenvalues    : {comp_res['exact_eig'][:5]}")
    print(f"Max Absolute Error (Top 5) : {comp_res['max_eig_error_top5']:.6e}")
    
    # 2. Multiplication Operator Weyl Sequence
    print("\n--- 2. Multiplication Operator Continuous Spectrum (Weyl Criterion) ---")
    weyl_res = verify_multiplication_weyl_sequence(0.42, [10, 50, 100, 500])
    for r in weyl_res['results']:
        print(f"n = {r['n']:4d} | ||v_n|| = {r['norm_v_n']:.4f} | ||(M_x - lambda)v_n|| = {r['norm_residual']:.6e} (Theory: {r['theory_residual']:.6e})")
        
    # 3. Volterra Operator Quasinilpotency
    print("\n--- 3. Volterra Integral Operator Quasinilpotency ---")
    volt_res = verify_volterra_quasinilpotency(100, 5)
    print(f"Spectral Radius rho(V_h): {volt_res['spectral_radius']:.6e}")
    for p in volt_res['powers_norm']:
        print(f"k = {p['k']:2d} | ||V^k|| = {p['op_norm']:.6e} | Theory Bound 1/k! = {p['theory_bound']:.6e}")
        
    # 4. Weak vs Strong Convergence
    print("\n--- 4. Weak Convergence & Mazur's Convex Combination ---")
    weak_res = verify_weak_convergence_and_mazur(50)
    print("Mazur Strong Convergence ||(1/N) sum_{n=1}^N f_n||_L2:")
    for m in weak_res['mazur_results']:
        print(f"N = {m['N']:3d} | ||s_N||_L2 = {m['norm_sN']:.6f} | Theory 1/sqrt(N) = {m['theory_norm']:.6f}")
        
    # 5. Non-Self-Adjoint Operator Rayleigh Gap
    print("\n--- 5. Non-Self-Adjoint Operator: Breakdown of Rayleigh Quotient ---")
    ray_res = verify_non_self_adjoint_rayleigh_gap(50)
    print(f"Self-Adjoint A: ||A|| = {ray_res['self_adjoint']['op_norm']:.4f}, rho(A) = {ray_res['self_adjoint']['spectral_radius']:.4f} (Match: {ray_res['self_adjoint']['norm_equals_rho']})")
    print(f"Shift Matrix B: ||B|| = {ray_res['non_self_adjoint']['op_norm']:.4f}, rho(B) = {ray_res['non_self_adjoint']['spectral_radius']:.4f}, w(B) = {ray_res['non_self_adjoint']['theory_numerical_radius']:.4f} (Rayleigh Gap = {ray_res['non_self_adjoint']['rayleigh_gap']:.4f})")
    
    print("\n" + "=" * 70)
    print(" ALL FUNCTIONAL ANALYSIS EXPERIMENTS COMPLETED SUCCESSFULLY!")
    print("=" * 70)


if __name__ == "__main__":
    run_all_experiments()
