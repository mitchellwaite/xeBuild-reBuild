"""s12 runner for variants whose tree bbs >= 112 are shifted by SHIFT (vX: 1).
python run12.py SLOT design.json [raw overrides...]  env MCD (build dir), SHIFT, ENTRYBB"""
import json, os, re, subprocess, sys
ROOT = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
SH = int(os.environ.get('SHIFT', '1'))
LOOPX = os.environ.get('LOOPX') == '1'   # vZ: extra asm-goto block at tree 50 (after the -keys test)
def m(b): return b + SH + (1 if LOOPX and b >= 50 else 0) if b >= 112 else (b + 1 if LOOPX and b >= 50 else b)
def e(s, d): return 'mode_client:%d>%d' % (m(s), d if (LOOPX and s == 49 and d == 50) else m(d))
FAKE = ['clientEraseBlock:%s>1=100' % i for i in os.environ.get('FAKE', '5 6 7 8').split()]
NAMES = {'M': e(105, 107), 'A': e(106, 107), 'H1': e(116, 118), 'H2': e(119, 121), 'd1': e(122, 123), 'd2': e(129, 130),
         'e2': 'clientEraseBlock:2>8', 'e3': 'clientEraseBlock:3>7', 'e4': 'clientEraseBlock:4>6',
         'ip': e(49, 50), 'r': e(50, 56), 'w': e(56, 64), 'e': e(64, 72)}
if os.environ.get('ERASE'):
    for k_, e_ in zip(('e2', 'e3', 'e4'), os.environ['ERASE'].split()):
        NAMES[k_] = 'clientEraseBlock:' + e_
def key(k):
    if k in NAMES: return NAMES[k]
    mm = re.match(r'mode_client:(\d+)>(\d+)$', k)
    return e(int(mm.group(1)), int(mm.group(2))) if mm else k
CASES = [m(c) for c in (113, 114, 115, 116, 119, 122, 125, 126, 127, 128, 129, 132)]
DISP = m(112); XB = m(111) + 1
def design(x):
    d = {k: v for k, v in x.items() if not (k[:2] in ('cw', 'fx', 'lx', 'ex'))}
    if any(k.startswith('cw') for k in x):
        tot = sum(x.get('cw%d' % c, 1) for c in CASES)
        for c in CASES: d['raw:mode_client:%d>%d' % (DISP, c)] = 100.0 * x.get('cw%d' % c, 1) / tot
    for k in x:
        if k.startswith('fx'): d['raw:mode_client:%d>%d' % (XB, m(int(k[2:])))] = x[k]   # sp numbering
        if k.startswith('ex'): d['raw:clientEraseBlock:2>%s' % k[2:]] = x[k]
        if k.startswith('lx'): d['raw:mode_client:50>%d' % m(int(k[2:]))] = x[k]
    return d
def run(slot, x, raw=()):
    x = design(x)
    ov = ['%s=%.4f' % (key(k), v) for k, v in x.items() if not k.startswith('raw:')]
    ov += [k[4:] + '=%.4f' % v for k, v in x.items() if k.startswith('raw:')] + list(raw)
    ov += [e(112, 133) + '=0'] + FAKE + ['--consistent', '--entry=clientEraseBlock:mode_client:%d' % m(127)]
    env = dict(os.environ, EXTRA='--param builtin-expect-probability=50', MCFDO_DIR=ROOT + r'\build' + '\\' +os.environ.get('MCD', 'mcvX'))
    r = subprocess.run([sys.executable, ROOT + r'\tools\wip\mc\s9\fdorun9.py', slot, '--over'] + ov, cwd=ROOT, env=env, capture_output=True, text=True)
    f = inv = pre = 999
    for l in r.stdout.splitlines():
        if l.startswith('fncmp'): f = int(l.split()[1])
        if l.startswith('round4'):
            inv = int(l.split()[1].split('=')[1]); pre = int(l.split()[2].split('=')[1])
    return f, inv, pre, r.stdout + r.stderr
if __name__ == '__main__':
    f, inv, pre, o = run(sys.argv[1], json.load(open(sys.argv[2])), sys.argv[3:])
    print(o)
