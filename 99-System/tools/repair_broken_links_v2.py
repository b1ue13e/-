import os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"f:\-"

stem_to_path = {}
ambiguous_stems = set()
for dp, dns, fns in os.walk(ROOT):
    dns[:] = [d for d in dns if d not in [".git",".obsidian",".claude",".claudian","__pycache__"]]
    for f in fns:
        if not f.endswith(".md"): continue
        rel = os.path.relpath(os.path.join(dp,f), ROOT).replace("\\","/")
        stem = f[:-3]; sl = stem.lower()
        if sl in stem_to_path: ambiguous_stems.add(sl)
        else: stem_to_path[sl] = rel[:-3]
print(f"Unique stems: {len(stem_to_path)-len(ambiguous_stems)}, ambiguous: {len(ambiguous_stems)}")

EXPLICIT = {
    "02-Knowledge/\U0001f9e0 \u5b66\u4e60\u7cfb\u7edf/11-\u8ba1\u7b97\u673a\u7ec4\u6210\u539f\u7406/\U0001f5fa\ufe0f \u5b66\u4e60\u8def\u5f84": "\U0001f5fa\ufe0f \u8ba1\u7b97\u673a\u7ec4\u6210\u539f\u7406\u5b66\u4e60\u8def\u5f84",
    "02-Knowledge/\U0001f9e0 \u5b66\u4e60\u7cfb\u7edf/12-\u4fe1\u53f7\u4e0e\u7cfb\u7edf/\U0001f5fa\ufe0f \u5b66\u4e60\u8def\u5f84": "\U0001f5fa\ufe0f \u4fe1\u53f7\u4e0e\u7cfb\u7edf\u5b66\u4e60\u8def\u5f84",
    "02-Knowledge/\U0001f9e0 \u5b66\u4e60\u7cfb\u7edf/06-\u5e38\u5fae\u5206\u65b9\u7a0b/\U0001f5fa\ufe0f \u5b66\u4e60\u8def\u5f84": "\U0001f5fa\ufe0f \u5e38\u5fae\u5206\u65b9\u7a0b\u5b66\u4e60\u8def\u5f84",
    "02-Knowledge/\U0001f9e0 \u5b66\u4e60\u7cfb\u7edf/02-\u65f6\u95f4\u5e8f\u5217\u5206\u6790/\U0001f5fa\ufe0f \u5b66\u4e60\u8def\u5f84": "\U0001f5fa\ufe0f \u65f6\u95f4\u5e8f\u5217\u5206\u6790\u5b66\u4e60\u8def\u5f84",
    "02-Knowledge/\U0001f9e0 \u5b66\u4e60\u7cfb\u7edf/03-\u91cf\u5316\u91d1\u878d/\U0001f5fa\ufe0f \u5b66\u4e60\u8def\u5f84": "\U0001f5fa\ufe0f \u91cf\u5316\u91d1\u878d\u5b66\u4e60\u8def\u5f84",
    "02-Knowledge/\U0001f9e0 \u5b66\u4e60\u7cfb\u7edf/07-\u6700\u4f18\u5316\u65b9\u6cd5/\U0001f5fa\ufe0f \u5b66\u4e60\u8def\u5f84": "\U0001f5fa\ufe0f \u6700\u4f18\u5316\u65b9\u6cd5\u5b66\u4e60\u8def\u5f84",
    "02-Knowledge/\U0001f9e0 \u5b66\u4e60\u7cfb\u7edf/17-\u673a\u5668\u5b66\u4e60/\U0001f5fa\ufe0f \u5b66\u4e60\u8def\u5f84": "\U0001f5fa\ufe0f \u673a\u5668\u5b66\u4e60\u5b66\u4e60\u8def\u5f84",
    "02-Knowledge/\U0001f9e0 \u5b66\u4e60\u7cfb\u7edf/33-\u8d1d\u53f6\u65af\u7edf\u8ba1/\U0001f5fa\ufe0f \u5b66\u4e60\u8def\u5f84": "\U0001f5fa\ufe0f \u8d1d\u53f6\u65af\u7edf\u8ba1\u5b66\u4e60\u8def\u5f84",
    "02-Knowledge/\U0001f9e0 \u5b66\u4e60\u7cfb\u7edf/30-\u5e94\u7528\u56de\u5f52\u5206\u6790/\U0001f5fa\ufe0f \u5b66\u4e60\u8def\u5f84": "\U0001f5fa\ufe0f \u5e94\u7528\u56de\u5f52\u5206\u6790\u5b66\u4e60\u8def\u5f84",
    "02-Knowledge/\U0001f9e0 \u5b66\u4e60\u7cfb\u7edf/01-\u793e\u4ea4\u7f51\u7edc\u6316\u6398/\U0001f5fa\ufe0f \u5b66\u4e60\u8def\u5f84": "\U0001f5fa\ufe0f \u793e\u4ea4\u7f51\u7edc\u6316\u6398\u5b66\u4e60\u8def\u5f84",
    "02-Knowledge/\U0001f9e0 \u5b66\u4e60\u7cfb\u7edf/04-\u79bb\u6563\u6570\u5b66/\U0001f5fa\ufe0f \u5b66\u4e60\u8def\u5f84": "\U0001f5fa\ufe0f \u79bb\u6563\u6570\u5b66\u5b66\u4e60\u8def\u5f84",
    "02-Knowledge/\U0001f9e0 \u5b66\u4e60\u7cfb\u7edf/05-\u8ba1\u7b97\u673a\u89c6\u89c9/\U0001f5fa\ufe0f \u5b66\u4e60\u8def\u5f84": "\U0001f5fa\ufe0f \u8ba1\u7b97\u673a\u89c6\u89c9\u5b66\u4e60\u8def\u5f84",
    "02-Knowledge/\U0001f9e0 \u5b66\u4e60\u7cfb\u7edf/08-NLP\u5168\u6808/\U0001f5fa\ufe0f \u5b66\u4e60\u8def\u5f84": "\U0001f5fa\ufe0f NLP\u5168\u6808\u5b66\u4e60\u8def\u5f84",
    "02-Knowledge/\U0001f9e0 \u5b66\u4e60\u7cfb\u7edf/09-\u9ad8\u7b49\u4ee3\u6570/\U0001f5fa\ufe0f \u5b66\u4e60\u8def\u5f84": "\U0001f5fa\ufe0f \u9ad8\u7b49\u4ee3\u6570\u5b66\u4e60\u8def\u5f84",
    "02-Knowledge/\U0001f9e0 \u5b66\u4e60\u7cfb\u7edf/10-\u6570\u636e\u7ed3\u6784\u4e0e\u7b97\u6cd5/\U0001f5fa\ufe0f \u5b66\u4e60\u8def\u5f84": "\U0001f5fa\ufe0f \u6570\u636e\u7ed3\u6784\u4e0e\u7b97\u6cd5\u5b66\u4e60\u8def\u5f84",
    "02-Knowledge/\U0001f9e0 \u5b66\u4e60\u7cfb\u7edf/13-\u5f3a\u5316\u5b66\u4e60/\U0001f5fa\ufe0f \u5b66\u4e60\u8def\u5f84": "\U0001f5fa\ufe0f \u5f3a\u5316\u5b66\u4e60\u5b66\u4e60\u8def\u5f84",
    "02-Knowledge/\U0001f9e0 \u5b66\u4e60\u7cfb\u7edf/14-\u6982\u7387\u56fe\u6a21\u578b/\U0001f5fa\ufe0f \u5b66\u4e60\u8def\u5f84": "\U0001f5fa\ufe0f \u6982\u7387\u56fe\u6a21\u578b\u5b66\u4e60\u8def\u5f84",
    "02-Knowledge/\U0001f9e0 \u5b66\u4e60\u7cfb\u7edf/15-\u63a7\u5236\u4e0e\u673a\u5668\u4eba\u5b66/\U0001f5fa\ufe0f \u5b66\u4e60\u8def\u5f84": "\U0001f5fa\ufe0f \u63a7\u5236\u4e0e\u673a\u5668\u4eba\u5b66\u5b66\u4e60\u8def\u5f84",
    "02-Knowledge/\U0001f9e0 \u5b66\u4e60\u7cfb\u7edf/16-\u591a\u5143\u7edf\u8ba1/\U0001f5fa\ufe0f \u5b66\u4e60\u8def\u5f84": "\U0001f5fa\ufe0f \u591a\u5143\u7edf\u8ba1\u5b66\u4e60\u8def\u5f84",
    "02-Knowledge/\U0001f9e0 \u5b66\u4e60\u7cfb\u7edf/22-\u6982\u7387\u8bba\u4e0e\u6570\u7406\u7edf\u8ba1/\U0001f5fa\ufe0f \u5b66\u4e60\u8def\u5f84": "\U0001f5fa\ufe0f \u6982\u7387\u8bba\u4e0e\u6570\u7406\u7edf\u8ba1\u5b66\u4e60\u8def\u5f84",
    "02-Knowledge/\U0001f9e0 \u5b66\u4e60\u7cfb\u7edf/23-\u56fe\u795e\u7ecf\u7f51\u7edc/\U0001f5fa\ufe0f \u5b66\u4e60\u8def\u5f84": "\U0001f5fa\ufe0f \u56fe\u795e\u7ecf\u7f51\u7edc\u5b66\u4e60\u8def\u5f84",
    "02-Knowledge/\U0001f9e0 \u5b66\u4e60\u7cfb\u7edf/24-\u968f\u673a\u8fc7\u7a0b/\U0001f5fa\ufe0f \u5b66\u4e60\u8def\u5f84": "\U0001f5fa\ufe0f \u968f\u673a\u8fc7\u7a0b\u5b66\u4e60\u8def\u5f84",
    "02-Knowledge/\U0001f9e0 \u5b66\u4e60\u7cfb\u7edf/27-\u6cdb\u51fd\u5206\u6790/\U0001f5fa\ufe0f \u5b66\u4e60\u8def\u5f84": "\U0001f5fa\ufe0f \u6cdb\u51fd\u5206\u6790\u5b66\u4e60\u8def\u5f84",
    "02-Knowledge/\U0001f9e0 \u5b66\u4e60\u7cfb\u7edf/28-\u6570\u5b66\u5206\u6790/\U0001f5fa\ufe0f \u5b66\u4e60\u8def\u5f84": "\U0001f5fa\ufe0f \u6570\u5b66\u5206\u6790\u5b66\u4e60\u8def\u5f84",
    "02-Knowledge/\U0001f9e0 \u5b66\u4e60\u7cfb\u7edf/29-\u8fd0\u7b79\u5b66/\U0001f5fa\ufe0f \u5b66\u4e60\u8def\u5f84": "\U0001f5fa\ufe0f \u8fd0\u7b79\u5b66\u5b66\u4e60\u8def\u5f84",
    "02-Knowledge/\U0001f9e0 \u5b66\u4e60\u7cfb\u7edf/34-\u504f\u5fae\u5206\u65b9\u7a0b/\U0001f5fa\ufe0f \u5b66\u4e60\u8def\u5f84": "\U0001f5fa\ufe0f \u504f\u5fae\u5206\u65b9\u7a0b\u5b66\u4e60\u8def\u5f84",
    "02-Knowledge/\U0001f9e0 \u5b66\u4e60\u7cfb\u7edf/35-\u6570\u5024\u5206\u6790/\U0001f5fa\ufe0f \u5b66\u4e60\u8def\u5f84": "\U0001f5fa\ufe0f \u6570\u5024\u5206\u6790\u5b66\u4e60\u8def\u5f84",
    "02-Knowledge/\U0001f9e0 \u5b66\u4e60\u7cfb\u7edf/36-\u6570\u636e\u6316\u6398\u4e0e\u4fe1\u606f\u68c0\u7d22/\U0001f5fa\ufe0f \u5b66\u4e60\u8def\u5f84": "\U0001f5fa\ufe0f \u6570\u636e\u6316\u6398\u4e0e\u4fe1\u606f\u68c0\u7d22\u5b66\u4e60\u8def\u5f84",
}
print(f"Explicit mappings loaded: {len(EXPLICIT)}")

link_re = re.compile(r"\[\[([^\]]+)\]\]")
fixed_files = 0; total_replaced = 0

def resolve(raw):
    global total_replaced
    alias = raw.split("|",1)[1] if "|" in raw else ""
    tp = raw.split("|",1)[0]
    anchor = ("#" + tp.split("#",1)[1]) if "#" in tp else ""
    path = tp.split("#",1)[0]
    path_c = path.rstrip("\\/").strip(); changed = (path_c != path)
    if path_c in EXPLICIT: path_c = EXPLICIT[path_c]; changed = True
    if "/" in path_c:
        stem = os.path.basename(path_c); sl = stem.lower()
        if sl in stem_to_path and sl not in ambiguous_stems:
            path_c = stem_to_path[sl]; changed = True
    if not changed: return None
    total_replaced += 1
    inner = path_c + anchor + ("|" + alias if alias else "")
    return f"[[{inner}]]"

for dp, dns, fns in os.walk(ROOT):
    dns[:] = [d for d in dns if d not in [".git",".obsidian",".claude",".claudian","__pycache__"]]
    for f in fns:
        if not f.endswith(".md"): continue
        p = os.path.join(dp,f)
        try: content = open(p,encoding="utf-8",errors="ignore").read()
        except: continue
        def rep(m):
            r = resolve(m.group(1))
            return r if r else m.group(0)
        nc = link_re.sub(rep, content)
        if nc != content:
            open(p,"w",encoding="utf-8",newline="\n").write(nc)
            fixed_files += 1

print(f"Done. Modified {fixed_files} files, repaired {total_replaced} links.")
