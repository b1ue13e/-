"""
Functional Analysis Automated Test Suite
========================================
Comprehensive Unit and Numerical Tests for:
1. Lax-Milgram Theorem & FEM Convergence (Céa's Lemma & Aubin-Nitsche Duality).
2. Trace Theorem & Non-Homogeneous Dirichlet Boundary Lifting.
3. Sobolev Regularity & 2D L-Shaped Corner Singularity.
4. Hilbert-Schmidt Spectral Theorem for Compact Integral Operators.
5. Continuous Spectrum & Weyl Criterion for Multiplication Operators.
6. Volterra Operator Quasinilpotency & Power Norm Factorial Decay.
7. Weak vs Strong Convergence & Mazur's Convex Combination Strong Limit.
8. Non-Self-Adjoint Operator Rayleigh Quotient Breakdown.
"""

import pytest
import numpy as np
import sys
import os

# Add scripts directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))

from fem_poisson_solver import (
    solve_poisson_1d,
    verify_poisson_convergence_orders,
    verify_nonhomogeneous_lifting_orders,
    solve_poisson_2d_lshaped,
    verify_2d_lshaped_singularity_orders
)
from spectral_integral_operator import (
    nystrom_integral_operator,
    verify_multiplication_weyl_sequence,
    verify_volterra_quasinilpotency,
    verify_weak_convergence_and_mazur,
    verify_non_self_adjoint_rayleigh_gap
)


class TestFunctionalAnalysisTheory:
    
    def test_poisson_1d_convergence_rates(self):
        """
        Verify Lax-Milgram Theorem, Céa's Lemma (H1 rate ~ 1.0) and Aubin-Nitsche (L2 rate ~ 2.0).
        """
        f_func = lambda x: np.pi ** 2 * np.sin(np.pi * x)
        u_exact = lambda x: np.sin(np.pi * x)
        du_exact = lambda x: np.pi * np.cos(np.pi * x)
        
        rates = verify_poisson_convergence_orders([10, 20, 40, 80], f_func, u_exact, du_exact)
        assert rates['rate_h1'] == pytest.approx(1.0, abs=0.08), f"H1 rate {rates['rate_h1']} != 1.0 (Céa's Lemma failed)"
        assert rates['rate_l2'] == pytest.approx(2.0, abs=0.08), f"L2 rate {rates['rate_l2']} != 2.0 (Aubin-Nitsche duality failed)"

    def test_trace_lifting_nonhomogeneous_bc(self):
        """
        Verify Sobolev Trace Theorem & Boundary Lifting (u = w + u_g):
        Homogenized zero-trace formulation w in H_0^1 achieves optimal O(h) and O(h^2) rates.
        """
        rates = verify_nonhomogeneous_lifting_orders([8, 16, 32, 64])
        assert rates['rate_h1'] == pytest.approx(1.0, abs=0.08), f"Lifting H1 rate {rates['rate_h1']} != 1.0"
        assert rates['rate_l2'] == pytest.approx(2.0, abs=0.08), f"Lifting L2 rate {rates['rate_l2']} != 2.0"

    def test_2d_lshaped_corner_singularity(self):
        """
        Verify 2D L-shaped domain re-entrant corner singularity:
        Weak solution exists in H^1(Omega), but convergence rate in H1 semi-norm is degraded
        below smooth rate 1.0 due to r^(2/3) singularity.
        """
        res_sub8 = solve_poisson_2d_lshaped(8)
        res_sub16 = solve_poisson_2d_lshaped(16)
        # Error must decrease as mesh refines
        assert res_sub16['h1_error'] < res_sub8['h1_error'], "H1 error must decrease with mesh refinement"
        # Asymptotic rate study
        rates = verify_2d_lshaped_singularity_orders([4, 8, 16])
        assert rates['rate_h1'] < 0.95, f"Corner singularity rate {rates['rate_h1']} must be degraded below smooth O(h^1)"

    def test_spectral_theorem_eigenvalue_decay(self):
        """
        Verify Hilbert-Schmidt Spectral Theorem: Compact operator eigenvalues decay as 1 / ((k-0.5)^2 * pi^2).
        """
        res = nystrom_integral_operator(120)
        assert res['max_eig_error_top5'] < 2.0e-3, f"Top 5 eigenvalues error {res['max_eig_error_top5']} exceeds tolerance"
        num_eigs = res['numerical_eig']
        assert num_eigs[0] > num_eigs[1] > num_eigs[2] > num_eigs[3], "Eigenvalues must strictly decay"
        assert num_eigs[-1] < 1.0e-3, "Tail eigenvalues must approach 0"

    def test_multiplication_operator_weyl_criterion(self):
        """
        Verify Weyl's Criterion for Continuous Spectrum: ||(M_x - lambda I) v_n|| = O(1/n) -> 0.
        """
        lambda_target = 0.35
        n_list = [20, 40, 80, 160]
        weyl_res = verify_multiplication_weyl_sequence(lambda_target, n_list)
        
        for r in weyl_res['results']:
            assert r['norm_v_n'] == pytest.approx(1.0, rel=1e-2), f"Weyl vector norm {r['norm_v_n']} != 1"
            assert r['rel_error'] < 0.05, f"Residual relative error {r['rel_error']} exceeds 5%"
            
        residuals = [r['norm_residual'] for r in weyl_res['results']]
        assert residuals[0] > residuals[1] > residuals[2] > residuals[3], "Weyl residuals must strictly decrease"
        assert residuals[-1] < 0.003, "Residual at n=160 must be very small"

    def test_volterra_quasinilpotency(self):
        """
        Verify Volterra Operator is Quasinilpotent: rho(V) = 0 and ||V^k|| <= 1/k!.
        """
        volt_res = verify_volterra_quasinilpotency(n_grid=80, max_power=5)
        assert volt_res['spectral_radius'] < 1.0e-10, f"Spectral radius {volt_res['spectral_radius']} must be 0"
        for p in volt_res['powers_norm']:
            assert p['op_norm'] <= p['theory_bound'] + 1.0e-4, f"Power norm {p['op_norm']} exceeds 1/k! bound {p['theory_bound']}"

    def test_weak_convergence_and_mazur_strong_limit(self):
        """
        Verify Weak Convergence Riemann-Lebesgue decay and Mazur's convex combination strong convergence.
        """
        weak_res = verify_weak_convergence_and_mazur(40)
        decay = weak_res['weak_decay']
        inner_last = decay[-1]['inner_g1']
        inner_first = decay[0]['inner_g1']
        assert abs(inner_last) < abs(inner_first) / 10.0, "Inner product <f_n, g> must decay significantly"
        
        for m in weak_res['mazur_results']:
            assert m['norm_sN'] == pytest.approx(m['theory_norm'], rel=0.05), f"Mazur norm {m['norm_sN']} != {m['theory_norm']}"

    def test_non_self_adjoint_rayleigh_breakdown(self):
        """
        Verify that for non-self-adjoint operators, spectral radius rho(T) < ||T||.
        """
        res = verify_non_self_adjoint_rayleigh_gap(40)
        assert res['self_adjoint']['norm_equals_rho'] is True, "Self-adjoint operator norm must equal spectral radius"
        assert res['non_self_adjoint']['spectral_radius'] < res['non_self_adjoint']['op_norm'], "Non-self-adjoint shift spectral radius must be strictly less than norm"


if __name__ == "__main__":
    pytest.main(["-v", __file__])
