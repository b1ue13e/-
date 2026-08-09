"""Unit tests for Capstone End-to-End Bayesian Decision Analysis Suite."""
import unittest
import numpy as np
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))
from bayesian_decision_system import (
    linex_loss,
    quantile_check_loss,
    solve_bayesian_expected_loss,
    analytical_linex_optimal_action,
    evaluate_lending_decision_policy
)


class TestBayesianDecisionSystem(unittest.TestCase):
    def setUp(self):
        np.random.seed(42)
        # 模拟 2000 个违约率/参数样本 ~ Beta(3, 17) (均值 0.15, 偏态)
        self.theta_draws = np.random.beta(3.0, 17.0, size=2000)

    def test_linex_loss_asymmetry(self):
        # 当 c > 0 时，高估惩罚严重大于低估惩罚
        loss_overestimate = linex_loss(theta=np.array([0.10]), a=0.20, c=5.0)
        loss_underestimate = linex_loss(theta=np.array([0.20]), a=0.10, c=5.0)
        self.assertGreater(float(loss_overestimate[0]), float(loss_underestimate[0]))

    def test_linex_numerical_vs_analytical_action(self):
        c = 3.0
        # 1. 解析解
        a_analytical = analytical_linex_optimal_action(self.theta_draws, c=c)
        
        # 2. 网格数值全期望最小化
        action_grid = np.linspace(0.01, 0.40, 400)
        a_numerical, min_loss, _ = solve_bayesian_expected_loss(
            self.theta_draws,
            lambda th, a: linex_loss(th, a, c=c),
            action_grid
        )
        
        # 验证数值解与解析解误差 < 0.005
        self.assertAlmostEqual(a_analytical, a_numerical, delta=0.005)

    def test_quantile_check_loss_action(self):
        tau = 0.90
        # 理论上 Check 损失的最优行动为后验 90% 分位数
        expected_q90 = np.percentile(self.theta_draws, 90)
        
        action_grid = np.linspace(0.01, 0.40, 400)
        a_opt, min_loss, _ = solve_bayesian_expected_loss(
            self.theta_draws,
            lambda th, a: quantile_check_loss(th, a, tau=tau),
            action_grid
        )
        
        self.assertAlmostEqual(expected_q90, a_opt, delta=0.005)

    def test_lending_business_decision_policy(self):
        policy_res = evaluate_lending_decision_policy(
            self.theta_draws,
            loan_amount=10000.0,
            interest_profit=1200.0,
            loss_given_default=8000.0
        )
        
        best_th = policy_res["best_approval_threshold"]
        max_prof = policy_res["max_expected_profit"]
        
        self.assertGreater(best_th, 0.05)
        self.assertLess(best_th, 0.25)
        self.assertGreater(max_prof, 0.0)


if __name__ == '__main__':
    unittest.main()
