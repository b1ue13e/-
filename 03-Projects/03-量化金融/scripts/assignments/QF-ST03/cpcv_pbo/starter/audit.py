from __future__ import annotations

import itertools
import math
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd


def _sharpe(values: np.ndarray) -> float:
    deviation = float(values.std(ddof=1))
    return float(values.mean() / deviation) if deviation > 0 else 0.0


def build_audit_summary(
    strategy_csv: Path, parameter_csv: Path, block_count: int = 6
) -> dict[str, object]:
    strategy_frame = pd.read_csv(strategy_csv)
    parameter_frame = pd.read_csv(parameter_csv)
    panel = strategy_frame.pivot(index="date", columns="strategy", values="value").sort_index().dropna()
    if block_count < 4 or block_count % 2:
        raise ValueError("block_count must be even and at least four")
    if panel.shape[0] < block_count * 2 or panel.shape[1] < 3:
        raise ValueError("PBO smoke input requires at least two rows per block and three strategies")
    if set(parameter_frame["strategy"]) != set(panel.columns):
        raise ValueError("parameter grid and strategy-return columns must identify the same strategies")

    blocks = [np.asarray(block, dtype=int) for block in np.array_split(np.arange(panel.shape[0]), block_count)]
    logits: list[float] = []
    selected: Counter[str] = Counter()
    for train_blocks in itertools.combinations(range(block_count), block_count // 2):
        train_set = set(train_blocks)
        test_blocks = [index for index in range(block_count) if index not in train_set]
        train_indices = np.concatenate([blocks[index] for index in train_blocks])
        test_indices = np.concatenate([blocks[index] for index in test_blocks])

        train_scores = {
            strategy: _sharpe(panel[strategy].to_numpy()[train_indices]) for strategy in panel.columns
        }
        winner = max(train_scores, key=train_scores.get)
        selected[winner] += 1
        test_scores = {
            strategy: _sharpe(panel[strategy].to_numpy()[test_indices]) for strategy in panel.columns
        }
        ordered = sorted(test_scores, key=test_scores.get)
        rank = ordered.index(winner) + 1
        relative_rank = (rank - 0.5) / len(ordered)
        logits.append(math.log(relative_rank / (1.0 - relative_rank)))

    pbo = sum(logit <= 0 for logit in logits) / len(logits)
    return {
        "method": "combinatorial_symmetric_cross_validation_pbo",
        "observations": int(panel.shape[0]),
        "strategies": panel.columns.tolist(),
        "block_count": block_count,
        "combinations": len(logits),
        "pbo": round(float(pbo), 8),
        "rank_logits": [round(float(value), 8) for value in logits],
        "selected_frequency": dict(sorted(selected.items())),
    }
