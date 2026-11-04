"""python tools/wip/dehint/iw11probe.py <base.c> [fn]: expect + param grid (mechanism probe only, never a candidate): on which branch and at what probability does
<fn> (default _finalizeImage) come out right from a base with the load order right?  Sites: D data test, S spare test (either helper or plain), E the ECC test.  Prints the best lines."""
import itertools, os, re, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import iwlib

base = open(sys.argv[1], newline='').read().replace('\r\n', '\n')
fn = sys.argv[2] if len(sys.argv) > 2 else '_finalizeImage'
PE = re.search(r'int pageErased\(const uint8_t \*data, const uint8_t \*spare\)\n\{.*?\n\}\n', base, re.S).group(0)


def site(t, s):
    if s == 'D':
        new = PE.replace('if (data[i] != 0xff)', 'if (__builtin_expect(data[i] != 0xff, 1))')
        assert new != PE
        return t.replace(PE, new)
    if s == 'S':
        new = PE.replace('if (spare[i] != 0xff)', 'if (__builtin_expect(spare[i] != 0xff, 1))').replace('if (byteUsed(spare[i]))', 'if (__builtin_expect(byteUsed(spare[i]), 1))')
        assert new != PE
        return t.replace(PE, new)
    if s == 'E':
        a = 'if (!pageErased(xb.hdr + (b * 32 + p) * 512,'
        assert a in t
        # the test may have either pointer spelling for spare: close the expect at the end of the line
        i = t.index(a)
        j = t.index('\n', i)
        line = t[i:j]
        body = line[len('if ('):line.rindex(')')]
        rest = line[line.rindex(')') + 1:]
        return t[:i] + 'if (__builtin_expect(' + body + ', 0))' + rest + t[j:]


jobs = [(s, p) for s in 'DSE' for p in list(range(3, 40, 2)) + list(range(40, 96, 5))]


def one(j):
    s, p = j
    r = iwlib.score_text(site(base, s), ['--param', 'builtin-expect-probability=%d' % p])
    if 'compile' in r:
        return s, p, 99999, r['compile'][:100]
    return s, p, r['per'].get(fn, 0) if not r.get('identical') else 0, r['per']


with ThreadPoolExecutor(4) as ex:
    res = list(ex.map(one, jobs))
for s in 'DSE':
    print(s, ' '.join('%d:%s' % (p, k) for ss, p, k, _ in res if ss == s))
res.sort(key=lambda x: x[2])
for x in res[:5]:
    print(x[0], x[1], x[2], str(x[3])[:150])
