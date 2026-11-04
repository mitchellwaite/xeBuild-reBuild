"""fl4final.py [write]: builds attempt 4's draft and verifies it whole-object and per section.  Change this, not the draft.
TESTS and EXTRA are the dead tests left; EXTRA is one inserted at a statement site found by fl4r.py."""
import os, sys
import fllib as L, fl4lib as F, fl4g as G, fl4r as R

TESTS = 'off3=2,off4=1,x=1'
EXTRA = [(62, 'off < -1', '*buf = 0')]
OUT = L.DRAFT
KU = "\t/* defensive and dead, as in findKey: sets the order of this function's\n\t   buf[i]/key[0] compare */\n\tif (key == NULL)\n\t\treturn NULL;\n"
KEYCMP = ('\t\tif (key[0] == buf[i]) {\n\t\t\tp = &buf[i];\n', '\t\tif (buf[i] == key[0]) {\n\t\t\tp = &buf[i];\n')


def build(tests=None, extra=None):
    s = G.mk(F.st(TESTS if tests is None else tests))
    ss = R.sites(s)
    for p, c, a in sorted(EXTRA if extra is None else extra, reverse=True):
        s = R.ins(s, ss[p][0], ss[p][1], c, a)
    s = L.sub(s, KU, '')
    s = L.sub(s, KEYCMP[0], KEYCMP[1])
    return s


def tidy(s):
    s = L.sub(s, '\tuint32_t noCrc;\n\tstruct fileent *e;\n\tchar *s;\n', '\tuint32_t noCrc;\n\tchar *s;\n')
    s = L.sub(s, 'static void setupFiles(void)\n{\n\tint i;\n\tstruct fileent *e;\n\n\t/* the files this build type uses */\n',
              '/* the files this build type uses.  Called once, so inlined after parseIni\'s own names are\n'
              '   numbered, and that placement sets the compare operands and copy orders further down\n'
              '   (notes/filelist_ini.md).  The test comes first in the body so that xb.nFiles is numbered\n'
              '   before i, which gives this loop\'s `cmp [nFiles],edi` */\n'
              'static void setupFiles(void)\n{\n\tint i;\n\tstruct fileent *e;\n\n')
    a = '\t\t\tif (off < -1) {\n\t\t\t\t*buf = 0;\n\t\t\t}\n\t\t\tif (pos >= end)\n\t\t\t\ti = 16;\n'
    s = L.sub(s, a, "\t\t\t/* this and the three can't-happen tests in [flashfs] are dead, and steer gcc: what they free\n"
              "\t\t\t   sets flashfs's threaded copy order and its comma/nul compare (notes/filelist_ini.md) */\n" + a)
    s = L.sub(s, '\t\t\t\t/* defensive, and dead (key was read above): VRP removes it, and\n\t\t\t\t   until then it sets findKey\'s SSA numbers in the getters */\n',
              '\t\t\t\t/* defensive, and dead (key was read above): VRP removes it, and\n\t\t\t\t   until then it sets findKey\'s SSA numbers in the getters (a register tie) */\n')
    return s


if __name__ == '__main__':
    s = tidy(build())
    o = L.compile(s, ['-O3'], 'a4final')
    assert L.same(o), L.score(o)[:4]
    a, b = L.sections(L.REF), L.sections(o)
    assert a == b
    if len(sys.argv) > 1 and sys.argv[1] == 'write':
        with open(OUT, 'w', newline='\n') as f:
            f.write(s)
    print('MATCH', len(a), 'sections:', sorted(a))
