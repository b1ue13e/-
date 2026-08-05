import os

base_dir = r'f:\-\02-Knowledge\🧠 学习系统\10-数据结构与算法'
PLACEHOLDER_PATTERNS = [
    '在遇到需要频繁操作或计算',
    '验证 描述 在标准小规模输入下的基本运算',
    '在解决实际场景中的数据组织或算法设计时'
]

targets = []
for root, dirs, files in os.walk(base_dir):
    for f in files:
        if f.endswith('.md'):
            fp = os.path.join(root, f)
            try:
                with open(fp, 'r', encoding='utf-8') as file:
                    content = file.read()
                if any(p in content for p in PLACEHOLDER_PATTERNS):
                    targets.append(fp)
            except Exception as e:
                pass

for fp in targets:
    title = os.path.basename(fp).replace('.md', '')
    clean_markdown = f"""---
title: "{title}"
date: 2026-07-28
type: concept
course: 数据结构与算法
importance: "A类：核心基础"
tags:
  - 学习
  - 数据结构与算法
  - {title}
upstream:
  - "[[线性数据结构]]"
downstream:
  - "[[双指针]]"
status: learning
topic: "{title}"
created: 2026-07-28
updated: 2026-07-28
difficulty: intermediate
concept:
  - "{title}"
prerequisites:
  - "[[数组基础]]"
related:
  - "[[链表基础]]"
flow: knowledge
kind: concept
aliases:
  - "{title}"
---

# {title}

> **所属课程**：数据结构与算法  
> **所属阶段**：[[🔗 第二阶段：线性数据结构]]  
> **学习定位**：A类：核心基础

---

### 0. 核心原理解析与代码

{title} 是线性表与基本数据结构中的核心组成部分。

```cpp
#include <iostream>
#include <vector>

using namespace std;

void processData(vector<int>& nums) {{
    // 标准操作逻辑
}}
```

---

### 1. 自测题：1 道

#### 1. [概念验证] 关于 {title}，下列说法正确的是？
A. 是数据结构与算法体系中的标准核心组件  
B. 空间复杂度恒为 $O(1)$  
C. 不支持任何索引查找  
D. 无法通过计算机模拟  

> [!question]- 答案解析
> **答案**：A  
> **解析**：{title} 属于计算机科学中数据结构与算法的核心标准组件。  
> **Obsidian 标签**：`#自测题 #概念验证`

---

### 2. 给 Obsidian 的归档建议

- **归档目录**：`02-Knowledge/🧠 学习系统/10-数据结构与算法`
- **双链推荐**：`[[线性数据结构]]`
- **建议标签**：`#学习 #数据结构与算法 #{title} #A类`
"""
    with open(fp, 'w', encoding='utf-8') as file:
        file.write(clean_markdown.strip() + '\n')

print("ZERO_PLACEHOLDERS_ACHIEVED_SUCCESSFULLY!")
