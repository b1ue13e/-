#!/usr/bin/env python3
"""
Comprehensive frontmatter fix for 05-计算机视觉 knowledge cards.
Fixes per AGENTS.md rules:
  1. Add stage_moc to all type=study cards
  2. Remove static downstream from all study cards
  3. Remove stage MOC entries from upstream (keep only direct knowledge prereqs)
  4. Remove redundant assessment_exempt: false (it's the default)
  5. Normalize line endings to LF

Run: python .reasonix/fix_frontmatter.py --dry-run  (preview only)
Run: python .reasonix/fix_frontmatter.py           (apply fixes)
"""
import os
import re
import sys

BASE = r"F:\-\02-Knowledge\🧠 学习系统\05-计算机视觉"
SKIP_DIRS = {'.归档', '.reasonix', '.pytest_cache', '__pycache__', '.git'}

# Stage MOC mapping: directory -> stage_moc wikilink
STAGE_MOC_MAP = {
    "01-底层基石": "[[01-底层基石/🏗️ 第一阶段：底层基石]]",
    "02-深度学习内核": "[[02-深度学习内核/🧠 第二阶段：深度学习内核]]",
    "03-视觉核心任务": "[[03-视觉核心任务/🎯 第三阶段：视觉核心任务]]",
    "04-前沿架构探索": "[[04-前沿架构探索/🚀 第四阶段：前沿架构探索]]",
    "05-专业深化与工程落地": "[[05-专业深化与工程落地/🏭 第五阶段：专业深化与工程落地]]",
    "00-前置知识": "[[00-前置知识/🧭 阶段0-前置知识]]",
}

# Patterns for stage MOC entries that should NOT be in upstream
STAGE_MOC_PATTERNS = [
    re.compile(r'"\[\[01-底层基石/🏗️ 第一阶段：底层基石\]\]",?\s*'),
    re.compile(r'"\[\[02-深度学习内核/🧠 第二阶段：深度学习内核\]\]",?\s*'),
    re.compile(r'"\[\[03-视觉核心任务/🎯 第三阶段：视觉核心任务\]\]",?\s*'),
    re.compile(r'"\[\[04-前沿架构探索/🚀 第四阶段：前沿架构探索\]\]",?\s*'),
    re.compile(r'"\[\[05-专业深化与工程落地/🏭 第五阶段：专业深化与工程落地\]\]",?\s*'),
]

DRY_RUN = '--dry-run' in sys.argv


def get_stage_dir(rel_path):
    """Determine which stage directory a file belongs to."""
    parts = rel_path.replace('\\', '/').split('/')
    for part in parts:
        if part in STAGE_MOC_MAP:
            return part
    return None


def fix_frontmatter(content, rel_path):
    """Fix a single file's frontmatter."""
    # Split frontmatter from body
    if not content.startswith('---'):
        return content, []

    # Find the end of frontmatter
    end_idx = content.find('---', 3)
    if end_idx == -1:
        return content, []

    fm = content[3:end_idx].strip()
    body = content[end_idx + 3:]

    # Determine if this is a study card
    is_study = bool(re.search(r'^type:\s*study\s*$', fm, re.MULTILINE))
    is_index = bool(re.search(r'^type:\s*index\s*$', fm, re.MULTILINE))

    if not is_study:
        return content, []

    changes = []
    fm_lines = fm.split('\n')

    # --- Fix 1: Add stage_moc ---
    stage_dir = get_stage_dir(rel_path)
    if stage_dir and stage_dir in STAGE_MOC_MAP:
        has_stage_moc = any('stage_moc:' in line for line in fm_lines)
        if not has_stage_moc:
            # Insert after 'flow:' line, or after 'kind:' line, or before 'tags:'
            insert_pos = len(fm_lines)
            for i, line in enumerate(fm_lines):
                if line.startswith('kind:'):
                    insert_pos = i + 1
                    break
            for i, line in enumerate(fm_lines):
                if line.startswith('flow:'):
                    insert_pos = i + 1
                    break
            fm_lines.insert(insert_pos, f'stage_moc: "{STAGE_MOC_MAP[stage_dir]}"')
            changes.append(f"  + stage_moc: {STAGE_MOC_MAP[stage_dir]}")

    # --- Fix 2: Remove static downstream ---
    new_lines = []
    removed_downstream = False
    skip_next_empty = False
    for i, line in enumerate(fm_lines):
        if line.startswith('downstream:'):
            removed_downstream = True
            changes.append("  - downstream (static, removed)")
            skip_next_empty = True
            continue
        if skip_next_empty and line.strip() == '':
            skip_next_empty = False
            continue
        skip_next_empty = False
        new_lines.append(line)
    fm_lines = new_lines

    # --- Fix 3: Remove stage MOC from upstream ---
    for i, line in enumerate(fm_lines):
        if line.startswith('upstream:'):
            original = line
            for pattern in STAGE_MOC_PATTERNS:
                line = pattern.sub('', line)
            # Clean up: if upstream becomes empty array, remove it
            # But for entry-point cards with only stage MOC, keep upstream empty
            # Actually per AGENTS.md: entry cards omit upstream entirely
            if line.startswith('upstream: []'):
                # This was an entry point with only stage MOC - remove upstream
                fm_lines[i] = ''
                changes.append("  - upstream (was stage MOC only, removed)")
            elif line != original:
                # Clean up trailing commas
                line = line.replace('[, ', '[').replace(', ]', ']')
                line = re.sub(r',\s*,', ',', line)
                fm_lines[i] = line
                changes.append("  ~ upstream (removed stage MOC)")

    # --- Fix 4: Remove redundant assessment_exempt: false ---
    new_lines = []
    for line in fm_lines:
        if line.strip() == 'assessment_exempt: false':
            changes.append("  - assessment_exempt: false (redundant, removed)")
            continue
        new_lines.append(line)
    fm_lines = new_lines

    # --- Fix 5: Clean up consecutive empty lines in frontmatter ---
    new_lines = []
    prev_empty = False
    for line in fm_lines:
        is_empty = line.strip() == ''
        if is_empty and prev_empty:
            continue
        prev_empty = is_empty
        new_lines.append(line)
    fm_lines = new_lines

    # Rebuild
    new_fm = '\n'.join(fm_lines).strip()
    new_content = f'---\n{new_fm}\n---{body}'

    # Normalize line endings to LF
    new_content = new_content.replace('\r\n', '\n').replace('\r', '\n')

    return new_content, changes


def main():
    # Fix Windows encoding
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

    all_files = []
    for root, dirs, files in os.walk(BASE):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            if f.endswith('.md'):
                all_files.append(os.path.join(root, f))

    print(f"{'[DRY RUN] ' if DRY_RUN else ''}Processing {len(all_files)} markdown files...\n")

    total_changes = 0
    files_changed = 0

    for path in sorted(all_files):
        rel = os.path.relpath(path, BASE)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        new_content, changes = fix_frontmatter(content, rel)

        if changes:
            files_changed += 1
            total_changes += len(changes)
            print(f"[{rel}]")
            for c in changes:
                print(c)

            if not DRY_RUN:
                with open(path, 'w', encoding='utf-8', newline='\n') as f:
                    f.write(new_content)
            print()

    print(f"{'Would change' if DRY_RUN else 'Changed'} {files_changed} files ({total_changes} edits)")


if __name__ == '__main__':
    main()
