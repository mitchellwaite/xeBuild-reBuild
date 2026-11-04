"""fl9final.py [write]: attempt 9's draft from src/filelist_ini.c: the three [flashfs] tests dropped, preParse back inline, bl's log line through an unsigned
local.  Prints the score; `write` saves tools/wip/dehint/drafts/filelist_ini_final.c and compares every section.  Change this, not the draft."""
import hashlib, os, sys
os.environ.setdefault('FLA', 'a9')
import fllib as L, fl6lib as F

LOG = '\t\t\tlog_printf(1, "found (%d) \'%s\' crc: 0x%08x\\n", i + 1, xb.files[blOrder[i]].name, xb.files[blOrder[i]].crc);\n'
NEWLOG = ('\t\t\tfile = blOrder[i];\n'
          '\t\t\tlog_printf(1, "found (%d) \'%s\' crc: 0x%08x\\n", i + 1, xb.files[file].name, xb.files[file].crc);\n')
HEAD = '\t\tfor (i = 0; i < nbl; ) {\n\t\t\tp = &buf[pos];\n'
NEWHEAD = ('\t\tfor (i = 0; i < nbl; ) {\n'
           '\t\t\t/* unsigned on purpose: no (sizetype) statement at laddress, and that one name fewer sets the\n'
           '\t\t\t   numbers of [rawpatch]\'s and [flashfs]\'s compares and copies (notes/filelist_ini.md, attempt 9) */\n'
           '\t\t\tuint32_t file;\n\n'
           '\t\t\tp = &buf[pos];\n')
FFC = ("/* an entry's name,crc separators.  Called once, so inlined after parseIni's own names are numbered, and the\n"
       "   loads and stores of *comma and *nul only go after that: it sets [security]'s compare order and takes the\n"
       "   place of the dead tests that did (notes/filelist_ini.md) */\n")
NEWFFC = ("/* an entry's name,crc separators.  Called once, so inlined after parseIni's own names are numbered, and the\n"
          "   loads and stores of *comma and *nul only go after that: it sets flashfs's copy order\n"
          "   (notes/filelist_ini.md) */\n")


def source(s=None):
    s = F.drop(s or F.S0, ['T1', 'T2', 'T3'])
    s = F.prein(s)
    s = F.secsub(s, 'bl', LOG, NEWLOG)
    s = L.sub(s, HEAD, NEWHEAD)
    s = L.sub(s, FFC, NEWFFC)
    return s


if __name__ == '__main__':
    s = source()
    o = L.compile(s, None, 'a9final')
    sc = L.score(o)
    print('nscore', F.nscore(o, sc), sc[2:], 'same', L.same(o))
    print('sha256', hashlib.sha256(open(o, 'rb').read()).hexdigest()[:16], 'ref', hashlib.sha256(open(L.REF, 'rb').read()).hexdigest()[:16])
    if len(sys.argv) > 1 and sys.argv[1] == 'write':
        assert L.same(o), 'no match, not written'
        open(L.DRAFT, 'w', newline='\n').write(s)
        o2 = L.compile(open(L.DRAFT, newline='').read(), None, 'a9final2')
        A, B = L.sections(o2), L.sections(os.path.join(L.R, 'build', 'obj', 'filelist_ini.o'))
        print('sections', {k: A[k] == B.get(k) for k in A}, 'same keys', set(A) == set(B))
        print('whole object', open(o2, 'rb').read() == open(os.path.join(L.R, 'build', 'obj', 'filelist_ini.o'), 'rb').read())
