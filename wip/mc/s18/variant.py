"""variant.py NAME X2ORD X1ORD RXFLAGS(126,117 or '') START_OV.json DESIGN.json
genq -> prep build/mc<NAME> -> runq (8 its, from START_OV with X1 edges swapped) -> report."""
import sys, os, json, subprocess
ROOT = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
name, x2, x1, rx, ov0, des = sys.argv[1:7]
ov0, des = os.path.abspath(ov0), os.path.abspath(des)
S = ROOT + r'\wip\mc\s18'
rxa = [{'126': '126:125', '117': '117:130'}[r] for r in rx.split(',') if r]
src = os.path.join(S, 'v_%s.c' % name)
subprocess.run([sys.executable, S + r'\genq.py', src, x2, x1] + rxa, check=True)
env = dict(os.environ, EXTRA='--param builtin-expect-probability=50')
d = ROOT + r'\build\mc' + name
subprocess.run([sys.executable, '-c', "import sys;sys.path.insert(0,r'%s\wip');import mcfdo;mcfdo.prep(r'%s',r'%s')" % (ROOT, d, src)], check=True, env=env, cwd=ROOT)
sd = d + r'\slotv'
os.makedirs(sd, exist_ok=True)
ov = json.load(open(ov0))
X2T = {112: 119, 115: 122, 103: 110, 117: 124, 130: 131, 107: 114, 108: 115, 109: 116, 116: 123, 119: 126, 120: 127,
       121: 128, 128: 129, 129: 130, 132: 133, 131: 132, 118: 125, 114: 121}
ov = {k: v for k, v in ov.items() if not k.startswith('mode_client:112>')}
x2s = set(int(t) for t in x2.split(',') if t)
for t, tt in X2T.items():
    k = 'mode_client:109>%d' % tt
    if t in x2s: ov.setdefault(k, 0.0)
    else: ov.pop(k, None)
for t in x1.split(','):
    if t: ov['mode_client:112>%d' % X2T[int(t)]] = 0.0
if '117' not in rx.split(','): ov.pop('mode_client:124>131', None)
else: ov.setdefault('mode_client:124>131', 0.0)
if '126' not in rx.split(','): ov.pop('clientEraseBlock:7>6', None)
else: ov.setdefault('clientEraseBlock:7>6', 0.0)
json.dump(ov, open(sd + r'\ov.json', 'w'))
env2 = dict(os.environ, MCD='mc' + name, X1T=x1, RX117='1' if '117' in rx.split(',') else '0', RX126='1' if '126' in rx.split(',') else '0')
r = subprocess.run([sys.executable, S + r'\runq.py', 'v', des, os.environ.get('ITS', '6')], env=env2, cwd=ROOT, capture_output=True, text=True)
print(r.stdout[-3000:], r.stderr[-2000:])
