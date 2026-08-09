import re, glob, os
WIKILINK = re.compile(r'\[\[([^\]]+)\]\]')
def clean(s):
    return s.split('|')[0].split('#')[0].strip()

def fm_requires(path):
    txt = open(path, encoding='utf-8-sig').read()
    m = re.match(r'^---\s*\n(.*?)\n---\s*\n', txt, re.S)
    if not m:
        return []
    block = m.group(1)
    # locate 'requires:' then collect following '  - link' lines
    lines = block.split('\n')
    req = []
    capture = False
    for ln in lines:
        s = ln.rstrip('\r')
        if re.match(r'^requires:\s*$', s):
            capture = True
            continue
        if capture:
            if re.match(r'^\s*-\s+', s):
                mm = WIKILINK.search(s)
                if mm:
                    req.append(clean(mm.group(1)))
            else:
                if s.strip() == '' or not s.startswith(' '):
                    break
    return req

def body_req(path):
    txt = open(path, encoding='utf-8-sig').read()
    m = re.search(r'##\s*所需知识\s*\n(.*?)(?:\n##\s|\Z)', txt, re.S)
    if not m:
        return None
    return [clean(x) for x in WIKILINK.findall(m.group(1))]

for f in sorted(glob.glob('课后作业/*.md') + glob.glob('阶段作业/*.md') + glob.glob('大作业/*.md')):
    fm = fm_requires(f)
    bd = body_req(f)
    if bd is None:
        print(f'{f}: 无[所需知识]节; fm_requires={fm}')
        continue
    fset, wset = set(fm), set(bd)
    miss_bd = fset - wset
    miss_fm = wset - fset
    if miss_bd or miss_fm:
        print(f'[MISMATCH] {f}')
        if miss_bd:
            print(f'   fm有/正文缺: {sorted(miss_bd)}')
        if miss_fm:
            print(f'   正文有/fm缺: {sorted(miss_fm)}')
    else:
        print(f'[OK] {f}  (fm={len(fm)}, body={len(bd)})')
print('---done---')
