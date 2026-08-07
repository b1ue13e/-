from __future__ import annotations

import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
COURSE_ROOT = REPO_ROOT / "02-Knowledge" / "02-Knowledge/🧠 学习系统" / "02-时间序列分析"
COURSE_LINK_ROOT = "02-时间序列分析"


def main() -> None:
    stage_links: dict[str, str] = {}
    for path in COURSE_ROOT.rglob("🧭 阶段*.md"):
        stage_links[path.stem] = f"{COURSE_LINK_ROOT}/{path.parent.name}/{path.stem}"

    changed = 0
    for path in sorted(COURSE_ROOT.rglob("*.md")):
        if ".tmp" in path.parts or ".reasonix" in path.parts:
            continue
        text = path.read_text(encoding="utf-8-sig")

        def replace(match: re.Match[str]) -> str:
            target = match.group(1)
            stem = target.split("/")[-1]
            if stem in stage_links:
                return f'stage_moc: "[[{stage_links[stem]}]]"'
            return match.group(0)

        updated = re.sub(r'^stage_moc:\s*"\[\[([^\]|]+)\]\]"\s*$', replace, text, flags=re.MULTILINE)
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            changed += 1
            print(path.relative_to(REPO_ROOT))
    print(f"changed_files={changed}")


if __name__ == "__main__":
    main()
