from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

import stochastic_process_lab as lab  # noqa: E402


class TransitionMatrixTests(unittest.TestCase):
    def test_invalid_transition_matrix_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            lab.validate_transition_matrix([[0.8, 0.3], [0.3, 0.7]])

    def test_stationary_distribution(self) -> None:
        result = lab.stationary_distribution([[0.8, 0.2], [0.3, 0.7]])
        self.assertAlmostEqual(result[0], 0.6, places=10)
        self.assertAlmostEqual(result[1], 0.4, places=10)

    def test_markov_empirical_frequency(self) -> None:
        path = lab.simulate_markov_chain(
            [[0.8, 0.2], [0.3, 0.7]], initial_state=0, steps=40_000, seed=7
        )
        frequency_zero = path.count(0) / len(path)
        self.assertLess(abs(frequency_zero - 0.6), 0.025)


class CountingAndQueueTests(unittest.TestCase):
    def test_poisson_count_moments(self) -> None:
        counts = lab.simulate_poisson_counts(3.0, 2.0, 12_000, seed=11)
        mean = sum(counts) / len(counts)
        variance = sum((value - mean) ** 2 for value in counts) / (len(counts) - 1)
        self.assertLess(abs(mean - 6.0), 0.12)
        self.assertLess(abs(variance - 6.0), 0.25)

    def test_mm1_stable_time_average(self) -> None:
        result = lab.simulate_mm1(2.0, 3.0, 20_000.0, 2_000.0, seed=13)
        self.assertLess(
            abs(result["time_average_number"] - result["theory_average_number"]),
            0.25,
        )
        self.assertGreaterEqual(result["arrivals"], result["departures"])

    def test_mm1_unstable_case_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "arrival_rate < service_rate"):
            lab.simulate_mm1(3.0, 3.0, 100.0, 10.0, seed=17)


class ContinuousProcessTests(unittest.TestCase):
    def test_brownian_terminal_and_quadratic_variation(self) -> None:
        result = lab.simulate_brownian_summary(4_000, 200, 1.0, seed=19)
        self.assertLess(abs(result["terminal_mean"]), 0.05)
        self.assertLess(abs(result["terminal_variance"] - 1.0), 0.06)
        self.assertLess(abs(result["quadratic_variation_mean"] - 1.0), 0.03)

    def test_ou_endpoint_moments(self) -> None:
        result = lab.simulate_ou_endpoints(
            1.5, 0.5, 0.7, -1.0, 2.0, 400, 4_000, seed=23
        )
        self.assertLess(abs(result["endpoint_mean"] - result["theory_mean"]), 0.04)
        self.assertLess(abs(result["endpoint_variance"] - result["theory_variance"]), 0.04)
        self.assertTrue(math.isclose(result["dt"], 0.005))

    def test_brownian_reflection_probability(self) -> None:
        result = lab.simulate_brownian_maximum(
            paths=6_000, steps=240, horizon=1.0, threshold=0.75, seed=31
        )
        self.assertLess(
            abs(
                result["empirical_maximum_probability"]
                - result["theory_maximum_probability"]
            ),
            0.035,
        )
        self.assertLess(
            abs(
                result["empirical_terminal_probability"]
                - result["theory_terminal_probability"]
            ),
            0.025,
        )

    def test_gamblers_ruin_matches_optional_stopping_baseline(self) -> None:
        result = lab.simulate_gamblers_ruin(3, 10, 12_000, seed=37)
        self.assertLess(
            abs(
                result["empirical_upper_hit_probability"]
                - result["theory_upper_hit_probability"]
            ),
            0.02,
        )
        self.assertLess(
            abs(
                result["empirical_mean_stopping_time"]
                - result["theory_mean_stopping_time"]
            ),
            0.8,
        )

    def test_gbm_coupled_error_study_recovers_strong_order(self) -> None:
        result = lab.simulate_gbm_error_study(
            0.08, 0.3, 1.0, 1.0, [16, 32, 64, 128], 2_000, seed=41
        )
        rows = result["rows"]
        self.assertLess(rows[-1]["strong_mae"], rows[0]["strong_mae"])
        self.assertGreater(result["estimated_strong_order"], 0.35)
        self.assertLess(result["estimated_strong_order"], 0.75)
        self.assertTrue(
            all(row["monte_carlo_standard_error"] > 0.0 for row in rows)
        )


class ReferenceReportTests(unittest.TestCase):
    def test_reference_report_contains_every_course_family(self) -> None:
        report = lab.build_reference_report(seed=29)
        self.assertEqual(
            set(report),
            {
                "manifest",
                "markov",
                "poisson",
                "brownian",
                "brownian_reflection",
                "stopped_walk",
                "mm1",
                "ou",
                "gbm_error_study",
            },
        )
        self.assertIn("purpose", report["manifest"])


if __name__ == "__main__":
    unittest.main()
