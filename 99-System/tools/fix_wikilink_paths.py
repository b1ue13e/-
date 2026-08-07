import sys, os, glob, re

sys.stdout.reconfigure(encoding='utf-8')

kb_dir = r'f:\-\02-Knowledge\🧠 学习系统\10-数据结构与算法'
proj_dir = r'f:\-\03-Projects\10-数据结构与算法'

files = [y for x in os.walk(kb_dir) for y in glob.glob(os.path.join(x[0], '*.md'))] + \
        [y for x in os.walk(proj_dir) for y in glob.glob(os.path.join(x[0], '*.md'))]

replacements = [
    (r'\[\[03-Projects/课程作业/10-数据结构与算法/课程作业总表([^\]]*)\]\]', r'[[课程作业总表\1]]'),
    (r'\[\[03-Projects/课程作业/10-数据结构与算法/项目-算法实现、复杂度与随机测试([^\]]*)\]\]', r'[[项目-算法实现、复杂度与随机测试\1]]'),
    (r'\[\[03-Projects/10-数据结构与算法/大作业/10-数据结构与算法-大作业-BYOW随机迷宫生成与高级数据结构\\([^\]]*)\]\]', r'[[10-数据结构与算法-大作业-BYOW随机迷宫生成与高级数据结构\1]]'),
    (r'\[\[03-Projects/10-数据结构与算法/大作业/10-数据结构与算法-大作业-BYOW随机迷宫生成与高级数据结构([^\]]*)\]\]', r'[[10-数据结构与算法-大作业-BYOW随机迷宫生成与高级数据结构\1]]'),
    (r'\[\[03-Projects/10-数据结构与算法/🧭 课程作业总索引([^\]]*)\]\]', r'[[🧭 课程作业总索引\1]]'),
    (r'\[\[03-Projects/10-数据结构与算法/质量审计/课程严苛审计([^\]]*)\]\]', r'[[课程严苛审计\1]]'),
]

fixed_count = 0

for f in files:
    with open(f, 'r', encoding='utf-8', errors='ignore') as fp:
        content = fp.read()
    original = content
    for pattern, repl in replacements:
        content = re.sub(pattern, repl, content)
    if content != original:
        with open(f, 'w', encoding='utf-8') as fp:
            fp.write(content)
        fixed_count += 1

print(f'Fixed wikilink path prefixes in {fixed_count} files!')
