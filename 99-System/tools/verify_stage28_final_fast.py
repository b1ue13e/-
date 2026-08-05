import csv, sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

CSV_PATH = Path("F:/-/knowledge_notes_harsh_scores_2026-07-31.csv")

print("=== Stage 28 计算机视觉卡片核验 ===")
targets = {"卷积神经网络CNN.md", "ResNet残差网络.md", "YOLO目标检测.md"}
with open(CSV_PATH, "r", encoding="utf-8-sig") as f:
    rows = [r for r in csv.DictReader(f) if Path(r["path"]).name in targets]
rows.sort(key=lambda r: float(r['score']), reverse=True)
for row in rows:
    print(f"• [{row['score']}分/{row['grade']}] {Path(row['path']).name} "
          f"字符={row['去模板有效正文字符']} 来源={row['证据来源']}/15 "
          f"例证={row['例证验证']}/10 主题={row['主题聚焦']} 严谨={row['严谨性']}")

print("\n=== 🏆 计算机视觉 80+ B级良好卡片明细 ===")
with open(CSV_PATH, "r", encoding="utf-8-sig") as f:
    b_rows = [r for r in csv.DictReader(f) if float(r['score']) >= 80 and "05-计算机视觉" in r['path']]
b_rows.sort(key=lambda r: float(r['score']), reverse=True)
for i, r in enumerate(b_rows, 1):
    print(f"{i:2d}. [{r['score']}分 / {r['grade']}] {r['path']}")
