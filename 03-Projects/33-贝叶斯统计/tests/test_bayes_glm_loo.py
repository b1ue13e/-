"""Unit tests for Bayesian GLM, WAIC and PSIS-LOO-CV Diagnostics."""
import unittest
import numpy as np
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))
from bayes_glm_loo import (
    fit_bayesian_logistic_regression,
    compute_pointwise_log_likelihood,
    compute_waic,
    compute_psis_loo,
    generate_posterior_predictive,
    compute_bayesian_p_value,
    posterior_predictive_check_stats,
    get_pymc_glm_code
)


class TestBayesGLMLOO(unittest.TestCase):
    def setUp(self):
        np.random.seed(42)
        self.n_obs = 10
        self.p_feats = 3
        self.X = np.random.randn(self.n_obs, self.p_feats)
        self.X[:, 0] = 1.0  # 偏置截距项
        self.n_trials = np.full(self.n_obs, 100)
        # 生成模拟转化计数
        true_beta = np.array([0.5, -0.8, 1.2])
        probs = 1.0 / (1.0 + np.exp(-self.X @ true_beta))
        self.y = np.random.binomial(self.n_trials, probs)

    def test_glm_map_fit(self):
        beta_map, cov_matrix = fit_bayesian_logistic_regression(self.X, self.y, self.n_trials)
        self.assertEqual(len(beta_map), self.p_feats)
        self.assertEqual(cov_matrix.shape, (self.p_feats, self.p_feats))
        # 协方差矩阵对角线元素必须正定
        self.assertTrue(np.all(np.diag(cov_matrix) > 0.0))

    def test_psis_loo_and_waic(self):
        beta_map, cov_matrix = fit_bayesian_logistic_regression(self.X, self.y, self.n_trials)
        # 从拉普拉斯后验中抽取 500 个样本
        beta_draws = np.random.multivariate_normal(beta_map, cov_matrix, size=500)
        log_lik = compute_pointwise_log_likelihood(beta_draws, self.X, self.y, self.n_trials)
        
        self.assertEqual(log_lik.shape, (500, self.n_obs))
        
        # 1. 测试 WAIC
        waic_res = compute_waic(log_lik)
        self.assertTrue(np.isfinite(waic_res["waic"]))
        self.assertGreater(waic_res["p_waic"], 0.0)
        
        # 2. 测试 PSIS-LOO
        loo_res = compute_psis_loo(log_lik)
        self.assertTrue(np.isfinite(loo_res["elpd_loo"]))
        self.assertLessEqual(loo_res["max_k_hat"], 1.5)
        self.assertEqual(len(loo_res["k_hats"]), self.n_obs)

    def test_posterior_predictive_check(self):
        beta_map, cov_matrix = fit_bayesian_logistic_regression(self.X, self.y, self.n_trials)
        beta_draws = np.random.multivariate_normal(beta_map, cov_matrix, size=200)
        
        y_rep = generate_posterior_predictive(beta_draws, self.X, self.n_trials, seed=42)
        self.assertEqual(y_rep.shape, (200, self.n_obs))
        
        ppc_res = posterior_predictive_check_stats(self.y, y_rep)
        self.assertTrue(0.0 <= ppc_res["p_val_mean"] <= 1.0)
        self.assertTrue(0.0 <= ppc_res["p_val_max"] <= 1.0)
        self.assertEqual(ppc_res["is_calibrated"], 1.0)
        
        code = get_pymc_glm_code()
        self.assertIn("pm.Model", code)


if __name__ == '__main__':
    unittest.main()

