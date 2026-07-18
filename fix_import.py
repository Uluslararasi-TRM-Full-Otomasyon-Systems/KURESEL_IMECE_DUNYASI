content = open('ADVANCED_DASHBOARD.py', 'r', encoding='utf-8').read()
lines = content.split('\n')
import_idx = None
for i, line in enumerate(lines):
    if 'import sys' in line and not line.strip().startswith('#'):
        import_idx = i
        break

if import_idx is not None:
    lines.insert(import_idx + 1, 'import threading')
    with open('ADVANCED_DASHBOARD.py', 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print('threading import added after sys')
else:
    print('sys import not found')
