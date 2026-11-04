"""python tools/wip/dehint/iw10b.py <gen_iwN.py> [-n TOP]: an expect-75 generator of attempt 9 (gen_iw153, 159, 160) with the stand-in taken out: every
__builtin_expect(X, 0) around the ECC test becomes X, plain -O3.  Does any explicit-reload form flip r187/r192 on its own?  (finalizeImage well below 241.)"""
import importlib.util, itertools, os, re, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import iwlib

gen = sys.argv[1]
top = int(sys.argv[sys.argv.index('-n') + 1]) if '-n' in sys.argv else 25
s = importlib.util.spec_from_file_location('gen', gen)
m = importlib.util.module_from_spec(s)
s.loader.exec_module(m)
base = open(os.path.join(iwlib.R, getattr(m, 'BASE')), newline='').read().replace('\r\n', '\n')


def strip(t):
    return re.sub(r'__builtin_expect\((!pageErased\(.*?\)), 0\)', r'\1', t)


def one(c):
    t = base
    lab = '+'.join(x[0] for x in c if x[0])
    for _, ed in c:
        for a, b in ed:
            if a not in t:
                return lab, {'compile': 'edit'}, 10**9
            t = t.replace(a, b)
    r = iwlib.score_text(strip(t), [])
    return lab, r, r.get('per', {}).get('_finalizeImage', 10**9 if 'compile' in r else 0)


with ThreadPoolExecutor(4) as ex:
    res = list(ex.map(one, itertools.product(*m.AXES)))
res.sort(key=lambda x: x[2])
print(len(res), 'variants')
for lab, r, k in res[:top]:
    print(k, '|', lab, '|', iwlib.fmt(r)[:170])
