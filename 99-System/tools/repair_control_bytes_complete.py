import os
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')
root_dir = r'f:\-\02-Knowledge\🧠 学习系统'

replacements = [
    (b"\x07", b"\\g"),
    (b"\x08", b"\\b"),
    (b"\x0c", b"\\f"),
    (b"\x0b", b"\\v"),
    (b"\x01", b"\\a"),
    (b"\x02", b"\\b"),
    (b"\x03", b"\\c"),
    (b"\x04", b"\\d"),
    (b"\x05", b"\\e"),
    (b"\x06", b"\\f"),
    (b"\x0e", b"\\n"),
    (b"\x0f", b"\\o"),
    (b"\x10", b"\\p"),
    (b"\x11", b"\\q"),
    (b"\x12", b"\\r"),
    (b"\x13", b"\\s"),
    (b"\x14", b"\\t"),
    (b"\x15", b"\\u"),
    (b"\x16", b"\\v"),
    (b"\x17", b"\\w"),
    (b"\x18", b"\\x"),
    (b"\x19", b"\\y"),
    (b"\x1a", b"\\z"),
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
            
            for damaged, correct in replacements:
                if damaged in new_data:
                    count = new_data.count(damaged)
                    new_data = new_data.replace(damaged, correct)
                    total_replacements += count
                    file_changed = True
                    
            if file_changed:
                with open(p, 'wb') as fp:
                    fp.write(new_data)
                modified_files += 1

print(f"✅ Complete control byte escape repair finished.")
print(f"Modified Files: {modified_files}")
print(f"Total Replacements: {total_replacements}")
