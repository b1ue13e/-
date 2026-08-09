import subprocess, os, sys
sys.stdout.reconfigure(encoding='utf-8')
env = dict(os.environ, GIT_OPTIONAL_LOCKS='0')
base = ["git", "-c", "core.fsmonitor=false"]
cwd = "F:/" + os.sep + "-"
# 列出课程范围所有 M 文件
r = subprocess.run(base + ["status", "--short", "--",
    "02-Knowledge/🧠 学习系统/05-计算机视觉", "03-Projects/05-计算机视觉"],
    capture_output=True, text=True, encoding='utf-8', cwd=cwd, env=env)
lines = [l for l in r.stdout.split('\n') if l.strip()]
modified = []
for l in lines:
    if l.startswith(' M '):
        path = l[3:].strip().strip('"')
        if '.reasonix' in path or '.归档' in path:
            continue
        modified.append(path)
print(f"待还原 M 文件: {len(modified)}")
for p in modified:
    # 确认无内容差异（-w）
    r2 = subprocess.run(base + ["diff", "-w", "--", p],
        capture_output=True, text=True, encoding='utf-8', cwd=cwd, env=env)
    diffs = [l for l in r2.stdout.split('\n') if l.startswith(('+', '-')) and not l.startswith(('+++', '---'))]
    if diffs:
        print(f"  [有内容差异，跳过] {p}: {len(diffs)} 行")
    else:
        subprocess.run(base + ["checkout", "--", p], capture_output=True, text=True, encoding='utf-8', cwd=cwd, env=env)
        print(f"  [CRLF 噪声，已还原] {p}")
print("完成")
