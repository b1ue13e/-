# -*- coding: utf-8 -*-
import sys, os, glob, re
sys.stdout.reconfigure(encoding='utf-8')
BASE = r'F:/-'
COURSE = os.path.join(BASE, '02-Knowledge', '🧠 学习系统', '07-最优化方法')
PROJ = os.path.join(BASE, '03-Projects', '07-最优化方法')
all_names = set()
for f in glob.glob(os.path.join(BASE, '02-Knowledge', '**', '*.md'), recursive=True) + glob.glob(os.path.join(BASE, '03-Projects', '**', '*.md'), recursive=True):
    all_names.add(os.path.splitext(os.path.basename(f))[0])
files = glob.glob(os.path.join(COURSE, '**', '*.md'), recursive=True) + glob.glob(os.path.join(PROJ, '**', '*.md'), recursive=True)
dead = set()
for f in files:
    t = open(f, encoding='utf-8').read()
    for m in re.findall(r'\[\[([^\]|#]+?)(?:\\\||\||#|\])', t):
        link = m.strip().replace('\\', '')
        if not link or link.startswith('http') or link.endswith(('.png', '.jpg', '.svg')):
            continue
        if '/' in link:
            c1 = os.path.normpath(os.path.join(COURSE, link + '.md'))
            c2 = os.path.normpath(os.path.join(BASE, link + '.md'))
            if not os.path.exists(c1) and not os.path.exists(c2):
                dead.add(link)
        elif link not in all_names:
            dead.add(link)
print('死链:', dead if dead else '无')
