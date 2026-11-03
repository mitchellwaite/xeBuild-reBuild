"""python tools/wip/dehint/cep.py <gen dir>: the alloc test's predictions per variant (block that calls calloc in ceDecrypt),
from -fdump-tree-profile_estimate. Prints the distinct lists with a count and one example."""
import concurrent.futures as cf, glob, os, re, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
BIN = os.path.join(ROOT, 'tools', 'toolchain-4745', 'mingw32', 'bin')


def one(src):
    env = dict(os.environ, PATH=BIN + os.pathsep + os.environ['PATH'])
    with tempfile.TemporaryDirectory() as d:
        r = subprocess.run([os.path.join(BIN, 'gcc.exe'), '-S', '-O3', '-fno-asynchronous-unwind-tables', '-masm=intel',
                            '-I', os.path.join(ROOT, 'src'), '-fdump-tree-profile_estimate-details', src, '-o', 'o.s'],
                           env=env, cwd=d, capture_output=True, text=True)
        if r.returncode:
            return src, 'compile error ' + r.stderr[:300]
        s = open(glob.glob(os.path.join(d, '*profile_estimate'))[0], errors='replace').read()
    m = re.search(r'^;; Function ceDecrypt\b.*', s, re.M | re.S)
    t = m.group(0)
    bb = None
    for b in re.finditer(r'<bb (\d+)>:(.*?)(?=<bb \d+>:|\Z)', t[t.index('ceDecrypt ('):], re.S):
        if 'calloc' in b.group(2):
            bb = b.group(1)
            break
    p = re.search(r'Predictions for bb %s\n(.*?)(?=Predictions for|\n\n|\Z)' % bb, t, re.S)
    if not p:
        return src, 'none'
    items = sorted(re.sub(r'\s+heuristics', '', x.strip()) for x in p.group(1).split('\n') if x.strip() and 'first match' not in x and 'combined' not in x)
    return src, '; '.join(items)


def main():
    files = sorted(glob.glob(os.path.join(os.path.abspath(sys.argv[1]), 'v*.c')), key=lambda x: int(re.search(r'v(\d+)', os.path.basename(x)).group(1)))
    res = {}
    with cf.ThreadPoolExecutor(os.cpu_count() or 4) as ex:
        for s, r in ex.map(one, files):
            res.setdefault(r, []).append(os.path.basename(s))
    for r, l in sorted(res.items(), key=lambda kv: -len(kv[1])):
        print(len(l), l[0], r)


if __name__ == '__main__':
    main()
