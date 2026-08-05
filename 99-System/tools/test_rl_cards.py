#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pytest 测试：13-强化学习 14 张知识点卡模板结构完整性（仅验证卡清单对应卡）。

强化学习卡清单指定：理论推导卡用数学证明模板（proof_mode: true），
算法实现卡用单知识点模板（type: concept）。两种模板二级标题均为 0-13 共 14 节。

运行：python -m pytest 99-System/tools/test_rl_cards.py -v
退出码：0=全部通过；1=存在失败
"""
import re
from pathlib import Path

import pytest

BASE = Path(r"F:\-\02-Knowledge\🧠 学习系统\13-强化学习")
TEMPLATE_SECTIONS = [
    "## 0. ", "## 1. ", "## 2. ", "## 3. ", "## 4. ", "## 5. ", "## 6. ",
    "## 7. ", "## 8. ", "## 9. ", "## 10. ", "## 11. ", "## 12. ", "## 13. ",
]
PLACEHOLDER = re.compile(r"待补充|待补全|TODO|TBD|占位|暂无内容|未完成")

# 卡清单 14 张卡的文件路径（相对 BASE，均位于根目录）
CARD_NAMES = [
    "多臂老虎机与探索-利用.md",
    "MDP 与贝尔曼方程.md",
    "动态规划：策略与值迭代.md",
    "蒙特卡洛方法.md",
    "时序差分与 Q-Learning.md",
    "值函数近似与 DQN.md",
    "策略梯度.md",
    "Actor-Critic 与 PPO.md",
    "搜索：BFS与DFS与A星.md",
    "博弈：Minimax与Expectimax.md",
    "离线 RL 与模仿学习.md",
    "奖励设计与环境工程.md",
    "RL 评估协议：种子方差与样本效率.md",
    "分层与多智能体 RL 简介.md",
]
CARD_FILES = [BASE / n for n in CARD_NAMES]


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

    # 数学证明模板卡（理论推导类）必须 proof_mode: true；算法卡用 type: concept
    if "proof_mode" in m.group(1):
        assert "proof_mode: true" in m.group(1), f"{card.name}: proof_mode 必须为 true"
    else:
        assert "type: concept" in m.group(1), f"{card.name}: 非证明卡应为 type: concept"
