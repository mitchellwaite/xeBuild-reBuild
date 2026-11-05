"""opbb.py TAG bb [bb..]: what applyIniOptions' bbro-time block bb holds (symbol refs, with the
.rdata strings resolved from TAG's o.s; frequency), from the first RTL listing in aio.bbro."""
import os, re, sys
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'build', 'v', 'aio_p1')
tag = sys.argv[1]
t = open(os.path.join(R, tag, 'aio.bbro')).read()
s = open(os.path.join(R, tag, 'o.s')).read()
lc = dict(re.findall(r'^(LC\d+):\n\t\.ascii "(.*)"', s, re.M))
starts = [(m.start(), int(m.group(1))) for m in re.finditer(r'\[bb (\d+)\] NOTE_INSN_BASIC_BLOCK', t)]
first = {}
for k, (p, b) in enumerate(starts):
    if b in first:
        continue
    e = starts[k + 1][0] if k + 1 < len(starts) else len(t)
    first[b] = t[p:e]
for b in map(int, sys.argv[2:]):
    blk = first.get(b, '')
    syms = re.findall(r'symbol_ref[^"]*"([^"]+)"', blk)
    print(b, ' '.join(lc.get(x.lstrip("*"), x)[:40] for x in syms) or '(no refs)', '| insns', blk.count('(insn ') + blk.count('(call_insn') + blk.count('(jump_insn'))
