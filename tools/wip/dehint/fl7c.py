"""fl7c.py [states]: do parseIni's dead tests change block frequencies?  Compiles src and each fl6lib state (tests to drop before |, axes after), prints
the sorted multiset of block frequencies in .optimized and how many differ from src's, and the same for the freq= of LRA's first assignment.
Default states: each of T1 T2 T3 dropped, all dropped, findField and preParse undone."""
import collections, glob, os, re, subprocess, sys
import fllib as L, fl6lib as F, fl7lib as K

D = os.path.join(K.A7, 'c')
os.makedirs(D, exist_ok=True)


def dumps(src, tag):
    d = os.path.join(D, tag)
    os.makedirs(d, exist_ok=True)
    for f in glob.glob(os.path.join(d, '*')):
        os.remove(f)
    inp = ('#line 1 "filelist_ini.c"\n' + src).encode()
    subprocess.run([L.GCC, '-c', '-O3', '-fdump-tree-optimized-blocks-details', '-fdump-rtl-reload', '-I' + os.path.join(L.R, 'src'), '-x', 'c', '-', '-o', 'x.o'],
                   input=inp, cwd=d, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    r = {}
    for suf, pat, key in (('optimized', r'basic block \d+, loop depth \d, count \d+, freq (\d+)', 'bb'), ('reload', r'Assign \d+ to [a-z ]*r\d+ \(freq=(\d+)\)', 'lra')):
        f = glob.glob(os.path.join(d, '*' + suf))[0]
        t = open(f, errors='replace').read()
        for part in re.split(r'(?m)^(?=;; Function )', t):
            if part.startswith(';; Function parseIni '):
                if key == 'lra':
                    part = part.split('Assignment #2')[0]
                r[key] = collections.Counter(int(x) for x in re.findall(pat, part))
    return r


if __name__ == '__main__':
    base = dumps(F.S0, 'src')
    print('src blocks', sum(base['bb'].values()), 'lra', sum(base['lra'].values()))
    for st in sys.argv[1:] or ['T1|', 'T2|', 'T3|', 'T1,T2,T3|', 'T1,T2,T3|ff=none', 'T1,T2,T3|pre=in', 'T1,T2,T3|ff=none,pre=in']:
        r = dumps(F.state(st), re.sub(r'\W', '_', st))
        print('%-28s' % st, 'blocks %d' % sum(r['bb'].values()),
              'bb only-src', sorted((base['bb'] - r['bb']).elements())[:14], 'bb only-state', sorted((r['bb'] - base['bb']).elements())[:14],
              '| lra n=%d' % sum(r['lra'].values()), 'lra only-src', sorted((base['lra'] - r['lra']).elements())[:10], 'only-state', sorted((r['lra'] - base['lra']).elements())[:10])
