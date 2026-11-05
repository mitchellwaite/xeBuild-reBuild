"""Measurement only, loadDump calling the real copyMmcImage: __builtin_expect on the zeropair test, on xb.dumpMmc and on !ret (none/1/0) at several probabilities.  Which frequencies does loadDump need?"""
import itertools, os, sys
from concurrent.futures import ThreadPoolExecutor
os.environ['IRLOOSE'] = '1'
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import irlib

text = open(os.path.join(irlib.R, 'build', 'ir', 'a5', 'nat.c'), newline='').read().replace('\r\n', '\n')
T1 = '	if (notZeropair())\n		return 1;\n'
T2 = '		if (xb.dumpMmc)\n			ret = copyMmcImage(raw);\n'
T3 = '		if (!ret)\n			buildCleanup();\n'
for t in (T1, T2, T3):
    assert t in text, t


def X(c, k):
    return c if k == 'n' else '__builtin_expect(%s, %s)' % (c, k)


def run(a):
    p, (k1, k2, k3) = a
    t = text.replace(T1, '	if (%s)\n		return 1;\n' % X('notZeropair()', k1))
    t = t.replace(T2, '		if (%s)\n			ret = copyMmcImage(raw);\n' % X('xb.dumpMmc', k2))
    t = t.replace(T3, '		if (%s)\n			buildCleanup();\n' % X('!ret', k3))
    r = irlib.score_text(t, ['--param', 'builtin-expect-probability=%d' % p])
    per = r.get('per', {})
    return per.get('_loadDump', 0), per.get('_copyMmcImage', 0), p, k1 + k2 + k3


args = [(p, k) for p in (51, 53, 55, 58, 60, 62, 65, 68, 70, 75, 80, 90) for k in itertools.product('n01', repeat=3)]
with ThreadPoolExecutor(4) as ex:
    res = sorted(ex.map(run, args))
for x in res[:24]:
    print(x)
