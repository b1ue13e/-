#!/usr/bin/env python3
"""Run an end-to-end spectral smoke test on the authors' Polblogs dataset."""

from __future__ import annotations

import argparse
import hashlib
import json
import urllib.request
import zipfile
from pathlib import Path

import networkx as nx
import numpy as np
from scipy.sparse import diags, eye
from scipy.sparse.linalg import LinearOperator, eigsh


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DIR = ROOT / "99-System" / ".tmp" / "social-network-course-audit" / "data"
URL = "https://public.websites.umich.edu/~mejn/netdata/polblogs.zip"
ZIP_SHA256 = "e047df21736fef9037f0450f7d3756ecb16a8e347417723181c0f7e493021ddb"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def obtain(data_dir: Path, allow_download: bool) -> tuple[Path, Path]:
    archive = data_dir / "polblogs.zip"
    if not archive.exists():
        if not allow_download:
            raise FileNotFoundError(f"missing {archive}; rerun with --download")
        data_dir.mkdir(parents=True, exist_ok=True)
        partial = archive.with_suffix(".zip.part")
        urllib.request.urlretrieve(URL, partial)
        partial.replace(archive)
    if sha256(archive) != ZIP_SHA256:
        raise AssertionError("polblogs.zip SHA-256 mismatch")

    extracted = data_dir / "polblogs-original"
    extracted.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive) as bundle:
        for name in ("polblogs.gml", "polblogs.txt"):
            target = extracted / name
            if not target.exists():
                target.write_bytes(bundle.read(name))
    return archive, extracted / "polblogs.gml"


def load_polblogs(path: Path) -> tuple[nx.Graph, dict[int, int], dict[str, int]]:
    # The original GML declares a DiGraph but contains duplicate arcs. Parse it as
    # a MultiDiGraph, then apply the assignment's undirected-simple projection.
    text = path.read_text(encoding="utf-8")
    text = text.replace("  directed 1\n", "  directed 1\n  multigraph 1\n", 1)
    raw = nx.parse_gml(text.splitlines(), label=None)
    graph = nx.Graph()
    graph.add_nodes_from(raw.nodes(data=True))
    graph.add_edges_from((u, v) for u, v in raw.edges() if u != v)
    largest = max(nx.connected_components(graph), key=len)
    graph = graph.subgraph(largest).copy()
    labels = {int(node): int(data["value"]) for node, data in graph.nodes(data=True)}
    metadata = {
        "raw_nodes": raw.number_of_nodes(),
        "raw_arcs": raw.number_of_edges(),
        "component_nodes": graph.number_of_nodes(),
        "component_edges": graph.number_of_edges(),
    }
    if metadata != {
        "raw_nodes": 1490,
        "raw_arcs": 19090,
        "component_nodes": 1222,
        "component_edges": 16714,
    }:
        raise AssertionError(f"unexpected Polblogs metadata: {metadata}")
    if set(labels.values()) != {0, 1} or set(labels) != set(graph):
        raise AssertionError("Polblogs label alignment failed")
    return graph, labels, metadata


def purity(prediction: np.ndarray, truth: np.ndarray) -> float:
    return sum(
        np.bincount(truth[prediction == cluster], minlength=2).max()
        for cluster in (0, 1)
    ) / len(truth)


def spectral_smoke(graph: nx.Graph, labels: dict[int, int]) -> dict[str, object]:
    nodes = sorted(graph)
    adjacency = nx.to_scipy_sparse_array(
        graph, nodelist=nodes, dtype=float, format="csr"
    )
    degree = np.asarray(adjacency.sum(axis=1)).ravel()
    if np.any(degree == 0):
        raise AssertionError("largest Polblogs component contains an isolate")

    inverse_sqrt = diags(1.0 / np.sqrt(degree))
    normalized = eye(len(nodes), format="csr") - inverse_sqrt @ adjacency @ inverse_sqrt
    ncut_values, ncut_vectors = eigsh(normalized, k=2, which="SM", tol=1e-8)
    order = np.argsort(ncut_values)
    ncut_vector = ncut_vectors[:, order[1]]
    ncut_prediction = (ncut_vector >= 0).astype(int)

    volume = degree.sum()
    def modularity_matvec(vector: np.ndarray) -> np.ndarray:
        return adjacency @ vector - degree * (degree @ vector) / volume

    modularity = LinearOperator(
        shape=(len(nodes), len(nodes)), matvec=modularity_matvec, dtype=float
    )
    mod_values, mod_vectors = eigsh(modularity, k=1, which="LA", tol=1e-8)
    mod_prediction = (mod_vectors[:, 0] >= 0).astype(int)
    truth = np.array([labels[node] for node in nodes], dtype=int)

    for prediction in (ncut_prediction, mod_prediction):
        if len(np.unique(prediction)) != 2:
            raise AssertionError("spectral rounding produced an empty cluster")
    ncut_residual = np.linalg.norm(normalized @ ncut_vector - ncut_values[order[1]] * ncut_vector)
    mod_vector = mod_vectors[:, 0]
    mod_residual = np.linalg.norm(modularity @ mod_vector - mod_values[0] * mod_vector)
    if ncut_residual > 1e-5 or mod_residual > 1e-5:
        raise AssertionError("eigenpair residual too large")

    return {
        "ncut": {
            "sizes": np.bincount(ncut_prediction, minlength=2).tolist(),
            "purity": purity(ncut_prediction, truth),
            "eigen_residual": float(ncut_residual),
        },
        "modularity": {
            "sizes": np.bincount(mod_prediction, minlength=2).tolist(),
            "purity": purity(mod_prediction, truth),
            "eigen_residual": float(mod_residual),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DIR)
    parser.add_argument("--download", action="store_true")
    parser.add_argument("--manifest", type=Path)
    args = parser.parse_args()
    archive, gml = obtain(args.data_dir, args.download)
    graph, labels, metadata = load_polblogs(gml)
    result = {
        "source": URL,
        "archive_sha256": sha256(archive),
        "metadata": metadata,
        "spectral": spectral_smoke(graph, labels),
    }
    if args.manifest:
        args.manifest.parent.mkdir(parents=True, exist_ok=True)
        args.manifest.write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    print(
        "PASS polblogs: "
        f"nodes={metadata['component_nodes']} edges={metadata['component_edges']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
