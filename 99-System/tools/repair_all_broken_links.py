import os
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')
root_dir = r'f:\-'

# Map all existing valid markdown stems to their canonical name/path
valid_stems = {}
for dirpath, dirnames, filenames in os.walk(root_dir):
    if any(x in dirpath for x in ['.git', '.obsidian', '.claude']): continue
    for f in filenames:
        if f.endswith('.md'):
            p = os.path.join(dirpath, f)
            rel_p = os.path.relpath(p, root_dir)
            stem = f[:-3]
            valid_stems[stem.lower()] = stem
            valid_stems[rel_p.lower()] = rel_p

print(f"Total valid stems mapped: {len(valid_stems)}")

# Fixed mapping rules for specific broken links:
explicit_mappings = {
    # Obsolete annual plan
    "99-System/🗓️ 计划执行系统/🧭 2026-05-22 ~ 2027-05-21 完整规划总纲": "99-System/🗓️ 计划执行系统/🧭 计划系统导航|计划系统导航",
    "99-System/🗓️ 计划执行系统/🗂️ 2026-06-04 ~ 2026-09-03 季度学习计划总索引": "99-System/🗓️ 计划执行系统/🗂️ 一年计划执行系统总索引|一年计划执行系统总索引",
    "99-System/🗓️ 计划执行系统/季度计划/Q1 2026-06-04 ~ 2026-09-03 季度计划": "99-System/🗓️ 计划执行系统/🧭 计划系统导航|计划系统导航",
    
    # Relative path learning paths
    "../🗺️ 计算机组成原理学习路径": "02-Knowledge/🧠 学习系统/11-计算机组成原理/🗺️ 学习路径|计算机组成原理学习路径",
    "../🗺️ 信号与系统学习路径": "02-Knowledge/🧠 学习系统/12-信号与系统/🗺️ 学习路径|信号与系统学习路径",
    "../🗺️ 常微分方程学习路径": "02-Knowledge/🧠 学习系统/06-常微分方程/🗺️ 学习路径|常微分方程学习路径",
    "../📚 教材挂载索引": "02-Knowledge/🧠 学习系统/📚 教材挂载总索引|教材挂载总索引",
    
    # Deleted stage pages
    "02-Knowledge/🧠 学习系统/11-计算机组成原理/03-进程调度/🔄 第三阶段：进程调度": "02-Knowledge/🧠 学习系统/11-计算机组成原理/03-进程调度/03-进程调度|进程调度",
    "02-Knowledge/🧠 学习系统/11-计算机组成原理/04-并发控制/🔒 第四阶段：并发控制": "02-Knowledge/🧠 学习系统/11-计算机组成原理/04-并发控制/04-并发控制|并发控制",
    "02-Knowledge/🧠 学习系统/15-控制与机器人学/11-工程实战/🛠️ 阶段11：工程实战": "02-Knowledge/🧠 学习系统/15-控制与机器人学/11-工程实战/11-工程实战|工程实战",
    "02-Knowledge/🧠 学习系统/12-信号与系统/07-数字篇-DFT与FFT/💻 第七阶段：DFT与FFT": "02-Knowledge/🧠 学习系统/12-信号与系统/07-数字篇-DFT与FFT/07-数字篇-DFT与FFT|DFT与FFT",
    "💻 第七阶段：DFT与FFT": "02-Knowledge/🧠 学习系统/12-信号与系统/07-数字篇-DFT与FFT/07-数字篇-DFT与FFT|DFT与FFT",
    "🔄 第三阶段：进程调度": "02-Knowledge/🧠 学习系统/11-计算机组成原理/03-进程调度/03-进程调度|进程调度",
    "🔒 第四阶段：并发控制": "02-Knowledge/🧠 学习系统/11-计算机组成原理/04-并发控制/04-并发控制|并发控制",
    "🛠️ 阶段11：工程实战": "02-Knowledge/🧠 学习系统/15-控制与机器人学/11-工程实战/11-工程实战|工程实战",
    
    # Concepts
    "ARIMA": "ARIMA模型",
    "GARCH": "GARCH模型",
    "协整分析": "协整",
    "卡尔曼滤波算法": "卡尔曼滤波",
    "LayerNorm层": "LayerNorm",
    "LoRA微调": "LoRA"
}

link_re = re.compile(r'\[\[(.*?)\]\]')
fixed_files_cnt = 0
total_replacements = 0

for dirpath, dirnames, filenames in os.walk(root_dir):
    if any(x in dirpath for x in ['.git', '.obsidian', '.claude']): continue
    for f in filenames:
        if f.endswith('.md'):
            p = os.path.join(dirpath, f)
            try:
                with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
                    content = fp.read()
            except Exception: continue
            
            def replace_link(m):
                global total_replacements
                raw_inner = m.group(1)
                target = raw_inner.split('|')[0].split('#')[0].strip()
                alias = raw_inner.split('|')[1] if '|' in raw_inner else ""
                anchor = ("#" + raw_inner.split('#')[1].split('|')[0]) if '#' in raw_inner else ""
                
                # Check explicit mappings first
                if target in explicit_mappings:
                    total_replacements += 1
                    rep = explicit_mappings[target]
                    return f"[[{rep}]]"
                    
                # Check if target stem exists in valid stems
                target_lower = target.lower()
                if target_lower not in valid_stems:
                    # Strip path prefix if any e.g. 02-Knowledge/🧠 学习系统/02-时间序列分析/ARIMA模型
                    base_target = os.path.basename(target).replace('.md', '')
                    if base_target.lower() in valid_stems:
                        canonical = valid_stems[base_target.lower()]
                        total_replacements += 1
                        display = alias if alias else base_target
                        return f"[[{canonical}{anchor}|{display}]]" if display != canonical else f"[[{canonical}{anchor}]]"
                        
                return m.group(0)

            new_content = link_re.sub(replace_link, content)
            if new_content != content:
                with open(p, 'w', encoding='utf-8') as fp:
                    fp.write(new_content)
                fixed_files_cnt += 1

print(f"Broken links repair completed. Modified {fixed_files_cnt} files, repaired {total_replacements} link occurrences.")

