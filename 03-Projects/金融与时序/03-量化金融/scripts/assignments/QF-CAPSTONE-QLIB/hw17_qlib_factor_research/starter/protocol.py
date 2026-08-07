from __future__ import annotations

import csv
from pathlib import Path


def _read_key_value_csv(path: Path, key_field: str, value_field: str) -> dict[str, str]:
    with path.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    return {row[key_field]: row[value_field] for row in rows}


def build_protocol_summary(manifest_csv: Path, workflow_csv: Path, baseline_csv: Path) -> dict[str, object]:
    manifest_map = _read_key_value_csv(manifest_csv, "key", "value")
    workflow_map = _read_key_value_csv(workflow_csv, "field", "value")
    baseline_map = _read_key_value_csv(baseline_csv, "protocol", "detail")

    checks = {
        "has_qlib_commit": "qlib_commit" in manifest_map,
        "has_data_release": "data_release" in manifest_map,
        "has_provider_uri": "provider_uri" in manifest_map,
        "uses_lightgbm": workflow_map.get("model") == "lightgbm",
        "uses_alpha158": workflow_map.get("dataset") == "Alpha158",
        "has_equal_weight_baseline": "E0" in baseline_map,
        "has_naive_signal_baseline": "E1" in baseline_map,
        "has_ml_baseline": "E2" in baseline_map,
    }
    return {
        "manifest": manifest_map,
        "workflow": workflow_map,
        "baseline_protocol": baseline_map,
        "checklist": checks,
        "all_checks_pass": all(checks.values()),
    }
