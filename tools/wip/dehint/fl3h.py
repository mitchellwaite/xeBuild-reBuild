"""fl3h.py [state label]: one extra natural test at places in the bl section, from a near state (tie 1 wrong).
Scores with the tie vector.  Looks for what can stand in for `comma < -1`, the uninitialised read."""
import itertools, os, sys
from concurrent.futures import ThreadPoolExecutor
import fllib as L, fl3g as G

LAB = sys.argv[1] if len(sys.argv) > 1 else 'len=3,off3=5,off4=1,off5=4'
G.mark('b0', '\t\tpos = off;\n\t\tfor (i = 0; i < nbl; ) {', '\t\t')
G.mark('b1', '\t\t\tp = &buf[pos];\n\t\t\tcomma = memFindChar(p, \',\', size - pos);\n\t\t\tnul = memFindChar(p, 0, size - pos);\n\t\t\tlen = comma;', '\t\t\t')
G.mark('b2', '\t\t\tlen = comma;\n\t\t\tnoCrc = 0;\n\t\t\tif (comma > nul) {', '\t\t\t')
G.mark('b3', '\t\t\tif (len < 0) {\n\t\t\t\tlog_printf(0, "\\n******* ERROR: ini problem, error in', '\t\t\t')
G.mark('b4', '\t\t\tstrncpy(xb.files[blOrder[i]].name, (char *)p, len);', '\t\t\t')
G.mark('b5', '\t\t\tpos = pos + len + 1;\n\t\t\tif (!noCrc) {\n\t\t\t\tn = memFindChar(&buf[pos], 0, size - pos);\n\t\t\t\tif (n == 0)\n\t\t\t\t\txb.files[blOrder[i]].crc = 0;', '\t\t\t')
G.mark('b6', '\t\t\tlog_printf(1, "found (%d) \'%s\' crc: 0x%08x\\n", i + 1,', '\t\t\t')
G.mark('b7', '\tif (xb.type != BUILD_JTAG && xb.type <= BUILD_DEVGL16) {', '\t')
G.mark('b8', '\t\tend = off + memFindChar(&buf[off], \'[\', size - off);\n\t\t/* this', '\t\t') if False else None
BS = ['b0', 'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7']
CONDS = ['blOrder == NULL', 'off < 0', 'p == NULL', 'buf == NULL', 'nbl <= 0', 'i < 0', 'pos < off', 'pos < 0', 'end < -1', 'size < 0', 'len < -1', 'nul < -1', 'comma < -1', 'i >= nbl', 'i < -1']
ARMS = [1, 2, 'return 0', 'free(buf); return 0', 'log_printf(0, "x"); free(buf); return 0', 'pos = size', 'i = nbl', 'len = 0', 'pos = 0']
base = G.st(LAB)
V = {}
for b, c, a in itertools.product(BS, CONDS, ARMS):
    s = dict(base)
    s[b] = (c, a)
    V['%s:%s:%s' % (b, c, a)] = G.gen(s)
print(len(V))


def one(kv):
    i, (n, s) = kv
    o = L.compile(s, None, 'h3_%d' % (i % 16 + 16 * (hash(n) % 4)))
    if o is None:
        return 10**7, '', n
    sc = L.score(o)
    return sc[0], G.vec(o), n


# tag per worker slot: one compile at a time per tag
import threading
loc = threading.local()
cnt = [0]
def one2(kv):
    if not hasattr(loc, 'id'):
        cnt[0] += 1
        loc.id = cnt[0]
    n, s = kv
    o = L.compile(s, None, 'h3_%d' % loc.id)
    if o is None:
        return 10**7, '', n
    sc = L.score(o)
    return sc[0], G.vec(o), n


with ThreadPoolExecutor(4) as ex:
    rs = sorted(ex.map(one2, V.items()), key=lambda r: r[0])
with open(L.BD + '/a3/h3.txt', 'w', newline='\n') as f:
    for r in rs:
        f.write('%s\t%s\t%s\n' % r)
for r in rs[:40]:
    print(r)
