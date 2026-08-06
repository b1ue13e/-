#!/usr/bin/env python3
from __future__ import annotations
import re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
ROOT=Path(__file__).resolve().parents[2]
COURSE=ROOT/"02-Knowledge"/"🧠 学习系统"/"03-量化金融"
PROJECT=ROOT/"03-Projects"/"金融与时序"/"03-量化金融"
STAGES=["00-前置知识","01-夯实基础","02-量化核心技能","03-研究验证与稳健性","04-深入精通"]
LINK_RE=re.compile(r"\[\[([^\]]+)\]\]")

def files(root):
    return [p for p in root.rglob("*.md") if ".recovery-hold" not in p.parts]

def clean(raw):
    return raw.replace("\\|","|").split("|",1)[0].split("#",1)[0].strip()

def resolve(source,raw,stems):
    target=clean(raw)
    if not target or "\${" in target or "<%" in target:
        return True
    candidate=Path(*target.replace("\\","/").split("/"))
    if candidate.suffix.lower()!=".md":
        candidate=candidate.with_suffix(".md")
    if (source.parent/candidate).exists() or (ROOT/candidate).exists():
        return True
    return "/" not in target and Path(target).stem in stems

def main():
    errors=[]
    route=COURSE/"🗺️ 量化金融学习路径.md"
    source=COURSE/"📚 教材挂载索引.md"
    homework=PROJECT/"🧭 课程作业总索引.md"
    for p in (route,source,homework):
        if not p.exists(): errors.append(f"missing canonical page: {p.relative_to(ROOT)}")
    scoped=files(COURSE)+files(PROJECT)
    stems={p.stem for p in files(ROOT)}
    for stage in STAGES:
        directory=COURSE/stage
        mocs=list(directory.glob("🧭*.md"))
        if len(mocs)!=1:
            errors.append(f"{stage} must contain exactly one stage MOC; found {len(mocs)}")
            continue
        text=mocs[0].read_text(encoding="utf-8-sig")
        if "## 阶段验收与作业" not in text: errors.append(f"{mocs[0].relative_to(ROOT)} missing stage assessment")
        for card in directory.glob("*.md"):
            if not card.name.startswith("🧭") and card.stem not in text:
                errors.append(f"{mocs[0].relative_to(ROOT)} omits {card.name}")
    route_text=route.read_text(encoding="utf-8-sig") if route.exists() else ""
    for week in range(10):
        if not re.search(rf"(?m)^\|\s*{week}\s*\|",route_text): errors.append(f"learning path missing Week {week} row")
    if not re.search(r"阶段\s*3",route_text) or "03-研究验证与稳健性" not in route_text: errors.append("learning path missing formal stage 3")
    if source.exists():
        text=source.read_text(encoding="utf-8-sig")
        if "## 多源课程融合自评" not in text: errors.append("source index missing multi-source self-assessment")
        match=re.search(r"\|\s*\*\*总分\*\*\s*\|\s*\*\*(\d+)\*\*",text)
        if not match or int(match.group(1))<85: errors.append("multi-source self-assessment must be at least 85")
    for name in ("课后作业","阶段作业","大作业"):
        directory=PROJECT/name
        if not directory.is_dir() or not list(directory.glob("*.md")): errors.append(f"missing assignment directory: {name}")
    forbidden=("李宏毅式","李宏毅-CMU模式","4-Tier","Boss Baseline","阶梯作业","[支线任务]")
    for p in scoped:
        text=p.read_text(encoding="utf-8-sig")
        for term in forbidden:
            if term in text: errors.append(f"forbidden legacy label in {p.relative_to(ROOT)}: {term}")
        if p.parent.name in {"课后作业","阶段作业","大作业"} and p.name!="MIT-OCW-18S096-来源与作答说明.md":
            for field in ("course:","source_type:","license:"):
                if field not in text: errors.append(f"assignment metadata incomplete: {p.relative_to(ROOT)} {field}")
        for raw in LINK_RE.findall(text):
            if not resolve(p,raw,stems): errors.append(f"broken link: {p.relative_to(ROOT)} -> {clean(raw)}")
    if errors:
        print(f"Quant route audit failed with {len(errors)} issue(s):")
        for error in errors: print(f"- {error}")
        return 1
    print("Quant route audit passed: five stages, Week 0-9, MOC coverage, assignments, sources, and links are consistent.")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
