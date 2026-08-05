import os

vault_dir = r'f:\-\02-Knowledge\🧠 学习系统'

# 需要转换的应用卡字典映射：(原相对路径, 理论主卡名, 新领域应用文件名, 领域名称, 专有物理/工程内容)
app_conversions = [
    # 1. 二分图 - 运筹学
    (r"29-运筹学\02-整数与网络优化\整数与网络优化-匹配与指派-二分图.md",
     "二分图", "二分图-指派应用", "运筹学",
     "在运筹学中，二分图主要用于解决**任务指派问题（Assignment Problem）与最大权匹配问题**。由于二分图的关联矩阵满足**全单模性（Totally Unimodular）**，其线性规划松弛解必定为整数解，直接保证了用单纯形法或匈牙利算法求解的有效性。"),
     
    # 2. 邻接矩阵 - GNN
    (r"23-图神经网络\01-图学习基础\图学习基础-图表示基础-邻接矩阵.md",
     "邻接矩阵", "邻接矩阵-图卷积应用", "图神经网络",
     "在图神经网络（GNN）中，邻接矩阵 $A$ 加上自环被重新定义为 $\tilde{A} = A + I_N$。对 $\tilde{A}$ 进行对称归一化 $\tilde{D}^{-1/2} \tilde{A} \tilde{D}^{-1/2}$，直接构成了 GCN（图卷积网络）的核心图卷积算子。"),

    # 3. 正规方程 - 泛函分析
    (r"27-泛函分析\02-Hilbert与基本定理\Hilbert与基本定理-应用入口-正规方程.md",
     "正规方程", "正规方程-Hilbert投影应用", "泛函分析",
     "在泛函分析与 Hilbert 空间理论中，正规方程 $A^T A x = A^T b$ 代表了**最佳逼近定理与正交投影定理（Orthogonal Projection Theorem）**。解 $x$ 是使误差向量 $b - Ax$ 垂直于 $A$ 的值域空间的唯一正交投影。"),

    # 4. 卷积定理 - 实变函数
    (r"26-实变函数\04-Fourier与应用\Fourier与应用-Fourier 变换-卷积定理.md",
     "卷积定理", "卷积定理-Fourier分析应用", "实变函数",
     "在实变函数与调和分析中，卷积定理表明 $L^1$ 或 $L^2$ 函数空间上的卷积在 Fourier 变换下转化为逐点乘积：$\mathcal{F}\{f * g\} = \mathcal{F}\{f\} \cdot \mathcal{F}\{g\}$。"),

    # 5. 经验分布函数 - 非参数统计
    (r"32-非参数统计\01-经验分布与秩统计\经验分布与秩统计-经验分布-经验分布函数.md",
     "经验分布函数", "经验分布函数-非参统计应用", "非参数统计",
     "在非参数统计中，经验分布函数 $F_n(x)$ 是总体累积分布函数 $F(x)$ 的无偏估计。依据 **Glivenko-Cantelli 定理（非参数统计基本定理）**，$F_n(x)$ 依概率全域一致收敛于 $F(x)$，并用于 Kolmogorov-Smirnov (K-S) 假设检验。"),

    # 6. LP松弛 - 运筹学
    (r"29-运筹学\02-整数与网络优化\整数与网络优化-求解策略-LP 松弛.md",
     "LP松弛", "LP松弛-分支定界应用", "运筹学",
     "在运筹整数规划中，LP 松弛通过去掉变量的整数约束，将其转化为普通线性规划。求解 LP 松弛获得下界，作为分支定界法（Branch and Bound）的剪枝依据。"),

    # 7. 矩阵转置 / Cramer法则 / 特征值 - ODE前置卡
    (r"06-常微分方程\00-前置知识准备\矩阵转置-ODE前置.md",
     "矩阵转置", "矩阵转置-ODE应用", "常微分方程",
     "在 ODE 一阶线性微分方程组 $\dot{x} = Ax$ 中，矩阵转置用于构造伴随方程组 $\dot{y} = -A^T y$ 以及对称矩阵的正交对角化。"),

    (r"06-常微分方程\00-前置知识准备\Cramer法则-ODE前置.md",
     "Cramer法则", "Cramer法则-ODE应用", "常微分方程",
     "在常微分方程非齐次线性方程组的**常数变易法（Variation of Parameters）**中，Cramer 法则用于显式求解朗斯基（Wronskian）行列式方程组。"),

    (r"06-常微分方程\00-前置知识准备\特征值定义-ODE前置.md",
     "特征值定义", "特征值定义-ODE应用", "常微分方程",
     "在线性常微分方程组中，系数矩阵 $A$ 的特征值 $\lambda$ 直接决定了系统平衡点的稳定性（渐近稳定、临界稳定、不稳定）与相图轨迹。")
]

converted_count = 0

for old_rel, main_card, new_title, course, domain_text in app_conversions:
    old_fp = os.path.join(vault_dir, old_rel)
    if os.path.exists(old_fp):
        dir_name = os.path.dirname(old_fp)
        new_fp = os.path.join(dir_name, f"{new_title}.md")
        
        content = f"""---
title: "{new_title}"
date: 2026-07-28
type: concept
course: {course}
importance: "A类：领域应用卡"
tags:
  - 学习
  - {course}
  - {main_card}
upstream:
  - "[[{main_card}]]"
downstream:
  - "[[{course}]]"
status: learning
topic: "{new_title}"
created: 2026-07-28
updated: 2026-07-28
difficulty: intermediate
concept:
  - "{main_card}"
prerequisites:
  - "{main_card}"
related:
  - "{main_card}"
flow: knowledge
kind: concept
aliases:
  - "{new_title}"
---

# {new_title}

> **所属课程**：{course}  
> **理论主卡**：[[{main_card}]] (理论主卡)  
> **学习定位**：A类：领域应用卡

---

### 0. 领域应用背景

本卡片为 **[[{main_card}]]** 在 **{course}** 领域中的专业应用卡。不重复复制理论主卡的基础定义与推导，专注记录该领域特有的建模流程、代码与工程细节。

{domain_text}

---

### 1. 自测题：1 道

#### 1. [领域应用] 关于 {new_title}，下列说法正确的是？
A. 必须显式引用理论主卡 [[{main_card}]]，且专注记录领域特有应用  
B. 空间复杂度恒为 $O(1)$  
C. 不支持任何数学推导  
D. 与理论主卡完全无关  

> [!question]- 答案解析
> **答案**：A  
> **解析**：遵循全库唯一主卡规范，领域应用卡专注于领域特有的建模与应用，基础定义统一收录在理论主卡 [[{main_card}]] 中。  
> **Obsidian 标签**：`#自测题 #领域应用`

---

### 2. 给 Obsidian 的归档建议

- **归档目录**：`02-Knowledge/🧠 学习系统/{course}`
- **理论主卡**：[[{main_card}]]
"""
        with open(new_fp, 'w', encoding='utf-8') as f:
            f.write(content.strip() + '\n')
            
        # 若旧文件名与新文件名不同，删除旧文件
        if old_fp != new_fp:
            os.remove(old_fp)
        converted_count += 1
        print(f"Converted: {old_rel} -> {new_title}.md")

print(f"=== BATCH APP CARDS CONVERSION COMPLETED: {converted_count} files ===")
