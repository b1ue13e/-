#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pytest 测试：37-复变函数 14 张知识点卡模板结构完整性。

运行：python -m pytest 99-System/tools/test_complex_analysis_cards.py -v
退出码：0=全部通过；1=存在失败
"""
import re
from pathlib import Path

import pytest

BASE = Path(r"F:\-\02-Knowledge\🧠 学习系统\37-复变函数")
TEMPLATE_SECTIONS = [
    "## 0. ", "## 1. ", "## 2. ", "## 3. ", "## 4. ", "## 5. ", "## 6. ",
    "## 7. ", "## 8. ", "## 9. ", "## 10. ", "## 11. ", "## 12. ", "## 13. ",
]
PLACEHOLDER = re.compile(r"待补充|待补全|TODO|TBD|占位|暂无内容|未完成")
SKIP_NAMES = ("📘", "📗", "📙", "📕", "📋", "📚", "🗺️", "🧭")

CARD_FILES = [
    f
    for f in sorted(BASE.rglob("*.md"))
    if not f.name.startswith(SKIP_NAMES)
]


def test_card_count():
    """应恰好 14 张知识点卡（不含阶段 MOC / 清单 / 教材索引 / 学习路径）。"""
    assert len(CARD_FILES) == 14, f"期望 14 张卡，实际 {len(CARD_FILES)}"


@pytest.mark.parametrize("card", CARD_FILES, ids=lambda p: p.name)
def test_card_template_structure(card):
    """每张卡必须：有 frontmatter、proof_mode: true、14 个模板节、无占位标记。"""
    txt = card.read_text(encoding="utf-8")
    assert len(txt.strip()) > 500, f"{card.name}: 内容过短"

    m = re.match(r"^---\n(.*?)\n---\n", txt, re.S)
    assert m, f"{card.name}: 无 frontmatter"
    assert "proof_mode: true" in m.group(1), f"{card.name}: 缺 proof_mode: true"

    missing = [s for s in TEMPLATE_SECTIONS if s not in txt]
    assert not missing, f"{card.name}: 缺模板节 {missing}"

    assert not PLACEHOLDER.search(txt), f"{card.name}: 含占位标记"
