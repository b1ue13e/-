import os
import shutil
import re

VAULT_ROOT = r"f:\-"
PROJECTS_ROOT = os.path.join(VAULT_ROOT, "03-Projects")
TARGET_DIR = os.path.join(PROJECTS_ROOT, "机器学习与AI应用", "05-计算机视觉")
os.makedirs(TARGET_DIR, exist_ok=True)

UNKNOWN_DIR = os.path.join(PROJECTS_ROOT, "通用项目")

def fix_cv_files():
    if not os.path.exists(UNKNOWN_DIR):
        print("No 通用项目 directory found.")
        return

    moved = 0
    for root, dirs, files in os.walk(UNKNOWN_DIR):
        for f in files:
            if f.endswith(".md"):
                src_path = os.path.join(root, f)
                dst_path = os.path.join(TARGET_DIR, f)

                with open(src_path, "r", encoding="utf-8") as file_in:
                    content = file_in.read()

                # Update Frontmatter
                if content.startswith("---"):
                    parts = content.split("---", 2)
                    fm = parts[1]
                    body = parts[2] if len(parts) > 2 else ""

                    fm = re.sub(r"^type:\s*.*$", 'type: project', fm, flags=re.MULTILINE) if 'type:' in fm else fm + '\ntype: project'
                    fm = re.sub(r"^flow:\s*.*$", 'flow: project', fm, flags=re.MULTILINE) if 'flow:' in fm else fm + '\nflow: project'
                    fm = re.sub(r"^kind:\s*.*$", 'kind: project', fm, flags=re.MULTILINE) if 'kind:' in fm else fm + '\nkind: project'
                    
                    if 'track:' in fm:
                        fm = re.sub(r"^track:\s*.*$", 'track: "机器学习与AI应用"', fm, flags=re.MULTILINE)
                    else:
                        fm = fm.strip() + '\ntrack: "机器学习与AI应用"\n'

                    if 'course:' in fm:
                        fm = re.sub(r"^course:\s*.*$", 'course: "05-计算机视觉"', fm, flags=re.MULTILINE)
                    else:
                        fm = fm.strip() + '\ncourse: "05-计算机视觉"\n'

                    if 'status:' not in fm:
                        fm = fm.strip() + '\nstatus: active\n'

                    content = f"---{fm.strip()}\n---\n{body.lstrip()}"

                with open(dst_path, "w", encoding="utf-8") as file_out:
                    file_out.write(content)

                os.remove(src_path)
                moved += 1

    shutil.rmtree(UNKNOWN_DIR, ignore_errors=True)
    print(f"Fixed and moved {moved} CV project files.")

if __name__ == "__main__":
    fix_cv_files()
