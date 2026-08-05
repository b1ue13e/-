#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量改进脚本：把 42 张卡的主动回忆区从「空白提示」改为「引导式填空」。

改进目标（自评项 2）：回忆区给半句提示 + 自查问题，降低启动成本，
同时保留提取练习（提示只引导结构，不给出答案）。

concept 卡（单知识点模板）：
  我的闭卷复述 / 我的推导复现 / 我的错误与卡点
proof 卡（数学证明模板）：
  我的闭卷复述 / 我的证明重建 / 我的反例与卡点

用法：python 99-System/tools/add_guided_recall_to_cards.py
幂等：含「写不出来 =」标记的卡跳过。
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

# concept 卡填空：闭卷复述 + 推导复现 + 错误与卡点
CONCEPT_BLOCK = """## 12. 我的主动回忆区

> **用法**：合上笔记，按引导填空。填不出 = 没掌握，回到第 4-5 节重读再重填。写不出来 = 卡点，记入下方。

### 我的闭卷复述
> 用 3 句话解释「{title}」：
> 1. 它解决什么问题：______
> 2. 它怎么做的（直觉）：______
> 3. 它的关键公式/条件：______

### 我的推导复现
> 不看上文，写出核心推导主线：
> - 第 1 步：______
> - 关键"转念"：______
> - 我能独立推到哪一步：______（卡住的步骤 = 复习重点）

### 我的错误与卡点
- 我填不出的空：______
- 我搞混的概念：______
- 修正后的理解：______

### 下次复习日期
- [ ] 明天
- [ ] 3 天后
- [ ] 7 天后
- [ ] 14 天后
"""

# proof 卡填空：闭卷复述 + 证明重建 + 反例与卡点
PROOF_BLOCK = """## 12. 我的主动回忆区

> **用法**：合上笔记，按引导填空。填不出 = 没掌握，回到第 4-6 节重读再重填。写不出来 = 卡点，记入下方。

### 我的闭卷复述
> 复述「{title}」的精确定义：
> - 前提条件：______
> - 结论：______
> - 符号含义（至少 3 个）：______

### 我的证明重建
> 不看上文，写出证明主线：
> - 第 1 步：______
> - 关键"转念"：______
> - 我卡住的证明步骤：______（复习重点）

### 我的反例与卡点
- 我构造的反例：______（对应哪个条件不能省）
- 我默写时卡住的步骤：______
- 修正后的理解：______

### 下次复习日期
- [ ] 明天
- [ ] 3 天后
- [ ] 7 天后
- [ ] 14 天后
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
        # 修复历史遗留：回忆区结尾的双 --- 归一为单个
        txt = re.sub(
            r"(- \[ \] 14 天后\n)\n---\n\n---\n(\n## 1[23]\.|\Z)",
            r"\1\n---\n\2", txt,
        )
        if "填不出 = 没掌握" in txt:
            p.write_text(txt, encoding="utf-8")
            skipped += 1
            continue
        # 取标题（frontmatter title 或 H1）
        title = "本知识点"
        m = re.search(r"^# (.+)$", txt, re.M)
        if m:
            title = m.group(1).strip()
        # 判断是 proof 卡（含"我的证明重建"）还是 concept 卡
        block = PROOF_BLOCK if "我的证明重建" in txt else CONCEPT_BLOCK
        filled = block.format(title=title)
        # 用正则定位回忆区整段（## 12. 到下一个 ## 或 --- 分隔）
        m = re.search(
            r"(^## 12\. 我的主动回忆区.*?)(?=\n---\n|\n## 13\.|\Z)",
            txt, re.M | re.S,
        )
        if not m:
            errors.append(f"未找到回忆区: {rel}")
            continue
        new_txt = txt[: m.start()] + filled + "\n" + txt[m.end():]
        p.write_text(new_txt, encoding="utf-8")
        changed += 1

    print(f"已改写回忆区: {changed} 张；跳过(已含引导): {skipped} 张")
    if errors:
        print("错误:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
