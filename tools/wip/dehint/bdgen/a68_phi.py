"""Attempt 68: for each variant (a60lib-style script), dump loadBlFiles with -fdump-tree-all and print
the switch join's r PHI (the PHI with the most arguments) after each pass from fixup_cfg4 to dom2,
plus dom2's FSM registrations through the sig-failed path.
python tools/wip/dehint/bdgen/a68_phi.py <script.py> [-p N] [-f substr] [-a]   (-a: all passes)"""
import glob, importlib.util, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdlib
from a60lib import apply

OUT = os.path.join(bdlib.R, 'build', 'bd', 'a68')
PASSES = ('fixup_cfg4', 'ccp2', 'mergephi2', 'vrp1', 'dce2', 'dom2')


def fnbody(t, fn='loadBlFiles'):
    i = t.find(';; Function %s ' % fn)
    if i < 0:
        return ''
    j = t.find(';; Function ', i + 10)
    return t[i:j if j > 0 else len(t)]


def bigphi(b):
    best = None
    for m in re.finditer(r'(r_\d+) = PHI <([^>]*)>', b):
        n = m.group(2).count(',') + 1
        if best is None or n > best[0]:
            best = (n, m.group(1), m.group(2))
    return best


def main():
    a = sys.argv[1:]
    p, filt, allp = 0, None, False
    for opt in ('-p', '-f'):
        if opt in a:
            i = a.index(opt); v = a[i + 1]; del a[i:i + 2]
            if opt == '-p': p = int(v)
            else: filt = v
    if '-a' in a:
        a.remove('-a'); allp = True
    spec = importlib.util.spec_from_file_location('v', a[0])
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    base = bdlib.read_src()
    fl = [] if p == 0 else ['--param', 'builtin-expect-probability=%d' % p]
    for lab, v in m.V.items():
        if filt and filt not in lab:
            continue
        try:
            t = apply(base, v)
        except ValueError as e:
            print(lab, 'SUBFAIL', e); continue
        d = os.path.join(OUT, 'phi_' + lab)
        os.makedirs(d, exist_ok=True)
        for f in glob.glob(os.path.join(d, 'k.c.*')):
            os.remove(f)
        open(os.path.join(d, 'k.c'), 'w', newline='\n').write('#line 1 "build.c"\n' + t)
        r = subprocess.run([bdlib.GCC, '-c', '-O3'] + fl + ['-fdump-tree-all', '-fdump-tree-dom2-details',
                           '-I' + os.path.join(bdlib.R, 'src'), 'k.c', '-o', 'k.o'], cwd=d, capture_output=True)
        if r.returncode:
            print(lab, 'ERR', r.stderr.decode()[:300]); continue
        print('==', lab)
        files = sorted(glob.glob(os.path.join(d, 'k.c.*t.*')), key=lambda f: int(re.search(r'\.(\d+)t\.', f).group(1)))
        for f in files:
            pn = re.search(r'\d+t\.(.*)$', f).group(1)
            if not allp and pn not in PASSES:
                continue
            b = fnbody(open(f, encoding='latin-1').read())
            bp = bigphi(b)
            if pn == 'dom2':
                fsm = sorted(set(re.findall(r'Registering FSM jump thread: (.*)', b)))
                for x in fsm:
                    print('   FSM', x.strip())
            if bp:
                print('  %-11s %s n=%d <%s>' % (pn, bp[1], bp[0], bp[2]))


if __name__ == '__main__':
    main()
