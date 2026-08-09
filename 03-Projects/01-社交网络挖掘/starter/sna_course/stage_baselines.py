from __future__ import annotations

import csv
import json
import random
from pathlib import Path

import networkx as nx


def _edge_rows(path: Path) -> list[tuple[int, int]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None or not {"source", "target"} <= set(reader.fieldnames):
            raise ValueError(f"{path} requires source and target columns")
        return [(int(row["source"]), int(row["target"])) for row in reader]


def _write_report(output: Path, name: str, report: dict[str, object]) -> dict[str, object]:
    output.mkdir(parents=True, exist_ok=True)
    (output / name).write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return report


def stage01_baseline(data_dir: Path, output: Path) -> dict[str, object]:
    rows = _edge_rows(data_dir / "directed_edges.csv")
    graph = nx.DiGraph(rows)
    unique_edges = set(rows)
    report: dict[str, object] = {
        "event_rows": len(rows),
        "nodes": graph.number_of_nodes(),
        "unique_edges": len(unique_edges),
        "duplicate_events": len(rows) - len(unique_edges),
        "self_loops": nx.number_of_selfloops(graph),
        "reciprocal_pairs": sum(
            1 for source, target in unique_edges if source < target and (target, source) in unique_edges
        ),
        "weak_components": nx.number_weakly_connected_components(graph),
        "strong_components": nx.number_strongly_connected_components(graph),
    }
    return _write_report(output, "stage01_baseline.json", report)


def _graph_statistics(graph: nx.Graph) -> dict[str, float | int]:
    largest_nodes = max(nx.connected_components(graph), key=len)
    largest = graph.subgraph(largest_nodes)
    return {
        "nodes": graph.number_of_nodes(),
        "edges": graph.number_of_edges(),
        "average_clustering": nx.average_clustering(graph),
        "largest_component_fraction": len(largest_nodes) / graph.number_of_nodes(),
        "largest_component_average_path": nx.average_shortest_path_length(largest),
    }


def stage02_baseline(data_dir: Path, output: Path, seed: int = 42) -> dict[str, object]:
    graph = nx.Graph(_edge_rows(data_dir / "structure_edges.csv"))
    er = nx.gnm_random_graph(graph.number_of_nodes(), graph.number_of_edges(), seed=seed)
    report: dict[str, object] = {
        "seed": seed,
        "observed": _graph_statistics(graph),
        "er_same_n_m": _graph_statistics(er),
        "boundary": "One ER draw is a smoke baseline, not a statistical conclusion.",
    }
    return _write_report(output, "stage02_baseline.json", report)


def stage03_baseline(data_dir: Path, output: Path) -> dict[str, object]:
    graph = nx.Graph(_edge_rows(data_dir / "structure_edges.csv"))
    communities = list(nx.community.greedy_modularity_communities(graph))
    report: dict[str, object] = {
        "method": "greedy_modularity_communities",
        "community_count": len(communities),
        "community_sizes": sorted((len(group) for group in communities), reverse=True),
        "modularity": nx.community.modularity(graph, communities),
        "oracle_labels_used_in_fit": False,
    }
    return _write_report(output, "stage03_baseline.json", report)


def _sir_spread(graph: nx.Graph, seeds: set[int], beta: float, gamma: float, seed: int) -> int:
    rng = random.Random(seed)
    susceptible = set(graph).difference(seeds)
    infected = set(seeds)
    recovered: set[int] = set()
    steps = 0
    while infected:
        steps += 1
        if steps > 10_000:
            raise RuntimeError("SIR simulation exceeded the step limit")
        new_infected: set[int] = set()
        new_recovered: set[int] = set()
        for node in sorted(infected):
            for neighbor in sorted(graph.neighbors(node)):
                if neighbor in susceptible and rng.random() < beta:
                    new_infected.add(neighbor)
            if rng.random() < gamma:
                new_recovered.add(node)
        susceptible.difference_update(new_infected)
        infected.update(new_infected)
        infected.difference_update(new_recovered)
        recovered.update(new_recovered)
        if len(recovered) == graph.number_of_nodes():
            break
    return len(recovered | infected)


def stage05_baseline(data_dir: Path, output: Path, seed: int = 42) -> dict[str, object]:
    graph = nx.Graph(_edge_rows(data_dir / "structure_edges.csv"))
    degree_seeds = {node for node, _ in sorted(graph.degree, key=lambda item: (-item[1], item[0]))[:3]}
    random_seeds = set(random.Random(seed).sample(sorted(graph), 3))
    simulation_seeds = list(range(seed, seed + 30))
    strategies = {"degree": degree_seeds, "random": random_seeds}
    report: dict[str, object] = {
        "beta": 0.04,
        "gamma": 0.3,
        "runs": len(simulation_seeds),
        "strategies": {},
        "boundary": "Synthetic edge transmission is a protocol exercise, not an epidemiological estimate.",
    }
    for name, selected in strategies.items():
        spreads = [
            _sir_spread(graph, selected, beta=0.04, gamma=0.3, seed=run_seed)
            for run_seed in simulation_seeds
        ]
        report["strategies"][name] = {
            "seeds": sorted(selected),
            "mean_spread": sum(spreads) / len(spreads),
            "min_spread": min(spreads),
            "max_spread": max(spreads),
        }
    return _write_report(output, "stage05_baseline.json", report)


def run_stage_baseline(stage: str, data_dir: Path, output: Path, seed: int = 42) -> dict[str, object]:
    runners = {
        "01": lambda: stage01_baseline(data_dir, output),
        "02": lambda: stage02_baseline(data_dir, output, seed),
        "03": lambda: stage03_baseline(data_dir, output),
        "05": lambda: stage05_baseline(data_dir, output, seed),
    }
    if stage not in runners:
        raise ValueError(f"unsupported starter stage: {stage}")
    return runners[stage]()
