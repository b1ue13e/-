"""Unit tests for Eight-Schools Hierarchical Partial Pooling & MCMC."""
import unittest
import numpy as np
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))
from hierarchical_shrinkage import (
    load_eight_schools_csv,
    compute_analytical_shrinkage,
    run_eight_schools_non_centered_mcmc,
    simulate_neals_funnel,
    detect_funnel_divergences,
    get_eight_schools_pymc_code
)


class TestHierarchicalShrinkage(unittest.TestCase):
    def setUp(self):
        self.csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'eight_schools.csv'))
        self.schools, self.y, self.sigma = load_eight_schools_csv(self.csv_path)

    def test_dataset_loading(self):
        self.assertEqual(len(self.schools), 8)
        self.assertEqual(len(self.y), 8)
        self.assertAlmostEqual(self.y[0], 28.0)

    def test_analytical_shrinkage_monotonicity(self):
        res = compute_analytical_shrinkage(self.y, self.sigma, mu=8.0, tau=5.0)
        shrinkage_b = res["shrinkage_b"]
        post_means = res["theta_post_mean"]
        
        # 验证收缩因子介于 (0, 1)
        self.assertTrue(np.all(shrinkage_b > 0.0))
        self.assertTrue(np.all(shrinkage_b < 1.0))
        
        # 验证极端学校 A (28) 被强力收缩拉向总体均值 8.0
        self.assertLess(post_means[0], 28.0)
        self.assertGreater(post_means[0], 8.0)

    def test_non_centered_mcmc_recovery(self):
        res = run_eight_schools_non_centered_mcmc(self.y, self.sigma, n_samples=3000, seed=123)
        mu_draws = res["mu"]
        tau_draws = res["tau"]
        theta_draws = res["theta"]
        
        # 验证总体均值 mu 位于合理经验区间 (4.0 ~ 12.0)
        mu_mean = float(np.mean(mu_draws))
        self.assertGreater(mu_mean, 4.0)
        self.assertLess(mu_mean, 12.0)
        
        # 验证组间尺度 tau > 0
        self.assertGreater(float(np.mean(tau_draws)), 0.5)
        self.assertEqual(theta_draws.shape[1], 8)

    def test_neals_funnel_and_divergences(self):
        x_samp, y_samp = simulate_neals_funnel(n_samples=2000, seed=42)
        self.assertEqual(len(x_samp), 2000)
        self.assertEqual(len(y_samp), 2000)
        
        diag = detect_funnel_divergences(x_samp, y_samp)
        self.assertEqual(diag["total_samples"], 2000)
        self.assertGreater(diag["in_neck_count"], 0)
        self.assertGreaterEqual(diag["divergence_rate"], 0.0)
        
        # 验证模板代码可用
        code = get_eight_schools_pymc_code()
        self.assertIn("pm.Model", code)


if __name__ == '__main__':
    unittest.main()

