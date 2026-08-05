import os
import sys
import re

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

VAULT_ROOT = r"f:\-"

def repair_links():
    print("=" * 60)
    print("🔗 开始全库双链扫描与路径修复")
    print("=" * 60)

    # Patterns matching old paths for project cards
    # 1. 02-Knowledge/🧠 学习系统/.../项目-XXX(.md)
    # 2. 03-Projects/课程作业/.../项目-XXX(.md)
    
    fixed_files = 0
    total_link_replacements = 0

    for root, dirs, files in os.walk(VAULT_ROOT):
        if ".git" in root or ".obsidian" in root:
            continue
        for f in files:
            if not f.endswith(".md"):
                continue
            abs_path = os.path.join(root, f)
            with open(abs_path, "r", encoding="utf-8") as file_in:
                content = file_in.read()

            new_content = content

            # Replace explicit path wikilinks: [[02-Knowledge/🧠 学习系统/.../(项目-[^|\]]+)(|...)?]] -> [[项目-XXX\2]]
            def replace_old_project_link(match):
                nonlocal total_link_replacements
                total_link_replacements += 1
                proj_name = match.group(1).rstrip(".md")
                alias_part = match.group(2) if match.group(2) else ""
                return f"[[{proj_name}{alias_part}]]"

            # Match [[.../项目-XXX...]]
            pattern1 = r"\[\[02-Knowledge/🧠 学习系统/[^\]]*?/(项目-[^\|\]]+?)(\.md)?(\|[^\]]+)?\]\]"
            pattern2 = r"\[\[03-Projects/课程作业/[^\]]*?/(项目-[^\|\]]+?)(\.md)?(\|[^\]]+)?\]\]"

            new_content = re.sub(pattern1, replace_old_project_link, new_content)
            new_content = re.sub(pattern2, replace_old_project_link, new_content)

            if new_content != content:
                with open(abs_path, "w", encoding="utf-8") as file_out:
                    file_out.write(new_content)
                fixed_files += 1
                rel = os.path.relpath(abs_path, VAULT_ROOT)
                print(f"  ✅ [FIXED LINKS] {rel}")

    print(f"\n修复完成: 在 {fixed_files} 个文件中共替换修复了 {total_link_replacements} 处显式长路径引用！")

if __name__ == "__main__":
    repair_links()
