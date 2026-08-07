# -*- coding: utf-8 -*-
"""11-计算机组成原理 frontmatter 批量修复脚本（AGENTS.md §3）。

用途：为课程 6 个阶段目录下的知识卡补 course/stage_moc/flow/kind，
把无内容的空壳模板卡 status 从 ongoing 改为 planned；
删除禁用的静态 downstream 字段。

用法：
  python fix_course11_frontmatter.py --dry-run    # 只预览不改写
  python fix_course11_frontmatter.py              # 实际改写
"""
import os
import re
import sys
import yaml

ROOT = r"F:\-\02-Knowledge\🧠 学习系统\11-计算机组成原理"
COURSE = "计算机组成原理"

STAGE_MOC = {
    "00-总图景": "[[🗺️ 阶段零：总图景]]",
    "01-CPU架构": "[[⚙️ 第一阶段：CPU架构]]",
    "02-内存管理": "[[💾 第二阶段：内存管理]]",
    "03-进程调度": "[[🔄 第三阶段：进程调度]]",
    "04-并发控制": "[[🔒 第四阶段：并发控制]]",
    "05-总复盘": "[[✅ 第五阶段：总复盘]]",
}

# canonical MOC filenames — skip them (already fixed)
MOC_FILES = {
    "00-总图景/🗺️ 阶段零：总图景.md",
    "01-CPU架构/⚙️ 第一阶段：CPU架构.md",
    "02-内存管理/💾 第二阶段：内存管理.md",
    "03-进程调度/🔄 第三阶段：进程调度.md",
    "04-并发控制/🔒 第四阶段：并发控制.md",
    "05-总复盘/✅ 第五阶段：总复盘.md",
}

DRY_RUN = "--dry-run" in sys.argv

def has_substance(body: str) -> bool:
    """粗略判断正文是否有实质内容（非空模板壳）。"""
    lines = body.splitlines()
    substantive = 0
    for ln in lines:
        s = ln.strip()
        if not s or s.startswith("#") or s.startswith("```") or s.startswith("~~~"):
            continue
        if re.match(r"^[>\-*•\d.\s\[\]|]+$", s):
            continue
        if re.match(r"^(一句话定义|核心定义|关键方法|一个最小例子|前置|相关|待补|这张卡要回答的问题[：:].*)$", s):
            continue
        if re.match(r"^（[^）]*|> *$", s):
            continue
        substantive += 1
    return substantive >= 6

def main():
    changed, planned_set, removed_downstream = [], 0, 0
    for dirpath, _, names in os.walk(ROOT):
        d = os.path.relpath(dirpath, ROOT).replace("\\", "/")
        if d not in STAGE_MOC:
            continue
        stage_moc = STAGE_MOC[d]
        for n in sorted(names):
            if not n.endswith(".md"):
                continue
            rel = f"{d}/{n}"
            if rel in MOC_FILES:
                continue
            path = os.path.join(dirpath, n)
            with open(path, encoding="utf-8") as f:
                content = f.read()
            m = re.match(r"^---\n(.*?)\n---\n?", content, re.S)
            if not m:
                continue
            fm_text = m.group(1)
            try:
                fm = yaml.safe_load(fm_text) or {}
            except Exception as e:
                print(f"  [PARSE-ERR] {rel}: {e}")
                continue
            if not isinstance(fm, dict):
                continue
            orig = dict(fm)
            fm["type"] = "study"
            fm["course"] = COURSE
            fm["stage_moc"] = stage_moc
            fm["flow"] = "knowledge"
            if "kind" not in fm:
                fm["kind"] = "concept"
            body = content[m.end():]
            if fm.get("status") == "ongoing" and not has_substance(body):
                fm["status"] = "planned"
                planned_set += 1
            if "downstream" in fm:
                del fm["downstream"]
                removed_downstream += 1
            if fm == orig:
                continue
            new_fm = yaml.safe_dump(fm, allow_unicode=True, sort_keys=False, default_flow_style=False).strip()
            new_content = "---\n" + new_fm + "\n---\n" + body
            changed.append((rel, new_content))
    print(f"would change: {len(changed)} files | shells->planned: {planned_set} | downstream removed: {removed_downstream}")
    if DRY_RUN:
        for rel, _ in changed:
            print("  ~", rel)
        return
    for rel, new_content in changed:
        path = os.path.join(ROOT, rel)
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("  W", rel)
    print("done.")

if __name__ == "__main__":
    main()
