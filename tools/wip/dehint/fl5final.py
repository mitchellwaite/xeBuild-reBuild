"""fl5final.py [write]: builds attempt 5's draft from current src and verifies it whole-object and per section.  Change this, not the draft.
Base is src with its parseIni tests per TESTS, findField for [security]'s searches, and PRE (fl4m's preParse)."""
import sys
import fllib as L, fl5lib as F, fl5f as X, fl5i as I, fl5n as N, fl5c as C

T = ('off4',)
EXTRA = N.parse('off < 0@98/1 @@ off < -1@81/1')
AXES = {'pre': 'y'}
OUT = L.DRAFT
COMMENT_OLD = "\t\t\t\t\tif (off < -1) {\n\t\t\t\t\t\t*buf = 0;\n\t\t\t\t\t}\n\t\t\t\t\tif (s == NULL)\n"


def build():
    base = X.gen({'hsec': 'cn'}, T)
    ss = I.sites(base)
    s = N.build(base, ss, EXTRA)
    for a, v in AXES.items():
        s = C.AX[a][v](s)
    return s


def tidy(s):
    s = s.replace('findField_sec', 'findField')
    s = L.sub(s, 'static void findField(unsigned char *p, int rem, int *comma, int *nul)\n',
              "/* an entry's name,crc separators.  Called once, so inlined after parseIni's own names are numbered, and the\n"
              "   loads and stores of *comma and *nul only go after that: it sets [security]'s compare order and takes the\n"
              "   place of the dead tests that did (notes/filelist_ini.md) */\n"
              'static void findField(unsigned char *p, int rem, int *comma, int *nul)\n')
    s = L.sub(s, 'static int preParse(unsigned char *buf, int size)\n',
              '/* the terminators around iniPreParse.  Called once, as with findField: numbers flashfs\'s len and noCrc copies */\n'
              'static int preParse(unsigned char *buf, int size)\n')
    # the first of the three remaining tests in [flashfs] carries the comment
    a = '\t\t\t\tif (off < -1) {\n\t\t\t\t\t*buf = 0;\n\t\t\t\t\tbuf[size] = 0;\n\t\t\t\t}\n\t\t\t\tstrncpy(xb.firmware[i], (char *)p, len);\n'
    s = L.sub(s, a, "\t\t\t\t/* this and the other two can't-happen tests in [flashfs] are dead, and steer gcc: what they free\n"
              "\t\t\t\t   sets [rawpatch]'s comma/nul compare and flashfs's copy order (notes/filelist_ini.md) */\n" + a)
    return s


if __name__ == '__main__':
    s = tidy(build())
    o = L.compile(s, ['-O3'], 'a5final')
    assert L.same(o), L.score(o)[:4]
    a, b = L.sections(L.REF), L.sections(o)
    assert a == b
    c = L.sections(L.os.path.join(L.R, 'build', 'obj', 'filelist_ini.o'))
    assert a == c
    assert open(o, 'rb').read() == open(L.os.path.join(L.R, 'build', 'obj', 'filelist_ini.o'), 'rb').read()
    if len(sys.argv) > 1 and sys.argv[1] == 'write':
        with open(OUT, 'w', newline='\n') as f:
            f.write(s)
    print('MATCH', len(a), 'sections:', sorted(a))
