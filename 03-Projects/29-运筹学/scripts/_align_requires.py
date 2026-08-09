import re, glob
WIKILINK = re.compile(r'\[\[([^\]]+)\]\]')
def clean(s):
    return s.split('|')[0].split('#')[0].strip()
def fm_requires(path):
    txt = open(path, encoding='utf-8-sig').read()
    m = re.match(r'^---\s*\n(.*?)\n---\s*\n', txt, re.S)
    if not m: return []
    block = m.group(1); req=[]; cap=False
    for ln in block.split('\n'):
        s = ln.rstrip('\r')
        if re.match(r'^requires:\s*$', s): cap=True; continue
        if cap:
            if re.match(r'^\s*-\s+', s):
                mm=WIKILINK.search(s)
                if mm: req.append(clean(mm.group(1)))
            else:
                if s.strip()=='' or not s.startswith(' '): break
    return req
def body_req(path):
    txt = open(path, encoding='utf-8-sig').read()
    m = re.search(r'##\s*所需知识\s*\n(.*?)(?=\n##\s|\Z)', txt, re.S)
    if not m: return None
    return [clean(x) for x in WIKILINK.findall(m.group(1))]
def replace_fm_requires(path, union):
    txt = open(path, encoding='utf-8-sig').read()
    m = re.match(r'^---\s*\n(.*?)\n---\s*\n', txt, re.S)
    block = m.group(1)
    lines = block.split('\n'); out=[]; cap=False; done=False
    for ln in lines:
        s = ln.rstrip('\r')
        if re.match(r'^requires:\s*$', s):
            cap=True; out.append(ln); continue
        if cap:
            if re.match(r'^\s*-\s+', s):
                if not done:
                    for item in union:
                        out.append(f'  - "[[{item}]]"')
                    done=True
                continue  # skip original items
            else:
                if s.strip()=='' or not s.startswith(' '):
                    if not done:
                        for item in union:
                            out.append(f'  - "[[{item}]]"')
                        done=True
                    cap=False; out.append(ln); continue
        out.append(ln)
    if cap and not done:
        for item in union:
            out.append(f'  - "[[{item}]]"')
    newblock='\n'.join(out)
    open(path,'w',encoding='utf-8').write(txt[:m.start(1)]+newblock+txt[m.end(1):])
def append_body_req(path, union):
    txt = open(path, encoding='utf-8-sig').read()
    m = re.search(r'(##\s*所需知识\s*\n)(.*?)(?=\n##\s|\Z)', txt, re.S)
    head, body = m.group(1), m.group(2)
    existing = [clean(x) for x in WIKILINK.findall(body)]
    add = [x for x in union if x not in existing]
    if not add: return False
    newbody = body.rstrip('\n')
    for item in add:
        newbody += f'\n- [[{item}]]'
    newbody += '\n'
    open(path,'w',encoding='utf-8').write(txt[:m.start()]+head+newbody+txt[m.end():])
    return True
changed=[]
for f in sorted(glob.glob('课后作业/*.md')+glob.glob('阶段作业/*.md')+glob.glob('大作业/*.md')):
    fm=fm_requires(f); bd=body_req(f)
    if bd is None: continue
    fset,wset=set(fm),set(bd)
    if fset==wset: continue
    union = sorted(fset | wset)
    ch=[]
    if fset - wset:
        if append_body_req(f, union): ch.append(('正文+', sorted(fset-wset)))
    if wset - fset:
        replace_fm_requires(f, union); ch.append(('fm+', sorted(wset-fset)))
    # if only fm superset, also set fm to union (already = fset) -> no change needed; if only body superset, set fm=union
    if wset - fset:
        pass
    else:
        # fm superset, body now=union, ensure fm also=union
        replace_fm_requires(f, union)
    changed.append((f, ch))
for f, ch in changed:
    print(f'{f}')
    for tag, items in ch:
        print(f'   {tag}: {items}')
print(f'--- 共对齐 {len(changed)} 份 ---')
