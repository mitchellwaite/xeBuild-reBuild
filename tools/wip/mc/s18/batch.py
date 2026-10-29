"""batch.py N SEED : random X1ORD/X2ORD source variants realized toward des_sane.json, then hanneal on each history."""
import sys, os, random, subprocess, json
S = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip\mc\s18'
ROOT = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
N, seed = int(sys.argv[1]), int(sys.argv[2])
random.seed(seed)
X2ALL = [112, 115, 103, 107, 108, 109, 119, 120, 121, 128, 129, 116, 132, 117, 130]
X1ALL = [112, 115, 121, 107, 108, 109, 116, 119, 120, 128, 129, 132, 117, 130, 103]
for it in range(N):
    name = 'b%d_%d' % (seed, it)
    if os.environ.get('BASEX2'):
        x2 = [int(t) for t in os.environ['BASEX2'].split(',')]
        x1 = [int(t) for t in os.environ['BASEX1'].split(',') if t]
        for _ in range(random.randint(1, 2)):
            r_ = random.random()
            if r_ < 0.5:
                i, j = random.randrange(len(x2)), random.randrange(len(x2)); x2[i], x2[j] = x2[j], x2[i]
            elif r_ < 0.75 and x1:
                i, j = random.randrange(len(x1)), random.randrange(len(x1)); x1[i], x1[j] = x1[j], x1[i]
            else:
                t = random.choice(X1ALL)
                if t in x1: x1.remove(t)
                else: x1.insert(random.randrange(len(x1) + 1), t)
    else:
        x2 = random.sample(X2ALL, len(X2ALL))
        x1 = [t for t in X1ALL if random.random() < 0.5]; random.shuffle(x1)
    if os.environ.get('DROPX2') == '1':
        for t in (117, 130):
            if random.random() < 0.6 and t in x2: x2.remove(t)
    rx = os.environ.get('BRX', '126')
    r = subprocess.run([sys.executable, S + r'\variant.py', name, ','.join(map(str, x2)), ','.join(map(str, x1)), rx,
                        os.environ.get('BASEOV', ROOT + r'\build\mcz8\slotz1\ov.json'), S + r'\des_sane.json'], capture_output=True, text=True,
                       env=dict(os.environ, ITS='6', STOPMISS='2'))
    sd = ROOT + r'\build\mc%s\slotv' % name
    h = subprocess.run([sys.executable, S + r'\hanneal.py', sd, os.environ.get('HEV', '40000'), str(it)], capture_output=True, text=True,
                       env=dict(os.environ, START=S + r'\des_sane.json', RXEV='117:130' if '117' in rx else ''))
    lines = [l for l in h.stdout.splitlines() if l.split(' ')[0].isdigit() or l.startswith('start')]
    last = lines[-1] if lines else 'none'
    miss = [l for l in r.stdout.splitlines() if l.startswith('it ')]
    print(name, 'x2', ','.join(map(str, x2)), 'x1', ','.join(map(str, x1)), '|', miss[-1] if miss else r.stderr[-200:], '|', last[:20], flush=True)
    open(S + r'\batch_%s.json' % name, 'w').write(last)
