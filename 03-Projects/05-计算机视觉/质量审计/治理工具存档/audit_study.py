# -*- coding: utf-8 -*-
"""C级复审：统计知识卡状态与结构"""
import re, io, os, collections

root = r'F:\-\02-Knowledge\🧠 学习系统\05-计算机视觉'
EXCLUDE = {'.workbuddy', '.归档', '.reasonix'}

study = 0
statuses = collections.Counter()
sizes = []
min_card = None
no_upstream = []
no_stage_moc = []
no_quiz = []

for dp, dns, fns in os.walk(root):
    dns[:] = [d for d in dns if d not in EXCLUDE]
    for fn in fns:
        if not fn.endswith('.md') or fn.startswith('🗺') or fn.startswith('📚'):
            continue
        fp = os.path.join(dp, fn)
        with io.open(fp, encoding='utf-8-sig') as f:
            content = f.read()
        m = re.match(r'^---\r?\n(.*?)\r?\n---', content, re.S)
        fm = m.group(1) if m else ''
        if not re.search(r'^type: study', fm, re.M):
            continue
        study += 1
        st = re.search(r'^status: (\S+)', fm, re.M)
        statuses[st.group(1) if st else 'MISSING'] += 1
        sizes.append(len(content))
        rel = os.path.relpath(fp, root)
        if not re.search(r'^upstream:', fm, re.M):
            no_upstream.append(rel)
        if not re.search(r'^stage_moc:', fm, re.M):
            no_stage_moc.append(rel)
        if '自测' not in content:
            no_quiz.append(rel)
        if min_card is None or len(content) < min_card[0]:
            min_card = (len(content), rel)

print(f'study 卡总数: {study}')
print(f'状态分布: {dict(statuses)}')
print(f'平均大小: {sum(sizes)//len(sizes)} 字节, 最薄: {min_card}')
print(f'缺 upstream: {len(no_upstream)}')
for x in no_upstream[:5]:
    print(f'   {x}')
print(f'缺 stage_moc: {len(no_stage_moc)}')
print(f'缺自测题: {len(no_quiz)}')
for x in no_quiz[:8]:
    print(f'   {x}')
