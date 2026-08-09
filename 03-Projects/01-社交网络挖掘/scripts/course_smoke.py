from __future__ import annotations

import argparse
import json
import platform
from pathlib import Path

import networkx as nx
import numpy as np


def run_smoke(output: Path) -> dict[str, object]:
    output.mkdir(parents=True, exist_ok=True)
    karate = nx.karate_club_graph()
    assert karate.number_of_nodes() == 34
    assert karate.number_of_edges() == 78
    assert nx.is_connected(karate)

    directed = nx.DiGraph([(0, 1), (1, 0), (1, 2), (2, 3), (3, 2), (4, 4)])
    components = sorted((sorted(component) for component in nx.strongly_connected_components(directed)), key=lambda x: (len(x), x))
    assert components == [[4], [0, 1], [2, 3]]
    assert len(list(nx.selfloop_edges(directed))) == 1

    adjacency = nx.to_numpy_array(nx.path_graph(3), nodelist=[0, 1, 2], dtype=float)
    degree = adjacency.sum(axis=1)
    transition = np.diag(1.0 / degree) @ adjacency
    assert np.allclose(transition.sum(axis=1), 1.0)

    report: dict[str, object] = {
        "python": platform.python_version(),
        "numpy": np.__version__,
        "networkx": nx.__version__,
        "checks": {
            "karate_nodes": karate.number_of_nodes(),
            "karate_edges": karate.number_of_edges(),
            "directed_scc": components,
            "directed_selfloops": 1,
            "transition_rows_sum_to_one": True,
        },
    }
    (output / "smoke_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Run course environment and invariant checks.")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = run_smoke(args.output)
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()
