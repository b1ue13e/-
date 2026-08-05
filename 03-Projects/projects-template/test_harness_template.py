"""
PyTest Test Harness Template for 4-Tier Baseline Assignment Validation
========================================================================
Usage:
    pytest 03-Projects/projects-<course_id>/tests/test_<hw_id>.py

Design:
    - Level 1: Simple Baseline (API run & Basic assert)
    - Level 2: Medium Baseline (Feature / Module numerical assert)
    - Level 3: Strong Baseline (Hand-crafted zero-dependency algorithm vs scipy/torch reference)
    - Level 4: Boss Baseline (Performance / Memory / Mathematical Invariants)
"""

import pytest
import numpy as np


# ----------------------------------------------------------------------
# Helper / Reference implementations for ground truth verification
# ----------------------------------------------------------------------
def reference_solution(inputs: np.ndarray) -> np.ndarray:
    """Ground truth reference implementation using standard scipy/numpy."""
    return np.sin(inputs) + 0.5 * inputs


# ----------------------------------------------------------------------
# Tier 1: Simple Baseline Test (🟢 L1)
# ----------------------------------------------------------------------
def test_l1_simple_baseline():
    """Verify basic pipeline execution and output shape/type sanity."""
    inputs = np.linspace(-3, 3, 10)
    outputs = reference_solution(inputs)
    
    assert outputs is not None, "Output should not be None"
    assert outputs.shape == inputs.shape, f"Shape mismatch: {outputs.shape} vs {inputs.shape}"
    assert not np.isnan(outputs).any(), "Output contains NaN values"


# ----------------------------------------------------------------------
# Tier 2: Medium Baseline Test (🟡 L2)
# ----------------------------------------------------------------------
def test_l2_medium_baseline():
    """Verify numerical tolerance, boundary conditions, and convergence."""
    inputs = np.array([0.0, np.pi / 2, np.pi])
    outputs = reference_solution(inputs)
    
    expected = np.array([0.0, 1.0 + 0.25 * np.pi, 0.5 * np.pi])
    np.testing.assert_allclose(outputs, expected, rtol=1e-5, atol=1e-5)


# ----------------------------------------------------------------------
# Tier 3: Strong Baseline - Hand-crafted Algorithmic Precision (🔴 L3)
# ----------------------------------------------------------------------
def test_l3_strong_baseline_handcrafted_precision():
    """Verify hand-crafted algorithm implementation against reference ground truth."""
    rng = np.random.default_rng(42)
    test_data = rng.uniform(-5, 5, size=(100,))
    
    ref_res = reference_solution(test_data)
    # TODO: Replace with student hand-crafted implementation call
    student_res = reference_solution(test_data) 
    
    np.testing.assert_allclose(
        student_res,
        ref_res,
        rtol=1e-4,
        atol=1e-4,
        err_msg="Student L3 hand-crafted solution deviates from ground truth!"
    )


# ----------------------------------------------------------------------
# Tier 4: Boss Baseline - Mathematical Invariants & Extremes (👑 L4)
# ----------------------------------------------------------------------
def test_l4_boss_baseline_invariants():
    """Verify extreme edge cases, numerical stability, and mathematical invariants."""
    large_inputs = np.array([1e-8, -1e-8, 1e5, -1e5])
    outputs = reference_solution(large_inputs)
    
    assert np.isfinite(outputs).all(), "Outputs must remain finite under extreme input range"
