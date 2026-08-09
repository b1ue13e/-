from __future__ import annotations

import json
from pathlib import Path

from starter.gnn_course.stages import estimate_attention_cost, run_s01, run_s02, run_s03, run_s04


def test_s01_worked_example_writes_protocol_and_metrics(tmp_path: Path) -> None:
    result = run_s01(tmp_path, seed=7, probe_epochs=3)
    assert len(result["rows"]) == 3
    assert (tmp_path / "cooccurrence.csv").exists()
    assert json.loads((tmp_path / "manifest.json").read_text(encoding="utf-8"))["assignment"] == "GNN-S01"


def test_s02_worked_example_runs_all_models_and_seeds(tmp_path: Path) -> None:
    rows = run_s02(tmp_path, seeds=(7,), epochs=3)
    assert len(rows) == 4
    assert {row["model"] for row in rows} == {"mlp", "gcn", "graphsage", "gat"}


def test_s03_worked_example_separates_pretraining_from_downstream(tmp_path: Path) -> None:
    result = run_s03(tmp_path, seed=7, pretrain_epochs=3, probe_epochs=3)
    assert {row["protocol"] for row in result["rows"]} == {"pretrained-frozen", "supervised-from-scratch"}
    assert result["final_pretrain_loss"] >= 0


def test_s04_cost_estimator_has_dense_sparse_and_zero_edge_boundaries(tmp_path: Path) -> None:
    rows = run_s04(tmp_path)
    assert len(rows) == 3
    assert rows[-1]["sparse_score_elements"] == 0
    assert rows[0]["dense_score_elements"] > rows[0]["sparse_score_elements"]
    assert estimate_attention_cost(10, 5, 4)["dense_attention_main_ops"] == 400
