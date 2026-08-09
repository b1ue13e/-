from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
import urllib.request
from pathlib import Path


DATASET_URL = "https://sociopatterns.org/assets/data/HighSchool2013_proximity_net.csv.gz"
DATASET_PAGE = "https://sociopatterns.org/datasets"
EXPECTED_SHA256 = "ecf4a90312c8d72057f72e936c366b470e63876da7db846300044795f045e2ea"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fetch_public_network(output: Path) -> dict[str, object]:
    output.mkdir(parents=True, exist_ok=True)
    raw_path = output / "HighSchool2013_proximity_net.csv.gz"
    urllib.request.urlretrieve(DATASET_URL, raw_path)
    actual_hash = _sha256(raw_path)
    if actual_hash != EXPECTED_SHA256:
        raise ValueError(
            f"dataset hash mismatch: expected {EXPECTED_SHA256}, got {actual_hash}"
        )

    events: list[tuple[int, int, int]] = []
    node_classes: dict[int, str] = {}
    with gzip.open(raw_path, "rt", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            parts = line.split()
            if len(parts) != 5:
                raise ValueError(f"invalid row {line_number}: expected 5 fields")
            timestamp, source, target = map(int, parts[:3])
            source_class, target_class = parts[3:]
            events.append((timestamp, source, target))
            node_classes.setdefault(source, source_class)
            node_classes.setdefault(target, target_class)
            if node_classes[source] != source_class or node_classes[target] != target_class:
                raise ValueError(f"inconsistent class metadata at row {line_number}")

    events.sort()
    with (output / "temporal_edges.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["timestamp", "source", "target"])
        writer.writerows(events)
    with (output / "node_attributes.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["node", "class"])
        writer.writerows(sorted(node_classes.items()))

    manifest: dict[str, object] = {
        "schema_version": 1,
        "dataset": "SocioPatterns High School 2013 proximity network",
        "source_url": DATASET_URL,
        "source_page": DATASET_PAGE,
        "download_sha256": actual_hash,
        "license": "CC BY-NC-SA 3.0",
        "citation": "R. Mastrandrea et al., PLoS ONE 10(9), e0136497 (2015)",
        "event_rows": len(events),
        "node_count": len(node_classes),
        "graph_semantics": "undirected face-to-face contacts observed in 20-second windows",
        "privacy": "source data uses anonymous participant identifiers",
        "limitations": [
            "Contacts are proximity events, not friendship or influence claims.",
            "The five-day school deployment does not support population-level generalization.",
            "License is non-commercial and share-alike; downstream redistribution must preserve it.",
        ],
    }
    (output / "dataset_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch and normalize the required public network.")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(fetch_public_network(args.output), ensure_ascii=False))


if __name__ == "__main__":
    main()

