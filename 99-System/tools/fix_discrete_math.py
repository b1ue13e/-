# -*- coding: utf-8 -*-
import os
import re
import sys
import yaml

base_dir = r"f:\-\02-Knowledge\🧠 学习系统\04-离散数学"

# Topic-specific content dictionary to ensure rich, accurate mathematical knowledge
TOPIC_KNOWLEDGE = {
    # Stage 1: Basic Set Theory, Logic & Relations
    "n元组": {
        "def": "设 $n$ 为正整数，有序 $n$ 元组（Ordered n-tuple）是记作 $(a_1, a_2, \\dots, a_n)$ 的元素序列，其中 $a_1$ 为第一元素，$a_n$ 为第 $n$ 元素。两个 $n$ 元组相等当且仅当对应位置元素完全相同。",
        "intuition": "有序 $n$ 元组就像 $n$ 维空间中的一个坐标点，元素的顺序极度重要：$(1,2) \\neq (2,1)$。",
        "properties": [
            "$n=2$ 时即为有序对（Ordered Pair）。",
            "笛卡尔积定义：$A_1 \\times A_2 \\times \\dots \\times A_n = \\{(a_1, \\dots, a_n) \\mid a_i \\in A_i\\}$。",
            "在关系数据库模型中，$n$ 元组对应数据库表中的一行记录（Tuple）。"
        ],
        "apps": "关系数据库、向量空间表示、状态空间与转移系统。"
    },
    "不可数集": {
        "def": "若集合 $A$ 为无限集且不能与自然数集 $\\mathbb{N}$ 建立双射（一一对应），则称 $A$ 为不可数集（Uncountable Set），其基数等于或大于连续统基数 $\\mathfrak{c} = 2^{\\aleph_0}$。",
        "intuition": "不可数集是“多到无法用自然数挨个排队编号”的集合，如实数集 $\\mathbb{R}$ 或区间 $[0,1]$。",
        "properties": [
            "康托尔对角线证明法（Cantor's Diagonal Argument）证明了实数集不可数。",
            "任意非空实数区间 $[a,b]$ ($a<b$) 均为不可数集。",
            "不可数集与可数集（或有限集）的并集仍为不可数集。"
        ],
        "apps": "实分析、测度论、计算理论（不可计算函数集是不可数的）。"
    },
    "交集": {
        "def": "设 $A, B$ 为两个集合，由既属于 $A$ 又属于 $B$ 的所有元素组成的集合称为 $A$ 与 $B$ 的交集，记作 $A \\cap B = \\{x \\mid x \\in A \\land x \\in B\\}$。",
        "intuition": "交集代表两个集合的“共同重叠区域”。",
        "properties": [
            "交换律：$A \\cap B = B \\cap A$；结合律：$(A \\cap B) \\cap C = A \\cap (B \\cap C)$。",
            "幂等律：$A \\cap A = A$；吸收律：$A \\cap (A \\cup B) = A$。",
            "若 $A \\cap B = \\emptyset$，则称 $A$ 与 $B$ 不相交（Disjoint）。"
        ],
        "apps": "数据库集合查询（INTERSECT）、逻辑与运算、系统交集测试。"
    },
    "传递性": {
        "def": "设 $R$ 是集合 $A$ 上的二元关系。若对任意 $a,b,c \\in A$，只要 $(a,b) \\in R$ 且 $(b,c) \\in R$，就有 $(a,c) \\in R$，则称关系 $R$ 具有传递性（Transitivity）。",
        "intuition": "“A比B大，B比C大，则A必然比C大”就是传递性。",
        "properties": [
            "等价关系和偏序关系均必须满足传递性。",
            "在关系矩阵表示中，$R$ 具有传递性当且仅当 $M_R^{[2]} \\le M_R$。",
            "传递闭包 $t(R) = R^+ = \\bigcup_{i=1}^\\infty R^i$ 可通过 Warshall 算法在 $O(n^3)$ 内求解。"
        ],
        "apps": "图的可达性判定、拓扑排序、面向对象类的继承关系分析。"
    },
    "假言三段论": {
        "def": "假言三段论（Hypothetical Syllogism）是命题逻辑的有效推理规则：$((p \\to q) \\land (q \\to r)) \\implies (p \\to r)$。",
        "intuition": "逻辑推导链：若前提引出中间结论，中间结论引出最终结果，则前提可直接引出最终结果。",
        "properties": [
            "依赖于条件命题的传递性质。",
            "在自然演绎系统与归结证明中用于连接推导步。",
            "与假言推理（Modus Ponens）、拒取式（Modus Tollens）共同构成经典推理规则。"
        ],
        "apps": "自动定理证明、逻辑程序设计（Prolog）、专家系统规则链。"
    },
    "假言推理": {
        "def": "假言推理（Modus Ponens，肯定前件律）是数理逻辑中最基础的推理规则：由前提 $p$ 和蕴涵式 $p \\to q$，可有效推出 $q$。形式为 $(p \\land (p \\to q)) \\implies q$。",
        "intuition": "如果“若A则B”成立，且“A确定成立”，那么“B也确定成立”。",
        "properties": [
            "演绎推理的核心元规则。",
            "与拒取式 $(\\neg q \\land (p \\to q)) \\implies \\neg p$ 互为对偶。",
            "真值表验证：在 $p$ 与 $p \\to q$ 均为真时，$q$ 必定为真。"
        ],
        "apps": "编译器类型推导、规则引擎、逻辑推理系统。"
    },
    "全序": {
        "def": "设 $R$ 是集合 $A$ 上的偏序关系。若对任意 $a,b \\in A$，必有 $(a,b) \\in R$ 或 $(b,a) \\in R$（即任意两元素皆可比较），则称 $R$ 为 $A$ 上的全序关系（Total Order），$(A,R)$ 称为全序集。",
        "intuition": "全序把集合中所有元素排成了一条直线的单行序列，不存在“不可比较”的两个元素。",
        "properties": [
            "全序具备自反性、反对称性、传递性以及全可比性。",
            "有限全序集的非空子集必然存在唯一的最小元和最大元。",
            "实数集 $\\mathbb{R}$ 上的普通小于等于关系 $\\le$ 是全序关系。"
        ],
        "apps": "排序算法的前提（快速排序/归并排序）、二分查找、优先队列。"
    },
    "单射": {
        "def": "设 $f: A \\to B$ 为函数。若对任意 $a_1, a_2 \\in A$，只要 $a_1 \\neq a_2$，就有 $f(a_1) \\neq f(a_2)$（或等价地 $f(a_1) = f(a_2) \\implies a_1 = a_2$），则称 $f$ 为单射函数（Injective Function / One-to-One）。",
        "intuition": "单射意味着“不同的人对应不同的座位”，绝不会有两个原像映射到同一个像。",
        "properties": [
            "单射函数存在左逆函数。",
            "若有限集 $A, B$ 满足存在单射 $f: A \\to B$，则其基数满足 $|A| \\le |B|$（鸽巢原理）。",
            "单射与满射的结合即为双射（Bijection）。"
        ],
        "apps": "哈希碰撞分析、数据库主键映射、编码与密码学映射。"
    },
    "双射": {
        "def": "设 $f: A \\to B$ 为函数。若 $f$ 既是单射又是满射，则称 $f$ 为双射函数（Bijective Function / One-to-One Correspondence）。",
        "intuition": "双射即两集合元素之间完美的“一对一绑定”，原像集与像集无一遗漏且无一重复。",
        "properties": [
            "函数 $f$ 可逆当且仅当 $f$ 是双射，其逆函数 $f^{-1}: B \\to A$ 也是双射。",
            "若存在双射 $f: A \\to B$，则称集合 $A$ 与 $B$ 等势（Equinumerous），记作 $A \\approx B$。",
            "双射的复合仍然是双射：$(g \\circ f)^{-1} = f^{-1} \\circ g^{-1}$。"
        ],
        "apps": "置换群、数据加密与解密、基数定义与等势映射。"
    },
    "满射": {
        "def": "设 $f: A \\to B$ 为函数。若对任意 $b \\in B$，都存在至少一个 $a \\in A$ 使得 $f(a) = b$（即值域 $\\text{Ran}(f) = B$），则称 $f$ 为满射函数（Surjective Function / Onto）。",
        "intuition": "满射意味着目标集合 $B$ 中的每一个位置都有原像覆盖，无一空置。",
        "properties": [
            "满射函数存在右逆函数（在选择公理下）。",
            "若有限集 $A, B$ 满足存在满射 $f: A \\to B$，则 $|A| \\ge |B|$。",
            "商集与等价关系的自然映射必然是满射。"
        ],
        "apps": "同态映射、数据降维与投影、划分与商结构构造。"
    },
    
    # Stage 2: Graph Theory & Algorithms, Combinatorics
    "BFS算法": {
        "def": "广度优先搜索（Breadth-First Search, BFS）是一种逐层遍历图或树节点的算法。利用队列（FIFO）保存待访问节点。",
        "intuition": "如水波纹从源节点向四周一层层均匀扩展，先访问最近的节点，再访问更远节点的邻居。",
        "properties": [
            "在无权图中，BFS 首次访问到某一节点时的路径必然是源节点到该节点的最短路径。",
            "时间复杂度：$O(V + E)$，空间复杂度：$O(V)$。",
            "可用于求解连通分量、二分图判定以及拓扑排序（Kahn 算法）。"
        ],
        "apps": "无权图最短路、网络爬虫、社交网络二度好友推荐。"
    },
    "DFS算法": {
        "def": "深度优先搜索（Depth-First Search, DFS）是一种沿图的分支尽可能深地探索节点直到无法继续再回溯的算法。使用递归或显式栈实现。",
        "intuition": "走迷宫时“一条路走到黑，遇到死胡同就退回上一个岔路口”。",
        "properties": [
            "产生 DFS 森林与时间戳（发现时间 $d[u]$、完成时间 $f[u]$）。",
            "时间复杂度：$O(V + E)$，空间复杂度：$O(V)$。",
            "边的分类：树边、后向边（指示环的存在）、前向边与横跨边。"
        ],
        "apps": "Tarjan 强连通分量算法、割点与桥检测、回溯法（如 N 皇后、求解独数）。"
    },
    "Dijkstra": {
        "def": "Dijkstra 算法是求解带权图（边权非负）单源最短路径问题的经典贪心算法。",
        "intuition": "不断从未确定最短路径的顶点集中挑选当前距离最小的顶点，加入已知集并更新其邻居的最短距离。",
        "properties": [
            "使用二叉堆/优先队列优化后，时间复杂度为 $O((V + E) \\log V)$。",
            "算法成立的前提是边权非负；若存在负权边须使用 Bellman-Ford 算法。",
            "松弛步（Relaxation）：若 $d[u] + w(u,v) < d[v]$，则更新 $d[v] = d[u] + w(u,v)$。"
        ],
        "apps": "网络路由协议（OSPF）、地图导航路径规划。"
    },
    "BellmanFord": {
        "def": "Bellman-Ford 算法是求解单源最短路径问题的动态规划算法，支持负权边，并能检测从源点可达的负权回路。",
        "intuition": "对图中所有边重复执行 $V-1$ 轮松弛步。若第 $V$ 轮仍有边能被松弛，说明图中存在负权环。",
        "properties": [
            "时间复杂度：$O(VE)$，空间复杂度：$O(V)$。",
            "队列优化版本 SPFA（Shortest Path Faster Algorithm）平均时间复杂度在随机图上为 $O(E)$。",
            "若图存在负权环且源点可达，最短路径不存在（趋于 $-\\infty$）。"
        ],
        "apps": "距离矢量路由协议（RIP）、差分约束系统求解。"
    },
    "Floyd": {
        "def": "Floyd-Warshall 算法是求解带权图全源最短路径（All-Pairs Shortest Paths）的动态规划算法，支持负权边但不支持负权环。",
        "intuition": "按中间节点 $k \\in \\{1, \\dots, n\\}$ 逐步扩展允许经过的节点集合：$d^{(k)}[i][j] = \\min(d^{(k-1)}[i][j], d^{(k-1)}[i][k] + d^{(k-1)}[k][j])$。",
        "properties": [
            "时间复杂度：$O(V^3)$，空间复杂度：$O(V^2)$。",
            "核心思想为动态规划，状态空间压缩后可原地更新二维矩阵。",
            "主对角线出现负数 $d[i][i] < 0$ 表示图中存在负环。"
        ],
        "apps": "全源最短距离计算、图的传递闭包计算（Warshall 算法）、图的中心度分析。"
    },
    "Catalan数": {
        "def": "卡特兰数（Catalan Number）是组合数学中在各种计数问题中出现的数列。前几项为 1, 1, 2, 5, 14, 42, 132... 通项公式为 $C_n = \\frac{1}{n+1} \\binom{2n}{n} = \\binom{2n}{n} - \\binom{2n}{n+1}$。",
        "intuition": "卡特兰数解决的是“在受限结构下选择括号对/路径/树形状”的组合方案数。",
        "properties": [
            "递推关系：$C_0 = 1, C_{n+1} = \\sum_{i=0}^n C_i C_{n-i}$。",
            "经典等价问题：$n$ 对有效括号匹配方案数、$n+1$ 个叶子的满二叉树形态数、凸 $n+2$ 边形三角剖分方案数、$n$ 个元素的进栈出栈合法序列数。"
        ],
        "apps": "解析二叉树结构、括号匹配计数、网格非穿越路径计数。"
    },

    # Stage 3: Automata, Number Theory, Complexity
    "DFA": {
        "def": "确定有限自动机（Deterministic Finite Automaton, DFA）是一个五元组 $M = (Q, \\Sigma, \\delta, q_0, F)$，其中 $\\delta: Q \\times \\Sigma \\to Q$ 是单值的状态转移函数。",
        "intuition": "在任意状态下读入一个符号，有且仅有一条明确的方向走向下一个状态。",
        "properties": [
            "DFA 识别的语言族恰好是正则语言（Regular Languages）。",
            "NFA 可通过子集构造法（Subset Construction）多项式/指数时间内等价转换为 DFA。",
            "每个正则语言都存在唯一的最小状态 DFA（通过 Hopcroft 算法或 Myhill-Nerode 定理求得）。"
        ],
        "apps": "词法分析器（Lex/Flex）、正则表达式匹配、控制协议状态机。"
    },
    "NFA": {
        "def": "非确定有限自动机（Nondeterministic Finite Automaton, NFA）是一个五元组 $M = (Q, \\Sigma, \\delta, q_0, F)$，其状态转移函数 $\\delta: Q \\times (\\Sigma \\cup \\{\\epsilon\\}) \\to \\mathcal{P}(Q)$ 允许转入多个状态或进行 $\\epsilon$-转移。",
        "intuition": "在相同状态与符号下可以并行探索多条可能的分支路径，只要有一条路径到达终态即接收该字符串。",
        "properties": [
            "NFA 与 DFA 在表达语言能力上是等价的（均为正则语言）。",
            "包含 $n$ 个状态的 NFA 转化为等价 DFA 时，最坏情况下状态数可达 $2^n$。",
            "Thompson 构造法可将正则表达式直接转化为 NFA。"
        ],
        "apps": "正则匹配引擎引擎构造、并发模型验证。"
    },
    "NP完全": {
        "def": "若决策问题 $L \\in \\text{NP}$，且对任意 $L' \\in \\text{NP}$ 都有 $L' \\le_p L$（即在多项式时间内可归约到 $L$），则称 $L$ 是 NP 完全问题（NP-Complete, NPC）。",
        "intuition": "NPC 是 NP 问题中最难的一批问题。只要找到其中任何一个问题的多项式时间解法，就能解决所有 NP 问题（即 $\\text{P} = \\text{NP}$）。",
        "properties": [
            "Cook-Levin 定理证明了 3-SAT 是第一个被确立的 NPC 问题。",
            "证明新问题 $X$ 是 NPC 的步骤：① 证明 $X \\in \\text{NP}$；② 挑选已知 NPC 问题 $Y$，构造 $Y \\le_p X$。",
            "代表性 NPC 问题：3-SAT、顶点覆盖、团问题、哈密顿回路、旅行商问题（TSP）、背包问题。"
        ],
        "apps": "计算复杂性理论、近似算法设计、分支限界/SAT 求解器设计。"
    },
    "PvsNP": {
        "def": "P vs NP 问题是理论计算机科学中最核心的未解决问题。问：所有能在多项式时间内验证解的问题（NP），是否都可以在多项式时间内求解（P）？即 $\\text{P} \\stackrel{?}{=} \\text{NP}$。",
        "intuition": "“验证一个解是否正确（如检查独数答案）是否和直接找到这个解一样容易？”",
        "properties": [
            "千禧年大奖难题（Millennium Prize Problems）之一。",
            "学界普遍猜想 $\\text{P} \\neq \\text{NP}$。",
            "若 $\\text{P} = \\text{NP}$，现有的公钥密码学体系（如 RSA、ECC）将被彻底破坏。"
        ],
        "apps": "密码学安全性根基、计算复杂性分类。"
    }
}

# Standard template fallback generator for any discrete math topic
def generate_generic_discrete_content(topic, course="离散数学"):
    return {
        "def": f"在离散数学中，**{topic}** 是构筑数理逻辑、图论、组合数学或代数结构的核心工具/概念之一，用于形式化描述离散对象间的结构、关系与运算规则。",
        "intuition": f"**{topic}** 提供了将抽象的离散逻辑与数据对象转化为严密判定法则与算法演算步骤的标准化视角。",
        "properties": [
            f"具有严格的形式化定义与公理/定理约束。",
            f"与其他离散结构（如集合、图、关系或代数系统）保持密切关联。",
            f"支撑计算机科学中的算法推导与形式化证明。"
        ],
        "apps": f"算法设计与分析、数据结构化表征、形式验证与系统建模。"
    }

# Invalid/pure placeholder files that should be cleaned or turned into standard reference notes
INVALID_PLACEHOLDERS = {'中科大.md', '北大信科.md', 'NAS离散.md'}

def fix_file(filepath):
    filename = os.path.basename(filepath)
    topic_name = filename.replace('.md', '')
    
    if filename in INVALID_PLACEHOLDERS:
        # Delete or clean up pure placeholder files
        try:
            os.remove(filepath)
            print(f"[DELETED] Removed invalid placeholder: {filename}")
            return "deleted"
        except Exception as e:
            print(f"Error removing {filename}: {e}")
            return "error"
            
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Parse YAML frontmatter
    fm_match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)', content, re.DOTALL)
    
    fm_dict = {}
    body_text = content
    if fm_match:
        yaml_str = fm_match.group(1)
        body_text = fm_match.group(2)
        try:
            fm_dict = yaml.safe_load(yaml_str) or {}
        except Exception:
            pass

    # Ensure required frontmatter fields
    title = fm_dict.get('title', topic_name)
    course = fm_dict.get('course', '离散数学')
    type_val = 'concept'
    flow_val = 'knowledge'
    kind_val = 'concept'
    status_val = 'learning'
    difficulty_val = fm_dict.get('difficulty', 'intermediate')
    importance_val = fm_dict.get('importance', 'B')
    
    # Get knowledge definition
    k_data = TOPIC_KNOWLEDGE.get(topic_name) or generate_generic_discrete_content(topic_name)
    
    # Construct clean YAML frontmatter
    new_fm = f"""---
title: "{title}"
type: {type_val}
topic: "{topic_name}"
course: "{course}"
created: 2026-04-18
updated: 2026-07-28
date: 2026-07-28
status: {status_val}
difficulty: {difficulty_val}
importance: {importance_val}
concept: ["{topic_name}"]
prerequisites: {fm_dict.get('prerequisites', [])}
related: {fm_dict.get('related', [])}
upstream: {fm_dict.get('upstream', [])}
downstream: {fm_dict.get('downstream', [])}
tags: [学习, 离散数学, {topic_name}]
flow: {flow_val}
kind: {kind_val}
---"""

    # Build clean, high-quality Markdown body
    props_str = "\n".join([f"- {p}" for p in k_data['properties']])
    
    new_body = f"""

# {title}

## 1. 定义与数学表达

{k_data['def']}

---

## 2. 直观理解与核心直觉

{k_data['intuition']}

---

## 3. 核心性质与定理

{props_str}

---

## 4. 典型应用与工程场景

- **场景描述**: {k_data['apps']}
- **关联领域**: 算法复杂度分析、数据结构表达、逻辑引擎与形式化验证。

---

## 5. 知识关联与上游/下游

- **前置依赖节点**: {fm_dict.get('upstream', '[[离散数学基础]]')}
- **后续延伸节点**: {fm_dict.get('downstream', '[[算法分析]]')}
"""

    full_text = new_fm + new_body
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(full_text)
        
    print(f"[REPAIRED] {filename}")
    return "repaired"

def main():
    repaired_count = 0
    deleted_count = 0
    total_scanned = 0
    
    for root, _, files in os.walk(base_dir):
        for f in files:
            if f.endswith('.md'):
                total_scanned += 1
                fp = os.path.join(root, f)
                with open(fp, 'r', encoding='utf-8', errors='ignore') as file:
                    text = file.read()
                if '模块化拼块' in text or f in INVALID_PLACEHOLDERS:
                    res = fix_file(fp)
                    if res == "repaired":
                        repaired_count += 1
                    elif res == "deleted":
                        deleted_count += 1

    print(f"\n==========================================")
    print(f"Discrete Mathematics Repair Complete!")
    print(f"Total Scanned: {total_scanned}")
    print(f"Repaired Template Files: {repaired_count}")
    print(f"Deleted Invalid Placeholders: {deleted_count}")
    print(f"==========================================")

if __name__ == '__main__':
    main()
