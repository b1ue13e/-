from __future__ import annotations

import json
import platform
from pathlib import Path

import numpy as np
import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[3]
PROJECT_ROOT = REPO_ROOT / "03-Projects" / "02-时间序列分析"
OUTPUT_ROOT = PROJECT_ROOT / "artifacts" / "homework-fixtures"
SEED = 20260807


def build_hw00() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "record_id": ["r01", "r02", "r03", "r04", "r05", "r06"],
            "date": ["2025-01-01", "2025-03-01", "2025-02-01", "2025-02-01", "2025-04-01", "2025-07-01"],
            "value": [12.0, 0.0, 14.0, 15.0, np.nan, 19.0],
            "published_at": ["2025-01-05", "2025-03-04", "2025-02-20", "2025-02-21", "2025-04-05", "2025-09-01"],
        }
    )


def build_hw01(random: np.random.Generator) -> pd.DataFrame:
    size = 160
    noise = random.normal(size=(size, 4))
    stationary = np.zeros(size)
    for index in range(1, size):
        stationary[index] = 0.55 * stationary[index - 1] + noise[index, 0]
    random_walk = np.cumsum(noise[:, 1])
    trend_stationary = 20 + 0.12 * np.arange(size) + noise[:, 2]
    changing_scale = np.exp(2.6 + 0.006 * np.arange(size) + 0.22 * noise[:, 3])
    return pd.DataFrame(
        {
            "timestamp": pd.date_range("2010-01-01", periods=size, freq="MS"),
            "series_a": stationary,
            "series_b": random_walk,
            "series_c": trend_stationary,
            "series_d": changing_scale,
        }
    )


def build_hw05(random: np.random.Generator) -> pd.DataFrame:
    size = 144
    time = np.arange(size)
    innovation = random.normal(0, 1.4, size)
    short_memory = np.zeros(size)
    for index in range(1, size):
        short_memory[index] = 0.45 * short_memory[index - 1] + innovation[index]
    value = 100 + 0.15 * time + 8 * np.sin(2 * np.pi * time / 12) + 3 * np.cos(2 * np.pi * time / 12) + short_memory
    return pd.DataFrame({"timestamp": pd.date_range("2010-01-01", periods=size, freq="MS"), "value": value})


def build_hw06(random: np.random.Generator) -> pd.DataFrame:
    burn_in = 200
    size = 240
    innovation = random.normal(size=burn_in + size)
    centered = np.zeros(burn_in + size)
    for index in range(2, len(centered)):
        centered[index] = 0.65 * centered[index - 1] - 0.20 * centered[index - 2] + innovation[index]
    return pd.DataFrame(
        {
            "timestamp": pd.date_range("2000-01-01", periods=size, freq="MS"),
            "value": 20 + centered[-size:],
        }
    )


def main() -> int:
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    random = np.random.default_rng(SEED)
    fixtures = {
        "hw00_observations.csv": build_hw00(),
        "hw01_structure_series.csv": build_hw01(random),
        "hw05_monthly_series.csv": build_hw05(random),
        "hw06_diagnostic_series.csv": build_hw06(random),
    }
    manifest = {
        "generated_at": "2026-08-07",
        "seed": SEED,
        "python": platform.python_version(),
        "command": "python scripts/build_lesson_homework_fixtures.py",
        "policy": "Synthetic inputs only; no answers, fitted models, or grading outputs are generated.",
        "files": {},
    }
    for name, frame in fixtures.items():
        frame.to_csv(OUTPUT_ROOT / name, index=False)
        manifest["files"][name] = {"rows": len(frame), "columns": list(frame.columns)}
    (OUTPUT_ROOT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output_root": str(OUTPUT_ROOT), "files": len(fixtures), "seed": SEED}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
