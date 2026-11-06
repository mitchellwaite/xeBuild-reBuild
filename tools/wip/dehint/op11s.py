"""Attempt 11: compile an options.c variant to assembly and print its string literal order
(.LC number -> first 50 chars), so .rdata order can be checked before a whole-object compare.

python tools/wip/dehint/op11s.py <file.c> [out.s] [grep]"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib


def lits(path, out=None):
    ok, o, d = optlib.compile_src(optlib.read_src(path), keep=out, asm=True)
    if not ok:
        print(o)
        sys.exit(1)
    s = open(o).read()
    res = []
    for m in re.finditer(r'^(LC\d+):\n\t\.ascii "(.*)"$', s, re.M):
        res.append((m.group(1), m.group(2)))
    if not out:
        optlib.cleanup(d)
    return res, s


if __name__ == '__main__':
    out = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2].endswith('.s') else None
    pat = sys.argv[-1] if len(sys.argv) > 2 and not sys.argv[-1].endswith('.s') else None
    res, _ = lits(sys.argv[1], out)
    for n, t in res:
        if not pat or re.search(pat, t):
            print(n, t[:70])
