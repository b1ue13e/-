#!/usr/bin/env python3
"""Quarantine failed non-route quant cards while preserving stable Obsidian paths."""
from __future__ import annotations

import csv
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
Q = ROOT / "02-Knowledge" / "02-Knowledge/🧠 学习系统" / "03-量化金融"
AUDIT_DIR = ROOT / "99-System" / "🗄️ 归档" / "知识库审计"
ARCHIVE = ROOT / ".recovery-hold" / "quarantine" / "量化金融未达标知识卡-2026-08-01"
CSV_PATH = AUDIT_DIR / "knowledge_notes_merciless_scores_2026-08-01.csv"


def main() -> None:
    with CSV_PATH.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = reader.fieldnames or []
        rows = [row for row in reader if row.get("subject", "").startswith("03-")]
    knowledge_category = Counter(row["category"] for row in rows).most_common(1)[0][0]
    issue_field = fields[-2]

    quarantined = []
    skipped_stage = []
    for row in rows:
        if row["category"] != knowledge_category or int(row["score"]) >= 60:
            continue
        source = ROOT / Path(row["path"])
        text = source.read_text(encoding="utf-8-sig")
        frontmatter = text.split("---", 2)[1] if text.startswith("---") else ""
        if re.search(r"(?m)^phase:\s*\d+", frontmatter):
            skipped_stage.append(source)
            continue
        if "quant-route-quality-v2" in text:
            raise RuntimeError(f"Refusing to quarantine a canonical K card: {source}")

        relative = source.relative_to(Q)
        archived = ARCHIVE / relative
        archived.parent.mkdir(parents=True, exist_ok=True)
        if not archived.exists():
            archived.write_text(text, encoding="utf-8")

        created = re.search(r"(?m)^created:\s*(.+)$", frontmatter)
        created_value = created.group(1).strip() if created else "2026-08-01"
        topic = source.stem
        reason = row[issue_field] or "极严审计低于 60 分"
        tick = chr(96)
        pointer = f"""---
type: index
topic: {json.dumps(topic + "：质量隔离页", ensure_ascii=False)}
created: {created_value}
updated: 2026-08-01
status: quarantined
flow: review
quality_gate: failed
audit_score: {row["score"]}
tags: [量化金融, 质量隔离, 待重建]
---
# ⛔ {topic}：当前不可作为学习材料

> 本路径保留用于维持旧链接稳定；原知识卡未通过严格质量闸门，已从活跃知识资产中隔离。

- 审计分数：**{row["score"]} / 100**
- 主要问题：{reason}
- 原文存档：{tick}{archived}{tick}
- 可信学习主线：[[🗺️ 量化金融学习路径]]、[[🧩 Qlib 项目知识点—作业—验收路线图]]

## 重新纳入条件

只有在补齐可定位权威来源、贴题正反例、可运行验证、成立条件、失效边界并通过复审后，才可恢复为 {tick}type: study{tick}。
"""
        source.write_text(pointer, encoding="utf-8")
        quarantined.append(source)

    print(f"Quarantined {len(quarantined)} failed cards; preserved originals under {ARCHIVE}.")
    print(f"Kept {len(skipped_stage)} phase pages active for separate stage-page repair.")


if __name__ == "__main__":
    main()
