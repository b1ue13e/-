"""Quick verification: check a few cards have proper query blocks."""
import os, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE = r"F:\-\02-Knowledge\🧠 学习系统\05-计算机视觉"

# Check MLP.md
path = os.path.join(BASE, "02-深度学习内核", "MLP.md")
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

checks = ["contains(upstream, this.file.link)", "contains(requires, this.file.link)"]
for check in checks:
    status = "[OK]" if check in content else "[MISSING]"
    print(f"  {status} {check}")

# Quick count across all study cards
count = 0
for root, dirs, files in os.walk(BASE):
    dirs[:] = [d for d in dirs if d not in {'.归档','.reasonix','.pytest_cache'}]
    for f in files:
        if f.endswith('.md'):
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8') as fh:
                c = fh.read()
            if 'type: study' in c:
                if 'contains(upstream, this.file.link)' in c:
                    count += 1
print(f"\nTotal study cards with query blocks: {count}")
