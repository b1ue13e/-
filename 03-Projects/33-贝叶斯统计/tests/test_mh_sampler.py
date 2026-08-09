"""Unit tests for Metropolis-Hastings Sampler & Rank-Normalized Diagnostics."""
import unittest
import numpy as np
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))
from mh_sampler import (
    run_mh_chain,
    run_parallel_mh,
    compute_classical_r_hat,
    compute_rank_normalized_r_hat,
    compute_ess,
    compute_mcse,
    target_mixture_gaussian_log_prob
)


class TestMHSampler(unittest.TestCase):
    def test_target_density(self):
        val = target_mixture_gaussian_log_prob(np.array([0.0]))
        self.assertTrue(np.isfinite(val[0]))

    def test_chain_execution_and_acceptance_rate(self):
        chain, accept_rate = run_mh_chain(init_val=0.0, n_iter=2000, proposal_std=1.0, seed=42)
        self.assertEqual(len(chain), 2000)
        # 验证接受率处于合理探索区间
        self.assertGreater(accept_rate, 0.15)
        self.assertLess(accept_rate, 0.70)

    def test_parallel_chains_and_rank_normalized_r_hat(self):
        init_vals = [-4.0, -1.0, 2.0, 5.0]
        chains, rates = run_parallel_mh(
            init_vals=init_vals,
            n_iter=4000,
            burn_in=1000,
            proposal_std=1.5,
            base_seed=100
        )
        self.assertEqual(chains.shape, (4, 3000))
        
        # 1. 经典 R-hat
        r_hat_classic = compute_classical_r_hat(chains)
        self.assertLess(r_hat_classic, 1.05)
        
        # 2. 现代秩归一化折叠 R-hat
        r_hat_rank = compute_rank_normalized_r_hat(chains)
        self.assertLess(r_hat_rank, 1.05)

    def test_ess_and_mcse(self):
        init_vals = [-2.0, 0.0, 3.0, 4.0]
        chains, _ = run_parallel_mh(init_vals=init_vals, n_iter=3000, burn_in=500, base_seed=200)
        ess = compute_ess(chains)
        mcse = compute_mcse(chains)
        
        self.assertGreater(ess, 100.0)
        self.assertLess(mcse, 0.35)


if __name__ == '__main__':
    unittest.main()
