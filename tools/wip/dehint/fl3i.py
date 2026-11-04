"""fl3i.py <N> <seed>: from the lean 7-test state, drop tests, re-roll small arms and move x.  Natural spellings
(off < 0, len < 0, i < 0) where they're known to behave the same.  Logs build/filelist_ini/a3/i3.txt."""
import random, sys, threading
from concurrent.futures import ThreadPoolExecutor
import fllib as L, fl3g as G

N, seed = int(sys.argv[1]), int(sys.argv[2])
rng = random.Random(seed)
# extra sites for the moved test y
PL = {
 'y0': ('\t\t\tp = &buf[pos];\n\t\t\tnul = memFindChar(p, 0, size - pos);\n@@nul', '\t\t\t'),
 'y1': ('\t\t\tnoCrc = 1;\n\t\t\tlen = nul;', '\t\t\t'),
 'y2': ('\t\t\tif (len <= 1023) {', '\t\t\t'),
 'y3': ('\t\t\t\tpos = pos + len + 1;\n\t\t\t\tif (xb.firmware[i][len - 1]', '\t\t\t\t'),
 'y4': ('\t\t\t\tif (!noCrc) {\n\t\t\t\t\tn = memFindChar(&buf[pos], 0, size - pos);\n\t\t\t\t\tif (n == 0)\n\t\t\t\t\t\tcrc', '\t\t\t\t'),
 'y5': ('\t\t\t\tlog_printf(1, "found (%d) \'%s\' crc: 0x%08x\\n", ++xb.nFirmware', '\t\t\t\t'),
 'y6': ('\toff = memFindStr(buf, size, "[security]", 1);', '\t'),
 'y7': ('\t\tfor (i = 0; i < 10; i++) {', '\t\t'),
 'y8': ('\t\tfor (i = 0; i < 256; i++) {', '\t\t'),
 'y9': ('\t\tfor (i = xb.nRawPatches; i < 16; i++) {', '\t\t'),
 'y10': ('\tfree(buf);\n\tlog_printf(1, "------ ini parsing completed', '\t'),
}
for k, (t, ind) in PL.items():
    G.mark(k, t, ind)
START = dict(comma=1, i=1, len=1, nul=1, off3=2, off4=1, x=2)
SP = {'comma': ['comma < -1'], 'i': ['i < 0', 'i < -1'], 'nul': ['nul < -1', 'i < 0'], 'off3': ['off < -1'], 'off4': ['off < -1'], 'len': ['len < 0', 'len < -1'], 'x': ['off < 0', 'off < -1'], 'off5': ['off < -1']}
ALLY = list(PL)
V = {}
while len(V) < N:
    keep = dict(START)
    for n in rng.sample(list(START), rng.choice([1, 1, 2, 2, 3])):
        del keep[n]
    for n in list(keep):
        if rng.random() < 0.4:
            keep[n] = rng.randint(1, 5)
    state = {n: (SP[n][0], k) for n, k in keep.items()}
    lab = ','.join('%s=%d' % kv for kv in sorted(keep.items()))
    if rng.random() < 0.6:
        y = rng.choice(ALLY)
        c = rng.choice(['off < 0', 'i < 0', 'size < -1']) if y not in ('y6', 'y10', 'y8', 'y9', 'y7') else rng.choice(['off < -1', 'size < -1', 'pos < -1'])
        k = rng.randint(1, 5)
        state[y] = (c, k)
        lab += '+%s:%s:%d' % (y, c, k)
    V[lab] = G.gen(state)

loc = threading.local()
cnt = [0]
lock = threading.Lock()


def one(kv):
    if not hasattr(loc, 'id'):
        with lock:
            cnt[0] += 1
            loc.id = cnt[0]
    n, s = kv
    o = L.compile(s, None, 'i%d_%d' % (seed, loc.id))
    if o is None:
        return 10**7, '', n
    return L.score(o)[0], G.vec(o), n


with ThreadPoolExecutor(3) as ex:
    rs = sorted(ex.map(one, V.items()), key=lambda r: (r[0], r[2].count('=')))
with open(L.BD + '/a3/i3.txt', 'a', newline='\n') as f:
    for r in rs:
        f.write('%s\t%s\t%s\n' % r)
for r in rs[:12]:
    print(r)
print('MATCH', [r[2] for r in rs if r[0] == 0][:20])
