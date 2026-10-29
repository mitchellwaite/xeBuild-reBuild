"""Compare two objdump -d listings (instructions incl. padding), print differences."""
import re, difflib, sys


def ins(path):
    out = []
    for l in open(path):
        m = re.match(r'\s*([0-9a-f]+):\s+(.*)$', l)
        if not m:
            continue
        t = m.group(2).strip()
        t = re.sub(r'<[^>]*>', '', t)
        t = re.sub(r'^(j\w+|call)\s+.*$', r'\1 X', t)
        t = re.sub(r'0x[0-9a-f]+', 'X', t)
        t = re.sub(r'\s+', ' ', t).strip()
        out.append((int(m.group(1), 16), t))
    return out


o = ins(sys.argv[1])
m = ins(sys.argv[2])
print(len(o), len(m), 'bytes', hex(o[-1][0] - o[0][0]), hex(m[-1][0] - m[0][0]))
on = [t for a, t in o]
mn = [t for a, t in m]
sm = difflib.SequenceMatcher(None, on, mn, autojunk=False)
for tag, a, b, c, d in sm.get_opcodes():
    if tag != 'equal':
        print(tag, hex(o[a][0]) if a < len(o) else '-', hex(m[c][0]) if c < len(m) else '-', on[a:b][:5], mn[c:d][:5])
