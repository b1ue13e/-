import sys
import os
import re

sys.stdout.reconfigure(encoding='utf-8')
root_dir = r'f:\-'

# Definition of Category 2 (Theory vs Application) renames:
# (old_rel_path, new_filename, new_topic, concept_tag, theory_link)
cat2_tasks = [
    (
        r"02-Knowledge\🧠 学习系统\03-量化金融\02-量化核心技能\ARIMA模型.md",
        "量化金融-ARIMA策略应用.md",
        "量化金融-ARIMA策略应用",
        "ARIMA模型",
        "[[ARIMA模型]]"
    ),
    (
        r"02-Knowledge\🧠 学习系统\03-量化金融\02-量化核心技能\GARCH模型.md",
        "量化金融-GARCH波动率策略.md",
        "量化金融-GARCH波动率策略",
        "GARCH模型",
        "[[GARCH模型]]"
    ),
    (
        r"02-Knowledge\🧠 学习系统\03-量化金融\02-量化核心技能\协整.md",
        "量化金融-配对交易与协整策略.md",
        "量化金融-配对交易与协整策略",
        "协整",
        "[[协整]]"
    ),
    (
        r"02-Knowledge\🧠 学习系统\03-量化金融\02-量化核心技能\单位根检验.md",
        "量化金融-平稳性与单位根检验实战.md",
        "量化金融-平稳性与单位根检验实战",
        "单位根检验",
        "[[单位根检验]]"
    ),
    (
        r"02-Knowledge\🧠 学习系统\03-量化金融\02-量化核心技能\残差诊断.md",
        "量化金融-模型残差诊断实战.md",
        "量化金融-模型残差诊断实战",
        "残差诊断",
        "[[残差诊断]]"
    ),
    (
        r"02-Knowledge\🧠 学习系统\03-量化金融\02-量化核心技能\误差修正模型.md",
        "量化金融-ECM套利策略.md",
        "量化金融-ECM套利策略",
        "误差修正模型",
        "[[误差修正模型]]"
    )
]

# Ensure Theory cards have concept field
cat2_theory_cards = [
    (r"02-Knowledge\🧠 学习系统\02-时间序列分析\03-经典模型层\ARIMA模型.md", "ARIMA模型"),
    (r"02-Knowledge\🧠 学习系统\02-时间序列分析\03-经典模型层\GARCH模型.md", "GARCH模型"),
    (r"02-Knowledge\🧠 学习系统\02-时间序列分析\04-建模与诊断层\协整.md", "协整"),
    (r"02-Knowledge\🧠 学习系统\02-时间序列分析\02-统计基础层\单位根检验.md", "单位根检验"),
    (r"02-Knowledge\🧠 学习系统\02-时间序列分析\04-建模与诊断层\残差诊断.md", "残差诊断"),
    (r"02-Knowledge\🧠 学习系统\02-时间序列分析\04-建模与诊断层\误差修正模型.md", "误差修正模型"),
]

# Definition of Category 3 (Disambiguation) renames:
# (old_rel_path, new_filename, new_topic, concept_tag)
cat3_tasks = [
    (
        r"02-Knowledge\🧠 学习系统\12-信号与系统\01-基础篇-兵器库\特征函数.md",
        "LTI系统-特征函数.md",
        "LTI系统-特征函数",
        "特征函数"
    ),
    (
        r"02-Knowledge\🧠 学习系统\14-概率图模型\05-隐马尔可夫模型\特征函数.md",
        "CRF-特征函数.md",
        "CRF-特征函数",
        "特征函数"
    ),
    (
        r"02-Knowledge\🧠 学习系统\13-强化学习\03-策略与价值函数\策略评估.md",
        "RL-策略评估.md",
        "RL-策略评估",
        "策略评估"
    ),
    (
        r"02-Knowledge\🧠 学习系统\03-量化金融\04-深入精通\策略评估.md",
        "量化-策略评估与回测.md",
        "量化-策略评估与回测",
        "策略评估"
    ),
    (
        r"02-Knowledge\🧠 学习系统\29-运筹学\03-随机与动态决策\随机与动态决策-Markov 决策过程-策略评估.md",
        "运筹学-MDP策略评估.md",
        "运筹学-MDP策略评估",
        "策略评估"
    ),
    (
        r"02-Knowledge\🧠 学习系统\05-计算机视觉\05-专业深化与工程落地\目标跟踪.md",
        "CV-视觉目标跟踪.md",
        "CV-视觉目标跟踪",
        "目标跟踪"
    ),
    (
        r"02-Knowledge\🧠 学习系统\15-控制与机器人学\10-状态估计\目标跟踪.md",
        "机器人-状态估计与目标跟踪.md",
        "机器人-状态估计与目标跟踪",
        "目标跟踪"
    ),
    (
        r"02-Knowledge\🧠 学习系统\13-强化学习\02-马尔可夫决策过程\轨迹定义.md",
        "RL-MDP轨迹定义.md",
        "RL-MDP轨迹定义",
        "轨迹定义"
    ),
    (
        r"02-Knowledge\🧠 学习系统\15-控制与机器人学\08-轨迹与路径跟踪\轨迹定义.md",
        "机器人-运动轨迹定义.md",
        "机器人-运动轨迹定义",
        "轨迹定义"
    ),
]

def update_frontmatter_and_rename(old_rel, new_filename, new_topic, concept_tag, theory_link=None):
    old_abs = os.path.join(root_dir, old_rel)
    if not os.path.exists(old_abs):
        print(f"⚠️ 文件不存在: {old_rel}")
        return False
        
    with open(old_abs, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
    # Update topic
    if 'topic:' in content:
        content = re.sub(r'^topic:\s*.*$', f'topic: "{new_topic}"', content, flags=re.MULTILINE)
    else:
        if '---' in content:
            parts = content.split('---', 2)
            content = f'---{parts[1].rstrip()}\ntopic: "{new_topic}"\n---' + parts[2]
            
    # Update H1 if present
    content = re.sub(r'^#\s+.*$', f'# {new_topic}', content, flags=re.MULTILINE, count=1)
    
    # Add/Update concept
    if 'concept:' in content:
        if concept_tag not in content:
            content = re.sub(r'concept:\s*\[(.*?)\]', rf'concept: [\1, "{concept_tag}"]', content)
    else:
        if '---' in content:
            parts = content.split('---', 2)
            content = f'---{parts[1].rstrip()}\nconcept: ["{concept_tag}"]\n---' + parts[2]
            
    # Add theory link note if requested
    if theory_link and theory_link not in content:
        note_block = f"\n\n> [!NOTE] 理论根基与方法论\n> 本应用卡片的底层数学理论见：{theory_link}。\n\n"
        # Insert after H1 or frontmatter
        if content.startswith('---'):
            parts = content.split('---', 2)
            content = f"---{parts[1]}---" + note_block + parts[2].lstrip()
        else:
            content = note_block + content

    new_dir = os.path.dirname(old_abs)
    new_abs = os.path.join(new_dir, new_filename)
    
    with open(old_abs, 'w', encoding='utf-8') as f:
        f.write(content)
        
    if old_abs != new_abs:
        os.rename(old_abs, new_abs)
        print(f"✅ [重命名与规范化] {old_rel} -> {new_filename}")
    else:
        print(f"✅ [更新元数据] {old_rel}")
    return True

print("=== 1. 处理理论卡 concept 增加 ===")
for theory_rel, c_name in cat2_theory_cards:
    abs_p = os.path.join(root_dir, theory_rel)
    if os.path.exists(abs_p):
        with open(abs_p, 'r', encoding='utf-8', errors='ignore') as f:
            c = f.read()
        if 'concept:' not in c:
            parts = c.split('---', 2)
            c = f'---{parts[1].rstrip()}\nconcept: ["{c_name}"]\n---' + parts[2]
            with open(abs_p, 'w', encoding='utf-8') as f:
                f.write(c)
            print(f"✅ [理论卡增加概念] {theory_rel} -> concept: [\"{c_name}\"]")

print("\n=== 2. 处理 6 组应用卡重命名与定位指引 ===")
for old_rel, new_fname, new_topic, c_tag, t_link in cat2_tasks:
    update_frontmatter_and_rename(old_rel, new_fname, new_topic, c_tag, t_link)

print("\n=== 3. 处理 4 组同名歧义卡重命名 ===")
for old_rel, new_fname, new_topic, c_tag in cat3_tasks:
    update_frontmatter_and_rename(old_rel, new_fname, new_topic, c_tag)

print("\n全部处理完毕！")
