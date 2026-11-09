"""Attempt 29: profile model of parseButtonX at its applyIniOptions site, from a standalone
compile's profile_estimate dump (0.25 s a variant; the numbers equal the in-file ones).

CF=0|1 python tools/wip/dehint/op29fast.py tools/wip/dehint/op29gen.py [-all]
  prints the variants whose keys fit bbro's heap (hit()): the call block is G = 132.3, block
  counts are round(freq x G / entry) and edges round(block x prob), as bbro computes them.
  N power block, ps its success probability, succ/fail its edges, el the else head's block,
  z the constant-0 block (sum of the edges that carry b = 0), part the split part's call."""
import os, re, subprocess, sys, tempfile, glob, shutil
from concurrent.futures import ThreadPoolExecutor
R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
TC = os.path.join(R, 'tools', 'toolchain-4745', 'mingw32', 'bin')
GCC = os.path.join(TC, 'gcc.exe')
os.environ['PATH'] = TC + os.pathsep + os.environ['PATH']
G = 132.3
PRE = '''#include <string.h>
extern struct { int xellButton; } xb;
int parseButtonPart(const char *s, int def);
int parseButtonX(const char *s)
{
'''
TMP = os.path.join(R, 'build', 'op', 'ft')
os.makedirs(TMP, exist_ok=True)

def metrics(body):
    d = tempfile.mkdtemp(dir=TMP)
    open(os.path.join(d, 'o.c'), 'w', newline='\n').write(PRE + body.strip('\n') + '\n}\n')
    r = subprocess.run([GCC, '-c', '-O3', 'o.c', '-o', 'o.o', '-fdump-tree-profile_estimate-details'], cwd=d, capture_output=True)
    if r.returncode:
        shutil.rmtree(d, ignore_errors=True)
        return None, 'ERR ' + r.stderr.decode()[:300]
    t = open(glob.glob(os.path.join(d, 'o.c.*profile_estimate'))[0]).read()
    shutil.rmtree(d, ignore_errors=True)
    t = t[t.index('\nparseButtonX ('):]
    blocks = {}
    for m in re.finditer(r';;   basic block (\d+), loop depth (\d+), count \d+, freq (\d+).*?\n(.*?);;    succ:(.*?)\n\n', t, re.S):
        n, depth, f, bodytxt, succ = m.groups()
        ss = re.findall(r'(\d+|EXIT) \[([\d.]+)%\]', succ)
        blocks[int(n)] = dict(f=int(f), body=bodytxt, succ=[(s, float(p)) for s, p in ss])
    ret = [n for n, b in blocks.items() if 'return' in b['body']][0]
    phi = re.search(r'# _\d+ = PHI <(.*?)>', blocks[ret]['body']).group(1)
    one = lambda key: [n for n, b in blocks.items() if key in b['body']][0]
    pw, part = one('"power"'), one('parseButtonPart')
    e0 = blocks[2]['f']
    sc = G / e0
    fi = lambda n: int(blocks[n]['f'] * sc + 0.5)
    ef = lambda n, p: int((fi(n) * int(round(p * 100)) + 5000) // 10000)
    z = 0
    zr = 0.0
    for a in phi.split(', '):
        v, src = re.match(r'(\S+)\((\d+)\)', a).groups()
        if v == '0':
            for s_, p in blocks[int(src)]['succ']:
                if s_ == str(ret):
                    z += ef(int(src), p)
                    zr += blocks[int(src)]['f'] * sc * p / 100
    ps = blocks[pw]['succ'][0][1]
    eln = int(blocks[pw]['succ'][1][0])
    succ, fail = ef(pw, ps), ef(pw, 100 - ps)
    m = dict(N=fi(pw), ps=ps, succ=succ, fail=fail, el=fi(eln), z=z, zr=zr, part=blocks[part]['f'] * 10000.0 / e0)
    return m, 'N %d ps %.1f succ %d fail %d el %d z %d (%.2f) part %.1f' % (m['N'], ps, succ, fail, m['el'], z, zr, m['part'])

def hit(m):
    k = 100 * m['fail'] + m['el']
    return m['z'] == 37 and m['succ'] <= 86 and m['part'] < 10 and 1718 <= k <= 1918 and m['ps'] > 50

if __name__ == '__main__':
    a = sys.argv[1:]
    ns = {}
    exec(open(a[0]).read(), ns)
    V = ns['V']
    names = list(V)
    with ThreadPoolExecutor(8) as ex:
        for n, (m, s) in zip(names, ex.map(lambda n: metrics(V[n]), names)):
            if m is None or '-all' in a or hit(m):
                print('%-30s %s' % (n, s), flush=True)
