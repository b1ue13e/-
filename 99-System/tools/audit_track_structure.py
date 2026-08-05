import os
import sys
import re

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

VAULT_ROOT = r"f:\-"

VALID_TRACKS = {
    "数学底座",
    "概率统计与数据建模",
    "机器学习与AI应用",
    "AI Agent工程",
    "系统与硬件",
    "金融与时序"
}

EXPECTED_MOCS = [
    r"02-Knowledge\MOC\主线-数学底座.md",
    r"02-Knowledge\MOC\主线-概率统计与数据建模.md",
    r"02-Knowledge\MOC\主线-机器学习与AI应用.md",
    r"02-Knowledge\MOC\主线-AI Agent工程.md",
    r"02-Knowledge\MOC\主线-系统与硬件.md",
    r"02-Knowledge\MOC\主线-金融与时序.md"
]

def run_audit():
    print("=" * 60)
    print("🔍 开始 6 大主线 (Main Tracks) 治理与结构完整性审计")
    print("=" * 60)
    
    score = 10.0
    deductions = []

    # 1. 检查 6 大主线 MOC 存在性
    print("\n--- [1/4] 检查 6 大主线 MOC 页面 ---")
    missing_mocs = []
    for moc_rel_path in EXPECTED_MOCS:
        abs_path = os.path.join(VAULT_ROOT, moc_rel_path)
        if os.path.exists(abs_path):
            print(f"  ✅ [EXIST] {moc_rel_path}")
        else:
            print(f"  ❌ [MISSING] {moc_rel_path}")
            missing_mocs.append(moc_rel_path)
            
    if missing_mocs:
        score -= len(missing_mocs) * 0.5
        deductions.append(f"缺失 {len(missing_mocs)} 个主线 MOC")

    # 2. 检查 45 个目录的 track 标注覆盖率
    print("\n--- [2/4] 检查 45 条课程路径 track 标注 ---")
    study_sys_dir = os.path.join(VAULT_ROOT, r"02-Knowledge\🧠 学习系统")
    all_subdirs = [d for d in os.listdir(study_sys_dir) if os.path.isdir(os.path.join(study_sys_dir, d))]
    
    path_dirs = [d for d in all_subdirs if re.match(r"^\d+-", d) and d[:2] not in ["18", "19", "20", "21"]]
    
    tagged_count = 0
    invalid_track_count = 0
    missing_index_count = 0
    
    for d in sorted(path_dirs):
        dp = os.path.join(study_sys_dir, d)
        indices = [f for f in os.listdir(dp) if f.startswith("🗺️") and f.endswith(".md")]
        if not indices:
            indices = [f for f in os.listdir(dp) if "学习路径" in f and f.endswith(".md")]
            
        if not indices:
            print(f"  ⚠️ [NO INDEX] {d}")
            missing_index_count += 1
            continue
            
        index_path = os.path.join(dp, indices[0])
        with open(index_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        track_match = re.search(r"^track:\s*[\"']?([^\"'\r\n]+)[\"']?", content, re.MULTILINE)
        if track_match:
            track_val = track_match.group(1).strip()
            if track_val in VALID_TRACKS:
                tagged_count += 1
            else:
                print(f"  ❌ [INVALID TRACK] {d} -> '{track_val}'")
                invalid_track_count += 1
        else:
            print(f"  ❌ [MISSING TRACK] {d}")
            
    print(f"\n课程路径总计: {len(path_dirs)} 门")
    print(f"成功标注有效 track: {tagged_count} / {len(path_dirs)}")
    
    if tagged_count < len(path_dirs):
        diff = len(path_dirs) - tagged_count
        score -= diff * 0.1
        deductions.append(f"有 {diff} 门课程路径未配置有效 track")

    # 3. 检查 AGENTS.md 45 条路径与 6 大主线描述
    print("\n--- [3/4] 检查 AGENTS.md 规范与主线条款 ---")
    agents_path = os.path.join(VAULT_ROOT, "AGENTS.md")
    with open(agents_path, "r", encoding="utf-8") as f:
        agents_content = f.read()
        
    agents_ok = True
    if "45 条" not in agents_content:
        print("  ❌ [AGENTS.md] 未包含 '45 条' 路径更新")
        agents_ok = False
    if "6 大主线" not in agents_content:
        print("  ❌ [AGENTS.md] 未包含 '6 大主线' 条款")
        agents_ok = False
    if "track" not in agents_content:
        print("  ❌ [AGENTS.md] Frontmatter 表格未增加 'track' 字段说明")
        agents_ok = False
        
    if agents_ok:
        print("  ✅ [AGENTS.md] 已成功更新 45 条路径、6 大主线及 track 字段说明")
    else:
        score -= 0.5
        deductions.append("AGENTS.md 条款更新不完整")

    # 4. 检查 🧭 学科分组导航.md 与 🎓 学习入口.md
    print("\n--- [4/4] 检查导航入口文件 ---")
    nav_path = os.path.join(study_sys_dir, "🧭 学科分组导航.md")
    entry_path = os.path.join(study_sys_dir, "🎓 学习入口.md")
    
    nav_ok = os.path.exists(nav_path) and "6 大主线" in open(nav_path, "r", encoding="utf-8").read()
    entry_ok = os.path.exists(entry_path) and "6 大主线" in open(entry_path, "r", encoding="utf-8").read()
    
    if nav_ok:
        print("  ✅ [🧭 学科分组导航.md] 已按 6 大主线重构")
    else:
        print("  ❌ [🧭 学科分组导航.md] 缺失或未包含 6 大主线内容")
        score -= 0.3
        
    if entry_ok:
        print("  ✅ [🎓 学习入口.md] 已按 6 大主线更新")
    else:
        print("  ❌ [🎓 学习入口.md] 缺失或未包含 6 大主线内容")
        score -= 0.3

    score = max(0.0, min(10.0, score))
    
    print("\n" + "=" * 60)
    print(f"🏆 最终主线治理审计得分: {score:.1f} / 10.0")
    if deductions:
        print("扣分原因:")
        for d in deductions:
            print(f"  - {d}")
    else:
        print("🎉 完美通过！符合 9.5+ 高质量交付标准！")
    print("=" * 60)
    return score

if __name__ == "__main__":
    run_audit()
