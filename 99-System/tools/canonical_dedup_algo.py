import os
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

VAULT_ROOT = Path("F:/-")
KNOWLEDGE_DIR = VAULT_ROOT / "02-Knowledge" / "02-Knowledge/🧠 学习系统"

if not KNOWLEDGE_DIR.exists():
    KNOWLEDGE_DIR = VAULT_ROOT / "02-Knowledge/🧠 学习系统"

ALGO_DIR = KNOWLEDGE_DIR / "10-数据结构与算法"

print(f"Rule 3 Check: Scanning duplicate files in {ALGO_DIR} vs rest of vault...")

# Find all md files in 10-数据结构与算法
algo_files = {f.stem: f for f in ALGO_DIR.glob("*.md")}
print(f"Total files in 10-数据结构与算法: {len(algo_files)}")

# Check duplicates in other folders
duplicates = []
for root, dirs, files in os.walk(KNOWLEDGE_DIR):
    rel_root = Path(root).relative_to(KNOWLEDGE_DIR)
    if str(rel_root).startswith("10-数据结构与算法"):
        continue
    for f in files:
        if f.endswith(".md"):
            stem = Path(f).stem
            if stem in algo_files:
                duplicates.append((stem, str(algo_files[stem]), os.path.join(root, f)))

print(f"Found {len(duplicates)} duplicate notes across folders:")
for stem, p1, p2 in duplicates[:10]:
    print(f"- Duplicate: {stem}\n  1: {p1}\n  2: {p2}")
