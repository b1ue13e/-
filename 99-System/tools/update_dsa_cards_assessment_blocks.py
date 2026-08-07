import os
import re

COURSE_DIR = r"f:\-\02-Knowledge\🧠 学习系统\10-数据结构与算法"

DATAVIEW_BLOCK = """

## 学完后可以完成

```dataview
LIST
FROM "03-Projects"
WHERE contains(requires, this.file.link)
SORT assignment_level ASC, file.name ASC
```
"""

updated_count = 0
skipped_count = 0

for root, dirs, files in os.walk(COURSE_DIR):
    for f in files:
        if not f.endswith(".md"):
            continue
        if f.startswith("🗺️") or f.startswith("📚") or f.startswith("🧭"):
            continue
        
        path = os.path.join(root, f)
        with open(path, "r", encoding="utf-8") as fp:
            content = fp.read()
        
        # Check if assessment_exempt: true
        if "assessment_exempt: true" in content:
            skipped_count += 1
            continue
            
        if "## 学完后可以完成" in content or "学完后可以完成" in content:
            skipped_count += 1
            continue
            
        # Append block
        new_content = content.rstrip() + DATAVIEW_BLOCK
        with open(path, "w", encoding="utf-8") as fp:
            fp.write(new_content)
        updated_count += 1

print(f"Done! Updated: {updated_count}, Skipped/Exempt/AlreadyPresent: {skipped_count}")
