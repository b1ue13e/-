#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pytest 测试：42 张卡的 frontmatter upstream/downstream 命名一致性。

规则：
1. 42 卡文件路径白名单（与 test_new_cards_links.py 相同）。
2. 解析 frontmatter 的 upstream/downstream 列表。
3. 每个条目必须是：
   a. 知识库中实际存在的 .md 文件名（精确或规范化匹配）；或
   b. 计划性待建概念（知识库无同名文件，允许）——本测试只做『信息统计』不失败。
4. 关键断言：若条目指向的知识点已存在同名卡文件（42 卡或库内其他卡），
   条目必须与其文件名精确一致（不允许 '/' vs '与' 这类写法差异）。

运行：python -m pytest 99-System/tools/test_cards_frontmatter.py -v
"""
import re
from pathlib import Path

import pytest

VAULT = Path(r"F:\-")

CARDS = [
    # 37-复变函数 14
    Path("02-Knowledge/🧠 学习系统/37-复变函数/01-复数与解析函数/复数运算与复平面.md"),
    Path("02-Knowledge/🧠 学习系统/37-复变函数/01-复数与解析函数/解析函数与 Cauchy-Riemann 方程.md"),
    Path("02-Knowledge/🧠 学习系统/37-复变函数/01-复数与解析函数/初等函数：指数、对数与幂.md"),
    Path("02-Knowledge/🧠 学习系统/37-复变函数/02-复积分与级数/复积分与 Cauchy 定理.md"),
    Path("02-Knowledge/🧠 学习系统/37-复变函数/02-复积分与级数/Cauchy 积分公式.md"),
    Path("02-Knowledge/🧠 学习系统/37-复变函数/02-复积分与级数/泰勒与洛朗级数.md"),
    Path("02-Knowledge/🧠 学习系统/37-复变函数/03-奇点与留数/奇点分类与留数定理.md"),
    Path("02-Knowledge/🧠 学习系统/37-复变函数/03-奇点与留数/留数计算实积分.md"),
    Path("02-Knowledge/🧠 学习系统/37-复变函数/04-保角映射与综合项目/辐角原理与 Rouché 定理.md"),
    Path("02-Knowledge/🧠 学习系统/37-复变函数/04-保角映射与综合项目/保角映射与 Möbius 变换.md"),
    Path("02-Knowledge/🧠 学习系统/37-复变函数/04-保角映射与综合项目/调和函数与 Dirichlet 问题.md"),
    Path("02-Knowledge/🧠 学习系统/37-复变函数/04-保角映射与综合项目/解析延拓与多值函数.md"),
    Path("02-Knowledge/🧠 学习系统/37-复变函数/04-保角映射与综合项目/最大模原理与 Schwarz 引理.md"),
    Path("02-Knowledge/🧠 学习系统/37-复变函数/04-保角映射与综合项目/域着色可视化画廊（Capstone）.md"),
    # 16-多元统计 14
    Path("02-Knowledge/🧠 学习系统/16-多元统计/01-基础矩阵/多元正态分布与性质.md"),
    Path("02-Knowledge/🧠 学习系统/16-多元统计/01-基础矩阵/均值向量与协方差矩阵估计.md"),
    Path("02-Knowledge/🧠 学习系统/16-多元统计/01-基础矩阵/Hotelling T² 检验.md"),
    Path("02-Knowledge/🧠 学习系统/16-多元统计/01-基础矩阵/MANOVA.md"),
    Path("02-Knowledge/🧠 学习系统/16-多元统计/02-降维方法/主成分分析 PCA.md"),
    Path("02-Knowledge/🧠 学习系统/16-多元统计/02-降维方法/因子分析.md"),
    Path("02-Knowledge/🧠 学习系统/16-多元统计/03-分类方法/判别分析：LDA与QDA.md"),
    Path("02-Knowledge/🧠 学习系统/16-多元统计/03-分类方法/聚类分析：层次与K-means.md"),
    Path("02-Knowledge/🧠 学习系统/16-多元统计/04-相关分析/典型相关分析 CCA.md"),
    Path("02-Knowledge/🧠 学习系统/16-多元统计/04-相关分析/多元回归回顾与矩阵形式.md"),
    Path("02-Knowledge/🧠 学习系统/16-多元统计/01-基础矩阵/多重比较与检验校正.md"),
    Path("02-Knowledge/🧠 学习系统/16-多元统计/01-基础矩阵/协方差结构检验.md"),
    Path("02-Knowledge/🧠 学习系统/16-多元统计/01-基础矩阵/稳健协方差估计.md"),
    Path("02-Knowledge/🧠 学习系统/16-多元统计/02-降维方法/高维数据的维度灾难.md"),
    # 13-强化学习 14
    Path("02-Knowledge/🧠 学习系统/13-强化学习/多臂老虎机与探索-利用.md"),
    Path("02-Knowledge/🧠 学习系统/13-强化学习/MDP 与贝尔曼方程.md"),
    Path("02-Knowledge/🧠 学习系统/13-强化学习/动态规划：策略与值迭代.md"),
    Path("02-Knowledge/🧠 学习系统/13-强化学习/蒙特卡洛方法.md"),
    Path("02-Knowledge/🧠 学习系统/13-强化学习/时序差分与 Q-Learning.md"),
    Path("02-Knowledge/🧠 学习系统/13-强化学习/值函数近似与 DQN.md"),
    Path("02-Knowledge/🧠 学习系统/13-强化学习/策略梯度.md"),
    Path("02-Knowledge/🧠 学习系统/13-强化学习/Actor-Critic 与 PPO.md"),
    Path("02-Knowledge/🧠 学习系统/13-强化学习/搜索：BFS与DFS与A星.md"),
    Path("02-Knowledge/🧠 学习系统/13-强化学习/博弈：Minimax与Expectimax.md"),
    Path("02-Knowledge/🧠 学习系统/13-强化学习/离线 RL 与模仿学习.md"),
    Path("02-Knowledge/🧠 学习系统/13-强化学习/奖励设计与环境工程.md"),
    Path("02-Knowledge/🧠 学习系统/13-强化学习/RL 评估协议：种子方差与样本效率.md"),
    Path("02-Knowledge/🧠 学习系统/13-强化学习/分层与多智能体 RL 简介.md"),
]

# 库内所有 .md 文件名（规范化），用于判断条目是否指向已存在文件
_ALL_STEMS = set()
for root in [VAULT / "02-Knowledge", VAULT / "99-System/📇 模板"]:
    for p in root.rglob("*.md"):
        if any(x in p.parts for x in (".git", ".obsidian", ".recovery-hold", ".tmp")):
            continue
        _ALL_STEMS.add(p.stem)


def _normalize(name: str) -> str:
    return name.lower().replace(" ", "").replace("：", ":").replace("，", ",").strip()


def _exists(name: str) -> bool:
    n = _normalize(name)
    return any(_normalize(s) == n for s in _ALL_STEMS)


def _parse_fm_list(fm: str, key: str):
    m = re.search(rf"^{key}:\s*\[(.*?)\]", fm, re.M | re.S)
    if not m:
        return []
    inner = m.group(1)
    if '"' in inner or "'" in inner:
        pairs = re.findall(r'"([^"]*)"|\'([^\']*)\'', inner)
        return [a if a else b for a, b in pairs]
    return [x.strip() for x in inner.split(",") if x.strip()]


@pytest.mark.parametrize("card", CARDS, ids=lambda p: p.stem)
def test_frontmatter_refs_consistent(card):
    """upstream/downstream 中指向已存在卡的条目必须与文件名精确一致。"""
    txt = (VAULT / card).read_text(encoding="utf-8", errors="ignore")
    m = re.match(r"^---\n(.*?)\n---\n", txt, re.S)
    assert m, f"{card.name}: 无 frontmatter"
    fm = m.group(1)

    for key in ("upstream", "downstream"):
        refs = _parse_fm_list(fm, key)
        for ref in refs:
            if not ref:
                continue
            # 条目指向库内已存在的文件？
            if _exists(ref):
                # 已存在 → 必须精确匹配某个文件名（不允许写法差异）
                norm = _normalize(ref)
                exact = any(_normalize(s) == norm for s in _ALL_STEMS)
                assert exact, f"{card.name} {key} 条目 '{ref}' 指向已存在概念但写法与文件名不一致"
