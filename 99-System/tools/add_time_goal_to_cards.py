#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量改进脚本：给 42 张新卡插入「预计耗时 + 行为目标」块（自评项 7）。

位置：H1 标题之后、## 0. 之前。
耗时按 frontmatter importance 差异化：A=45-60min，B=30-45min，C=20-30min。
行为目标按模板类型生成：concept 卡=能解释+能推导+能做题；proof 卡=能复述+能重建证明+能造反例。

用法：python 99-System/tools/add_time_goal_to_cards.py
幂等：含「预计耗时」的卡跳过。
"""
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

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

TIME_BY_IMPORTANCE = {"A": "45–60 分钟", "B": "30–45 分钟", "C": "20–30 分钟", "D": "15–20 分钟"}

CONCEPT_GOAL = """- **学完你能**：
  - 用一句话说清它解决什么问题（能讲给外行听）；
  - 不看笔记写出核心公式并解释每个符号；
  - 手算/口算出至少 1 道基础题；
  - 说出 2 个常见误区及其正确理解。
"""
PROOF_GOAL = """- **学完你能**：
  - 精确复述定义与定理（量词一个不差）；
  - 不看笔记重建证明主线并指出关键"转念"；
  - 独立构造 1 个反例并说明哪个条件不能省；
  - 对 2 个条件变式给出成立/不成立的判断。
"""


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
        if "预计耗时" in txt:
            skipped += 1
            continue
        # 读 importance
        imp = "B"
        m = re.search(r"^importance:\s*[\"']?([A-E])", txt, re.M)
        if m:
            imp = m.group(1)
        time_str = TIME_BY_IMPORTANCE.get(imp, "30–45 分钟")
        goal = PROOF_GOAL if "我的证明重建" in txt else CONCEPT_GOAL
        block = (
            f"> **⏱ 预计耗时**：{time_str}（第 0-6 节理解 + 第 7 节例子 + 第 10/11 节闭卷自测）\n"
            f"> **🎯 行为目标**：完成本卡后，\n"
        ) + "\n".join("> " + line for line in goal.strip().split("\n")) + "\n"
        # 在 H1 后、## 0. 前插入（H1 → 空行 → --- → 空行 → ## 0.）
        m = re.search(r"(^# .+\n\n---\n\n)(?=## 0\.)", txt, re.M)
        if not m:
            errors.append(f"未找到插入点: {rel}")
            continue
        new_txt = txt[: m.end()] + block + "\n" + txt[m.end():]
        p.write_text(new_txt, encoding="utf-8")
        changed += 1

    print(f"已插入耗时/目标: {changed} 张；跳过: {skipped} 张")
    if errors:
        print("错误:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
