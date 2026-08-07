import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
KB = "F:" + os.sep + "-"
COURSE = KB + os.sep + "02-Knowledge" + os.sep + "🧠 学习系统" + os.sep + "05-计算机视觉"
SKIP = {'.归档', '.reasonix', '.recovery-hold', '.pytest_cache', '__pycache__', '.git', '.obsidian', '.tmp'}
def walk(base):
    for r, d, fs in os.walk(base):
        d[:] = [x for x in d if x not in SKIP]
        for f in fs:
            if f.endswith('.md'):
                yield os.path.join(r, f)
# 已建 study 卡短名集合
study_names = set()
for p in walk(COURSE):
    with open(p, encoding='utf-8') as f:
        c = f.read()
    if 'type: study' in c:
        study_names.add(os.path.basename(p)[:-3])
# 扫描 MOC 中 ⬜ 行，检查其"笔记列/主题"是否对应已建卡
mocs = [p for p in walk(COURSE) if os.path.basename(p).startswith(('🧭','🏗️','🧠','🎯','🚀','🏭')) and any(k in os.path.basename(p) for k in ('阶段','前置'))]
# 概念名 -> 卡名 模糊映射（MOC 主题列 vs 卡文件名）
for p in mocs:
    with open(p, encoding='utf-8') as f:
        lines = f.readlines()
    for i, l in enumerate(lines, 1):
        if not l.lstrip().startswith('|') or '⬜' not in l:
            continue
        # 提取主题名（**...**）
        cells = l.split('|')
        for cell in cells:
            m = re.search(r'\*\*(.+?)\*\*', cell)
            if m:
                topic = m.group(1).strip()
                # 匹配已建卡
                for sn in study_names:
                    if topic in sn or sn in topic:
                        print(f"{os.path.basename(p)} L{i}: ⬜ 主题『{topic}』匹配已建卡『{sn}』")
                        break
print("扫描完成")
