"""python tools/wip/dehint/bdpwin.py [file.c] [p,p,..] (attempt 22, diagnostic): score src (or argv[1]) at several builtin-expect-probability values and print the
per-function strict/loose lines of the functions whose only expect is one of the targets."""
import os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdlib, bdrun

src = bdlib.read_src(sys.argv[1]) if len(sys.argv) > 1 else bdlib.read_src()
FN = ['_addBlsToImage', '_buildFlash', '_addUpdateBls', '_loadConsoleBlFiles']
ps = [int(x) for x in (sys.argv[2].split(',') if len(sys.argv) > 2 else
                      '50,55,60,65,70,72,75,77,80,82,85,88,90,92,94,96,98,99'.split(','))]


def one(p):
    return p, bdrun.score(src, ['--param', 'builtin-expect-probability=%d' % p])


with ThreadPoolExecutor(4) as ex:
    for p, r in ex.map(one, ps):
        print(p, ' '.join('%s:%d/%d' % (f[1:], r['L'].get(f, 0), r['S'].get(f, 0)) for f in FN))
