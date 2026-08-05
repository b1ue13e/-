#!/usr/bin/env python3
"""Download and smoke-test the still-public Stanford SNAP course datasets."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import urllib.request
from dataclasses import dataclass
from pathlib import Path

import networkx as nx


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATA_DIR = ROOT / "99-System" / ".tmp" / "social-network-course-audit" / "data"


@dataclass(frozen=True)
class Dataset:
    filename: str
    url: str
    rows: int
    nodes: int
    self_loops: int
    sha256: str
    columns: int = 2


DATASETS = {
    "wiki-vote": Dataset(
        "wiki-Vote.txt.gz",
        "https://snap.stanford.edu/data/wiki-Vote.txt.gz",
        103_689,
        7_115,
        0,
        "7d3e53626e14b8b09fb3b396bece9d481ad606bd64ceab066349ff57d4ada7fc",
    ),
    "ca-grqc": Dataset(
        "ca-GrQc.txt.gz",
        "https://snap.stanford.edu/data/ca-GrQc.txt.gz",
        28_980,
        5_242,
        12,
        "a254442cdf5d684712578b630c2e0d7543518ab154ef2341cabb607572ce7230",
    ),
    "email-euall": Dataset(
        "email-EuAll.txt.gz",
        "https://snap.stanford.edu/data/email-EuAll.txt.gz",
        420_045,
        265_214,
        1_089,
        "c256f8be57084fe7b2dbe96f99d4d79e56c19228773526058abc99a6fa86e9d9",
    ),
    "soc-epinions1": Dataset(
        "soc-Epinions1.txt.gz",
        "https://snap.stanford.edu/data/soc-Epinions1.txt.gz",
        508_837,
        75_879,
        0,
        "69a2dab71fa5e3a0715487599fc16ca17ddc847379325a6c765bbad6e3e36938",
    ),
    "soc-sign-epinions": Dataset(
        "soc-sign-epinions.txt.gz",
        "https://snap.stanford.edu/data/soc-sign-epinions.txt.gz",
        841_372,
        131_828,
        573,
        "214513a32f1375695ceab7d7581e463ebe44daa573492de699b0c5d1cf3dde60",
        columns=3,
    ),
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def download(dataset: Dataset, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    partial = path.with_suffix(path.suffix + ".part")
    urllib.request.urlretrieve(dataset.url, partial)
    partial.replace(path)


def scan(dataset: Dataset, path: Path) -> dict[str, object]:
    nodes: set[int] = set()
    rows = 0
    self_loops = 0
    signs: set[int] = set()
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip() or line.startswith(("#", "%")):
                continue
            parts = line.split()
            if len(parts) < dataset.columns:
                raise ValueError(f"short row in {path}: {line!r}")
            source, target = int(parts[0]), int(parts[1])
            nodes.update((source, target))
            rows += 1
            self_loops += source == target
            if dataset.columns == 3:
                signs.add(int(parts[2]))

    result = {
        "file": dataset.filename,
        "sha256": sha256(path),
        "rows": rows,
        "nodes": len(nodes),
        "self_loops": self_loops,
        "signs": sorted(signs),
    }
    expected = {
        "sha256": dataset.sha256,
        "rows": dataset.rows,
        "nodes": dataset.nodes,
        "self_loops": dataset.self_loops,
    }
    for field, value in expected.items():
        if result[field] != value:
            raise AssertionError(
                f"{dataset.filename}: {field}={result[field]!r}, expected {value!r}"
            )
    if dataset.columns == 3 and signs != {-1, 1}:
        raise AssertionError(f"{dataset.filename}: unexpected signs {sorted(signs)}")
    return result


def graph_smoke_test(name: str, path: Path) -> dict[str, object]:
    if name == "wiki-vote":
        graph = nx.read_edgelist(
            path, comments="#", nodetype=int, create_using=nx.DiGraph
        )
        assert sum(dict(graph.in_degree()).values()) == graph.number_of_edges()
        assert sum(dict(graph.out_degree()).values()) == graph.number_of_edges()
        largest_wcc = max(nx.weakly_connected_components(graph), key=len)
        return {"stored_edges": graph.number_of_edges(), "largest_wcc": len(largest_wcc)}
    if name == "ca-grqc":
        graph = nx.read_edgelist(path, comments="#", nodetype=int, create_using=nx.Graph)
        graph.remove_edges_from(nx.selfloop_edges(graph))
        assert graph.number_of_nodes() == 5_242
        assert graph.number_of_edges() == 14_484
        assert sum(dict(graph.degree()).values()) == 2 * graph.number_of_edges()
        return {"stored_edges": graph.number_of_edges(), "components": nx.number_connected_components(graph)}
    if name == "soc-epinions1":
        graph = nx.read_edgelist(
            path, comments="#", nodetype=int, create_using=nx.DiGraph
        )
        assert graph.number_of_nodes() == 75_879
        assert graph.number_of_edges() == 508_837
        assert sum(dict(graph.in_degree()).values()) == graph.number_of_edges()
        assert sum(dict(graph.out_degree()).values()) == graph.number_of_edges()
        largest_wcc = max(nx.weakly_connected_components(graph), key=len)
        largest_scc = max(nx.strongly_connected_components(graph), key=len)
        return {
            "stored_edges": graph.number_of_edges(),
            "largest_wcc": len(largest_wcc),
            "largest_scc": len(largest_scc),
        }
    return {"streaming_only": True}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR)
    parser.add_argument("--dataset", choices=["all", *DATASETS], default="all")
    parser.add_argument("--download", action="store_true")
    parser.add_argument("--manifest", type=Path)
    args = parser.parse_args()

    names = list(DATASETS) if args.dataset == "all" else [args.dataset]
    results: dict[str, object] = {}
    for name in names:
        dataset = DATASETS[name]
        path = args.data_dir / dataset.filename
        if not path.exists():
            if not args.download:
                raise FileNotFoundError(
                    f"missing {path}; rerun with --download while the official URL is available"
                )
            download(dataset, path)
        result = scan(dataset, path)
        result["graph_smoke"] = graph_smoke_test(name, path)
        results[name] = result
        print(f"PASS {name}: rows={result['rows']} nodes={result['nodes']}")

    if args.manifest:
        args.manifest.parent.mkdir(parents=True, exist_ok=True)
        args.manifest.write_text(
            json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print(f"manifest={args.manifest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
