"""Sweep expect-hint subsets x builtin-expect-probability for getImageKv in
wip/image_read.c, checked with fncmp then wip/jcmp.py (jump targets;
0.5 = fncmp MATCH but a jump goes to the wrong identical block).
MAXK=max hints, P0/P1/PS probabilities.  python wip/kvsweep.py"""
import itertools, os, re, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\wip')
from irlit import externize

ROOT = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
S = os.path.join(ROOT, 'build', 'image_read')   # scratch variants go to build/image_read/sw
src = open(os.path.join(ROOT, 'wip', 'image_read.c')).read()
FN = 'getImageKv'
CONDS = ['size == 0x8000', 'xb.kv.data != 0', 'xb.kvAlt.data != 0',
         'verifyExtended(xb.kv.data, xb.kv.size)', 'verifyExtended(xb.kvAlt.data, xb.kvAlt.size)',
         'addr + size < 528 * xb.numPages', 'size != 0x4000 && size != 0x8000', '!addr']
PLAIN = ['size == 0x8000', 'xb.kv.data', 'xb.kvAlt.data',
         'verifyExtended(xb.kv.data, xb.kv.size)', 'verifyExtended(xb.kvAlt.data, xb.kvAlt.size)',
         'addr + size < 528 * xb.numPages', 'size != 0x4000 && size != 0x8000', '!addr']
f0 = re.search(r'\nvoid getImageKv\(void\)\n\{.*?\n\}\n', src, re.S).group(0)
f = re.sub(r'__builtin_expect\((.*?), [01]\)\) \{', r'\1) {', f0)
f = f.replace('xb.kv.data != 0) {', 'xb.kv.data) {').replace('xb.kvAlt.data != 0) {', 'xb.kvAlt.data) {')
for p in PLAIN:
    assert ('if (%s) {' % p) in f, p
OPT = [(i, d) for i in range(len(CONDS)) for d in (0, 1)]
PROBS = range(int(os.environ.get('P0', 60)), int(os.environ.get('P1', 81)), int(os.environ.get('PS', 2)))
MAXK = int(os.environ.get('MAXK', 3))


def variant(subset):
    g = f
    for i, d in subset:
        g = g.replace('if (%s) {' % PLAIN[i], 'if (__builtin_expect(%s, %d)) {' % (CONDS[i], d), 1)
    return src.replace(f0, g)


def run(job):
    i, subset, p = job
    path = os.path.join(S, 'sw', 'k%d.c' % i)
    open(path, 'w', newline='\n').write(externize(variant(subset)))
    fl = ['-O3', '--param', 'builtin-expect-probability=%d' % p]
    r = subprocess.run([sys.executable, os.path.join(ROOT, 're', 'fncmp.py'), path, FN] + fl,
                       capture_output=True, text=True, cwd=ROOT)
    o = r.stdout + r.stderr
    n = 0 if o.strip() == 'MATCH' else sum(1 for l in o.splitlines() if re.match(r'^[-+](?![-+])', l))
    if n == 0:
        r = subprocess.run([sys.executable, os.path.join(ROOT, 'wip', 'jcmp.py'), path, FN] + fl,
                           capture_output=True, text=True, cwd=ROOT)
        if 'JMATCH' not in r.stdout + r.stderr:
            n = 0.5
    return n, subset, p


os.makedirs(os.path.join(S, 'sw'), exist_ok=True)
jobs = []
for k in range(1, MAXK + 1):
    for subset in itertools.combinations(OPT, k):
        if len({i for i, _ in subset}) < k:
            continue
        for p in PROBS:
            jobs.append((len(jobs), subset, p))
print(len(jobs), 'jobs', flush=True)
with ThreadPoolExecutor(8) as ex:
    res = list(ex.map(run, jobs))
res.sort(key=lambda r: r[0])
for n, subset, p in res[:30]:
    print(n, ['%s:%d' % (CONDS[i], d) for i, d in subset], p)
