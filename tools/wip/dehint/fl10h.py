"""fl10h: Part 2 generator on current src.  Edits as functions on the source:
 ff: findField inlined.  loop: setupFiles' plain for.  chN: which of bl's uses go through unsigned `file`.
 python fl10h.py base          scores
 python fl10h.py diff <labels> diff of a state (labels: ff,loop,fileall,...)
 python fl10h.py write <labels> <path> writes the state's source
"""
import os, sys, re
import fllib as L, fl10lib as F

S = F.S0


def ff(s):
    a = s.index("/* an entry's name,crc separators.")
    b = s.index("/* read the file list ini:")
    s = s[:a] + s[b:]
    return L.sub(s, "findField(p, size - pos, &comma, &nul);", "comma = memFindChar(p, ',', size - pos);\n\t\t\tnul = memFindChar(p, 0, size - pos);")


def loop(s):
    s = L.sub(s, "for (i = 0; ; i++) {\n\t\tif (i >= xb.nFiles)\n\t\t\tbreak;\n\t\te = &xb.files[i];", "for (i = 0; i < xb.nFiles; i++) {\n\t\te = &xb.files[i];")
    return s


# bl's section: every xb.files[blOrder[i]] and a loop-top `file`
BLA = S.index("for (i = 0; i < nbl; ) {")
BLB = S.index("if (xb.type != BUILD_JTAG && xb.type <= BUILD_DEVGL16) {")


def blsec(s, fn):
    a = s.index("for (i = 0; i < nbl; ) {")
    b = s.index("if (xb.type != BUILD_JTAG && xb.type <= BUILD_DEVGL16) {")
    return s[:a] + fn(s[a:b]) + s[b:]


CMT = "\t\t\t/* unsigned on purpose: no (sizetype) statement at laddress, and that one name fewer sets the\n\t\t\t   numbers of [rawpatch]'s and [flashfs]'s compares and copies (notes/filelist_ini.md, attempt 9) */\n"


def fileall(s):
    """`uint32_t file = blOrder[i];` at the top of the loop, used everywhere"""
    def f(t):
        t = t.replace(CMT, '')
        t = t.replace("\t\t\tfile = blOrder[i];\n", '')
        t = t.replace("uint32_t file;\n\n", "uint32_t file = blOrder[i];\n\n")
        t = t.replace("xb.files[blOrder[i]]", "xb.files[file]")
        return t
    return blsec(s, f)


def filetop(s):
    """`file` assigned at the top of the loop, used for the listed uses only (others keep blOrder[i])"""
    def f(t):
        t = t.replace(CMT, '')
        t = t.replace("\t\t\tfile = blOrder[i];\n", '')
        t = t.replace("uint32_t file;\n\n", "uint32_t file = blOrder[i];\n\n")
        return t
    return blsec(s, f)


EDITS = {'ff': ff, 'loop': loop, 'fileall': fileall, 'filetop': filetop}


def state(lab):
    s = S
    for k in [x for x in lab.split(',') if x]:
        s = EDITS[k](s)
    return s


if __name__ == '__main__':
    if sys.argv[1] == 'base':
        F.run({k: state(k) for k in ('', 'ff', 'loop', 'ff,loop', 'fileall', 'fileall,ff', 'filetop')}, 'h')
    elif sys.argv[1] == 'diff':
        F.diff(state(sys.argv[2]))
    elif sys.argv[1] == 'write':
        open(sys.argv[3], 'w', newline='\n').write(state(sys.argv[2]))
