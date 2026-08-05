import os
import sys
import re
import shutil

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

VAULT_ROOT = r"f:\-"
PROJECTS_ROOT = os.path.join(VAULT_ROOT, "03-Projects")
LEARNING_SYS_ROOT = os.path.join(VAULT_ROOT, r"02-Knowledge\🧠 学习系统")
ARCHIVE_ROOT = os.path.join(VAULT_ROOT, r"99-System\🗄️ 归档")

COURSE_TO_TRACK = {
    "01-社交网络挖掘": "机器学习与AI应用",
    "02-时间序列分析": "金融与时序",
    "03-量化金融": "金融与时序",
    "04-离散数学": "数学底座",
    "05-计算机视觉": "机器学习与AI应用",
    "06-常微分方程": "数学底座",
    "07-最优化方法": "金融与时序",
    "08-NLP全栈": "机器学习与AI应用",
    "09-高等代数": "数学底座",
    "10-数据结构与算法": "系统与硬件",
    "11-计算机组成原理": "系统与硬件",
    "12-信号与系统": "系统与硬件",
    "13-强化学习": "机器学习与AI应用",
    "14-概率图模型": "机器学习与AI应用",
    "15-控制与机器人学": "系统与硬件",
    "16-多元统计": "概率统计与数据建模",
    "17-机器学习": "机器学习与AI应用",
    "22-概率论与数理统计": "概率统计与数据建模",
    "23-图神经网络": "机器学习与AI应用",
    "24-随机过程": "概率统计与数据建模",
    "25-测度论": "数学底座",
    "26-实变函数": "数学底座",
    "27-泛函分析": "数学底座",
    "28-数学分析": "数学底座",
    "29-运筹学": "金融与时序",
    "30-应用回归分析": "概率统计与数据建模",
    "31-属性数据分析": "概率统计与数据建模",
    "32-非参数统计": "概率统计与数据建模",
    "33-贝叶斯统计": "概率统计与数据建模",
    "34-偏微分方程": "数学底座",
    "35-数值分析": "数学底座",
    "36-数据挖掘与信息检索": "机器学习与AI应用",
    "37-复变函数": "数学底座",
    "38-AI Agent设计与工程实践": "AI Agent工程",
    "39-HelloAgents从零构建智能体": "AI Agent工程",
    "40-微软AI-Agents入门与工程实践": "AI Agent工程",
    "41-HuggingFace-Agents开源框架与实战": "AI Agent工程",
    "42-LangGraph复杂工作流与状态机": "AI Agent工程",
    "43-MCP协议与智能体服务编排": "AI Agent工程",
    "44-OpenAI-Agents-SDK架构与设计模式": "AI Agent工程",
    "45-生成式AI基础与Prompt工程": "AI Agent工程",
    "哲学": "辅助系统",
    "心理学": "辅助系统",
    "深度学习": "机器学习与AI应用"
}

def determine_course_and_track(rel_path, content):
    # Try match course directory name from path
    parts = rel_path.replace("\\", "/").split("/")
    course = None
    for p in parts:
        if p in COURSE_TO_TRACK:
            course = p
            break
        # Match pattern like 01-社交网络挖掘
        if re.match(r"^\d{2}-", p):
            course = p
            break

    # If course in frontmatter
    if not course:
        cmatch = re.search(r"^course:\s*[\"']?([^\"'\r\n]+)[\"']?", content, re.MULTILINE)
        if cmatch:
            course_val = cmatch.group(1).strip()
            for key in COURSE_TO_TRACK:
                if key in course_val or course_val in key:
                    course = key
                    break

    if not course:
        course = "通用与跨学科"
        track = "通用项目"
    else:
        track = COURSE_TO_TRACK.get(course, "通用项目")

    return course, track

def run_migration():
    print("=" * 60)
    print("🚀 开始 264 张项目卡物理搬迁与 Frontmatter 统一")
    print("=" * 60)

    # 1. 扫描所有 项目-*.md
    all_projects = []
    for root, dirs, files in os.walk(VAULT_ROOT):
        if ".git" in root or ".obsidian" in root or "99-System" in root:
            continue
        for f in files:
            if f.startswith("项目-") and f.endswith(".md"):
                abs_path = os.path.join(root, f)
                rel_path = os.path.relpath(abs_path, VAULT_ROOT)
                all_projects.append((f, rel_path, abs_path))

    print(f"找到项目卡总计: {len(all_projects)} 张\n")

    moved_count = 0
    updated_fm_count = 0
    old_paths_map = {}

    for fname, rel_path, abs_path in all_projects:
        with open(abs_path, "r", encoding="utf-8") as f:
            content = f.read()

        course, track = determine_course_and_track(rel_path, content)
        
        # Target destination: 03-Projects/<track>/<course>/<fname>
        target_dir = os.path.join(PROJECTS_ROOT, track, course)
        os.makedirs(target_dir, exist_ok=True)
        target_abs_path = os.path.join(target_dir, fname)
        target_rel_path = os.path.relpath(target_abs_path, VAULT_ROOT)

        # Update frontmatter content
        new_content = content
        if new_content.startswith("---"):
            parts = new_content.split("---", 2)
            fm = parts[1]
            body = parts[2] if len(parts) > 2 else ""

            # Update type, flow, kind
            fm = re.sub(r"^type:\s*.*$", 'type: project', fm, flags=re.MULTILINE) if 'type:' in fm else fm + '\ntype: project'
            fm = re.sub(r"^flow:\s*.*$", 'flow: project', fm, flags=re.MULTILINE) if 'flow:' in fm else fm + '\nflow: project'
            fm = re.sub(r"^kind:\s*.*$", 'kind: project', fm, flags=re.MULTILINE) if 'kind:' in fm else fm + '\nkind: project'

            # Update or add track & course
            if 'track:' in fm:
                fm = re.sub(r"^track:\s*.*$", f'track: "{track}"', fm, flags=re.MULTILINE)
            else:
                fm = fm.strip() + f'\ntrack: "{track}"\n'

            if 'course:' in fm:
                fm = re.sub(r"^course:\s*.*$", f'course: "{course}"', fm, flags=re.MULTILINE)
            else:
                fm = fm.strip() + f'\ncourse: "{course}"\n'

            # Check status / asset_eligibility
            if 'asset_eligibility: reference-only' in fm or 'asset_eligibility:' in fm:
                if 'status:' in fm:
                    fm = re.sub(r"^status:\s*.*$", 'status: reference', fm, flags=re.MULTILINE)
                else:
                    fm = fm.strip() + '\nstatus: reference\n'
            elif 'status:' not in fm:
                fm = fm.strip() + '\nstatus: active\n'

            new_content = f"---{fm.strip()}\n---\n{body.lstrip()}"
        else:
            new_content = f'---\ntitle: "{fname[:-3]}"\ntype: project\nflow: project\nkind: project\ntrack: "{track}"\ncourse: "{course}"\nstatus: active\n---\n\n' + content

        # Save to target file
        with open(target_abs_path, "w", encoding="utf-8") as f:
            f.write(new_content)

        old_paths_map[rel_path.replace("\\", "/")] = target_rel_path.replace("\\", "/")

        # If source location is different from target, delete old file
        if os.path.abspath(abs_path) != os.path.abspath(target_abs_path):
            os.remove(abs_path)
            moved_count += 1

        updated_fm_count += 1

    print(f"✅ 物理移动文件: {moved_count} 个")
    print(f"✅ 身份与 Frontmatter 统一: {updated_fm_count} 个")

    # Clean up empty old '课程作业' folder under 03-Projects if it exists
    old_hw_dir = os.path.join(PROJECTS_ROOT, "课程作业")
    if os.path.exists(old_hw_dir):
        shutil.rmtree(old_hw_dir)
        print(f"🧹 已清理旧 '03-Projects/课程作业/' 目录")

    # Move root audit files in 03-Projects to 99-System/🗄️ 归档/
    audit_files_to_move = [
        "33门课程作业来源审计总表.md",
        "33门课程完整作业编目审计-2026-07-28.md",
        "旧项目与作业资产资格审计-2026-07-28.md",
        "正式作业包修复审计-2026-07-28.md"
    ]
    for af in audit_files_to_move:
        af_abs = os.path.join(PROJECTS_ROOT, af)
        if os.path.exists(af_abs):
            os.makedirs(ARCHIVE_ROOT, exist_ok=True)
            shutil.move(af_abs, os.path.join(ARCHIVE_ROOT, af))
            print(f"📦 已将根目录审计文件 {af} 归档到 99-System/🗄️ 归档/")

    print("\n完成物理搬迁与身份统一！")

if __name__ == "__main__":
    run_migration()
