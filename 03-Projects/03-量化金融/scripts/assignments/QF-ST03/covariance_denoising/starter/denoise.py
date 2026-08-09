from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


def _matrix_payload(matrix: np.ndarray) -> list[list[float]]:
    return [[round(float(value), 12) for value in row] for row in matrix]


def build_denoise_summary(returns_csv: Path) -> dict[str, object]:
    frame = pd.read_csv(returns_csv)
    panel = frame.pivot(index="date", columns="asset", values="value").sort_index().dropna()
    observations, asset_count = panel.shape
    if observations <= asset_count or asset_count < 3:
        raise ValueError("RMT denoising requires T > N and at least three assets")

    covariance = panel.cov().to_numpy()
    standard_deviation = np.sqrt(np.diag(covariance))
    correlation = covariance / np.outer(standard_deviation, standard_deviation)
    correlation = np.clip(correlation, -1.0, 1.0)

    eigenvalues, eigenvectors = np.linalg.eigh(correlation)
    aspect_ratio = observations / asset_count
    lambda_plus = (1.0 + np.sqrt(1.0 / aspect_ratio)) ** 2
    noise_mask = eigenvalues <= lambda_plus
    cleaned_eigenvalues = eigenvalues.copy()
    if np.any(noise_mask):
        cleaned_eigenvalues[noise_mask] = float(eigenvalues[noise_mask].mean())

    cleaned_correlation = eigenvectors @ np.diag(cleaned_eigenvalues) @ eigenvectors.T
    normalizer = np.sqrt(np.diag(cleaned_correlation))
    cleaned_correlation = cleaned_correlation / np.outer(normalizer, normalizer)
    cleaned_covariance = cleaned_correlation * np.outer(standard_deviation, standard_deviation)

    return {
        "method": "marchenko_pastur_eigenvalue_clipping",
        "observations": observations,
        "assets": panel.columns.tolist(),
        "aspect_ratio_t_over_n": round(float(aspect_ratio), 8),
        "lambda_plus": round(float(lambda_plus), 8),
        "signal_eigenvalues": int((~noise_mask).sum()),
        "raw_min_eigenvalue": round(float(np.linalg.eigvalsh(covariance).min()), 12),
        "denoised_min_eigenvalue": round(float(np.linalg.eigvalsh(cleaned_covariance).min()), 12),
        "raw_covariance": _matrix_payload(covariance),
        "denoised_covariance": _matrix_payload(cleaned_covariance),
    }
