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
# 各阶段目录 -> 实际 study 卡文件名
stage_dirs = {
    "01": "01-底层基石",
    "02": "02-深度学习内核",
    "03": "03-视觉核心任务",
    "04": "04-前沿架构探索",
    "05": "05-专业深化与工程落地",
}
# 阶段 MOC 文件名
moc_files = {
    "01": "01-底层基石/🏗️ 第一阶段：底层基石.md",
    "02": "02-深度学习内核/🧠 第二阶段：深度学习内核.md",
    "03": "03-视觉核心任务/🎯 第三阶段：视觉核心任务.md",
    "04": "04-前沿架构探索/🚀 第四阶段：前沿架构探索.md",
    "05": "05-专业深化与工程落地/🏭 第五阶段：专业深化与工程落地.md",
}
for stage, dirname in stage_dirs.items():
    dpath = os.path.join(COURSE, dirname)
    moc_basename = os.path.basename(moc_files[stage])
    # 实际卡（排除阶段 MOC 文件本身）
    cards = []
    for f in os.listdir(dpath):
        if not f.endswith('.md'):
            continue
        if f == moc_basename:
            continue
        with open(os.path.join(dpath, f), encoding='utf-8') as fh:
            c = fh.read()
        if 'type: study' in c:
            cards.append(f[:-3])
    # MOC 中引用的卡（wikilink basename）
    mp = os.path.join(COURSE, moc_files[stage])
    with open(mp, encoding='utf-8') as fh:
        mc = fh.read()
    linked = set()
    for m in re.finditer(r'\[\[([^\]]+?)(?:\||\]\])', mc):
        t = m.group(1).strip().rstrip('\\')
        linked.add(t.split('/')[-1])
    missing = [c for c in cards if c not in linked]
    if missing:
        print(f"阶段{stage} ({dirname}) MOC 漏列 {len(missing)} 张卡:")
        for c in missing:
            print(f"  - {c}")
    else:
        print(f"阶段{stage} ({dirname}): 全部 {len(cards)} 张卡已在 MOC 中 ✅")
