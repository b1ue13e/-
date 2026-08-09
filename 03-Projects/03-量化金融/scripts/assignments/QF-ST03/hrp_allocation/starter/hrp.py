from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import leaves_list, linkage
from scipy.spatial.distance import squareform


def _cluster_variance(covariance: pd.DataFrame, assets: list[str]) -> float:
    submatrix = covariance.loc[assets, assets]
    inverse_diagonal = 1.0 / np.diag(submatrix.to_numpy())
    weights = inverse_diagonal / inverse_diagonal.sum()
    return float(weights @ submatrix.to_numpy() @ weights)


def _recursive_bisection(covariance: pd.DataFrame, ordered_assets: list[str]) -> pd.Series:
    weights = pd.Series(1.0, index=ordered_assets, dtype=float)
    clusters = [ordered_assets]
    while clusters:
        next_clusters: list[list[str]] = []
        for cluster in clusters:
            if len(cluster) <= 1:
                continue
            midpoint = len(cluster) // 2
            left, right = cluster[:midpoint], cluster[midpoint:]
            left_variance = _cluster_variance(covariance, left)
            right_variance = _cluster_variance(covariance, right)
            alpha = 1.0 - left_variance / (left_variance + right_variance)
            weights[left] *= alpha
            weights[right] *= 1.0 - alpha
            next_clusters.extend([left, right])
        clusters = next_clusters
    return weights / weights.sum()


def build_hrp_summary(returns_csv: Path) -> dict[str, object]:
    frame = pd.read_csv(returns_csv)
    panel = frame.pivot(index="date", columns="asset", values="value").sort_index().dropna()
    if panel.shape[0] < 8 or panel.shape[1] < 3:
        raise ValueError("HRP smoke input requires at least 8 rows and 3 complete assets")

    covariance = panel.cov()
    correlation = panel.corr().clip(-1.0, 1.0)
    distance = np.sqrt(np.maximum((1.0 - correlation.to_numpy()) / 2.0, 0.0))
    hierarchy = linkage(squareform(distance, checks=False), method="single")
    ordered_assets = correlation.index[leaves_list(hierarchy)].tolist()
    weights = _recursive_bisection(covariance, ordered_assets)

    return {
        "method": "hierarchical_risk_parity",
        "observations": int(panel.shape[0]),
        "assets": panel.columns.tolist(),
        "cluster_order": ordered_assets,
        "weights": {asset: round(float(weights[asset]), 10) for asset in ordered_assets},
        "weight_sum": round(float(weights.sum()), 10),
        "portfolio_variance": round(float(weights @ covariance.loc[ordered_assets, ordered_assets] @ weights), 12),
    }
