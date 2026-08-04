from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from dataset import TEST_FEATURES, TRAIN_FEATURES, TRAIN_LABELS, validate_official_contract


DRIVE_FILE_ID = "1HPkcmQmFGu-3OknddKIa5dNDsR05lIQR"
DOWNLOAD_URL = (
    "https://drive.usercontent.google.com/download"
    f"?id={DRIVE_FILE_ID}&export=download&confirm=t"
)
EXPECTED_ARCHIVE_BYTES = 372_407_869


def default_data_root() -> Path:
    return Path(__file__).resolve().parents[3] / "data" / "ml_hw02"


def request_source() -> urllib.request.Request:
    return urllib.request.Request(DOWNLOAD_URL, headers={"User-Agent": "Mozilla/5.0"})


def check_source() -> int | None:
    request = request_source()
    request.method = "HEAD"
    with urllib.request.urlopen(request, timeout=60) as response:
        size = response.headers.get("Content-Length")
        disposition = response.headers.get("Content-Disposition", "")
        print(f"SOURCE status={response.status} bytes={size or 'unknown'} {disposition}")
        return int(size) if size else None


def download_archive(destination: Path) -> tuple[int, str]:
    destination.parent.mkdir(parents=True, exist_ok=True)
    partial = destination.with_suffix(destination.suffix + ".part")
    digest = hashlib.sha256()
    downloaded = 0

    with urllib.request.urlopen(request_source(), timeout=120) as response, partial.open("wb") as handle:
        total = int(response.headers.get("Content-Length", "0"))
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            handle.write(chunk)
            digest.update(chunk)
            downloaded += len(chunk)
            if total:
                print(f"\rDownloading: {downloaded / 1024**2:.1f}/{total / 1024**2:.1f} MiB", end="")
        print()

    if downloaded < 100_000_000:
        partial.unlink(missing_ok=True)
        raise RuntimeError(f"Downloaded file is unexpectedly small: {downloaded} bytes")
    partial.replace(destination)
    return downloaded, digest.hexdigest()


def safe_extract(archive: Path, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    base = destination.resolve()
    with zipfile.ZipFile(archive) as bundle:
        bad_member = bundle.testzip()
        if bad_member:
            raise RuntimeError(f"Corrupt ZIP member: {bad_member}")
        for member in bundle.infolist():
            target = (destination / member.filename).resolve()
            if target != base and base not in target.parents:
                raise RuntimeError(f"Unsafe ZIP path: {member.filename}")
        bundle.extractall(destination)


def locate_data_dir(root: Path) -> Path:
    expected = {TRAIN_FEATURES, TRAIN_LABELS, TEST_FEATURES}
    candidates = [root, root / "timit_11", *[path for path in root.rglob("*") if path.is_dir()]]
    for candidate in candidates:
        if expected.issubset({path.name for path in candidate.glob("*.npy")}):
            return candidate
    raise FileNotFoundError(f"Could not find {sorted(expected)} below {root}")


def validate_data(data_dir: Path) -> dict[str, object]:
    train = np.load(data_dir / TRAIN_FEATURES, mmap_mode="r", allow_pickle=False)
    labels = np.load(data_dir / TRAIN_LABELS, mmap_mode="r", allow_pickle=False)
    test = np.load(data_dir / TEST_FEATURES, mmap_mode="r", allow_pickle=False)
    validate_official_contract(train, labels)
    validate_official_contract(test)
    if len(train) != len(labels):
        raise ValueError("Official feature and label row counts differ")
    return {
        TRAIN_FEATURES: {"shape": list(train.shape), "dtype": str(train.dtype)},
        TRAIN_LABELS: {"shape": list(labels.shape), "dtype": str(labels.dtype)},
        TEST_FEATURES: {"shape": list(test.shape), "dtype": str(test.dtype)},
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download and validate the official ML2021 HW02 arrays.")
    parser.add_argument("--data-root", type=Path, default=default_data_root())
    parser.add_argument("--check-only", action="store_true", help="Verify the remote file without downloading it.")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--keep-archive", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.check_only:
        size = check_source()
        if size is not None and size != EXPECTED_ARCHIVE_BYTES:
            raise RuntimeError(f"Remote archive size changed: {size} != {EXPECTED_ARCHIVE_BYTES}")
        return

    data_root = args.data_root.resolve()
    archive = data_root / "timit_11_v2.zip"
    if args.force and data_root.exists():
        shutil.rmtree(data_root)
    data_root.mkdir(parents=True, exist_ok=True)

    try:
        existing = locate_data_dir(data_root)
    except FileNotFoundError:
        existing = None
    if existing is not None:
        shapes = validate_data(existing)
        print(f"READY existing data at {existing}")
        print(json.dumps(shapes, ensure_ascii=False, indent=2))
        return

    size, sha256 = download_archive(archive)
    safe_extract(archive, data_root)
    data_dir = locate_data_dir(data_root)
    shapes = validate_data(data_dir)
    manifest = {
        "source": "李宏毅 ML2021 HW02 official notebook",
        "source_url": "https://github.com/ga642381/ML2021-Spring/tree/main/HW02",
        "download_url": DOWNLOAD_URL,
        "google_drive_file_id": DRIVE_FILE_ID,
        "downloaded_at": datetime.now(timezone.utc).isoformat(),
        "archive_bytes": size,
        "archive_sha256": sha256,
        "files": shapes,
        "redistribution": "link-only; do not commit the TIMIT-derived arrays",
    }
    (data_root / "source_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    if not args.keep_archive:
        archive.unlink(missing_ok=True)
    print(f"READY official data at {data_dir}")
    print(json.dumps(shapes, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise
