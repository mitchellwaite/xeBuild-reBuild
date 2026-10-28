"""hill-climb/random search of split-test (sp.c) crafted profiles, scored by fncmp.
python wip/mc/s9/search.py N [seed]   (needs build/mcsp prepared, see sp.sh)"""
import random, subprocess, sys, json, os
from concurrent.futures import ThreadPoolExecutor
ROOT = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
P = {  # name: (edge, lo, hi, start)
 'M': ('mode_client:105>107', 1, 40, 10), 'A': ('mode_client:106>107', 50.2, 60, 50.5),
 'H1': ('mode_client:116>118', 40, 50, 50), 'H2': ('mode_client:119>121', 40, 50, 50),
 'd1': ('mode_client:122>123', 1, 50, 12), 'd2': ('mode_client:129>130', 1, 50, 12),
 'e2': ('clientEraseBlock:2>8', 1, 50, 12), 'e3': ('clientEraseBlock:3>7', 5, 50, 33), 'e4': ('clientEraseBlock:4>6', 5, 50, 40),
 'ip': ('mode_client:49>50', 15, 40, 26.9231), 'r': ('mode_client:50>56', 10, 50, 28.5714),
 'w': ('mode_client:56>64', 10, 50, 50), 'e': ('mode_client:64>72', 10, 50, 50),
}
FIX = ['mode_client:112>133=0']
FAKE = ['clientEraseBlock:%d>1=100' % i for i in (5, 6, 7, 8)]
LOG = os.path.join(ROOT, 'wip', 'mc', 's9', os.environ.get('SLOG', 'search2.log'))
def run(slot, x):
    ov = ['%s=%.4f' % (P[k][0], v) for k, v in x.items()] + FIX + FAKE + ['--consistent', '--entry=clientEraseBlock:mode_client:127']
    env = dict(os.environ, EXTRA='--param builtin-expect-probability=50', MCFDO_DIR=ROOT + r'\build\mcsp')
    r = subprocess.run([sys.executable, ROOT + r'\wip\mc\s9\fdorun9.py', slot, '--over'] + ov, cwd=ROOT, env=env, capture_output=True, text=True)
    f = inv = 999
    for l in r.stdout.splitlines():
        if l.startswith('fncmp'):
            f = int(l.split()[1])
        if l.startswith('round4'):
            inv = int(l.split()[1].split('=')[1])
    return f if f == 0 else f + 4 * inv
def main():
    n = int(sys.argv[1]); random.seed(int(sys.argv[2]) if len(sys.argv) > 2 else 1)
    best = {k: v[3] for k, v in P.items()}
    if os.path.exists(LOG + '.best'):
        best = json.load(open(LOG + '.best'))
    bs = run('s0', best); print('start', bs, flush=True)
    log = open(LOG, 'a')
    with ThreadPoolExecutor(4) as ex:
        for it in range(n):
            cands = []
            for j in range(4):
                x = dict(best)
                for k in random.sample(list(P), random.choice((1, 1, 2, 3))):
                    lo, hi = P[k][1], P[k][2]
                    x[k] = round(min(hi, max(lo, x[k] + random.gauss(0, (hi - lo) / 4))), 2)
                cands.append(x)
            res = list(ex.map(lambda a: run('s%d' % (a[0] + 1), a[1]), enumerate(cands)))
            for x, s in zip(cands, res):
                log.write('%d %s\n' % (s, json.dumps(x)))
                if s <= bs:
                    if s < bs: print(it, s, x, flush=True)
                    bs, best = s, x
                    json.dump(best, open(LOG + '.best', 'w'))
                    if s == 0:
                        print('MATCH', x); return
            log.flush()
    print('best', bs, best)
main()
