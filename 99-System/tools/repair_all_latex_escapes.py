import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
root_dir = r'f:\-\02-Knowledge\🧠 学习系统'

REPLACEMENTS = [
    (b"\text", b"\\text"),
    (b"\times", b"\\times"),
    (b"\theta", b"\\theta"),
    (b"\tau", b"\\tau"),
    (b"\to", b"\\to"),
    (b"\right", b"\\right"),
    (b"\left", b"\\left"),
    (b"\mathbb", b"\\mathbb"),
    (b"\mathcal", b"\\mathcal"),
    (b"\max", b"\\max"),
    (b"\min", b"\\min"),
    (b"\sum", b"\\sum"),
    (b"\prod", b"\\prod"),
    (b"\lim", b"\\lim"),
    (b"\inf", b"\\inf"),
    (b"\sup", b"\\sup"),
    (b"\frac", b"\\frac"),
    (b"\sqrt", b"\\sqrt"),
    (b"\hat", b"\\hat"),
    (b"\tilde", b"\\tilde"),
    (b"\bar", b"\\bar"),
    (b"\vec", b"\\vec"),
    (b"\dot", b"\\dot"),
    (b"\ddot", b"\\ddot"),
]

modified_files = 0
total_replacements = 0

for dirpath, dirnames, filenames in os.walk(root_dir):
    dirnames[:] = [d for d in dirnames if not d.startswith('.')]
    for f in filenames:
        if f.endswith('.md'):
            p = os.path.join(dirpath, f)
            try:
                with open(p, 'rb') as fp:
                    data = fp.read()
            except Exception:
                continue
                
            new_data = data
            file_changed = False
            
            for damaged, correct in REPLACEMENTS:
                if damaged in new_data:
                    count = new_data.count(damaged)
                    new_data = new_data.replace(damaged, correct)
                    total_replacements += count
                    file_changed = True
                    
            if file_changed:
                with open(p, 'wb') as fp:
                    fp.write(new_data)
                modified_files += 1

print(f"✅ LaTeX control character repair completed.")
print(f"Modified Files: {modified_files}")
print(f"Total Replacements: {total_replacements}")
