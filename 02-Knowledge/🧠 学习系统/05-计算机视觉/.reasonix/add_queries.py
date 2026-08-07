"""Add Dataview derived query blocks to knowledge cards.
Per AGENTS.md §2, each study card should show:
  1. Downstream cards (cards whose upstream points to this one)
  2. Completable assignments (assignments whose requires contains this card)

The queries use Dataview which renders in Obsidian. We add them
at the end of each card, before any existing query blocks.
"""
import os
import re

BASE = r"F:\-\02-Knowledge\🧠 学习系统\05-计算机视觉"
SKIP = {'.归档', '.reasonix', '.pytest_cache', '__pycache__'}

QUERY_BLOCK = """
---

## 🔗 知识图谱

```dataview
LIST
FROM "02-Knowledge/🧠 学习系统"
WHERE contains(upstream, this.file.link)
SORT file.name ASC
```

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
"""


def needs_query_block(content):
    """Check if the card already has the derivable downstream query."""
    return 'contains(upstream, this.file.link)' not in content


def add_query_block(content):
    """Add Dataview query block at end of card content."""
    # Don't add to cards that already have it
    if not needs_query_block(content):
        return content, False
    
    # Check if there's already a "学完本节后可完成的作业" section
    # If so, we still add the Dataview block for automatic derivation
    
    # Add at the end
    new_content = content.rstrip() + '\n' + QUERY_BLOCK.lstrip()
    return new_content, True


def main():
    import sys, io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    
    added = 0
    skipped = 0
    for root, dirs, files in os.walk(BASE):
        dirs[:] = [d for d in dirs if d not in SKIP]
        for f in sorted(files):
            if not f.endswith('.md'):
                continue
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8') as fh:
                content = fh.read()
            
            # Only process study cards
            if not ('\ntype: study\n' in content or content.startswith('---\ntype: study\n')):
                continue
            
            new_content, changed = add_query_block(content)
            if changed:
                with open(path, 'w', encoding='utf-8', newline='\n') as fh:
                    fh.write(new_content)
                added += 1
                print(f"  + Query block: {os.path.relpath(path, BASE)}")
            else:
                skipped += 1
    
    print(f"\nAdded query blocks to {added} cards, {skipped} already had them.")


if __name__ == '__main__':
    main()
