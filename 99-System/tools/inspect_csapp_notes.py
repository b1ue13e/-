import sys, os, pathlib
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

p = pathlib.Path('F:/-/02-Knowledge/🧠 学习系统/11-计算机组成原理')
if not p.exists():
    p = pathlib.Path('F:/-/02-Knowledge/🧠 学习系统/11-计算机组成原理')

files = list(p.glob('*.md'))
print(f"Total notes in 11-计算机组成原理: {len(files)}")

short_files = []
for f in files:
    try:
        txt = f.read_text(encoding='utf-8', errors='ignore')
        sz = f.stat().st_size
        if sz < 1200 or "TODO" in txt or "占位" in txt or "待补充" in txt:
            short_files.append((f.name, sz))
    except:
        pass

print(f"Found {len(short_files)} short/placeheld notes needing repair:")
for name, sz in short_files[:25]:
    print(f"- {name} ({sz} bytes)")
