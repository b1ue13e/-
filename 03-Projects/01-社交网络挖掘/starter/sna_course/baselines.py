from __future__ import annotations

import math
import random

import networkx as nx

from .split import Pair


def training_graph(edges: tuple[Pair, ...]) -> nx.Graph:
    graph = nx.Graph()
    graph.add_edges_from(edges)
    return graph


def score_pairs(
    graph: nx.Graph,
    pairs: list[Pair],
    seed: int = 42,
) -> dict[str, list[float]]:
    rng = random.Random(seed)
    scores = {
        "random": [],
        "preferential_attachment": [],
        "common_neighbors": [],
        "jaccard": [],
        "adamic_adar": [],
    }
    for source, target in pairs:
        source_neighbors = set(graph.neighbors(source))
        target_neighbors = set(graph.neighbors(target))
        common = source_neighbors.intersection(target_neighbors)
        union = source_neighbors.union(target_neighbors)
        scores["random"].append(rng.random())
        scores["preferential_attachment"].append(
            float(graph.degree(source) * graph.degree(target))
        )
        scores["common_neighbors"].append(float(len(common)))
        scores["jaccard"].append(float(len(common) / len(union)) if union else 0.0)
        scores["adamic_adar"].append(
            float(sum(1.0 / math.log(graph.degree(node)) for node in common))
        )
    return scores

