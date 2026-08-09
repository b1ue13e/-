from __future__ import annotations

import json

from starter.gnn_course.data import graph_hash, make_contextual_sbm, make_toy_graph
from starter.gnn_course.protocol import assert_disjoint_masks, assert_graph_contract, build_manifest, write_manifest


def test_toy_graph_contract_is_deterministic() -> None:
    first = make_toy_graph()
    second = make_toy_graph()
    assert first.x.shape == (12, 4)
    assert first.adj.shape == (12, 12)
    assert graph_hash(first) == graph_hash(second)
    assert first.adj.equal(first.adj.T)
    assert not first.adj.diag().any()


def test_masks_are_disjoint_and_manifest_is_explicit(tmp_path) -> None:
    data = make_toy_graph()
    assert_disjoint_masks(data)
    manifest = build_manifest(data, (7, 42, 2026))
    assert manifest["protocol"] == "transductive-node-classification"
    assert manifest["labels_used_for_loss"] == "train_mask_only"
    assert manifest["split_counts"] == {"train": 6, "validation": 3, "test": 3}
    assert sorted(
        manifest["split_indices"]["train"]
        + manifest["split_indices"]["validation"]
        + manifest["split_indices"]["test"]
    ) == list(range(12))
    path = tmp_path / "split_manifest.json"
    write_manifest(path, data, (7, 42, 2026))
    loaded = json.loads(path.read_text(encoding="utf-8"))
    assert len(loaded["graph_sha256"]) == 64
    assert loaded["seeds"] == [7, 42, 2026]


def test_contextual_sbm_is_deterministic_and_has_useful_split_sizes() -> None:
    first = make_contextual_sbm()
    second = make_contextual_sbm()
    assert_graph_contract(first)
    assert graph_hash(first) == graph_hash(second)
    assert first.num_nodes == 120
    assert int(first.train_mask.sum()) >= 30
    assert int(first.val_mask.sum()) >= 30
    assert int(first.test_mask.sum()) >= 40
