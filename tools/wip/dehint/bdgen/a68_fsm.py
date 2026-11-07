"""Attempt 68: cheap filter for the setKitBuild route: compile each variant with
-fdump-tree-dom2-details and report whether dom2 registers src's FSM threads through the
setFlashBuild block (two loadBlFiles FSM paths of exactly three edges, e.g. (19, 22) incoming;
(22, 23) (23, 100) (100, 101)) -- 'good' -- or k1's two-edge ones -- 'bad'.
python tools/wip/dehint/bdgen/a68_fsm.py <script.py> [-p N] [-f substr] [-s]   (-s: also score good ones)"""
import importlib.util, os, re, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdlib
from a60lib import apply
from a58lib import score


def fsm(t, fl):
    d = tempfile.mkdtemp(dir=bdlib.BUILD, prefix='f')
    open(os.path.join(d, 'k.c'), 'w', newline='\n').write('#line 1 "build.c"\n' + t)
    r = subprocess.run([bdlib.GCC, '-c', '-O3'] + fl + ['-fdump-tree-dom2-details',
                       '-I' + os.path.join(bdlib.R, 'src'), 'k.c', '-o', 'k.o'], cwd=d, capture_output=True)
    if r.returncode:
        bdlib.cleanup(d)
        return 'ERR ' + r.stderr.decode()[:200]
    f = [x for x in os.listdir(d) if x.endswith('dom2')][0]
    b = open(os.path.join(d, f), encoding='latin-1').read()
    bdlib.cleanup(d)
    i = b.find(';; Function loadBlFiles ')
    j = b.find(';; Function ', i + 10)
    b = b[i:j]
    lines = sorted(set(re.findall(r'Registering FSM jump thread: \(\d+, \d+\) incoming edge;(.*)', b)))
    n3 = sum(1 for l in lines if len(re.findall(r'\(\d+, \d+\)', l.split('nocopy')[0])) == 3)
    return ('good' if n3 >= 2 else 'bad') + ' n3=%d' % n3


def main():
    a = sys.argv[1:]
    p, filt, sc = 0, None, False
    for opt in ('-p', '-f'):
        if opt in a:
            i = a.index(opt); v = a[i + 1]; del a[i:i + 2]
            if opt == '-p': p = int(v)
            else: filt = v
    if '-s' in a:
        a.remove('-s'); sc = True
    spec = importlib.util.spec_from_file_location('v', a[0])
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    base = bdlib.read_src()
    fl = [] if p == 0 else ['--param', 'builtin-expect-probability=%d' % p]
    jobs = []
    for lab, v in m.V.items():
        if filt and filt not in lab:
            continue
        try:
            jobs.append((lab, apply(base, v)))
        except ValueError as e:
            print(lab, 'SUBFAIL', e)

    def one(j):
        lab, t = j
        res = fsm(t, fl)
        if sc and res.startswith('good'):
            r = score(t, fl, os.path.join(bdlib.R, 'src'))
            if 'err' in r:
                res += ' ERR'
            elif r['identical']:
                res += ' IDENTICAL'
            else:
                res += ' L%d S%d %s' % (sum(r['L'].values()), sum(r['S'].values()),
                                        ' '.join('%s:%d/%d' % (k[1:], r['L'].get(k, 0), v) for k, v in r['S'].items()))
        return lab, res
    with ThreadPoolExecutor(4) as ex:
        for lab, res in ex.map(one, jobs):
            print('%-24s %s' % (lab, res), flush=True)


if __name__ == '__main__':
    main()
