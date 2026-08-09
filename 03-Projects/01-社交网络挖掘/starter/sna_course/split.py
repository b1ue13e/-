from __future__ import annotations

import random
from dataclasses import dataclass

from .data_contract import TemporalEdge


Pair = tuple[int, int]


@dataclass(frozen=True)
class TemporalSplit:
    train_cutoff: int
    validation_cutoff: int
    train_edges: tuple[Pair, ...]
    validation_positive: tuple[Pair, ...]
    test_positive: tuple[Pair, ...]
    validation_negative: tuple[Pair, ...]
    test_negative: tuple[Pair, ...]


def _canonical_pair(source: int, target: int, directed: bool) -> Pair:
    return (source, target) if directed else (min(source, target), max(source, target))


def _first_occurrences(events: list[TemporalEdge], directed: bool) -> list[TemporalEdge]:
    first: dict[Pair, TemporalEdge] = {}
    for event in events:
        pair = _canonical_pair(event.source, event.target, directed)
        first.setdefault(
            pair,
            TemporalEdge(event.timestamp, pair[0], pair[1]),
        )
    return sorted(first.values())


def _sample_negative_pairs(
    nodes: list[int],
    forbidden: set[Pair],
    count: int,
    seed: int,
    directed: bool,
) -> tuple[Pair, ...]:
    rng = random.Random(seed)
    selected: set[Pair] = set()
    max_candidates = len(nodes) * max(len(nodes) - 1, 0)
    if not directed:
        max_candidates //= 2
    if max_candidates - len(forbidden) < count:
        raise ValueError("candidate space is too small for the requested negatives")

    attempts = 0
    max_attempts = max(10_000, count * 100)
    while len(selected) < count and attempts < max_attempts:
        source, target = rng.sample(nodes, 2)
        pair = _canonical_pair(source, target, directed)
        if pair not in forbidden:
            selected.add(pair)
        attempts += 1
    if len(selected) != count:
        raise RuntimeError("negative sampling did not converge within the attempt limit")
    return tuple(sorted(selected))


def temporal_link_split(
    events: list[TemporalEdge],
    train_fraction: float = 0.6,
    validation_fraction: float = 0.2,
    seed: int = 42,
    directed: bool = True,
) -> TemporalSplit:
    if not 0 < train_fraction < 1:
        raise ValueError("train_fraction must be between 0 and 1")
    if not 0 < validation_fraction < 1 - train_fraction:
        raise ValueError("validation_fraction leaves no test interval")

    first_events = _first_occurrences(events, directed)
    if len(first_events) < 10:
        raise ValueError("at least 10 first-time links are required")

    train_index = max(1, int(len(first_events) * train_fraction)) - 1
    validation_index = max(
        train_index + 1,
        int(len(first_events) * (train_fraction + validation_fraction)) - 1,
    )
    validation_index = min(validation_index, len(first_events) - 2)
    train_cutoff = first_events[train_index].timestamp
    validation_cutoff = first_events[validation_index].timestamp

    train = {
        (event.source, event.target)
        for event in first_events
        if event.timestamp <= train_cutoff
    }
    train_nodes = sorted({node for edge in train for node in edge})
    validation = {
        (event.source, event.target)
        for event in first_events
        if train_cutoff < event.timestamp <= validation_cutoff
        and event.source in train_nodes
        and event.target in train_nodes
    }
    test = {
        (event.source, event.target)
        for event in first_events
        if event.timestamp > validation_cutoff
        and event.source in train_nodes
        and event.target in train_nodes
    }
    if not validation or not test:
        raise ValueError("closed-world validation/test positives are empty")

    observed = {(event.source, event.target) for event in first_events}
    validation_negative = _sample_negative_pairs(
        train_nodes, observed, len(validation), seed, directed
    )
    test_negative = _sample_negative_pairs(
        train_nodes,
        observed.union(validation_negative),
        len(test),
        seed + 1,
        directed,
    )

    assert train.isdisjoint(validation | test)
    assert validation.isdisjoint(test)
    assert set(validation_negative).isdisjoint(observed)
    assert set(test_negative).isdisjoint(observed)

    return TemporalSplit(
        train_cutoff=train_cutoff,
        validation_cutoff=validation_cutoff,
        train_edges=tuple(sorted(train)),
        validation_positive=tuple(sorted(validation)),
        test_positive=tuple(sorted(test)),
        validation_negative=validation_negative,
        test_negative=test_negative,
    )
