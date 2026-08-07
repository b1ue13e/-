import sys
sys.stdout.reconfigure(encoding='utf-8')
p = "F:/" + "-" + "/03-Projects/05-计算机视觉/tests/verify_links_cv.py"
with open(p, encoding='utf-8') as f:
    c = f.read()

# 在 upstream 检查后（"# 空壳检测"前）插入正文链接检查
old = """        # 空壳检测：<1500 字节
        if os.path.getsize(path) < 1500:
            issues.append(f'[疑似空壳] {rel}: {os.path.getsize(path)} 字节')"""

new = """        # 正文 wikilink 可解析性（跳过 frontmatter 与代码围栏；处理 \\\\| 转义）
        body = content.split('---', 2)[2] if content.startswith('---') else content
        in_fence = False
        for i, line in enumerate(body.split('\\n'), 1):
            if re.match(r'^\\s*(```|~~~)', line):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            for raw in re.findall(r'\\[\\[([^\\]]+)\\]\\]', line):
                target = re.sub(r'\\\\\\|.*$', '', raw).split('#')[0].strip().removesuffix('.md')
                if not resolve(target, os.path.dirname(path)):
                    issues.append(f'[正文死链] {rel}:{i} [[{raw[:60]}]]')
        # 空壳检测：<1500 字节
        if os.path.getsize(path) < 1500:
            issues.append(f'[疑似空壳] {rel}: {os.path.getsize(path)} 字节')"""

assert old in c
c = c.replace(old, new)
with open(p, 'w', encoding='utf-8') as f:
    f.write(c)
print("verify_links_cv.py 已补充正文 wikilink 可解析性检查")
