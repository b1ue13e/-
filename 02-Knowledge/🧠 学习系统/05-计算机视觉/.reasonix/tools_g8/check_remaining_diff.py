import subprocess, os, sys
sys.stdout.reconfigure(encoding='utf-8')
env = dict(os.environ, GIT_OPTIONAL_LOCKS='0')
base = ["git", "-c", "core.fsmonitor=false"]
r = subprocess.run(base + ["diff", "-w", "--name-only", "--",
    "02-Knowledge/🧠 学习系统/05-计算机视觉"],
    capture_output=True, text=True, encoding='utf-8', cwd="F:/" + os.sep + "-", env=env)
files = [l for l in r.stdout.split('\n') if l.strip() and 'desktop-topic' not in l and '.reasonix' not in l]
print("内容有差异的文件:", len(files))
for f in files:
    r2 = subprocess.run(base + ["diff", "-w", "--", f],
        capture_output=True, text=True, encoding='utf-8', cwd="F:/" + os.sep + "-", env=env)
    diffs = [l for l in r2.stdout.split('\n') if l.startswith(('+', '-')) and not l.startswith(('+++', '---'))]
    print(f"  {f}: {len(diffs)} 行")
    for d in diffs[:3]:
        print(f"    {d[:100]}")
