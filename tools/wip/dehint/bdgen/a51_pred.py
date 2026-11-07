"""Attempt 51: loadBl24's own profile per body: predictions (bdpred-style) and the summed
frequency of its defaultBl60 call blocks at profile_estimate (of 10000; target about 8600).
python tools/wip/dehint/bdgen/a51_pred.py [names..]   (bodies in a51_bodies.py; -v prints predictions)"""
import os, re, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a51_bodies as B

R = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
GCC = os.path.join(R, 'tools', 'toolchain-4745', 'mingw32', 'bin', 'gcc.exe')
env = dict(os.environ, PATH=os.path.dirname(GCC) + os.pathsep + os.environ['PATH'])
OUT = os.path.join(R, 'build', 'bd', 'a51')


def share(name, body, verbose=False):
    src = open(os.path.join(R, 'src', 'build.c'), newline='').read()
    assert B.OLD in src
    t = src.replace(B.OLD, body)
    d = tempfile.mkdtemp(dir=OUT)
    open(os.path.join(d, 'b.c'), 'w', newline='\n').write('#line 1 "build.c"\n' + t)
    p = subprocess.run([GCC, '-c', '-O3', '--param', 'builtin-expect-probability=99', '-I' + os.path.join(R, 'src'),
                        'b.c', '-o', 'b.o', '-fdump-tree-profile_estimate-details-blocks'], cwd=d, env=env,
                       capture_output=True, text=True)
    if p.returncode:
        return 'ERR ' + p.stderr[:300]
    dump = [f for f in os.listdir(d) if f.endswith('profile_estimate')][0]
    x = open(os.path.join(d, dump), errors='replace').read()
    parts = [m.start() for m in re.finditer(r'^;; Function loadBl24 ', x, re.M)]
    if not parts:
        return 'no loadBl24'
    s = parts[0]
    e = x.find('\n;; Function ', parts[-1] + 10)
    body_txt = x[s:e if e > 0 else len(x)]
    last = x[parts[-1]:e if e > 0 else len(x)]
    blk = {}
    for m in re.finditer(r';;   basic block (\d+), loop depth \d+, count \d+, freq (\d+).*?\n(.*?)(?=;;   basic block|\Z)', last, re.S):
        if "defaultBl60" in m.group(3):
            blk[m.group(1)] = int(m.group(2))
    tot = sum(blk.values())
    out = '%-8s calls %5d' % (name, tot)
    if verbose:
        out += '\n' + '\n'.join(l for l in body_txt.splitlines()
                                if 'heuristics' in l or l.startswith('Predictions') or l.startswith('  if') or 'freq' in l)
    return out


if __name__ == '__main__':
    a = sys.argv[1:]
    v = '-v' in a
    a = [x for x in a if x != '-v']
    names = a or list(B.BODIES)
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(4) as ex:
        for r in ex.map(lambda n: share(n, B.BODIES[n], v), names):
            print(r, flush=True)
