"""python tools/wip/dehint/bdorder.py <gen.py> [regex]: for each case of a bdrun generator, the calcBlAreaSize statement
before each setPatchSlot call in the .optimized dump (or the lines matching regex), with the bdrun score.

Attempt 20's check for pin_size: the kit arm's sum must come out as `size_N + prephitmp_M` (size's PHI first), which is
what the pin gives; without it PRE's names are lower than the size PHI's and fold puts the load first."""
import importlib.util, os, re, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdlib, bdrun


def opt_lines(text, fn='calcBlAreaSize', rx=None):
    d = tempfile.mkdtemp(dir=bdlib.BUILD, prefix='o')
    src = '#line 1 "build.c"\n' + text
    subprocess.run([bdlib.GCC, '-c', '-O3'] + bdlib.P98 + ['-fdump-tree-optimized', '-I' + os.path.join(bdlib.R, 'src'),
                                                      '-x', 'c', '-', '-o', 'o.o'], input=src.encode(), cwd=d, capture_output=True)
    out = []
    for f in os.listdir(d):
        if f.endswith('.optimized'):
            on = False
            prev = ''
            for l in open(os.path.join(d, f), errors='replace'):
                if l.startswith(';; Function '):
                    on = l.split()[2] == fn
                if not on:
                    continue
                if rx:
                    if re.search(rx, l):
                        out.append(l.strip())
                elif 'setPatchSlot (' in l:
                    out.append(prev.strip())
                if l.strip() and not l.startswith(';;'):
                    prev = l
    bdlib.cleanup(d)
    return out


def main():
    spec = importlib.util.spec_from_file_location('gen', sys.argv[1])
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    rx = sys.argv[2] if len(sys.argv) > 2 else None
    base = bdlib.read_src(os.path.join(bdlib.R, getattr(m, 'BASE', 'src/build.c')))
    if hasattr(m, 'PRE'):
        base = m.PRE(base)

    def one(c):
        lab, f = c
        try:
            t = f(base) if callable(f) else f
        except ValueError as e:
            return lab, str(e), []
        if t is None:
            return lab, 'skip', []
        r = bdrun.score(t)
        s = 'IDENTICAL' if r.get('identical') else ('L%d S%d' % (sum(r['L'].values()), sum(r['S'].values())) if 'S' in r else 'ERR')
        return lab, s, opt_lines(t, rx=rx)
    with ThreadPoolExecutor(4) as ex:
        for lab, s, ls in ex.map(one, m.CASES(base)):
            print('%-40s %-12s %s' % (lab, s, ' | '.join(ls)))


if __name__ == '__main__':
    main()
