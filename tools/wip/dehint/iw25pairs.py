"""python tools/wip/dehint/iw25pairs.py <base.c> <out_prefix> [first] [last] [threads] [cap]: past a hill climb's plateau. Runs every single move of gen_iw<first..last> (same filter as iw20climb.py), groups them by the object they produce, keeps one move per object for those within `cap` lines, then runs all pairs of those moves. Stops at the first IDENTICAL (<out_prefix>_0.c). Logs to <out_prefix>.log: the singles' classes, every pair at or below the base's lines."""
import hashlib, os, re, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import iwlib

src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'iw20climb.py')).read()
exec(compile(src[:src.index("def apply(")].replace("os.path.abspath(__file__)", repr(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'iw20climb.py')))), 'iw20climb', 'exec'))

base, pre = sys.argv[1:3]
first = int(sys.argv[3]) if len(sys.argv) > 3 else 100
last = int(sys.argv[4]) if len(sys.argv) > 4 else 400
th = int(sys.argv[5]) if len(sys.argv) > 5 else 4
cap = int(sys.argv[6]) if len(sys.argv) > 6 else 30
text = open(base, newline='').read().replace('\r\n', '\n')
log = open(pre + '.log', 'a', newline='\n')


def app(t, ed):
    for a, b in ed:
        if a not in t:
            return None
        t = t.replace(a, b)
    return t


def score(t):
    d = tempfile.mkdtemp(dir=iwlib.BUILD, prefix='pa')
    ok, o, d = iwlib.compile_src(t, [], workdir=d)
    try:
        if not ok:
            return None
        h = hashlib.md5(open(o, 'rb').read()).hexdigest()
        idn, tot, per, notes = iwlib.report(o)
        return idn, tot, per, h
    finally:
        iwlib.cleanup(d)


b0 = score(text)
print('base', b0[1], b0[2], flush=True)
ms = moves(first, last)
jobs = [(m, app(text, m[2])) for m in ms]
jobs = [(m, t) for m, t in jobs if t is not None and t != text]
print(len(jobs), 'singles', flush=True)
res = list(ThreadPoolExecutor(th).map(lambda j: score(j[1]), jobs))
cls = {}
for (m, t), r in zip(jobs, res):
    if r is None:
        continue
    if r[0]:
        open(pre + '_0.c', 'w', newline='\n').write(t)
        print('IDENTICAL single', m[0], m[1], flush=True)
        sys.exit(0)
    if r[1] <= cap and r[3] != b0[3] and r[3] not in cls:
        cls[r[3]] = (m, r)
for k, (m, r) in sorted(cls.items(), key=lambda kv: kv[1][1][1]):
    log.write('class %d gen%d %s %s\n' % (r[1], m[0], m[1], r[2]))
log.flush()
reps = [m for m, r in cls.values()]
print(len(reps), 'classes within', cap, flush=True)
pairs = []
for i in range(len(reps)):
    for j in range(i + 1, len(reps)):
        t = app(text, reps[i][2])
        t = app(t, reps[j][2]) if t is not None else None
        if t is not None:
            pairs.append((reps[i], reps[j], t))
print(len(pairs), 'pairs', flush=True)
best = b0[1]


def run(p):
    return p, score(p[2])


with ThreadPoolExecutor(th) as ex:
    for p, r in ex.map(run, pairs):
        if r is None:
            continue
        if r[0]:
            open(pre + '_0.c', 'w', newline='\n').write(p[2])
            print('IDENTICAL pair gen%d %s + gen%d %s' % (p[0][0], p[0][1], p[1][0], p[1][1]), flush=True)
            log.write('ZERO gen%d %s + gen%d %s\n' % (p[0][0], p[0][1], p[1][0], p[1][1]))
            log.close()
            os._exit(0)
        if r[1] <= b0[1]:
            log.write('pair %d gen%d %s + gen%d %s %s\n' % (r[1], p[0][0], p[0][1], p[1][0], p[1][1], r[2]))
            log.flush()
        if r[1] < best:
            best = r[1]
            open(pre + '_%d.c' % best, 'w', newline='\n').write(p[2])
            print('better', best, 'gen%d %s + gen%d %s' % (p[0][0], p[0][1], p[1][0], p[1][1]), r[2], flush=True)
print('done, best', best, flush=True)
