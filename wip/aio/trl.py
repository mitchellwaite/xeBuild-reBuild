"""Traces of our build with role labels.  python trl.py <dir>  (after dumps.sh)"""
import difflib, re, sys
sys.path.insert(0, '.')
import lab
d = sys.argv[1]
labs, ids = lab.our_blocks(d + '/o.s')
ours = open(d + '/o.s').read().split('\n')
t = open(d + '/aio.bbro').read()
fo = t[t.index('Final order:'):].split('\n')[1].split()
pre = open(d + '/a.c.272r.cprop_hardreg').read()
pre = pre[pre.index(';; Function applyIniOptions'):]
pre = pre[:pre.index(';; Function', 10)]
idc = {m.group(1): (int(m.group(2)) or int(m.group(3))) for m in re.finditer(r'^;; basic block (\d+), loop depth \d+, count (\d+), freq (\d+)', pre, re.M)}
bcnt = [idc.get(b, -1) for b in fo]
dcnt = []
for l in ours[ours.index('_applyIniOptions:') + 1:]:
    if l.startswith('\t.def'):
        break
    m = re.match(r'\s*# BLOCK (\d+) freq:(\d+)(?: count:(\d+))?', l)
    if m:
        dcnt.append(int(m.group(3) or m.group(2)))
L = {}
sm = difflib.SequenceMatcher(None, bcnt, dcnt, autojunk=False)
for a, b, size in sm.get_matching_blocks():
    for k in range(size):
        L[fo[a + k]] = labs[b + k]
for m in re.finditer(r'^Trace (\d+) \(round (\d+)\):\s+(.*)$', t, re.M):
    bbs = re.findall(r'(\d+) \[(\d+)\]', m.group(3))
    print('T%-3s r%s  %s' % (m.group(1), m.group(2), '  '.join('%s[%s]%s' % (b, f, L.get(b, '?').split('/')[0]) for b, f in bbs)))
