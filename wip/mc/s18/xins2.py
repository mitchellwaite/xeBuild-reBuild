"""xins2.py EVALS SEED N name... : random XINS1 (X1-time) / XINS (X2-time) arm injections + hanneal"""
import sys, random, subprocess, os
EV, SEED, N = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
random.seed(SEED)
ARMS = [131, 118, 114]
for v in sys.argv[4:]:
    for i in range(N):
        a = ARMS[:]; random.shuffle(a)
        x1, x2 = [], []
        for t in a:
            r = random.random()
            if r < 0.33: x1.append(t)
            elif r < 0.75: x2.append(t)
        env = dict(os.environ, XINS=','.join(map(str, x2)), XINS1=','.join(map(str, x1)), RXEV='117:130', START='des_sane.json')
        out = subprocess.run([sys.executable, 'hanneal.py', '../../../build/mc%s/slotv' % v, EV, str(i)], capture_output=True, text=True, env=env).stdout
        lines = [l for l in out.splitlines() if l.split(' ')[0].isdigit()]
        last = lines[-1] if lines else 'none'
        tag = '%s_x1_%s_x2_%s' % (v, '-'.join(map(str, x1)), '-'.join(map(str, x2)))
        open('xj_%s.out' % tag, 'w').write(last + '\n')
        print(tag, last[:16], flush=True)
