import re, glob, os

print("=== 作业 frontmatter stage_id / assignment_level ===")
for f in sorted(glob.glob("03-Projects/系统与硬件/11-计算机组成原理/**/*.md", recursive=True)):
    if "质量审计" in f or "索引" in f:
        continue
    head = open(f, encoding="utf-8").read()[:500]
    sid = re.search(r"stage_id:\s*\"(\d+)\"", head)
    lvl = re.search(r"assignment_level:\s*(\w+)", head)
    print("  ", sid.group(1) if sid else "NONE", lvl.group(1) if lvl else "?", os.path.basename(f))

print("=== MOC 作业入口 Dataview stage_id ===")
for f in sorted(glob.glob("02-Knowledge/🧠 学习系统/11-计算机组成原理/*/*.md")):
    txt = open(f, encoding="utf-8").read()
    m = re.search(r"WHERE stage_id = \"([^\"]+)\"", txt)
    if m:
        print("  ", os.path.basename(f), "->", m.group(1))

print("=== dataviewjs 旧路径残留 '05-总复盘' ===")
for f in sorted(glob.glob("02-Knowledge/🧠 学习系统/11-计算机组成原理/**/*.md", recursive=True)):
    txt = open(f, encoding="utf-8").read()
    if "05-总复盘" in txt:
        print("  ", f)

print("=== MOC phase frontmatter ===")
for f in sorted(glob.glob("02-Knowledge/🧠 学习系统/11-计算机组成原理/*/*.md")):
    txt = open(f, encoding="utf-8").read()
    if "kind: moc" not in txt and "kind:index" not in txt:
        continue
    m = re.search(r"^phase:\s*(\d+)", txt, re.M)
    print("  ", os.path.basename(f), "-> phase:", m.group(1) if m else "NONE")
