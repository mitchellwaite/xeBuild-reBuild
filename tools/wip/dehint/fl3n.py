"""fl3n.py [state]: from the 4-test state (tie 1 only), one natural test anywhere: real arms with returns and calls, not only stores."""
import itertools, sys, threading
from concurrent.futures import ThreadPoolExecutor
import fllib as L, fl3g as G

LAB = sys.argv[1] if len(sys.argv) > 1 else 'len=3,off3=2,off4=1,x=2'
base = G.st(LAB)
if len(sys.argv) > 2:  # any second argument: the nbl test at comma's site
    base['comma'] = ('nbl != 6 && nbl != 9', int(sys.argv[2]))
PL = {
 'v0': ('\tif (off != -1) {\n\t\tmemset(xb.kernelStr', '\t'),
 'v1': ('\t\tlog_printf(1, "ini version %s\\n"', '\t\t'),
 'v2': ('\txb.nFlashFiles = xb.nFiles - 2;', '\t'),
 'v3': ('\tcheckFileCase();', '\t'),
 'f0': ('\tfor (i = 0; i < xb.nFiles; i++) {', '\t'),
 'f1': ('\t\tswitch (e->type) {', '\t\t'),
 'l0': ('\tif (xb.blSuffix[0])\n\t\tsprintf(label', '\t'),
 'l1': ('\toff = memFindStr(buf, size, label, 1);', '\t'),
 'b0': ('\t\tlog_printf(1, "\\nini: label %s found\\n", label);', '\t\t'),
 'b1': ('\t\tpos = off;\n\t\tfor (i = 0; i < nbl; ) {', '\t\t'),
 'b2': ('\t\t\tp = &buf[pos];\n\t\t\tcomma = memFindChar(p, \',\', size - pos);\n\t\t\tnul = memFindChar(p, 0, size - pos);\n\t\t\tlen = comma;', '\t\t\t'),
 'b3': ('\t\t\tlen = comma;\n\t\t\tnoCrc = 0;\n\t\t\tif (comma > nul) {', '\t\t\t'),
 'b4': ('\t\t\tif (len < 0) {\n\t\t\t\tlog_printf(0, "\\n******* ERROR: ini problem, error in', '\t\t\t'),
 'b5': ('\t\t\tpos = pos + len + 1;\n\t\t\tif (!noCrc) {\n\t\t\t\tn = memFindChar(&buf[pos], 0, size - pos);\n\t\t\t\tif (n == 0)\n\t\t\t\t\txb.files[blOrder[i]].crc = 0;', '\t\t\t'),
 'b6': ('\t\t\tlog_printf(1, "found (%d) \'%s\' crc: 0x%08x\\n", i + 1,', '\t\t\t'),
 'b7': ('\t\t\ti++;\n\t\t\tif (pos > end) {', '\t\t\t'),
 'c0': ('\tif (xb.type != BUILD_JTAG && xb.type <= BUILD_DEVGL16) {', '\t'),
 'c1': ('\toff = memFindStr(buf, size, "[rawpatch]", 1);', '\t'),
 'r0': ('\t\tend = off + memFindChar(&buf[off], \'[\', size - off);\n\t\tlog_printf(1, "\\nini: label [rawpatch]', '\t\t'),
 'r1': ('\t\tpos = off;\n\t\tfor (i = xb.nRawPatches; i < 16; i++) {', '\t\t'),
 'r2': ('\t\t\tif (comma == -1 || comma >= nul) {', '\t\t\t'),
 'r3': ('\t\t\tif (comma <= 1023) {', '\t\t\t'),
 'r4': ('\t\t\tif (pos >= end)\n\t\t\t\ti = 16;', '\t\t\t'),
 'r5': ('\t\tif (pos < end) {\n\t\t\tlog_printf(0, "\\n******* ERROR: %d of %d [rawpatch]', '\t\t'),
 's0': ('\toff = memFindStr(buf, size, "[flashfs]", 1);', '\t'),
 's1': ('\t\txb.nFirmware = 0;', '\t\t'),
 't0': ('\toff = memFindStr(buf, size, "[security]", 1);', '\t'),
 't1': ('\t\tpos = off;\n\t\tfor (i = 0; i < 10; i++) {', '\t\t'),
 't2': ('\t\t\tif (len <= 21) {', '\t\t\t'),
 't3': ('\t\t\tif (pos >= end)\n\t\t\t\ti = 10;', '\t\t\t'),
 'z0': ('\tfree(buf);\n\tlog_printf(1, "------ ini parsing completed', '\t'),
}
for k, (t, ind) in PL.items():
    G.mark(k, t, ind)
CONDS = ['off < 0', 'off < -1', 'size < -1', 'pos < -1', 'buf == NULL', 'path == NULL', 'i < 0', 'len < -1', 'nbl <= 0', 'n < -1']
ARMS = ['return 0', 'free(buf); return 0', 'log_printf(0, "x\\n"); free(buf); return 0', 'log_printf(0, "x\\n"); return 0', 'pos = size', 'i = 0', 1, 2, 3]
V = {}
for b, c, a in itertools.product(PL, CONDS, ARMS):
    s = dict(base)
    s[b] = (c, a)
    V['%s:%s:%s' % (b, c, a)] = G.gen(s)
print(len(V))
loc = threading.local()
cnt = [0]
lock = threading.Lock()


def one(kv):
    if not hasattr(loc, 'id'):
        with lock:
            cnt[0] += 1
            loc.id = cnt[0]
    n, s = kv
    o = L.compile(s, None, 'n3_%d' % loc.id)
    if o is None:
        return 10**7, '', n
    return L.score(o)[0], G.vec(o), n


with ThreadPoolExecutor(4) as ex:
    rs = sorted(ex.map(one, V.items()), key=lambda r: r[0])
with open(L.BD + '/a3/n3.txt', 'w', newline='\n') as f:
    for r in rs:
        f.write('%s\t%s\t%s\n' % r)
from collections import Counter
print(Counter((r[0], r[1]) for r in rs if r[0] < 30).most_common(12))
for r in [r for r in rs if r[1].startswith('1')][:15]:
    print(r)
print('MATCH', [r[2] for r in rs if r[0] == 0][:30])
