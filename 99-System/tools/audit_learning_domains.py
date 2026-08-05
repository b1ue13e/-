"""Semantic audit for the three weakest learning domains in the vault.

The original audit only checked whether headings existed. This audit also
detects placeholder cards, repeated boilerplate, and wikilinks that do not
resolve to a note in the vault.
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


VAULT_ROOT = Path(__file__).resolve().parents[2]
LEARNING_ROOT = VAULT_ROOT / "02-Knowledge" / "🧠 学习系统"
DOMAINS = {
    "social_network_mining": "01-社交网络挖掘",
    "time_series": "02-时间序列分析",
    "quantitative_finance": "03-量化金融",
}
META_MARKERS = ("学习路径", "专题支线导航", "教材挂载索引", "阶段", "导航", "知识地图")
PLACEHOLDER_MARKERS = (
    "待写",
    "待补",
    "待完善",
    "TODO",
    "TBD",
    "占位",
    "这里填写",
)
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")


def is_meta(path: Path) -> bool:
    return any(marker in path.name for marker in META_MARKERS)


def normalise_target(raw: str) -> str:
    target = raw.strip().replace("\\", "/")
    return target.removesuffix(".md").split("/")[-1]


def audit_domain(path: Path, all_note_names: set[str]) -> dict:
    notes = [p for p in path.rglob("*.md") if not is_meta(p)]
    placeholder_notes: list[str] = []
    boilerplate = Counter()
    broken_links: list[dict[str, str]] = []

    for note in notes:
        text = note.read_text(encoding="utf-8", errors="replace")
        body = text.split("---", 2)[-1] if text.lstrip().startswith("---") else text
        if any(marker in body for marker in PLACEHOLDER_MARKERS):
            placeholder_notes.append(str(note.relative_to(VAULT_ROOT)))
        # The first 6 non-empty body lines are enough to detect copied shells.
        signature = "\n".join(line.strip() for line in body.splitlines() if line.strip())[:500]
        if signature:
            boilerplate[signature] += 1
        for match in WIKILINK_RE.finditer(text):
            target = normalise_target(match.group(1))
            if target and target not in all_note_names:
                broken_links.append(
                    {"file": str(note.relative_to(VAULT_ROOT)), "target": target}
                )

    repeated_shells = sum(count - 1 for count in boilerplate.values() if count > 1)
    return {
        "files": len(notes),
        "placeholder_files": len(placeholder_notes),
        "placeholder_rate": round(len(placeholder_notes) / len(notes) * 100, 1) if notes else 0.0,
        "placeholder_examples": placeholder_notes[:20],
        "repeated_shells": repeated_shells,
        "broken_wikilinks": len(broken_links),
        "broken_wikilink_examples": broken_links[:20],
    }


def main() -> None:
    all_notes = list(LEARNING_ROOT.rglob("*.md"))
    all_note_names = {note.stem for note in all_notes}
    report = {
        "generated_by": "audit_learning_domains.py",
        "domains": {
            key: audit_domain(LEARNING_ROOT / folder, all_note_names)
            for key, folder in DOMAINS.items()
        },
    }
    output = VAULT_ROOT / "99-System" / "🗄️ 归档" / "知识库审计" / "domain_audit_report.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
