#!/usr/bin/env python3
from __future__ import annotations
import ast,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
COURSE=ROOT/"02-Knowledge"/"🧠 学习系统"/"03-量化金融"
PROJECT=ROOT/"03-Projects"/"金融与时序"/"03-量化金融"
LINK_RE=re.compile(r"\[\[([^\]]+)\]\]")
FENCE_RE=re.compile(r"\x60{3}(?:python|py)\s*\n(.*?)\x60{3}",re.S|re.I)

def files(root):
    return [p for p in root.rglob("*.md") if ".recovery-hold" not in p.parts]

def clean(raw):
    return raw.replace("\\|","|").split("|",1)[0].split("#",1)[0].strip()

def link_ok(source,raw,stems):
    target=clean(raw)
    if not target or "\${" in target or "<%" in target: return True
    candidate=Path(*target.replace("\\","/").split("/"))
    if candidate.suffix.lower() not in {".md",".py",".csv",".json",".pdf"}: candidate=candidate.with_suffix(".md")
    if (source.parent/candidate).exists() or (ROOT/candidate).exists():
        return True
    return "/" not in target and Path(target).stem in stems

def main():
    errors=[]; study_count=0
    stems={p.stem for p in files(ROOT)}
    source=COURSE/"📚 教材挂载索引.md"
    for p in files(COURSE):
        text=p.read_text(encoding="utf-8-sig")
        fm=text.split("---",2)[1] if text.startswith("---") and text.count("---")>=2 else ""
        if "type: study" in fm:
            study_count+=1
            for field in ("type:","topic:","course:","tags:","created:","status:","difficulty:","concept:","prerequisites:","related:","flow:","kind:","assessment_exempt:"):
                if field not in fm: errors.append(f"study frontmatter missing {field}: {p.relative_to(ROOT)}")
            if "assessment_exempt: false" in fm and "## 🧪 学完本节后可完成的作业" not in text: errors.append(f"study card missing assessment: {p.relative_to(ROOT)}")
            if "assessment_exempt: true" in fm and "assessment_exempt_reason:" not in fm: errors.append(f"exempt page missing reason: {p.relative_to(ROOT)}")
        for block in FENCE_RE.findall(text):
            try: ast.parse(block)
            except SyntaxError as exc: errors.append(f"invalid Python block in {p.relative_to(ROOT)}: {exc.msg}")
        for raw in LINK_RE.findall(text):
            if not link_ok(p,raw,stems): errors.append(f"broken link: {p.relative_to(ROOT)} -> {clean(raw)}")
    for p in files(PROJECT):
        text=p.read_text(encoding="utf-8-sig")
        for raw in LINK_RE.findall(text):
            if not link_ok(p,raw,stems): errors.append(f"broken project link: {p.relative_to(ROOT)} -> {clean(raw)}")
    for p in files(COURSE)+files(PROJECT):
        text=p.read_text(encoding="utf-8-sig")
        for term in ("李宏毅式","李宏毅-CMU模式","4-Tier","Boss Baseline","阶梯作业","[支线任务]"):
            if term in text: errors.append(f"legacy label in {p.relative_to(ROOT)}: {term}")
    if not source.exists() or "## 多源课程融合自评" not in source.read_text(encoding="utf-8-sig"): errors.append("source index missing fusion self-assessment")
    for name in ("课后作业","阶段作业","大作业"):
        directory=PROJECT/name
        if not directory.is_dir() or not list(directory.glob("*.md")): errors.append(f"assignment directory missing: {name}")
    if study_count<100: errors.append(f"unexpectedly low study-card count: {study_count}")
    if errors:
        print(f"Quant course quality gate failed with {len(errors)} issue(s):")
        for error in errors: print(f"- {error}")
        return 1
    print(f"Quant course quality gate passed: {study_count} study cards, five stages, links, metadata, sources, and assignment contracts are valid.")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
