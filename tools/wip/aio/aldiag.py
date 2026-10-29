"""For applyIniOptions in <dir>: each label's alignment request (from the
alignments dump) vs what the original needs (alignreq.txt: P/N/F), matched by
position in the instruction stream.  python aldiag.py <dir>"""
import re, sys, difflib
sys.path.insert(0, '.')
import discmp_lib as D

d = sys.argv[1]
# our -dA asm: BLOCK id per instruction, and whether a .p2align precedes the block
lines = open(d + '/o.s').read().split('\n')
s = lines.index('_applyIniOptions:')
blk, al, cur, pend = [], {}, None, False
ours = []
for l in lines[s + 1:]:
    if l.startswith('\t.def'):
        break
    m = re.match(r'\s*# BLOCK (\d+)', l)
    if m:
        cur = int(m.group(1)); al[cur] = False; continue
    if '.p2align 4' in l:
        al[cur] = True; continue
    t = l.strip()
    if not t or t.startswith('#') or t.startswith('.') or re.match(r'^L\d+:', t):
        continue
    ours.append((cur, D.norm_gcc(t).replace('4194304', 'offset l')))
# alignments dump info per BB
info = {}
t = open(d + '/a.c.280r.alignments').read()
t = t[t.index(';; Function applyIniOptions'):]
t = t[:t.index(';; Function', 10)]
fm = re.search(r'freq_max: (\d+)', t).group(1)
for m in re.finditer(r'BB +(\d+) freq +(\d+) loop +\d+ loop_depth +\d+ fall +(\d+) branch +(\d+)[^\n]*\n(  (jump|internal loop) alignment added\.)?', t):
    info[int(m.group(1))] = (int(m.group(2)), int(m.group(3)), int(m.group(4)), m.group(6) or '')
# original instruction stream with label marks
req = {}
for l in open('alignreq.txt'):
    a, k = l.split()[:2]
    req[int(a, 16)] = k
orig = D.orig_stream()   # [(addr, label_addr_or_None, norm)]
on = [x[2] for x in orig]
mn = [x[1] for x in ours]
print('freq_max', fm, len(on), len(mn), sum(1 for x, y in zip(on, mn) if x != y))
seen = set()
for a, b, n in [(0, 0, min(len(on), len(mn)))]:
    for k in range(n):
        oa, olab, _ = orig[a + k]
        bb = ours[b + k][0]
        if olab is None or bb in seen:
            continue
        seen.add(bb)
        need = req.get(olab, '?')
        got = al.get(bb, False)
        bad = (need == 'P' and not got) or (need == 'N' and got)
        if bad or '-v' in sys.argv:
            f, fa, br, why = info.get(bb, (0, 0, 0, ''))
            print('%s %x need %s got %s  BB %d freq %d fall %d branch %d %s' % ('*' if bad else ' ', olab, need, got, bb, f, fa, br, why))
