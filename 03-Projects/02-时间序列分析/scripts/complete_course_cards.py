from __future__ import annotations

import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
COURSE_ROOT = REPO_ROOT / "02-Knowledge" / "02-Knowledge/🧠 学习系统" / "02-时间序列分析"
DERIVED_VIEW = """

## 派生视图

### 下游知识

```dataview
LIST
FROM "02-Knowledge/🧠 学习系统"
WHERE contains(upstream, this.file.link)
SORT file.name ASC
```

### 可完成作业

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
"""


def field(frontmatter: str, name: str) -> str:
    match = re.search(rf"^{re.escape(name)}:\s*(.+)$", frontmatter, re.MULTILINE)
    return match.group(1).strip().strip('"') if match else ""


def complete(path: Path) -> bool:
    text = path.read_text(encoding="utf-8-sig")
    match = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.DOTALL)
    if not match:
        return False
    frontmatter, body = match.groups()
    if field(frontmatter, "type") != "study":
        return False
    if field(frontmatter, "assessment_exempt").lower() == "true":
        return False
    changed = False
    if not re.search(r"^source(?:_url|s)?:", frontmatter, re.MULTILINE):
        frontmatter += '\nsource: "[待验证]"\nsource_url: "[待验证]"\naccessed: 2026-08-06\nlicense: "[待验证]"'
        changed = True
    if "WHERE contains(upstream, this.file.link)" not in body:
        body = body.rstrip() + DERIVED_VIEW
        changed = True
    if changed:
        path.write_text(f"---\n{frontmatter}\n---\n{body.lstrip()}\n", encoding="utf-8")
    return changed


def main() -> None:
    changed = 0
    for path in sorted(COURSE_ROOT.rglob("*.md")):
        if ".tmp" in path.parts or ".reasonix" in path.parts:
            continue
        if complete(path):
            changed += 1
            print(path.relative_to(REPO_ROOT))
    print(f"changed_files={changed}")


if __name__ == "__main__":
    main()
