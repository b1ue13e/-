import sys
import os
import glob
import re
import shutil

sys.stdout.reconfigure(encoding='utf-8')
root_dir = r'f:\-'

# 1. Action: Delete backup directory
backup_dir = os.path.join(root_dir, r'99-System\tmp\backup_20260727_01空心卡')
if os.path.exists(backup_dir):
    print(f"Deleting backup directory: {backup_dir}")
    shutil.rmtree(backup_dir)
    print("Backup directory successfully deleted.")
else:
    print("Backup directory does not exist or was already deleted.")

# 2. Define the 16 merge pairs: (concept_name, main_path, secondary_path)
merge_pairs = [
    (
        "BLIP",
        r"02-Knowledge\🧠 学习系统\05-计算机视觉\04-前沿架构探索\BLIP.md",
        r"02-Knowledge\🧠 学习系统\08-NLP全栈\06-专业方向深入\BLIP.md"
    ),
    (
        "LLaVA",
        r"02-Knowledge\🧠 学习系统\05-计算机视觉\04-前沿架构探索\LLaVA.md",
        r"02-Knowledge\🧠 学习系统\08-NLP全栈\06-专业方向深入\LLaVA.md"
    ),
    (
        "LayerNorm",
        r"02-Knowledge\🧠 学习系统\08-NLP全栈\04-Transformer与预训练模型\LayerNorm.md",
        r"02-Knowledge\🧠 学习系统\05-计算机视觉\02-深度学习内核\LayerNorm.md"
    ),
    (
        "LoRA",
        r"02-Knowledge\🧠 学习系统\08-NLP全栈\04-Transformer与预训练模型\LoRA.md",
        r"02-Knowledge\🧠 学习系统\05-计算机视觉\04-前沿架构探索\LoRA.md"
    ),
    (
        "Lyapunov稳定",
        r"02-Knowledge\🧠 学习系统\06-常微分方程\03-进阶\Lyapunov稳定.md",
        r"02-Knowledge\🧠 学习系统\15-控制与机器人学\05-状态空间与现代控制\Lyapunov稳定.md"
    ),
    (
        "二分图匹配",
        r"02-Knowledge\🧠 学习系统\10-数据结构与算法\04-图论基础\二分图匹配.md",
        r"02-Knowledge\🧠 学习系统\04-离散数学\02-核心深化\二分图匹配.md"
    ),
    (
        "协方差矩阵",
        r"02-Knowledge\🧠 学习系统\16-多元统计\01-基础矩阵\协方差矩阵.md",
        r"02-Knowledge\🧠 学习系统\15-控制与机器人学\10-状态估计\协方差矩阵.md"
    ),
    (
        "卡尔曼滤波",
        r"02-Knowledge\🧠 学习系统\14-概率图模型\05-隐马尔可夫模型\卡尔曼滤波.md",
        r"02-Knowledge\🧠 学习系统\15-控制与机器人学\卡尔曼滤波.md"
    ),
    (
        "感知机",
        r"02-Knowledge\🧠 学习系统\17-机器学习\03-正则优化\感知机.md",
        r"02-Knowledge\🧠 学习系统\05-计算机视觉\02-深度学习内核\感知机.md"
    ),
    (
        "极点",
        r"02-Knowledge\🧠 学习系统\12-信号与系统\04-变换篇-拉普拉斯\极点.md",
        r"02-Knowledge\🧠 学习系统\37-复变函数\04-级数奇点留数与应用\极点.md"
    ),
    (
        "欧拉公式",
        r"02-Knowledge\🧠 学习系统\12-信号与系统\01-基础篇-兵器库\欧拉公式.md",
        r"02-Knowledge\🧠 学习系统\04-离散数学\02-核心深化\欧拉公式.md"
    ),
    (
        "特征工程",
        r"02-Knowledge\🧠 学习系统\17-机器学习\01-基础概念\特征工程.md",
        r"02-Knowledge\🧠 学习系统\03-量化金融\02-量化核心技能\特征工程.md"
    ),
    (
        "线性ODE",
        r"02-Knowledge\🧠 学习系统\06-常微分方程\01-入门\线性ODE.md",
        r"02-Knowledge\🧠 学习系统\15-控制与机器人学\01-控制地基\线性ODE.md"
    ),
    (
        "背包问题",
        r"02-Knowledge\🧠 学习系统\10-数据结构与算法\05-算法思想进阶\背包问题.md",
        r"02-Knowledge\🧠 学习系统\04-离散数学\04-融会贯通\背包问题.md"
    ),
    (
        "谱聚类",
        r"02-Knowledge\🧠 学习系统\17-机器学习\04-无监督学习\谱聚类.md",
        r"02-Knowledge\🧠 学习系统\01-社交网络挖掘\谱聚类.md"
    ),
    (
        "预测方程推导",
        r"02-Knowledge\🧠 学习系统\15-控制与机器人学\09-MPC深入\预测方程推导.md",
        r"02-Knowledge\🧠 学习系统\15-控制与机器人学\20-推导笔记\预测方程推导.md"
    )
]

def ensure_concept_in_frontmatter(content, concept_name):
    if 'concept:' in content:
        # Check if concept_name already present
        if concept_name in content:
            return content
        # Add to existing concept array
        content = re.sub(r'concept:\s*\[(.*?)\]', rf'concept: [\1, "{concept_name}"]', content)
        content = content.replace('", "', '", "').replace('[, ', '[')
        return content
    else:
        # Insert concept before tags or created
        if '---' in content:
            parts = content.split('---', 2)
            fm = parts[1]
            new_fm = fm.rstrip() + f'\nconcept: ["{concept_name}"]\n'
            return f"---{new_fm}---" + parts[2]
        return content

print("\nProcessing 16 merge groups...")
success_count = 0

for concept_name, rel_main, rel_sec in merge_pairs:
    abs_main = os.path.join(root_dir, rel_main)
    abs_sec = os.path.join(root_dir, rel_sec)
    
    main_name = os.path.splitext(os.path.basename(abs_main))[0]
    
    # 1. Update main card frontmatter
    if os.path.exists(abs_main):
        with open(abs_main, 'r', encoding='utf-8', errors='ignore') as f:
            m_content = f.read()
        new_m_content = ensure_concept_in_frontmatter(m_content, concept_name)
        with open(abs_main, 'w', encoding='utf-8') as f:
            f.write(new_m_content)
        print(f"✅ [主卡更新概念] {concept_name} -> {rel_main}")
    else:
        print(f"⚠️ 主卡不存在: {abs_main}")
        
    # 2. Replace secondary card with redirection card
    if os.path.exists(abs_sec):
        redirect_content = f"""---
type: study
topic: "{concept_name}（重定向）"
tags: [学习, 重定向]
concept: ["{concept_name}"]
created: 2026-07-27
redirect_to: "[[{main_name}]]"
---

> [!NOTE] 知识重定向
> 本概念的主主题卡片已统一收录于底层学科目录中：
> 👉 **[[{main_name}]]**
> 
> 请直接点击上方双链跳转至主卡阅读完整直观理解、推导与代码实现。
"""
        with open(abs_sec, 'w', encoding='utf-8') as f:
            f.write(redirect_content)
        print(f"🔄 [副卡替换为双链重定向] {rel_sec} -> [[{main_name}]]")
        success_count += 1
    else:
        print(f"⚠️ 副卡不存在: {abs_sec}")

print(f"\n全部完成！处理成功 {success_count}/16 组物理知识卡。")

