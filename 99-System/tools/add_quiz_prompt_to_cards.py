#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量改进脚本：给 42 张新卡的自测题/分级习题区插入"先闭卷作答再展开核对"提示行。

改进目标（自评项 1）：恢复提取练习——答案 callout 保持折叠，但在题目前加
强制先作答的提示，避免小白直接展开答案短路测试效应。

用法：python 99-System/tools/add_quiz_prompt_to_cards.py
幂等：已含提示行的卡跳过。
"""
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

VAULT = Path(r"F:\-")
PROMPT = (
    "> [!important] 先闭卷作答，再展开核对\n"
    "> 合上笔记独立完成下列题目；**全部写完后再逐题展开答案对照**。\n"
    "> 直接看答案 = 测试效应归零，等于没练。\n"
)

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

SECTION_RE = re.compile(
    r"^(## 11\. (?:自测题：5 道|分级习题))\s*(\n+)",
    re.M,
)


def _normalize_block(txt: str) -> str:
    """把「11 节标题 + 若干空行 + 提示块」规范化为「标题 + 单空行 + 提示块 + 单空行」。"""
    m = re.search(
        r"(^## 11\. (?:自测题：5 道|分级习题))\s*\n+(> \[!important\] 先闭卷作答，再展开核对.*?直接看答案 = 测试效应归零，等于没练。\n)(?:\s*\n)*",
        txt, re.M | re.S,
    )
    if not m:
        return None
    head = m.group(1)
    block = m.group(2).rstrip()
    return txt[: m.start()] + head + "\n\n" + block + "\n\n" + txt[m.end():]


def main():
    changed = 0
    skipped = 0
    errors = []
    for rel in CARDS:
        p = VAULT / rel
        if not p.exists():
            errors.append(f"缺失: {rel}")
            continue
        txt = p.read_text(encoding="utf-8")
        if "先闭卷作答" in txt:
            new_txt = _normalize_block(txt)
            if new_txt is None:
                errors.append(f"提示块未匹配: {rel}")
                continue
            p.write_text(new_txt, encoding="utf-8")
            changed += 1
            continue
        new_txt, n = SECTION_RE.subn(
            lambda m: m.group(1) + "\n\n" + PROMPT.rstrip() + "\n\n", txt, count=1
        )
        if n == 0:
            errors.append(f"未找到 11 节标题: {rel}")
            continue
        p.write_text(new_txt, encoding="utf-8")
        changed += 1

    print(f"已处理: {changed} 张；未变更: {skipped} 张")
    if errors:
        print("错误:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
