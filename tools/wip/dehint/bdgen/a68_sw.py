"""Attempt 68: the setKitBuild route (void setKitBuild(uint32_t i, int type), IPA-inlined, tail test
(int)r < 0, no param) crossed with natural perturbations of loadBlFiles that change which edges reach
the switch join and in what order: every single move of one case block of the switch.
python tools/wip/dehint/bdgen/a68_fsm.py tools/wip/dehint/bdgen/a68_sw.py -s"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdlib
from a68_kit import V as KV

BASES = {'riv': KV['riv']}


def cases(t):
    i = t.index('int loadBlFiles(void)')
    s = t.index('\t\t\tswitch (type) {\n', i) + len('\t\t\tswitch (type) {\n')
    e = t.index('\n\t\t\t}\n', s) + 1
    body = t[s:e]
    starts = [m.start() for m in re.finditer(r'^\t\t\t(case |default:)', body, re.M)]
    blocks = [body[a:b] for a, b in zip(starts, starts[1:] + [len(body)])]
    out = []
    for b in blocks:
        if out and re.fullmatch(r'(\t\t\tcase [^\n]*\n)+', out[-1]):
            out[-1] += b
        else:
            out.append(b)
    return s, e, out


def mover(k, j, base):
    def f(t):
        from a60lib import apply
        t = apply(t, base)
        s, e, bl = cases(t)
        b = bl.pop(k)
        bl.insert(j, b)
        return t[:s] + ''.join(bl) + t[e:]
    return f


V = {}
from a60lib import apply
_t = apply(bdlib.read_src(), KV['riv'])
_, _, _bl = cases(_t)
NB = len(_bl)
for k in range(NB):
    for j in range(NB):
        if j == k:
            continue
        V['m%d_%d' % (k, j)] = mover(k, j, KV['riv'])
