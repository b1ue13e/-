#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pytest 测试：16-多元统计 14 张知识点卡模板结构完整性（仅验证卡清单对应卡）。

多元统计卡清单指定：检验/性质卡用数学证明模板（proof_mode: true），
方法应用卡用单知识点模板（type: concept）。两种模板二级标题均为 0-13 共 14 节。

运行：python -m pytest 99-System/tools/test_multivariate_stats_cards.py -v
退出码：0=全部通过；1=存在失败
"""
import re
from pathlib import Path

import pytest

BASE = Path(r"F:\-\02-Knowledge\🧠 学习系统\16-多元统计")
TEMPLATE_SECTIONS = [
    "## 0. ", "## 1. ", "## 2. ", "## 3. ", "## 4. ", "## 5. ", "## 6. ",
    "## 7. ", "## 8. ", "## 9. ", "## 10. ", "## 11. ", "## 12. ", "## 13. ",
]
PLACEHOLDER = re.compile(r"待补充|待补全|TODO|TBD|占位|暂无内容|未完成")

# 卡清单 14 张卡的文件路径（相对 BASE）
CARD_PATHS = [
    "01-基础矩阵/多元正态分布与性质.md",
    "01-基础矩阵/均值向量与协方差矩阵估计.md",
    "01-基础矩阵/Hotelling T² 检验.md",
    "01-基础矩阵/MANOVA.md",
    "02-降维方法/主成分分析 PCA.md",
    "02-降维方法/因子分析.md",
    "03-分类方法/判别分析：LDA与QDA.md",
    "03-分类方法/聚类分析：层次与K-means.md",
    "04-相关分析/典型相关分析 CCA.md",
    "04-相关分析/多元回归回顾与矩阵形式.md",
    "01-基础矩阵/多重比较与检验校正.md",
    "01-基础矩阵/协方差结构检验.md",
    "01-基础矩阵/稳健协方差估计.md",
    "02-降维方法/高维数据的维度灾难.md",
]
CARD_FILES = [BASE / p for p in CARD_PATHS]


def test_card_count():
    """卡清单 14 张卡文件必须全部存在。"""
    missing = [str(p) for p in CARD_FILES if not p.exists()]
    assert not missing, f"缺失卡文件: {missing}"


@pytest.mark.parametrize("card", CARD_FILES, ids=lambda p: p.name)
def test_card_template_structure(card):
    """每张卡必须：有 frontmatter、14 个模板节、无占位标记；proof_mode 卡还需 proof_mode: true。"""
    txt = card.read_text(encoding="utf-8")
    assert len(txt.strip()) > 500, f"{card.name}: 内容过短"

    m = re.match(r"^---\n(.*?)\n---\n", txt, re.S)
    assert m, f"{card.name}: 无 frontmatter"

    missing = [s for s in TEMPLATE_SECTIONS if s not in txt]
    assert not missing, f"{card.name}: 缺模板节 {missing}"

    assert not PLACEHOLDER.search(txt), f"{card.name}: 含占位标记"

    # 数学证明模板卡（检验/性质类）必须 proof_mode: true；方法应用卡用 type: concept
    if "proof_mode" in m.group(1):
        assert "proof_mode: true" in m.group(1), f"{card.name}: proof_mode 必须为 true"
    else:
        assert "type: concept" in m.group(1), f"{card.name}: 非证明卡应为 type: concept"
