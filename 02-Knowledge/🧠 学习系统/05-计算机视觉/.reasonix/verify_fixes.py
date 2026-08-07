"""Verify frontmatter fixes for 05-计算机视觉."""
import os

BASE = r"F:\-\02-Knowledge\🧠 学习系统\05-计算机视觉"
SKIP = {'.归档', '.reasonix', '.pytest_cache', '__pycache__'}

study_files = []
for root, dirs, files in os.walk(BASE):
    dirs[:] = [d for d in dirs if d not in SKIP]
    for f in files:
        if f.endswith('.md'):
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8') as fh:
                content = fh.read()
            if '\ntype: study\n' in content or content.startswith('---\ntype: study\n'):
                has_sm = 'stage_moc:' in content
                has_ds = '\ndownstream:' in content
                study_files.append((path, has_sm, has_ds))

print(f'Total study cards: {len(study_files)}')
no_sm = [p for p, sm, _ in study_files if not sm]
has_ds = [p for p, _, ds in study_files if ds]
print(f'Missing stage_moc: {len(no_sm)}')
for p in no_sm:
    print(f'  FAIL: {os.path.relpath(p, BASE)}')
print(f'Has static downstream: {len(has_ds)}')
for p in has_ds:
    print(f'  FAIL: {os.path.relpath(p, BASE)}')

if len(no_sm) == 0 and len(has_ds) == 0:
    print('\nALL CHECKS PASSED')
else:
    print(f'\nFAILURES: {len(no_sm) + len(has_ds)}')
    exit(1)
