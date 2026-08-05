#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate Standardized Concept Note Skeletons (概念卡骨架生成器)
============================================================
This script scans learning path folders in `02-Knowledge/🧠 学习系统/`,
and creates clean, standardized blank concept note skeletons for planned
topics that do not have note files yet.

Frontmatter Schema generated:
-----------------------------
---
title: "<Concept Title>"
type: concept
kind: concept
flow: knowledge
course: "<Course Name>"
status: planned
difficulty: intermediate
importance: A
sources:
  - title: "<Open Textbook Title>"
    url: "<Source URL>"
    locator: "Chapter X"
    source_type: open-textbook
    verified_at: 2026-08-02
concept: ["<Concept Name>"]
prerequisites: []
related: []
upstream: []
downstream: []
tags: [学习, <Course Tag>, 概念]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

Usage:
    python 99-System/tools/generate_note_skeletons.py [--dry-run]
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# Enforce UTF-8 encoding for stdout/stderr
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

VAULT_ROOT = Path(__file__).resolve().parent.parent.parent
LEARNING_SYS_DIR = VAULT_ROOT / "02-Knowledge" / "🧠 学习系统"

SKELETON_BODY_TEMPLATE = """---
title: "{title}"
type: concept
kind: concept
flow: knowledge
course: "{course}"
status: planned
difficulty: intermediate
importance: A
sources:
  - title: "{textbook_title}"
    url: "{textbook_url}"
    locator: "Chapter 1"
    source_type: open-textbook
    verified_at: "{date_str}"
concept: ["{title}"]
prerequisites: []
related: []
upstream: []
downstream: []
tags: [学习, {course_tag}, 概念]
created: {date_str}
updated: {date_str}
---

# {title}

> 💡 **一句话直觉**：«这东西其实就像……»

---

## 1. 🎯 它解决什么问题？（动机与背景）

- **背景开场**：
- **核心痛点**：如果不引入这个工具，我们在实际分析或推导中会遇到什么困难？

---

## 2. 🧠 费曼直觉与几何类比

- **生活类比 / 几何图像**：
- **为什么这个想法很自然**：

---

## 3. 📐 正式定义与核心公式

### 核心公式
$$
[待补充核心公式]
$$

### 符号说明表

| 符号 | 含义 | 备注 |
| :--- | :--- | :--- |
| $\\mathbf{{x}}$ | 输入数据 | |

---

## 4. 📝 典型例题与工程实现 (L1-L3)

### 基础例题（可手算）
- **题目描述**：
- **解题关键步骤**：

### 核心代码实现 (L3 手撕底层)
```python
# 核心算法解耦实现
```

---

## 5. 🧯 常见误区与坑点

- **误区 1**：
- **坑点 2**：

---

## 6. 闭卷自查 Checklist (10项)

- [ ] 1. 用一句话说明它解决什么问题。
- [ ] 2. 用直觉语言解释它。
- [ ] 3. 独立默写正式定义与公式。
- [ ] 4. 说明公式中每个符号的物理/统计含义。
- [ ] 5. 手算做出一道基础例题。
- [ ] 6. 说出核心推导的关键转念。
- [ ] 7. 说出至少两个常见易错坑点。
- [ ] 8. 区分它与相近概念的区别。
- [ ] 9. 指出它在实际工程/论文中的应用场景。
- [ ] 10. 合上笔记独立向他人讲解一遍。

---

## 🃏 Anki 卡片 (复盘回收)

- Q: {title} 的核心直觉与定义是什么？
- A: [卡片答案]
"""

def generate_skeleton_file(filepath: Path, title: str, course: str, textbook_title: str = "开源权威教材", textbook_url: str = "", dry_run: bool = False):
    date_str = datetime.now().strftime("%Y-%m-%d")
    course_tag = course.replace(" ", "")
    
    content = SKELETON_BODY_TEMPLATE.format(
        title=title,
        course=course,
        textbook_title=textbook_title,
        textbook_url=textbook_url,
        course_tag=course_tag,
        date_str=date_str
    )
    
    if dry_run:
        print(f"[DRY-RUN] Would create: {filepath.relative_to(VAULT_ROOT)}")
    else:
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_text(content, encoding="utf-8")
        print(f"Created concept skeleton: {filepath.relative_to(VAULT_ROOT)}")

def main():
    print("Starting Concept Note Skeleton Generator...")
    print(f"Scanning directory: {LEARNING_SYS_DIR}")
    count = 0
    for course_dir in sorted(LEARNING_SYS_DIR.glob("*")):
        if not course_dir.is_dir() or course_dir.name.startswith("."):
            continue
        course_name = course_dir.name
        for stage_dir in sorted(course_dir.glob("*")):
            if stage_dir.is_dir() and not stage_dir.name.startswith("."):
                stage_name = stage_dir.name
    print("Done scanning.")

if __name__ == "__main__":
    main()
