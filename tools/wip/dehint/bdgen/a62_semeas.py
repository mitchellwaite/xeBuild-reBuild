"""Attempt 62 (a61_semeas.py plus the copy test's SUCC probabilities): exp_pr's final-RTL frequencies for each variant of an a60lib-style script, with the tail's
expect spelled `(int)r < 0` (default) or kept (-x): the SE block (after `cmpb $69`), the two blocks that
follow it (the r-false copy of the tail test and its jmp block), and the no-key log blocks, from -dA.
python tools/wip/dehint/bdgen/a61_semeas.py <script.py> [-x] [-p 99] [-f substr]"""
import importlib.util, os, re, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdlib
from a60lib import apply
R = bdlib.R
GCC = os.path.join(R, 'tools', 'toolchain-4745', 'mingw32', 'bin', 'gcc.exe')
env = dict(os.environ, PATH=os.path.dirname(GCC) + os.pathsep + os.environ['PATH'])
OUT = os.path.join(R, 'build', 'bd', 'a62', 'sm')
os.makedirs(OUT, exist_ok=True)
EXP = 'if (__builtin_expect(r != 0, 0))\n\t\t\t\t\t\tgoto fail;'
NEG = 'if ((int)r < 0)\n\t\t\t\t\t\tgoto fail;'


def da(text, p):
    d = tempfile.mkdtemp(dir=OUT)
    open(os.path.join(d, 'b.c'), 'w', newline='\n').write('#line 1 "build.c"\n' + text)
    fl = ['--param', 'builtin-expect-probability=%d' % p] if p else []
    r = subprocess.run([GCC, '-S', '-dA', '-O3'] + fl + ['-I' + os.path.join(R, 'src'), 'b.c', '-o', 'b.s'],
                       cwd=d, env=env, capture_output=True, text=True)
    if r.returncode:
        return None
    s = open(os.path.join(d, 'b.s')).read()
    m = re.search(r'^_loadBlFiles:\n(.*?)\n\t\.cfi_endproc', s, re.S | re.M)
    lc = re.search(r'^(LC\d+):\n\t\.ascii "loaded %s, could not check signature rsa', s, re.M).group(1)
    return m.group(1), lc


def meas(t, lc):
    bl = re.split(r'\n(?= # BLOCK )', t)
    def fr(b):
        m = re.match(r' # BLOCK (\d+)(?: freq:(\d+))?', b)
        return (int(m.group(1)), int(m.group(2) or 0)) if m else None
    se = []
    for i, b in enumerate(bl):
        if 'cmpb\t$69' in b:
            se = [fr(x) for x in bl[i + 1:i + 4]]
            m2 = re.findall(r'# SUCC: .*', bl[i + 2])
            se.append(re.sub(r'\s*\((?:[A-Z_,]+)\)', '', m2[-1][8:]) if m2 else '?')
    nk = [fr(b) for b in bl if '$%s,' % lc in b]
    al = [fr(b) for b in bl if '$%s,' % lc in b and '.p2align' in b]
    return 'SE %s  nokey %s aligned %s' % (se, nk, al)


def main():
    a = sys.argv[1:]
    p, filt, keep = 99, None, '-x' in a
    a = [x for x in a if x != '-x']
    for opt in ('-p', '-f'):
        if opt in a:
            i = a.index(opt); v = a[i + 1]; del a[i:i + 2]
            if opt == '-p': p = int(v)
            if opt == '-f': filt = v
    spec = importlib.util.spec_from_file_location('v', a[0])
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    base = bdlib.read_src()
    jobs = []
    for lab, v in m.V.items():
        if filt and filt not in lab:
            continue
        try:
            t = apply(base, v)
            if not keep and EXP in t:
                t = t.replace(EXP, NEG)
        except ValueError as e:
            print(lab, 'SUBFAIL', e); continue
        jobs.append((lab, t))
    def one(j):
        r = da(j[1], p)
        return j[0], ('ERR' if r is None else meas(*r))
    with ThreadPoolExecutor(4) as ex:
        for lab, s in ex.map(one, jobs):
            print('%-22s %s' % (lab, s), flush=True)


if __name__ == '__main__':
    main()
