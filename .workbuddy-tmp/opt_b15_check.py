# -*- coding: utf-8 -*-
import sys, os, glob, re
from collections import Counter
sys.stdout.reconfigure(encoding='utf-8')
BASE = r'F:/-'
COURSE = os.path.join(BASE, '02-Knowledge', '🧠 学习系统', '07-最优化方法')
PROJ = os.path.join(BASE, '03-Projects', '07-最优化方法')
allmd = glob.glob(os.path.join(COURSE, '**', '*.md'), recursive=True)
cards = [f for f in allmd if not os.path.basename(f).startswith(('🧭', '🗺', '📚'))]

print('=== B15 全量验证 ===')
print('1. 知识卡数:', len(cards))
no_anki = [os.path.basename(f) for f in cards if '<!-- id:' not in open(f, encoding='utf-8').read()]
no_quiz = [os.path.basename(f) for f in cards if '[!question]' not in open(f, encoding='utf-8').read()]
print('2. 无Anki卡:', no_anki if no_anki else '无')
print('3. 无自测卡:', no_quiz if no_quiz else '无')

ids = []
for f in allmd:
    ids += re.findall(r'<!-- id: (\S+) -->', open(f, encoding='utf-8').read())
dup = {k: v for k, v in Counter(ids).items() if v > 1}
print('4. Anki id 总数:', len(ids), '| 重复:', dup if dup else '无')

# 紧凑卡行数（检查是否达标）
print('5. 深化卡行数:')
for root, dirs, fs in os.walk(COURSE):
    for fn in sorted(fs):
        if not fn.endswith('.md') or fn.startswith('🧭'):
            continue
        t = open(os.path.join(root, fn), encoding='utf-8').read()
        n = len(t.splitlines())
        if n < 150:
            print('   [短]', fn, n, '行')

# 坏公式
bad = []
for f in allmd:
    t = open(f, encoding='utf-8').read()
    for p in ['gpprox', 'grg', 'glpha', 'array(`', 'beqin', 'lamba']:
        if p in t:
            bad.append((os.path.basename(f), p))
print('6. 坏公式残留:', bad if bad else '无')

# upstream 空数组
empty_up = [os.path.basename(f) for f in allmd if re.search(r'^upstream:\s*\[\s*\]', open(f, encoding='utf-8').read(), re.M)]
print('7. 空upstream:', empty_up if empty_up else '无')

# 缺学完后可以完成
miss = [os.path.basename(f) for f in cards if '学完后可以完成' not in open(f, encoding='utf-8').read()]
print('8. 缺派生区块:', miss if miss else '无')

# 缺H1
no_h1 = [os.path.basename(f) for f in cards if not re.search(r'^# .+', open(f, encoding='utf-8').read(), re.M)]
print('9. 缺H1:', no_h1 if no_h1 else '无')
