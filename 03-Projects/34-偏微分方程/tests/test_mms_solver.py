# -*- coding: utf-8 -*-
"""
Automated unit test for MMS Poisson solver verifying second-order convergence.
"""
import pytest
import numpy as np
import sys
from pathlib import Path

# Add scripts directory to path
script_dir = Path(__file__).parent.parent / "scripts"
sys.path.append(str(script_dir))

from mms_poisson_solver import solve_poisson_2d

def test_poisson_solver_single_grid():
    h, l2_err, linf_err = solve_poisson_2d(20)
    assert h == 0.05
    assert l2_err < 0.01
    assert linf_err < 0.01

def test_poisson_solver_second_order_convergence():
    N_list = [20, 40, 80]
    errors_l2 = []
    h_list = []
    
    for N in N_list:
        h, l2, _ = solve_poisson_2d(N)
        h_list.append(h)
        errors_l2.append(l2)
        
    # Calculate observed convergence orders
    order1 = np.log(errors_l2[0] / errors_l2[1]) / np.log(h_list[0] / h_list[1])
    order2 = np.log(errors_l2[1] / errors_l2[2]) / np.log(h_list[1] / h_list[2])
    
    print(f"\nObserved convergence rates: {order1:.4f}, {order2:.4f}")
    assert 1.95 <= order1 <= 2.05, f"Order {order1} does not match expected second order (O(h^2))"
    assert 1.95 <= order2 <= 2.05, f"Order {order2} does not match expected second order (O(h^2))"
