import os
import sys

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

VAULT_ROOT = r"f:\-"
DIRS_TO_SCAN = [
    os.path.join(VAULT_ROOT, "03-Projects"),
    os.path.join(VAULT_ROOT, r"02-Knowledge\🧠 学习系统")
]

def scan_fast():
    project_files = []
    for s_dir in DIRS_TO_SCAN:
        for root, dirs, files in os.walk(s_dir):
            for f in files:
                if f.startswith("项目-") and f.endswith(".md"):
                    rel_path = os.path.relpath(os.path.join(root, f), VAULT_ROOT)
                    project_files.append((f, rel_path, os.path.join(root, f)))

    print(f"Total '项目-*.md' files found: {len(project_files)}")
    
    in_03 = [p for p in project_files if p[1].startswith("03-Projects")]
    in_02 = [p for p in project_files if p[1].startswith(r"02-Knowledge\🧠 学习系统")]
    
    print(f"  - In 03-Projects: {len(in_03)}")
    print(f"  - In 02-Knowledge/🧠 学习系统: {len(in_02)}")
    
    names = [p[0] for p in project_files]
    unique_names = set(names)
    print(f"Unique project file names: {len(unique_names)}")
    if len(names) != len(unique_names):
        print(f"⚠️ Duplicate count: {len(names) - len(unique_names)}")

if __name__ == "__main__":
    scan_fast()
