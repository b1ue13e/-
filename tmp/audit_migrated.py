import os, re, glob

base = "/f/-/03-Projects/12-信号与系统"
src = os.path.join(base, "项目")  # old originals
dirs = ["课后作业", "阶段作业", "大作业"]

print("=== MIGRATED FILES: H1 / topic / internal 项目 refs ===")
for d in dirs:
    for fp in sorted(glob.glob(os.path.join(base, d, "*.md"))):
        txt = open(fp, encoding="utf-8").read()
        lines = txt.splitlines()
        h1 = next((l for l in lines if l.startswith("# ")), "(none)")
        m = re.search(r"^topic:\s*(.*)$", txt, re.M)
        topic = m.group(1).strip() if m else "(no topic)"
        oldrefs = len(re.findall(r"项目[-/]", txt))
        print(f"[{d}] {os.path.basename(fp)}")
        print(f"    H1={h1!r}")
        print(f"    topic={topic!r}  oldpath_refs={oldrefs}")

print()
print("=== ORIGINAL 项目/ files (to be deleted after backup) ===")
orig = sorted(os.listdir(src))
print(f"count={len(orig)}")
for f in orig:
    print("   ", f)

print()
print("=== DIFF one pair: 项目-卷积计算 vs 课后作业-02-卷积计算 ===")
oa = open(os.path.join(src, "项目-卷积计算.md"), encoding="utf-8").read()
nb = open(os.path.join(base, "课后作业", "信号与系统-课后作业-02-卷积计算.md"), encoding="utf-8").read()
print(f"orig len={len(oa)}  new len={len(nb)}")
# show orig body lines vs new body (after frontmatter)
def body(t):
    if t.startswith("---"):
        i = t.find("\n---", 3)
        return t[i+4:] if i>=0 else t
    return t
ob = body(oa); nb2 = body(nb)
print("--- orig body (first 25 lines) ---")
print("\n".join(ob.splitlines()[:25]))
print("--- new body (first 25 lines) ---")
print("\n".join(nb2.splitlines()[:25]))
