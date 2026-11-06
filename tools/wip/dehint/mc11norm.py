"""mode_client attempt 11: diff a source's mode_client against the reference with jump and
call targets blanked, so a moved block counts its own lines only (not every jump into it).

python tools/wip/dehint/mc11norm.py A.c [-v]"""
import difflib, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdlib, mc1lib

TGT = re.compile(r'^(j\w+|call)\s+[-0-9a-f]+$')


def norm(lines):
    return [TGT.sub(r'\1 X', l) for l in lines]


def ndiff(text, fn='_mode_client', show=False):
    ok, o, d = mc1lib.compile_src(text, [])
    if not ok:
        return None
    fns, _ = bdlib.disasm(o)
    mc1lib.cleanup(d)
    a, b = norm(mc1lib._ref['fns'][fn]), norm(fns.get(fn, []))
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    n = sum(max(i2 - i1, j2 - j1) for op, i1, i2, j1, j2 in sm.get_opcodes() if op != 'equal')
    if show:
        for l in difflib.unified_diff(a, b, 'ref', 'new', n=1, lineterm=''):
            print(l)
    return n


if __name__ == '__main__':
    print(ndiff(mc1lib.read_src(sys.argv[1]), show='-v' in sys.argv))
