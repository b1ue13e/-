from __future__ import annotations

import csv
import json
from pathlib import Path

from scripts.course_smoke import run_smoke
from scripts.fetch_public_network import EXPECTED_SHA256
from scripts.generate_course_data import generate_course_data
from starter.sna_course.data_contract import read_node_features, read_temporal_edges
from starter.sna_course.pipeline import run_baseline_pipeline
from starter.sna_course.stage_baselines import run_stage_baseline


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def test_generation_is_deterministic(tmp_path: Path) -> None:
    first = generate_course_data(tmp_path / "first", seed=42)
    second = generate_course_data(tmp_path / "second", seed=42)
    assert first == second
    assert len(first["files"]) == 10


def test_temporal_and_node_invariants(tmp_path: Path) -> None:
    output = tmp_path / "data"
    manifest = generate_course_data(output, seed=7)
    events = _read_csv(output / "temporal_edges.csv")
    timestamps = [int(row["timestamp"]) for row in events]
    pairs = [(int(row["source"]), int(row["target"])) for row in events]
    features = _read_csv(output / "node_features.csv")
    labels = _read_csv(output / "node_labels.csv")

    assert timestamps == sorted(timestamps)
    assert len(pairs) == len(set(pairs))
    assert all(source != target for source, target in pairs)
    assert len(features) == manifest["node_count"] == 24
    assert {int(row["node"]) for row in features} == set(range(24))
    assert set(features[0]) == {"node", "feature_a", "feature_b"}
    assert set(labels[0]) == {"node", "community"}
    nodes, matrix = read_node_features(output / "node_features.csv")
    assert len(nodes) == len(matrix) == 24


def test_manifest_hashes_match_files(tmp_path: Path) -> None:
    output = tmp_path / "data"
    generate_course_data(output, seed=42)
    manifest = json.loads((output / "generation_manifest.json").read_text(encoding="utf-8"))
    for name, metadata in manifest["files"].items():
        assert len(metadata["sha256"]) == 64
        assert metadata["rows"] == len(_read_csv(output / name))


def test_smoke_report(tmp_path: Path) -> None:
    report = run_smoke(tmp_path / "smoke")
    assert report["checks"]["karate_nodes"] == 34
    assert report["checks"]["karate_edges"] == 78
    assert report["checks"]["transition_rows_sum_to_one"] is True
    assert (tmp_path / "smoke" / "smoke_report.json").exists()


def test_baseline_pipeline_is_deterministic_and_leak_resistant(tmp_path: Path) -> None:
    data_dir = tmp_path / "data"
    generate_course_data(data_dir, seed=42)
    first = run_baseline_pipeline(data_dir / "temporal_edges.csv", tmp_path / "run-1", seed=7)
    second = run_baseline_pipeline(data_dir / "temporal_edges.csv", tmp_path / "run-2", seed=7)

    assert first == second
    assert set(first) == {
        "random",
        "preferential_attachment",
        "common_neighbors",
        "jaccard",
        "adamic_adar",
    }
    assert all(0.0 <= value <= 1.0 for metrics in first.values() for value in metrics.values())
    assert read_temporal_edges(data_dir / "temporal_edges.csv")
    assert (tmp_path / "run-1" / "split_manifest.json").exists()
    assert (tmp_path / "run-1" / "predictions.csv").exists()

    undirected = run_baseline_pipeline(
        data_dir / "temporal_edges.csv",
        tmp_path / "run-undirected",
        seed=7,
        directed=False,
    )
    assert set(undirected) == set(first)
    manifest = json.loads(
        (tmp_path / "run-undirected" / "split_manifest.json").read_text(encoding="utf-8")
    )
    assert manifest["policy"]["edge_identity"] == "undirected first occurrence"


def test_public_dataset_pin_is_a_sha256() -> None:
    assert len(EXPECTED_SHA256) == 64
    int(EXPECTED_SHA256, 16)


def test_stage_baselines_generate_inspectable_reports(tmp_path: Path) -> None:
    data_dir = tmp_path / "data"
    generate_course_data(data_dir, seed=42)
    for stage in ("01", "02", "03", "05"):
        first = run_stage_baseline(stage, data_dir, tmp_path / f"stage-{stage}-a", seed=7)
        second = run_stage_baseline(stage, data_dir, tmp_path / f"stage-{stage}-b", seed=7)
        assert first == second
