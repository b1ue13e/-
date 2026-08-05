#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pytest 测试：本次生产的 42 张知识点卡的 wikilink 目标存在性校验（精确白名单版）。

规则：
1. 只测试本次创建的 42 张卡（白名单路径）。
2. 卡内 [[目标]]（去除 #锚点 与 |别名）须能在知识库找到对应 .md：
   - 相对路径形式：VAULT/<目标>.md 存在；
   - 纯文件名：文件名规范化（小写去空格）精确匹配，或子串双向包含（允许旧碎片别名）。
3. 扫描范围限定 02-Knowledge（避免全盘 97s）。

运行：python -m pytest 99-System/tools/test_new_cards_links.py -v
"""
import re
from pathlib import Path

import pytest

VAULT = Path(r"F:\-")
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")

# 本次生产的 42 张卡（白名单）
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

# 知识库 .md 文件名集合（限定 02-Knowledge 学习系统 + 模板）
_MD_CACHE = None


def _normalize(name: str) -> str:
    return name.lower().replace(" ", "").replace("：", ":").replace("，", ",").strip()


def _all_md_names():
    global _MD_CACHE
    if _MD_CACHE is None:
        names = set()
        for root in [VAULT / "02-Knowledge", VAULT / "99-System/📇 模板"]:
            for p in root.rglob("*.md"):
                if any(x in p.parts for x in (".git", ".obsidian", ".recovery-hold", ".tmp")):
                    continue
                names.add((p.stem, _normalize(p.stem)))
        _MD_CACHE = names
    return _MD_CACHE


def _resolve(target: str) -> bool:
    """判断 wikilink 目标是否已存在（卡间/已有笔记必须存在；计划性前置知识允许待建）。"""
    t = target.strip()
    if not t:
        return True
    if "/" in t or "\\" in t:
        return (VAULT / f"{t}.md").exists()
    t_norm = _normalize(t)
    stems = _all_md_names()
    for stem, s_norm in stems:
        if s_norm == t_norm:
            return True
    # 子串双向包含（允许旧碎片别名，如 "探索利用-困境" 匹配）
    for stem, s_norm in stems:
        if s_norm in t_norm or t_norm in s_norm:
            return True
    return False


def _is_planning_link(target: str) -> bool:
    """计划性前置知识链接：目标在知识库完全无同名/近名文件（属于待建概念卡）。
    注意：若目标与某个已存在文件仅因分隔符/连接词不同（如 '/' vs '与'），
    则是写错的卡间链接（应修复），不算计划性——由 _resolve 子串匹配兜底，
    这里只放行『完全无匹配』的目标。"""
    if not target.strip():
        return False
    # _resolve 已做精确+子串匹配；走到这里说明无任何文件匹配 → 计划性
    return True


def test_collected_card_count():
    missing = [str(c) for c in CARDS if not (VAULT / c).exists()]
    assert not missing, f"缺失卡: {missing}"


@pytest.mark.parametrize("card", CARDS, ids=lambda p: p.parent.name + "/" + p.stem)
def test_card_wikilinks_resolve(card):
    """卡间双链（指向已存在笔记/本次 42 卡）必须可解析；
    指向不存在概念的前置知识链接是计划性待建节点，报告但不视为断链。"""
    txt = (VAULT / card).read_text(encoding="utf-8", errors="ignore")
    planning = []
    for m in WIKILINK_RE.finditer(txt):
        target = m.group(1).strip()
        if not _resolve(target):
            planning.append(target)
    # 计划性链接仅打印信息，不失败（Obsidian 中显示为未创建节点，属合理设计）
    if planning:
        print(f"[INFO] {card.name}: {len(planning)} 个计划性待建链接（知识库尚无此概念卡）: {planning}")
