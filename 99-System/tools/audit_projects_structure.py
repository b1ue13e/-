import os
import sys
import re

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

VAULT_ROOT = r"f:\-"
PROJECTS_ROOT = os.path.join(VAULT_ROOT, "03-Projects")
LEARNING_SYS_ROOT = os.path.join(VAULT_ROOT, r"02-Knowledge\🧠 学习系统")

VALID_TRACKS = {
    "数学底座",
    "概率统计与数据建模",
    "机器学习与AI应用",
    "AI Agent工程",
    "系统与硬件",
    "金融与时序",
    "辅助系统",
    "通用项目"
}

def run_project_audit():
    print("=" * 60)
    print("🔍 开始项目卡物理收拢、身份统一与看板完整性审计")
    print("=" * 60)

    score = 10.0
    deductions = []

    # 1. 检查 02-Knowledge 是否还有项目卡残留
    print("\n--- [1/5] 检查 02-Knowledge 残留项目卡 ---")
    rem_in_02 = []
    for root, dirs, files in os.walk(LEARNING_SYS_ROOT):
        for f in files:
            if f.startswith("项目-") and f.endswith(".md"):
                rem_in_02.append(os.path.join(root, f))

    if len(rem_in_02) == 0:
        print("  ✅ [PASS] 02-Knowledge 中零项目卡残留，全部清理完毕！")
    else:
        print(f"  ❌ [FAIL] 02-Knowledge 中仍残留 {len(rem_in_02)} 张项目卡！")
        score -= len(rem_in_02) * 0.1
        deductions.append(f"02-Knowledge 残留 {len(rem_in_02)} 张项目卡")

    # 2. 检查 03-Projects 中的项目卡总数与唯一性
    print("\n--- [2/5] 检查 03-Projects 项目卡归集与同名唯一性 ---")
    projects_in_03 = []
    for root, dirs, files in os.walk(PROJECTS_ROOT):
        for f in files:
            if f.startswith("项目-") and f.endswith(".md"):
                projects_in_03.append((f, os.path.join(root, f)))

    print(f"  03-Projects 包含项目卡总计: {len(projects_in_03)} 张")

    names = [p[0] for p in projects_in_03]
    if len(names) == len(set(names)):
        print("  ✅ [PASS] 03-Projects 项目卡无重名冲突！")
    else:
        diff = len(names) - len(set(names))
        print(f"  ❌ [FAIL] 存在 {diff} 个同名冲突！")
        score -= diff * 0.5
        deductions.append(f"存在 {diff} 个同名冲突")

    # 3. 检查 Frontmatter 身份与元数据
    print("\n--- [3/5] 检查 Frontmatter 身份字段 (type/flow/kind/track/course) ---")
    fm_errors = 0
    for fname, abs_path in projects_in_03:
        with open(abs_path, "r", encoding="utf-8") as f:
            content = f.read()

        type_m = re.search(r"^type:\s*[\"']?project[\"']?", content, re.MULTILINE)
        flow_m = re.search(r"^flow:\s*[\"']?project[\"']?", content, re.MULTILINE)
        kind_m = re.search(r"^kind:\s*[\"']?project[\"']?", content, re.MULTILINE)
        track_m = re.search(r"^track:\s*[\"']?([^\"'\r\n]+)[\"']?", content, re.MULTILINE)
        course_m = re.search(r"^course:\s*[\"']?([^\"'\r\n]+)[\"']?", content, re.MULTILINE)

        if not (type_m and flow_m and kind_m and track_m and course_m):
            fm_errors += 1
            rel = os.path.relpath(abs_path, PROJECTS_ROOT)
            print(f"  ❌ [FM ERROR] {rel}")

    if fm_errors == 0:
        print(f"  ✅ [PASS] 全部 {len(projects_in_03)} 张项目卡 Frontmatter 统一规范达成 (100%)！")
    else:
        print(f"  ❌ [FAIL] 有 {fm_errors} 张卡片 Frontmatter 缺失规范字段")
        score -= fm_errors * 0.05
        deductions.append(f"{fm_errors} 张卡片 Frontmatter 规范不符合要求")

    # 4. 检查 03-Projects 根目录整洁度
    print("\n--- [4/5] 检查 03-Projects 根目录整洁度 ---")
    root_files = [f for f in os.listdir(PROJECTS_ROOT) if os.path.isfile(os.path.join(PROJECTS_ROOT, f))]
    dirty_audit_files = [f for f in root_files if "审计" in f]
    
    if len(dirty_audit_files) == 0:
        print("  ✅ [PASS] 03-Projects 根目录无杂乱审计报告！")
    else:
        print(f"  ❌ [FAIL] 根目录残留审计文件: {dirty_audit_files}")
        score -= len(dirty_audit_files) * 0.3
        deductions.append(f"根目录残留 {len(dirty_audit_files)} 个审计文件")

    # 5. 检查 03-🛠️ Projects.md 主页
    print("\n--- [5/5] 检查 03-🛠️ Projects.md 主页看板 ---")
    homepage = os.path.join(PROJECTS_ROOT, "03-🛠️ Projects.md")
    if os.path.exists(homepage):
        with open(homepage, "r", encoding="utf-8") as f:
            hp_content = f.read()
        if "6 大主线" in hp_content or "Dataview" in hp_content or "dataview" in hp_content:
            print("  ✅ [PASS] 03-🛠️ Projects.md 项目主页重构完毕且包含 6 大主线动态看板！")
        else:
            print("  ❌ [FAIL] 03-🛠️ Projects.md 缺少主线看板内容")
            score -= 0.5
            deductions.append("项目主页缺失主线看板")
    else:
        print("  ❌ [FAIL] 03-🛠️ Projects.md 不存在！")
        score -= 1.0
        deductions.append("缺失 03-🛠️ Projects.md")

    score = max(0.0, min(10.0, score))

    print("\n" + "=" * 60)
    print(f"🏆 最终项目体系治理审计得分: {score:.1f} / 10.0")
    if deductions:
        print("扣分原因:")
        for d in deductions:
            print(f"  - {d}")
    else:
        print("🎉 完美通过！符合 9.5+ 高质量交付标准！")
    print("=" * 60)
    return score

if __name__ == "__main__":
    run_project_audit()
