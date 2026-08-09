from __future__ import annotations

import torch

from starter.gnn_course.data import make_toy_graph, sample_batch_subgraph, sample_neighbor_adjacency
from starter.gnn_course.models import GAT, GCN, GraphSAGE, MLP, _symmetric_normalize
from starter.gnn_course.train import _macro_f1, run_model, run_suite
from starter.gnn_course.data import GraphData


def test_all_models_return_node_logits() -> None:
    data = make_toy_graph()
    for model_type in (MLP, GCN, GraphSAGE, GAT):
        model = model_type(data.x.shape[1], 8, 2)
        logits = model(data.x, data.adj)
        assert logits.shape == (data.num_nodes, 2)
        assert torch.isfinite(logits).all()


def test_all_graph_models_are_permutation_equivariant() -> None:
    torch.manual_seed(7)
    data = make_toy_graph()
    permutation = torch.tensor([4, 1, 8, 0, 7, 3, 10, 2, 11, 5, 9, 6])
    for model_type in (GCN, GraphSAGE, GAT):
        model = model_type(data.x.shape[1], 8, 2)
        original = model(data.x, data.adj)
        permuted = model(data.x[permutation], data.adj[permutation][:, permutation])
        assert torch.allclose(permuted, original[permutation], atol=1e-6)


def test_gcn_normalization_matches_hand_calculation() -> None:
    adj = torch.tensor([[0.0, 1.0], [1.0, 0.0]])
    expected = torch.tensor([[0.5, 0.5], [0.5, 0.5]])
    assert torch.allclose(_symmetric_normalize(adj), expected)


def test_gat_attention_is_local_and_row_normalized() -> None:
    data = make_toy_graph()
    model = GAT(data.x.shape[1], 8, 2)
    model(data.x, data.adj)
    attention = model.last_attention
    assert attention is not None
    allowed = data.adj + torch.eye(data.num_nodes)
    assert torch.allclose(attention.sum(dim=1), torch.ones(data.num_nodes), atol=1e-6)
    assert torch.equal(attention[allowed == 0], torch.zeros_like(attention[allowed == 0]))


def test_neighbor_sampling_is_deterministic_and_respects_fanout() -> None:
    data = make_toy_graph()
    first = sample_neighbor_adjacency(data.adj, fanout=2, seed=7)
    second = sample_neighbor_adjacency(data.adj, fanout=2, seed=7)
    assert torch.equal(first, second)
    assert bool((first.sum(dim=1) <= 2).all())
    assert bool((first[data.adj == 0] == 0).all())


def test_batch_subgraph_is_deterministic_and_limits_each_expansion() -> None:
    data = make_toy_graph()
    first = sample_batch_subgraph(data.adj, torch.tensor([0, 6]), (2, 2), seed=7)
    second = sample_batch_subgraph(data.adj, torch.tensor([0, 6]), (2, 2), seed=7)
    assert all(torch.equal(left, right) for left, right in zip(first, second))
    node_ids, sub_adj, target_positions = first
    assert target_positions.tolist() == [0, 1]
    assert node_ids.numel() <= data.num_nodes
    assert bool((sub_adj.sum(dim=1) <= 2).all())
    assert bool((sub_adj[data.adj.index_select(0, node_ids).index_select(1, node_ids) == 0] == 0).all())


def test_training_updates_each_model() -> None:
    for model_name in ("mlp", "gcn", "graphsage", "gat"):
        report = run_model(model_name, seed=7, epochs=60)
        assert report["final_train_loss"] < report["initial_train_loss"]
        assert report["parameter_delta_l2"] > 0
        assert 0.0 <= report["test_accuracy"] <= 1.0
        assert 0.0 <= report["test_macro_f1"] <= 1.0


def test_macro_f1_counts_all_declared_classes() -> None:
    data = GraphData(
        x=torch.zeros((3, 1)),
        adj=torch.eye(3),
        y=torch.tensor([0, 1, 2]),
        train_mask=torch.tensor([True, True, True]),
        val_mask=torch.tensor([True, True, True]),
        test_mask=torch.tensor([True, True, True]),
    )
    logits = torch.tensor([[9.0, 0.0, 0.0], [0.0, 9.0, 0.0], [9.0, 0.0, 0.0]])
    assert abs(_macro_f1(logits, data, data.test_mask) - (2 / 3 + 1 + 0) / 3) < 1e-6


def test_suite_writes_inspectable_artifacts(tmp_path) -> None:
    rows = run_suite(tmp_path, seeds=(7, 42, 2026), epochs=30)
    assert len(rows) == 12
    assert (tmp_path / "split_manifest.json").exists()
    assert (tmp_path / "runs.csv").exists()
    assert (tmp_path / "summary.json").exists()
