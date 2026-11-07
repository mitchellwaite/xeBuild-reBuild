"""Attempt 52: unified diff of one function between two sources compiled the same way, with extra gcc flags
for diagnostics (e.g. -fno-early-inlining, to see what a helper does once only IPA inlines it).
python tools/wip/dehint/bdgen/a52_cmp.py <a.c> <b.c> <_symbol> [gcc flags..]   (p99)"""
import difflib, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import bdlib


def fns(p, ex):
    ok, o, d = bdlib.compile_src(open(p, newline='').read(), ['--param', 'builtin-expect-probability=99'], extra=ex)
    if not ok:
        sys.exit(o)
    return bdlib.disasm(o)[0]


if __name__ == '__main__':
    a, b, fn, ex = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:]
    x, y = fns(a, ex), fns(b, ex)
    for l in difflib.unified_diff(x.get(fn, []), y.get(fn, []), lineterm='', n=2):
        print(l)
