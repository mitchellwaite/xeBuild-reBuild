"""Per label of the original applyIniOptions: P (padding before it: alignment
requested), N (no padding and not 16-aligned: must not be requested), or F
(16-aligned: either).  With role labels of the block that follows."""
import os, json, re, sys
sys.path.insert(0, '.')
import lab
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
d = json.load(open(ROOT + '/build/xeBuild.lines.json'))
lines = open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'src', 'app', 'options.s')).read().split('\n')
st = lab.strings(lines, r'^(\w+):\s*$', r'\s*\.string "(.*)"')
# label -> address from the line/addr table
ref = [(l, a) for l, a in zip(d['lines'], d['addr']) if a is not None and 0x4259a0 <= a < 0x427000]
s = lines.index('_applyIniOptions:')
out, cur, curlab, pad = [], [], None, False
for l in lines[s + 1:]:
    if l.startswith('#@C') or l.startswith('.section') or re.match(r'^_\w+:', l):
        break
    m = re.match(r'^(L_([0-9a-f]+)):', l.strip())
    if m:
        if curlab:
            out.append((curlab, pad, cur))
        curlab, cur, pad = int(m.group(2), 16), [], padnext if 'padnext' in dir() else False
        padnext = False
        continue
    if re.search(r'\.byte|\bnop\b|mov ESI,ESI|lea ESI|lea EDI', l):
        padnext = True
        continue
    t = l.split('#')[0].strip()
    if t and not t.startswith('.'):
        cur.append(t)
if curlab:
    out.append((curlab, pad, cur))
for a, p, b in out:
    k = 'P' if p else ('F' if a % 16 == 0 or 16 - a % 16 > 10 else 'N')
    print('%x %s %s' % (a, k, lab.label(b[:12], st)))
