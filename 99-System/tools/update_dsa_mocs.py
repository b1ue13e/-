import sys, os, glob, re

sys.stdout.reconfigure(encoding='utf-8')

kb_root = r'f:\-\02-Knowledge\🧠 学习系统\10-数据结构与算法'

stages = [
    ('00-前置知识', '🧭 数据结构与算法-前置知识.md', '前置知识', '第 0 阶段 - 基础支架与能力诊断', '[[🧭 阶段1-算法入门与基本分析]]'),
    ('01-算法入门与基本分析', '🧭 阶段1-算法入门与基本分析.md', '阶段1-算法入门与基本分析', '第 1 阶段 - 算法入门与基本分析', '[[🧭 阶段2-线性数据结构]]'),
    ('02-线性数据结构', '🧭 阶段2-线性数据结构.md', '阶段2-线性数据结构', '第 2 阶段 - 线性数据结构', '[[🧭 阶段3-树与堆]]'),
    ('03-树与堆', '🧭 阶段3-树与堆.md', '阶段3-树与堆', '第 3 阶段 - 树与堆', '[[🧭 阶段4-图论基础]]'),
    ('04-图论基础', '🧭 阶段4-图论基础.md', '阶段4-图论基础', '第 4 阶段 - 图论基础', '[[🧭 阶段5-算法思想进阶]]'),
    ('05-算法思想进阶', '🧭 阶段5-算法思想进阶.md', '阶段5-算法思想进阶', '第 5 阶段 - 算法思想进阶', '[[🧭 阶段6-高级与综合训练]]'),
    ('06-高级与综合训练', '🧭 阶段6-高级与综合训练.md', '阶段6-高级与综合训练', '第 6 阶段 - 高级与综合训练', '[[🗺️ 数据结构与算法学习路径]]')
]

for s_dir, moc_file, title_tag, stage_desc, next_stage in stages:
    dir_path = os.path.join(kb_root, s_dir)
    moc_path = os.path.join(dir_path, moc_file)
    
    # Collect all knowledge cards in this directory
    cards = []
    if os.path.exists(dir_path):
        for f in sorted(os.listdir(dir_path)):
            if f.endswith('.md') and not f.startswith('🧭') and f not in ['🗺️ 数据结构与算法学习路径.md', '📚 教材挂载索引.md']:
                stem = os.path.splitext(f)[0]
                cards.append(f'[[{stem}]]')
                
    card_links_text = '\n'.join([f'- [ ] {c}' for c in cards])
    
    content = f'''---
title: "{moc_file.replace('.md', '')}"
type: study
topic: "{title_tag}"
course: "数据结构与算法"
created: 2026-07-28
updated: 2026-08-06
status: active
flow: knowledge
kind: moc
tags:
  - 学习
  - 数据结构与算法
  - MOC
  - {title_tag}
---

# {moc_file.replace('.md', '')}

> **所属课程**：数据结构与算法  
> **阶段定位**：{stage_desc}  
> **学习目标**：系统掌握本阶段核心数据结构模型与算法推导，建立可复用的算法思维。

---

## 核心导航

- **课程总入口**：[[🗺️ 数据结构与算法学习路径]]
- **下一阶段衔接**：{next_stage}

---

## 阶段目标

1. 掌握该阶段的核心数据组织形式与算法原理解析。
2. 熟练书写标准 C++ / Python 代码实现，并通过测试验证。
3. 掌握复杂度分析与典型场景下的边界条件处理。

---

## 为什么现在学

数据结构与算法呈阶梯递进。本阶段知识承上启下，为后续更复杂的算法思想与工程应用打下坚实基础。

---

## 有序知识卡

{card_links_text}

---

## 阶段验收与作业

### 对应作业
- **完整作业包**：[[03-Projects/课程作业/10-数据结构与算法/课程作业总表|数据结构与算法完整作业包]]
- **作业索引**：[[03-Projects/10-数据结构与算法/🧭 课程作业总索引|课程作业总索引]]
'''
    with open(moc_path, 'w', encoding='utf-8') as fp:
        fp.write(content)
    print(f'Updated MOC: {moc_file} ({len(cards)} cards registered)')

print('All Stage MOCs updated successfully!')
