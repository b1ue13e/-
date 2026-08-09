# -*- coding: utf-8 -*-
import sys, os, glob, re
from collections import Counter
sys.stdout.reconfigure(encoding='utf-8')
base = r'F:/-/02-Knowledge/🧠 学习系统/07-最优化方法'
ids = []
for f in glob.glob(base + '/**/*.md', recursive=True):
    ids += re.findall(r'<!-- id: (\S+) -->', open(f, encoding='utf-8').read())
dup = {k: v for k, v in Counter(ids).items() if v > 1}
print('全课程Anki id总数:', len(ids), '| 重复:', dup if dup else '无')
for n in ['分布式优化', 'SDP松弛', '稀疏与结构化']:
    for root, dirs, fs in os.walk(base):
        for fn in fs:
            if n in fn and fn.endswith('.md'):
                t = open(os.path.join(root, fn), encoding='utf-8').read()
                a = t.count('<!-- id:')
                q = t.count('[!question]')
                print(fn, ':', len(t.splitlines()), '行, Anki:', a, ', 自测:', q)
