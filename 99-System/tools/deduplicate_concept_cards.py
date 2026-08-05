import os
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')
root_dir = r'f:\-'

# Exact mapping of secondary cards to rename:
# { (relative_path_to_secondary_card): new_filename_without_ext }
rename_map = {
    r"02-Knowledge\🧠 学习系统\05-计算机视觉\02-深度学习内核\LayerNorm.md": "LayerNorm-CV应用",
    r"02-Knowledge\🧠 学习系统\05-计算机视觉\04-前沿架构探索\LoRA.md": "LoRA-CV应用",
    r"02-Knowledge\🧠 学习系统\05-计算机视觉\04-前沿架构探索\BLIP.md": "BLIP-CV应用",
    r"02-Knowledge\🧠 学习系统\05-计算机视觉\04-前沿架构探索\LLaVA.md": "LLaVA-CV应用",
    r"02-Knowledge\🧠 学习系统\05-计算机视觉\02-深度学习内核\感知机.md": "感知机-CV应用",
    r"02-Knowledge\🧠 学习系统\05-计算机视觉\05-工程与扩展\度量学习.md": "度量学习-CV应用",
    r"02-Knowledge\🧠 学习系统\15-控制与机器人学\卡尔曼滤波.md": "卡尔曼滤波-机器人应用",
    r"02-Knowledge\🧠 学习系统\15-控制与机器人学\10-状态估计\协方差矩阵.md": "协方差矩阵-机器人应用",
    r"02-Knowledge\🧠 学习系统\15-控制与机器人学\05-状态空间与现代控制\Lyapunov稳定.md": "Lyapunov稳定-控制应用",
    r"02-Knowledge\🧠 学习系统\15-控制与机器人学\01-控制地基\线性ODE.md": "线性ODE-控制应用",
    r"02-Knowledge\🧠 学习系统\04-离散数学\02-核心深化\二分图匹配.md": "二分图匹配-离散应用",
    r"02-Knowledge\🧠 学习系统\04-离散数学\04-融会贯通\背包问题.md": "背包问题-离散应用",
    r"02-Knowledge\🧠 学习系统\03-量化金融\02-量化核心技能\特征工程.md": "特征工程-量化应用",
    r"02-Knowledge\🧠 学习系统\06-常微分方程\00-前置知识准备\矩阵转置.md": "矩阵转置-ODE前置",
    r"02-Knowledge\🧠 学习系统\06-常微分方程\00-前置知识准备\Cramer法则.md": "Cramer法则-ODE前置",
    r"02-Knowledge\🧠 学习系统\06-常微分方程\00-前置知识准备\特征值定义.md": "特征值定义-ODE前置",
    r"02-Knowledge\🧠 学习系统\01-社交网络挖掘\03-社区发现与链接预测\谱聚类.md": "谱聚类-社交网络应用",
    r"02-Knowledge\🧠 学习系统\37-复变函数\04-级数奇点留数与应用\极点.md": "极点-复变函数应用",
    r"02-Knowledge\🧠 学习系统\15-控制与机器人学\20-推导笔记\预测方程推导.md": "预测方程推导-MPC专题",
    r"02-Knowledge\🧠 学习系统\15-控制与机器人学\02-机器人学基础模型\阻抗控制.md": "阻抗控制-机器人应用",
    r"02-Knowledge\🧠 学习系统\30-应用回归分析\03-广义与层次扩展\非线性模型.md": "非线性模型-回归应用",
    r"02-Knowledge\🧠 学习系统\30-应用回归分析\10-概念笔记\多元线性回归模型.md": "多元线性回归模型-概念卡"
}

# Misplaced stage duplicate index files to delete
stage_duplicates_to_delete = [
    r"02-Knowledge\🧠 学习系统\06-常微分方程\00-前置知识准备\📘 第一阶段：入门.md",
    r"02-Knowledge\🧠 学习系统\06-常微分方程\01-入门\📗 第二阶段：中级.md",
    r"02-Knowledge\🧠 学习系统\06-常微分方程\03-进阶\📕 第四阶段：精通与专题.md",
    r"02-Knowledge\🧠 学习系统\10-数据结构与算法\02-线性数据结构\🌱 第一阶段：算法入门与基本分析.md",
    r"02-Knowledge\🧠 学习系统\10-数据结构与算法\04-图论基础\🌳 第三阶段：树与堆.md",
    r"02-Knowledge\🧠 学习系统\10-数据结构与算法\05-算法思想进阶\🕸️ 第四阶段：图论基础.md",
    r"02-Knowledge\🧠 学习系统\11-计算机组成原理\30-题型笔记\核心主线常见题型.md",
    r"02-Knowledge\🧠 学习系统\11-计算机组成原理\00-总图景\⚙️ 第一阶段：CPU架构.md",
    r"02-Knowledge\🧠 学习系统\11-计算机组成原理\02-内存管理\⚙️ 第一阶段：CPU架构.md",
    r"02-Knowledge\🧠 学习系统\11-计算机组成原理\00-总图景\存储层次-寄存器.md",
    r"02-Knowledge\🧠 学习系统\11-计算机组成原理\03-进程调度\💾 第二阶段：内存管理.md",
    r"02-Knowledge\🧠 学习系统\11-计算机组成原理\04-并发控制\✅ 第五阶段：总复盘.md",
    r"02-Knowledge\🧠 学习系统\12-信号与系统\01-基础篇-兵器库\🎯 第二阶段：核心篇.md",
    r"02-Knowledge\🧠 学习系统\12-信号与系统\03-变换篇-傅里叶\项目-均衡器.md",
    r"02-Knowledge\🧠 学习系统\12-信号与系统\03-变换篇-傅里叶\🌊 第四阶段：拉普拉斯变换.md",
    r"02-Knowledge\🧠 学习系统\12-信号与系统\05-变换篇-Z变换\🌉 第六阶段：采样定理.md",
    r"02-Knowledge\🧠 学习系统\12-信号与系统\07-数字篇-DFT与FFT\🌉 第六阶段：采样定理.md",
    r"02-Knowledge\🧠 学习系统\12-信号与系统\07-数字篇-DFT与FFT\💻 第七阶段：DFT与FFT.md",
    r"02-Knowledge\🧠 学习系统\15-控制与机器人学\10-状态估计\📡 阶段10：状态估计.md",
    r"02-Knowledge\🧠 学习系统\15-控制与机器人学\10-状态估计\🛠️ 阶段11：工程实战.md"
]

print("1. Deleting misplaced stage/concept duplicate files...")
del_cnt = 0
for rel_del in stage_duplicates_to_delete:
    abs_del = os.path.join(root_dir, rel_del)
    if os.path.exists(abs_del):
        os.remove(abs_del)
        del_cnt += 1
        print(f"  - Deleted duplicate: {rel_del}")

print(f"Deleted {del_cnt} duplicate stage/index files.")

print("\n2. Renaming secondary concept cards...")
link_replacements = {}
renamed_cnt = 0

for rel_old, new_name in rename_map.items():
    abs_old = os.path.join(root_dir, rel_old)
    if not os.path.exists(abs_old):
        print(f"  - Skipping missing file: {rel_old}")
        continue
    dir_name = os.path.dirname(abs_old)
    old_filename = os.path.basename(abs_old)
    old_stem = old_filename.replace('.md', '')
    
    abs_new = os.path.join(dir_name, new_name + ".md")
    
    # Store wikilink replacement rule if needed
    # Note: Primary card retains old_stem, secondary card gets new_name
    
    os.rename(abs_old, abs_new)
    renamed_cnt += 1
    print(f"  - Renamed: {old_stem}.md -> {new_name}.md ({os.path.basename(os.path.dirname(dir_name))})")

print(f"Successfully renamed {renamed_cnt} concept cards.")

