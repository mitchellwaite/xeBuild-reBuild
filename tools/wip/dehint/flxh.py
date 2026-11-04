"""flxh.py: other shapes for [flashfs]'s path check that give the literal order without an asm:
goto to the loop's tail, flag-free `else if`, the check after the name.  All 256 dead subsets each."""
import itertools, os, re
from concurrent.futures import ThreadPoolExecutor
import fllib as L, flx as X, flx7 as T

ERR = X.PATHERR
FIND = "\t\t\tif (pos >= size)\n\t\t\t\ti = 256;\n"


def plain_removed(s):
    m = X.FLEN_C.search(s)
    return s[:m.start()], s[m.end():]


def form(s, how):
    a, b = plain_removed(s)
    if how == 'gototail':
        s = a + '\t\t\tif (len > 1023)\n\t\t\t\tgoto tooLong;\n' + b
        return L.sub(s, FIND, FIND + '\t\t\tcontinue;\ntooLong:\n\t\t\t' + ERR.replace('\t\t\t\t', '\t\t\t'))
    if how == 'gotoafter':
        s = a + '\t\t\tif (len > 1023)\n\t\t\t\tgoto tooLong;\n' + b
        o = '\t} else {\n\t\tlog_printf(0, "\\n******* ERROR: could not find label [flashfs] in file list ini\\n");'
        return L.sub(s, FIND + '\t\t}\n' + o, FIND + '\t\t}\n\t\tgoto flashDone;\ntooLong:\n\t\t' + ERR.replace('\t\t\t\t', '\t\t') + o).replace(
            '\t/* [security]: name[,crc] */\n', 'flashDone:\n\t/* [security]: name[,crc] */\n')
    if how == 'nestname':
        # the good path nests only as far as the name check; the rest follows
        s = a + '\t\t\tif (len <= 1023) {\n' + b
        k = s.index('\t\t\tpos = pos + len + 1;\n\t\t\tif (xb.firmware[i][len - 1]')
        return s[:k] + '\t\t\t} else {\n\t\t\t\t' + ERR + '\t\t\t}\n' + s[k:]
    if how == 'nestcopy':
        s = a + '\t\t\tif (len <= 1023) {\n' + b
        k = s.index('\t\t\tif (off < -1)\n\t\t\t\tbuf[0] = 1;\n\t\t\tif (len > 21) {') if '\t\t\tif (off < -1)\n\t\t\t\tbuf[0] = 1;\n\t\t\tif (len > 21) {' in s else s.index('\t\t\tif (len > 21) {')
        return s[:k] + '\t\t\t} else {\n\t\t\t\t' + ERR + '\t\t\t}\n' + s[k:]
    raise ValueError(how)


def main():
    V = {}
    for how in ['gototail', 'gotoafter', 'nestname', 'nestcopy']:
        for r in range(len(X.ALLDEAD) + 1):
            for rm in itertools.combinations(X.ALLDEAD, r):
                # asm-free source, then the shape
                V[how + '|' + '+'.join(x for x in X.ALLDEAD if x not in rm)] = form(X.gen(rm, 'asm'), how)

    def one(kv):
        i, (n, s) = kv
        o = L.compile(s, None, 'hh' + str(i))
        if o is None:
            return 10**7, '', n
        sc = L.score(o)
        v = T.vec(o)
        os.remove(o)
        return sc[0], v, n + ' ' + ','.join(sc[3])
    with ThreadPoolExecutor(4) as ex:
        rs = sorted(ex.map(one, enumerate(V.items())), key=lambda r: r[0])
    for r in rs[:30]:
        print(r)
    with open(L.BD + '/xh.txt', 'w', newline='\n') as f:
        for r in rs:
            f.write('%s\t%s\t%s\n' % r)


if __name__ == '__main__':
    main()
