# climb.py TAG ROUNDS BASE_EDITS... : greedy climb over candidate edits (cands list built below)
import sys, subprocess, shlex, concurrent.futures as cf
tag, rounds = sys.argv[1], int(sys.argv[2]); base = sys.argv[3:]
J = ["c10","c11","dsp","fail","hdd4,hdd5","hdd4,s5,hdd5","i1","p0","p1,cdef","s4,c12","s5"]
L = "c1 c2 c3 c7 c8 c9 c10 c11 c12 cdef i0 i1 p0 p1 t4 t5 hdd4 hdd5".split()
def cands(cur):
    cs = []
    txt = open('b18.c').read()
    for j in J:
        for l in L:
            if l in j.split(','): continue
            cs.append('R=JMP(%s)|JMP(%s,%s)' % (j, j, l))
    for e in ["Hk", "K=kky,2,85", "K=kky,1,85", "S=kky,2,85", "W=kky,2,85", "E=kipt,1,86", "E=kipt,2,86", "E=kky,1,87", "E=krb,1,88", "E=ks2,1,89", "B=kky,2,85", "T=kky,4,85"]:
        cs.append(e)
    return [c for c in cs if c not in cur]
def run(name, edits):
    subprocess.run(['sh', 'run0.sh', name] + edits, capture_output=True)
    for l in reversed(open('res.txt').read().splitlines()):
        if l.startswith(name + ' '):
            try: return int(l.split()[1][3:])
            except: return 9999
    return 9999
cur = list(base); best = run('%s_0' % tag, cur); print('start', best, flush=True)
for r in range(1, rounds + 1):
    cs = cands(cur)
    with cf.ThreadPoolExecutor(4) as ex:
        res = list(ex.map(lambda ic: (run('%s_%d_%d' % (tag, r, ic[0]), cur + [ic[1]]), ic[1]), enumerate(cs)))
    res.sort(key=lambda x: x[0])
    print('round', r, res[:5], flush=True)
    if res[0][0] >= best: break
    best = res[0][0]; cur.append(res[0][1])
    print('cur', best, cur, flush=True)
