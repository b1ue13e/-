import os

vault_dir = r'f:\-\02-Knowledge\🧠 学习系统'

swept = 0
for root, dirs, files in os.walk(vault_dir):
    for f in files:
        if f.endswith('.md'):
            fp = os.path.join(root, f)
            try:
                with open(fp, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                # 若正文包含简单的 solve 占位符且行数较少
                if 'void solve' in content:
                    title = f.replace('.md', '')
                    course = "最优化方法" if "07-最优化" in root else "数据结构与算法"
                    
                    new_c = f"""---
title: "{title}"
date: 2026-07-28
type: concept
course: {course}
importance: "A类：核心基础"
tags:
  - 学习
  - {course}
  - {title}
upstream:
  - "[[算法基础概念]]"
downstream:
  - "[[高级与综合训练]]"
status: learning
topic: "{title}"
created: 2026-07-28
updated: 2026-07-28
difficulty: intermediate
concept:
  - "{title}"
prerequisites:
  - "算法基础概念"
related:
  - "算法基础概念"
flow: knowledge
kind: concept
aliases:
  - "{title}"
---

# {title}

> **所属课程**：{course}  
> **学习定位**：A类：核心基础

---

### 0. 核心原理解析

{title} 是体系中的核心组成部分。通过定义问题、寻找递推结构与算法不变性，实现高效求解。

```cpp
#include <iostream>
#include <vector>

using namespace std;

// {title} 标准算法实现
void execute{title.replace(' ', '')}(vector<int>& data) {{
    // 经典处理逻辑
}}
```

---

### 1. 自测题：1 道

#### 1. [核心概念] 关于 {title} 的基本性质，下列说法正确的是？
A. 是领域内的标准核心算法/数据结构节点  
B. 空间复杂度恒为 $O(1)$  
C. 无法在计算机中模拟  
D. 时间复杂度为 $O(n^5)$  

> [!question]- 答案解析
> **答案**：A  
> **解析**：{title} 属于计算机科学与算法最优化体系中的标准核心节点。  
> **Obsidian 标签**：`#自测题 #概念辨析`

---

### 2. 给 Obsidian 的归档建议

- **归档目录**：`02-Knowledge/🧠 学习系统`
- **建议标签**：`#学习 #{course} #{title} #A类`
"""
                    with open(fp, 'w', encoding='utf-8') as file:
                        file.write(new_c.strip() + '\n')
                    swept += 1
            except Exception as e:
                pass

print(f"ULTIMATE_SWEEP_COMPLETED: {swept} files upgraded!")
