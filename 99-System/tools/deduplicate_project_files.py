import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
root_dir = r'f:\-'

redundant_project_files = [
    r"02-Knowledge\🧠 学习系统\04-前沿架构探索\项目-CLIP检索.md",
    r"02-Knowledge\🧠 学习系统\04-前沿架构探索\项目-SD微调.md",
    r"02-Knowledge\🧠 学习系统\04-前沿架构探索\项目-ViT实现.md",
    r"02-Knowledge\🧠 学习系统\04-前沿架构探索\项目-自监督.md",
    r"02-Knowledge\🧠 学习系统\05-专业深化与工程落地\项目-NeRF.md",
    r"02-Knowledge\🧠 学习系统\05-专业深化与工程落地\项目-模型部署.md",
    r"02-Knowledge\🧠 学习系统\05-专业深化与工程落地\项目-视频分析.md",
    r"02-Knowledge\🧠 学习系统\05-专业深化与工程落地\项目-边缘部署.md",
    r"02-Knowledge\🧠 学习系统\04-离散数学\04-融会贯通\项目-知识图谱.md"
]

print("Deleting 9 redundant project copies in pending governance directories...")
deleted_cnt = 0

for rel_p in redundant_project_files:
    abs_p = os.path.join(root_dir, rel_p)
    if os.path.exists(abs_p):
        os.remove(abs_p)
        deleted_cnt += 1
        print(f"✅ Deleted: {rel_p}")
    else:
        print(f"⚠️ File not found (already deleted): {rel_p}")

print(f"\nSuccessfully removed {deleted_cnt} redundant project copies.")

