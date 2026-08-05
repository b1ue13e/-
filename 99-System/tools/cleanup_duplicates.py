import os
import sys

VAULT_ROOT = r"f:\-"
PROJECTS_ROOT = os.path.join(VAULT_ROOT, "03-Projects")

def cleanup_duplicates_and_fix_fm():
    files_map = {}
    for root, dirs, files in os.walk(PROJECTS_ROOT):
        for f in files:
            if f.startswith("项目-") and f.endswith(".md"):
                abs_path = os.path.join(root, f)
                files_map.setdefault(f, []).append(abs_path)

    removed = 0
    for f, paths in files_map.items():
        if len(paths) > 1:
            print(f"Duplicate found for '{f}': {paths}")
            # Keep the one with proper track/course, remove others
            paths_sorted = sorted(paths, key=lambda p: ("通用项目" in p, len(p)))
            keep = paths_sorted[0]
            for to_remove in paths_sorted[1:]:
                os.remove(to_remove)
                removed += 1
                print(f"  Removed duplicate: {to_remove}")

    # Re-scan all projects and fix Frontmatters
    fixed_fm = 0
    for root, dirs, files in os.walk(PROJECTS_ROOT):
        for f in files:
            if f.startswith("项目-") and f.endswith(".md"):
                abs_path = os.path.join(root, f)
                with open(abs_path, "r", encoding="utf-8") as file_in:
                    content = file_in.read()

                rel_parts = os.path.relpath(abs_path, PROJECTS_ROOT).split(os.sep)
                track = rel_parts[0] if len(rel_parts) > 1 else "通用项目"
                course = rel_parts[1] if len(rel_parts) > 2 else "通用课程"

                if content.startswith("---"):
                    parts = content.split("---", 2)
                    fm = parts[1]
                    body = parts[2] if len(parts) > 2 else ""

                    new_fm = fm
                    if "type:" not in new_fm: new_fm += "\ntype: project"
                    else: new_fm = re.sub(r"^type:\s*.*$", 'type: project', new_fm, flags=re.MULTILINE)

                    if "flow:" not in new_fm: new_fm += "\nflow: project"
                    else: new_fm = re.sub(r"^flow:\s*.*$", 'flow: project', new_fm, flags=re.MULTILINE)

                    if "kind:" not in new_fm: new_fm += "\nkind: project"
                    else: new_fm = re.sub(r"^kind:\s*.*$", 'kind: project', new_fm, flags=re.MULTILINE)

                    if "track:" not in new_fm: new_fm += f'\ntrack: "{track}"'
                    else: new_fm = re.sub(r"^track:\s*.*$", f'track: "{track}"', new_fm, flags=re.MULTILINE)

                    if "course:" not in new_fm: new_fm += f'\ncourse: "{course}"'
                    else: new_fm = re.sub(r"^course:\s*.*$", f'course: "{course}"', new_fm, flags=re.MULTILINE)

                    if "status:" not in new_fm: new_fm += '\nstatus: active'

                    new_content = f"---{new_fm.strip()}\n---\n{body.lstrip()}"
                    if new_content != content:
                        with open(abs_path, "w", encoding="utf-8") as file_out:
                            file_out.write(new_content)
                        fixed_fm += 1

    print(f"Cleanup finished. Removed {removed} duplicates, fixed {fixed_fm} frontmatters.")

if __name__ == "__main__":
    import re
    cleanup_duplicates_and_fix_fm()
