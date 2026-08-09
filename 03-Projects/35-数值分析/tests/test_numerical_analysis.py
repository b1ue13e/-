#!/usr/bin/env python3
"""
Automated Test Suite for Numerical Analysis (35-数值分析)
Covers all homework tasks HW01-HW08, Stage Projects and Capstone MMS.
"""

import sys
import unittest
from pathlib import Path

# Add scripts directory to path
script_dir = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(script_dir))

import numpy as np
from numerical_methods import (
    BarycentricChebyshevInterpolator,
    gauss_legendre_integrate,
    golub_welsch_gauss_legendre,
    householder_qr,
    kahan_sum,
    lu_factor_pivot,
    lu_solve_pivot,
    measure_machine_epsilon,
    newton_raphson_nd,
    qr_least_squares,
    rk4_solve,
    solve_poisson_2d,
    stable_cancellation_demo,
)


class TestNumericalAnalysis(unittest.TestCase):

    def test_hw01_machine_epsilon(self):
        eps = measure_machine_epsilon()
        expected = np.finfo(np.float64).eps
        self.assertAlmostEqual(eps, expected, delta=1e-18)
        self.assertTrue(1.0 + eps > 1.0)
        self.assertEqual(1.0 + eps / 2.0, 1.0)

    def test_hw01_catastrophic_cancellation(self):
        x = 1e-8
        direct, stable = stable_cancellation_demo(x)
        self.assertAlmostEqual(stable, 0.5, delta=1e-12)

    def test_hw01_kahan_summation(self):
        n = 100000
        val = np.float32(1e-4)
        arr = np.full(n, val, dtype=np.float32)
        naive_s = np.float32(0.0)
        for x in arr:
            naive_s += x
        kahan_s = kahan_sum(arr)
        expected = 10.0
        self.assertLess(abs(float(kahan_s) - expected), 1e-4)

    def test_hw02_lu_pivoting(self):
        np.random.seed(42)
        n = 10
        A = np.random.randn(n, n) + 5.0 * np.eye(n)
        b = np.random.randn(n)

        piv, L, U = lu_factor_pivot(A)
        PA = A[piv, :]
        reconstruct_err = np.linalg.norm(PA - L @ U) / np.linalg.norm(A)
        self.assertLess(reconstruct_err, 1e-14)

        x_sol = lu_solve_pivot(piv, L, U, b)
        residual = np.linalg.norm(A @ x_sol - b) / (
            np.linalg.norm(A) * np.linalg.norm(x_sol) + np.linalg.norm(b)
        )
        self.assertLess(residual, 1e-14)

    def test_hw03_householder_qr(self):
        np.random.seed(42)
        m, n = 20, 8
        A = np.random.randn(m, n)
        b = np.random.randn(m)

        Q, R = householder_qr(A)
        # Q has shape (m, n) - thin QR
        ortho_err = np.linalg.norm(Q.T @ Q - np.eye(n))
        self.assertLess(ortho_err, 1e-14)

        reconstruct_err = np.linalg.norm(A - Q @ R) / np.linalg.norm(A)
        self.assertLess(reconstruct_err, 1e-14)

        x_qr = qr_least_squares(A, b)
        x_np, _, _, _ = np.linalg.lstsq(A, b, rcond=None)
        self.assertLess(np.linalg.norm(x_qr - x_np), 1e-13)

    def test_hw04_chebyshev_barycentric_interpolation(self):
        f = lambda x: 1.0 / (1.0 + 25.0 * (x**2))
        interp = BarycentricChebyshevInterpolator(f, n_points=50)
        x_dense = np.linspace(-1, 1, 500)
        y_interp = interp.evaluate(x_dense)
        y_exact = f(x_dense)
        max_err = float(np.max(np.abs(y_interp - y_exact)))
        # 50 points on Runge function should achieve < 2e-4 error (Bernstein ellipse rate)
        self.assertLess(max_err, 2e-4)

    def test_hw05_gauss_legendre_quadrature(self):
        # Integral of exp(x) on [0, 1] is e - 1
        res = gauss_legendre_integrate(np.exp, 0.0, 1.0, n=8)
        expected = np.e - 1.0
        self.assertAlmostEqual(res, expected, delta=1e-14)

        # 5-point Gauss should integrate exact degree 9 polynomial
        poly = lambda x: x**9 - 3 * (x**7) + 2 * (x**2)
        # Integral from -1 to 1 of odd powers is 0, int 2*x^2 is 4/3
        res_poly = gauss_legendre_integrate(poly, -1.0, 1.0, n=5)
        self.assertAlmostEqual(res_poly, 4.0 / 3.0, delta=1e-14)

    def test_hw06_newton_raphson_multidimensional(self):
        # Solve: x1^2 + x2^2 = 4, exp(x1) + x2 = 1
        def F(x):
            return np.array([x[0] ** 2 + x[1] ** 2 - 4.0, np.exp(x[0]) + x[1] - 1.0])

        def J(x):
            return np.array([[2.0 * x[0], 2.0 * x[1]], [np.exp(x[0]), 1.0]])

        x0 = np.array([1.0, -1.0])
        x_star, iters, converged = newton_raphson_nd(F, J, x0, tol=1e-12)
        self.assertTrue(converged)
        self.assertLess(np.linalg.norm(F(x_star)), 1e-12)
        self.assertLess(iters, 10)

    def test_hw07_rk4_convergence_rate(self):
        # y' = y, y(0) = 1 on [0, 1]
        f_ode = lambda t, y: y
        steps_list = [10, 20, 40, 80]
        errors = []
        for n in steps_list:
            _, Y = rk4_solve(f_ode, y0=1.0, t_span=(0.0, 1.0), n_steps=n)
            err = float(np.abs(np.squeeze(Y[-1]) - np.e))
            errors.append(err)

        # Slope of log(error) vs log(h)
        h_vals = 1.0 / np.array(steps_list, dtype=np.float64)
        log_h = np.log(h_vals)
        log_e = np.log(np.array(errors, dtype=np.float64))
        p = np.polyfit(log_h, log_e, 1)
        slope = float(p[0])
        self.assertTrue(3.95 <= slope <= 4.05, f"Expected slope ~4, got {slope:.3f}")

    def test_hw08_and_capstone_pde_mms_convergence(self):
        # MMS solution: u = sin(pi*x)*sin(pi*y)
        # -Laplace(u) = 2*pi^2 * sin(pi*x)*sin(pi*y)
        f_src = lambda x, y: 2.0 * (np.pi**2) * np.sin(np.pi * x) * np.sin(np.pi * y)
        g_bc = lambda x, y: np.zeros_like(x)

        grid_sizes = [16, 32, 64]
        errors = []
        for N in grid_sizes:
            X, Y, U_calc = solve_poisson_2d(f_src, g_bc, N)
            U_exact = np.sin(np.pi * X) * np.sin(np.pi * Y)
            err = float(np.max(np.abs(U_calc - U_exact)))
            errors.append(err)

        h_vals = 1.0 / np.array(grid_sizes, dtype=np.float64)
        log_h = np.log(h_vals)
        log_e = np.log(np.array(errors, dtype=np.float64))
        p = np.polyfit(log_h, log_e, 1)
        slope = float(p[0])
        self.assertTrue(1.92 <= slope <= 2.05, f"Expected slope ~2, got {slope:.3f}")


if __name__ == "__main__":
    unittest.main()
