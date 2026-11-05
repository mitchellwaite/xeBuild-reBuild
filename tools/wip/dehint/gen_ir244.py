"""Attempt 19, measurement: the attribute's last job is IF-CASE-1 at S_bad (then = E's edge copy `edi = 0x1000`, one insn): P(then) x cost needs P(then) under about 21, so r = P(bad) at S_bad >= 79, while
S_ok's P = (r - x) / (1 - x) stays where layout wants it; x = P(zero or bad address) at S.  Joint scan with one expect probability on bad and on each address test."""
import os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import irlib

t = open(os.path.join(irlib.BUILD, 'a19', 'a0.c'), newline='').read().replace('\r\n', '\n')
E = lambda c: '__builtin_expect(!!(%s), 1)' % c
REP = {
    'bad': ('if (bad > 0) {', 'if (' + E('bad > 0') + ') {'),
    'wrong': ('if (wrong > 0)', 'if (' + E('wrong > 0') + ')'),
    'tt': ('if (t != 0x1000) {', 'if (' + E('t != 0x1000') + ') {'),
    'ok': ('if (ok <= 0) {', 'if (' + E('ok <= 0') + ') {'),
}
SETS = [('bad', 'wrong'), ('bad', 'tt'), ('bad', 'wrong', 'tt'), ('bad', 'ok')]
jobs = []
for s in SETS:
    x = t
    for k in s:
        a, b = REP[k]
        assert a in x
        x = x.replace(a, b, 1)
    for p in range(70, 100, 2):
        jobs.append(('+'.join(s), p, x))


def one(j):
    lab, p, x = j
    ok, o, d = irlib.compile_src(x, ['--param', 'builtin-expect-probability=%d' % p])
    idn, tot, per, notes = irlib.report(o)
    irlib.cleanup(d)
    return lab, p, 'ID' if idn else per.get('_getImageSmc', 0)


res = {}
with ThreadPoolExecutor(os.cpu_count()) as ex:
    for lab, p, r in ex.map(one, jobs):
        res.setdefault(lab, []).append('%d:%s' % (p, r))
for k, v in res.items():
    print(k, ' '.join(v))
