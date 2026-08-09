from __future__ import annotations

import json
from pathlib import Path


def package_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_manifest() -> dict:
    return json.loads((package_root() / "package_manifest.json").read_text(encoding="utf-8"))
