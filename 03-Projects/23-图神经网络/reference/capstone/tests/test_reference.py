from __future__ import annotations

import csv
import json
from pathlib import Path

from reference.capstone.run import _load_config, run_reference


def test_reference_submission_writes_complete_evidence(tmp_path: Path) -> None:
    config = _load_config(Path(__file__).parents[1] / "config.json")
    config["epochs"] = 8
    config["patience"] = 3
    config["seeds"] = [7]
    rows = run_reference(config, tmp_path)
    assert len(rows) == 10
    manifest = json.loads((tmp_path / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["submission_type"] == "reference_submission"
    assert manifest["test_used_for_selection"] is False
    assert len(manifest["split_indices"]["test"]) > 0
    with (tmp_path / "runs.csv").open(encoding="utf-8", newline="") as handle:
        saved = list(csv.DictReader(handle))
    assert len(saved) == len(rows)
    assert all(row["status"] == "completed" for row in saved)
    trained = [row for row in saved if int(row["parameters"]) > 0]
    assert all(float(row["parameter_delta_l2"]) > 0 for row in trained)
    assert all(row["test_evaluations"] == "1" for row in saved)
    sampled = [row for row in saved if row["experiment"] == "graphsage-fanout-3"]
    assert sampled and all(float(row["sampled_nodes_mean"]) > 0 for row in sampled)
    baselines = {row["model"] for row in saved if int(row["parameters"]) == 0}
    assert baselines == {"majority", "label-propagation"}
    assert (tmp_path / "summary.json").exists()
    assert (tmp_path / "error_nodes.json").exists()
