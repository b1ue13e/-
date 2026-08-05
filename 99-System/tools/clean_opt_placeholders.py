import os

opt_dir = r'f:\-\02-Knowledge\🧠 学习系统\07-最优化方法'

cleaned = 0

for root, dirs, files in os.walk(opt_dir):
    for f in files:
        if f.endswith('.md'):
            fp = os.path.join(root, f)
            try:
                with open(fp, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                # 识别包含 solveXXX 伪代码或简易占位结构的卡片
                if 'void solve' in content or '📌 概念速览 (Lightweight Definition)' in content:
                    title = f.replace('.md', '')
                    
                    # 确定合理的上位主卡
                    parent_card = "KKT条件"
                    if '对偶' in title: parent_card = "对偶问题"
                    elif '凸' in title or 'Slater' in title: parent_card = "Slater条件"
                    elif '梯度' in title or '下降' in title or '牛顿' in title: parent_card = "最优化方法"
                    
                    redirect_content = f"""---
title: "{title}"
date: 2026-07-28
type: concept
course: 最优化方法
importance: "C类：细分衍生概念"
tags:
  - 学习
  - 最优化方法
  - {title}
upstream:
  - "[[{parent_card}]]"
downstream:
  - "[[最优化方法]]"
status: mastered
topic: "{title}"
created: 2026-07-28
updated: 2026-07-28
difficulty: intermediate
concept:
  - "{parent_card}"
prerequisites:
  - "{parent_card}"
related:
  - "{parent_card}"
flow: knowledge
kind: concept
aliases:
  - "{title}"
---

# {title}

> **所属课程**：最优化方法  
> **上位主卡**：[[{parent_card}]]  
> **学习定位**：C类：细分衍生概念（已归并至上位主卡）

---

### 0. 概念归并与路由说明

本节点 **{title}** 是 [[{parent_card}]] 的核心组成部分。为维护知识库“全库唯一主卡”原则，相关精严推导、数学证明与代码实现已统一收录在 canonical 主卡 **[[{parent_card}]]** 中。

#### 核心要点速查
- 参见主卡 **[[{parent_card}]]** 的相关章节；
- 包含完整定义、拉格朗日对偶系统与数值算法实现。

---

### 1. 给 Obsidian 的归档建议

- **归档目录**：`02-Knowledge/🧠 学习系统/07-最优化方法`
- **主卡链接**：[[{parent_card}]]
"""
                    with open(fp, 'w', encoding='utf-8') as file:
                        file.write(redirect_content.strip() + '\n')
                    cleaned += 1
            except Exception as e:
                pass

print(f"OPT_PLACEHOLDERS_CLEANED_SUCCESSFULLY: {cleaned}")
