#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ensure the 5 knowledge asset index files exist in 02-Knowledge subdirectories."""

import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]

FILES = {
    ROOT / "02-Knowledge" / "MOC" / "🗺️ MOC地图总索引.md": ("MOC地图总索引", "moc"),
    ROOT / "02-Knowledge" / "概念-主题卡" / "🧠 概念与主题卡总索引.md": ("概念与主题卡总索引", "concept"),
    ROOT / "02-Knowledge" / "推导" / "📐 推导笔记总索引.md": ("推导笔记总索引", "derivation"),
    ROOT / "02-Knowledge" / "题型" / "📝 题型笔记总索引.md": ("题型笔记总索引", "problem-type"),
    ROOT / "02-Knowledge" / "错题" / "🧯 错题与漏洞总索引.md": ("错题与漏洞总索引", "mistake"),
}

for path, (title, kind) in FILES.items():
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        content = f"""---
title: "{title}"
type: index
topic: "{title}"
created: 2026-07-29
updated: 2026-07-29
status: active
flow: knowledge
kind: moc
tags: [知识, 索引, {kind}]
---

# {path.stem}

> 本页面为 {title} 的全库物理分类索引。包含所有 `kind: {kind}` 类型的底层卡片。

## 📊 分类 Dataview 动态视图

```dataview
TABLE topic, course, updated, status
FROM "02-Knowledge"
WHERE kind = "{kind}" OR note_role = "{kind}"
SORT updated DESC
```
"""
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Created: {path.name}")
    else:
        print(f"Already exists: {path.name}")
