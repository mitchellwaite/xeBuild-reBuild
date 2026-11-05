"""Attempt 19 helpers.
python tools/wip/dehint/ir19.py ref            : reference getImageSmc disassembly
python tools/wip/dehint/ir19.py <fn.c> [flags] : score a getImageSmc text (replaces it in src/image_read.c) and print the loose diff
python tools/wip/dehint/ir19.py <fn.c> -dump <pass,...> : also print the named tree dumps' getImageSmc part (e.g. pre,dom2,vrp1)"""
import glob, os, re, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import irlib
from ir17lib import put, score, diff


def dumps(text, passes, flags=()):
    """{pass: getImageSmc text} from -fdump-tree-all-details (dump files are <n>t.<pass>)"""
    d = tempfile.mkdtemp(dir=irlib.BUILD, prefix='d')
    ok, o, _ = irlib.compile_src(text, list(flags) + ['-fdump-tree-all'], workdir=d)
    res = {}
    if not ok:
        return {'error': o}
    for f in sorted(os.listdir(d)):
        for p in passes:
            if re.search(r'\.\d+t\.' + re.escape(p) + r'$', f) or f.endswith('.' + p):
                t = open(os.path.join(d, f), errors='replace').read()
                m = re.search(r';; Function getImageSmc.*?(?=\n;; Function |\Z)', t, re.S)
                res[p] = m.group(0) if m else ''
    irlib.cleanup(d)
    return res


if __name__ == '__main__':
    if sys.argv[1] == 'ref':
        for l in irlib.ref()['fns']['_getImageSmc']:
            print(l)
        sys.exit()
    fn = open(sys.argv[1], newline='').read().replace('\r\n', '\n')
    a = sys.argv[2:]
    ps = []
    if '-dump' in a:
        i = a.index('-dump')
        ps = a[i + 1].split(',')
        del a[i:i + 2]
    t = put(fn)
    print(score(t, a))
    print(diff(t, a))
    for k, v in dumps(t, ps, a).items():
        print('=====', k)
        print(v)
