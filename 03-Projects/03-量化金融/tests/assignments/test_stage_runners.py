from __future__ import annotations

import csv
import importlib.util
import json
import math
import subprocess
import sys
from datetime import date
from pathlib import Path

import numpy as np
import pytest


ROOT = Path(__file__).resolve().parents[2]
SCRIPT_ROOT = ROOT / "scripts" / "assignments"
DATA = ROOT / "data" / "smoke"


def load_function(path: Path, function_name: str):
    module_name = "audit_" + "_".join(path.parts[-5:]).replace(".", "_")
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, function_name)


def test_stage_one_baseline_enforces_signal_delay_and_cost_identity(tmp_path: Path) -> None:
    build = load_function(
        SCRIPT_ROOT / "QF-ST01" / "data_protocol_baseline" / "starter" / "baseline.py",
        "build_baseline_summary",
    )
    summary = build(DATA / "data_protocol_baseline" / "ohlcv.csv")
    assert summary["method"] == "lagged_ma_baseline"
    assert summary["signal_is_lagged"] is True
    assert summary["leakage_negative_control_differs"] is True
    assert summary["net_identity_holds"] is True
    assert summary["max_drawdown"] <= 0

    with (DATA / "data_protocol_baseline" / "ohlcv.csv").open("r", encoding="utf-8", newline="") as file:
        rows = list(csv.DictReader(file))
    rows[0]["volume"] = "0"
    zero_volume = tmp_path / "ohlcv_zero_volume.csv"
    with zero_volume.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    assert build(zero_volume)["observations"] == len(rows)


def test_evt_uses_pot_gpd_and_reports_finite_tail_risk() -> None:
    build = load_function(
        SCRIPT_ROOT / "QF-ST02" / "evt_tail_risk" / "starter" / "tail_risk.py",
        "build_tail_risk_summary",
    )
    summary = build(DATA / "evt_tail_risk" / "returns.csv")
    assert summary["method"] == "POT-GPD"
    assert summary["tail_event_count"] >= 8
    assert math.isfinite(summary["shape"]) and summary["scale"] > 0
    assert summary["expected_shortfall"] >= summary["var"] > summary["threshold_loss"]


def test_evt_smoke_dates_are_valid_and_strictly_increasing() -> None:
    with (DATA / "evt_tail_risk" / "returns.csv").open("r", encoding="utf-8", newline="") as file:
        rows = list(csv.DictReader(file))
    dates = [date.fromisoformat(row["date"]) for row in rows]
    assert all(current > previous for previous, current in zip(dates, dates[1:]))


def test_activity_bars_conserve_volume_and_dollar_value() -> None:
    build = load_function(
        SCRIPT_ROOT / "QF-ST03" / "volume_dollar_bars" / "starter" / "bars.py",
        "build_bar_summary",
    )
    summary = build(DATA / "volume_dollar_bars" / "ticks.csv")
    assert summary["method"] == "threshold_activity_bars"
    assert summary["volume_conserved"] is True
    assert summary["dollar_conserved"] is True
    assert len(summary["volume_bars"]) >= 3
    assert len(summary["dollar_bars"]) >= 3
    with pytest.raises(ValueError, match="thresholds must be positive"):
        build(DATA / "volume_dollar_bars" / "ticks.csv", volume_threshold=-1)


def test_hrp_performs_clustering_and_recursive_bisection() -> None:
    build = load_function(
        SCRIPT_ROOT / "QF-ST03" / "hrp_allocation" / "starter" / "hrp.py",
        "build_hrp_summary",
    )
    summary = build(DATA / "hrp_allocation" / "asset_returns.csv")
    assert summary["method"] == "hierarchical_risk_parity"
    assert set(summary["cluster_order"]) == set(summary["assets"])
    assert sum(summary["weights"].values()) == pytest.approx(1.0)
    assert all(weight > 0 for weight in summary["weights"].values())


def test_rmt_denoising_returns_a_psd_covariance() -> None:
    build = load_function(
        SCRIPT_ROOT / "QF-ST03" / "covariance_denoising" / "starter" / "denoise.py",
        "build_denoise_summary",
    )
    summary = build(DATA / "covariance_denoising" / "asset_returns.csv")
    raw = np.asarray(summary["raw_covariance"])
    denoised = np.asarray(summary["denoised_covariance"])
    assert summary["method"] == "marchenko_pastur_eigenvalue_clipping"
    assert summary["lambda_plus"] > 1
    assert np.linalg.eigvalsh(denoised).min() >= -1e-10
    assert not np.allclose(raw, denoised)


def test_pbo_uses_symmetric_combinatorial_splits() -> None:
    build = load_function(
        SCRIPT_ROOT / "QF-ST03" / "cpcv_pbo" / "starter" / "audit.py",
        "build_audit_summary",
    )
    summary = build(
        DATA / "cpcv_pbo" / "strategy_returns.csv",
        DATA / "cpcv_pbo" / "parameter_grid.csv",
    )
    assert summary["method"] == "combinatorial_symmetric_cross_validation_pbo"
    assert summary["combinations"] == math.comb(6, 3)
    assert len(summary["rank_logits"]) == summary["combinations"]
    assert 0 <= summary["pbo"] <= 1
    assert len(set(summary["rank_logits"])) > 1


def test_execution_schedules_liquidate_the_parent_order() -> None:
    build = load_function(
        SCRIPT_ROOT / "QF-ST04" / "almgren_chriss" / "starter" / "execution.py",
        "build_execution_summary",
    )
    summary = build(
        DATA / "almgren_chriss" / "parent_order.csv",
        DATA / "almgren_chriss" / "liquidity_profile.csv",
    )
    assert summary["method"] == "continuous_almgren_chriss_sampled_grid"
    assert summary["inventory_conserved"] is True
    assert sum(summary["optimal_schedule"]) == pytest.approx(summary["total_qty"])
    assert summary["inventory_path"][0] == summary["total_qty"]
    assert summary["inventory_path"][-1] == pytest.approx(0.0)


def test_queue_model_tracks_events_and_bounds_probability(tmp_path: Path) -> None:
    build = load_function(
        SCRIPT_ROOT / "QF-ST04" / "queue_fill_probability" / "starter" / "queue_model.py",
        "build_queue_summary",
    )
    summary = build(DATA / "queue_fill_probability" / "lob_events.csv")
    assert summary["method"] == "poisson_unit_depletion_fill_approximation"
    assert summary["observed_reached_front"] is True
    assert summary["observed_filled"] is True
    assert summary["queue_path"][0] == summary["initial_ahead"]
    assert summary["own_order_path"][0] == summary["own_order_units"]
    assert summary["own_order_path"][-1] == 0
    assert summary["fill_event_index"] > summary["reached_front_event_index"]
    assert 0 <= summary["fill_probability"] <= 1
    assert summary["fill_probability"] <= summary["reach_front_probability"] <= 1
    assert summary["observed_duration_seconds"] == 8
    assert summary["probability_model_ignores_add_ahead"] is True

    fields = ["timestamp", "event_type", "units", "initial_ahead", "own_order_units", "horizon_seconds"]
    over_cancel = tmp_path / "over_cancel.csv"
    with over_cancel.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(
            [
                {"timestamp": 0, "event_type": "cancel_ahead", "units": 50, "initial_ahead": 10, "own_order_units": 2, "horizon_seconds": 2},
                {"timestamp": 1, "event_type": "trade", "units": 2, "initial_ahead": 10, "own_order_units": 2, "horizon_seconds": 2},
            ]
        )
    assert build(over_cancel)["depletion_units"] == 12

    zero_ahead = tmp_path / "zero_ahead.csv"
    with zero_ahead.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(
            [
                {"timestamp": 0, "event_type": "trade", "units": 1, "initial_ahead": 0, "own_order_units": 2, "horizon_seconds": 2},
                {"timestamp": 1, "event_type": "trade", "units": 1, "initial_ahead": 0, "own_order_units": 2, "horizon_seconds": 2},
            ]
        )
    zero_summary = build(zero_ahead)
    assert zero_summary["reached_front_event_index"] == -1
    assert zero_summary["observed_filled"] is True
    assert zero_summary["reach_front_probability"] == 1.0

    nonzero_start = tmp_path / "nonzero_start.csv"
    with nonzero_start.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(
            [
                {"timestamp": 1, "event_type": "trade", "units": 1, "initial_ahead": 2, "own_order_units": 1, "horizon_seconds": 2},
                {"timestamp": 2, "event_type": "trade", "units": 2, "initial_ahead": 2, "own_order_units": 1, "horizon_seconds": 2},
            ]
        )
    with pytest.raises(ValueError, match="t=0"):
        build(nonzero_start)


def test_every_active_runner_executes_against_its_registered_smoke_data(tmp_path: Path) -> None:
    manifests = sorted(SCRIPT_ROOT.rglob("package_manifest.json"))
    assert len(manifests) == 9
    for manifest_path in manifests:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        starter = manifest_path.parent / "starter"
        input_dir = ROOT / manifest["smoke_data_dir"]
        output_dir = tmp_path / manifest["slug"]
        completed = subprocess.run(
            [
                sys.executable,
                str(starter / "run.py"),
                "--input-dir",
                str(input_dir),
                "--output-dir",
                str(output_dir),
            ],
            cwd=starter,
            text=True,
            capture_output=True,
            check=False,
        )
        assert completed.returncode == 0, completed.stderr
        summary = json.loads((output_dir / "results" / "summary.json").read_text(encoding="utf-8"))
        if manifest["id"] == "QF-CAPSTONE-QLIB":
            contract = summary["contract_summary"]
            assert contract["contract_status"] == "contract_template_ready"
            assert contract["provider_status"] == "placeholder"
            assert contract["qlib_execution_status"] == "blocked_on_provider"
            assert contract["qlib_execution_passed"] is False
            assert all(contract["contract_checks"].values())
