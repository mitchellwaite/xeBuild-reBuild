"""fl9m.py: from the draft, try to lose findField and setupFiles' test-first loop with fl6lib's natural axes and [security]'s split forms, one at a time."""
import itertools, os
os.environ.setdefault('FLA', 'a9')
import fllib as L, fl6lib as F, fl8lib as G, fl9i, fl9k

SPL = "\t\t\tif (comma > nul) {\n\t\t\t\tnoCrc = 1;\n\t\t\t\tlen = nul;\n\t\t\t} else {\n\t\t\t\tnoCrc = 0;\n\t\t\t\tlen = comma;\n\t\t\t}\n"
assert F.S0.count(SPL) == 1
SEC = {
    'le': SPL.replace("noCrc = 1;\n\t\t\t\tlen = nul;", "len = nul;\n\t\t\t\tnoCrc = 1;").replace("noCrc = 0;\n\t\t\t\tlen = comma;", "len = comma;\n\t\t\t\tnoCrc = 0;"),
    'flip': "\t\t\tif (comma <= nul) {\n\t\t\t\tnoCrc = 0;\n\t\t\t\tlen = comma;\n\t\t\t} else {\n\t\t\t\tnoCrc = 1;\n\t\t\t\tlen = nul;\n\t\t\t}\n",
    'def': "\t\t\tnoCrc = 0;\n\t\t\tlen = comma;\n\t\t\tif (comma > nul) {\n\t\t\t\tnoCrc = 1;\n\t\t\t\tlen = nul;\n\t\t\t}\n",
    'def2': "\t\t\tlen = comma;\n\t\t\tnoCrc = 0;\n\t\t\tif (comma > nul) {\n\t\t\t\tlen = nul;\n\t\t\t\tnoCrc = 1;\n\t\t\t}\n",
    'nfirst': None,
}


def sec(k):
    def f(s):
        if k == 'nfirst':
            return F.secsub(s, 'sec', F.CFIRST, F.NFIRST)
        return F.secsub(s, 'sec', SPL, SEC[k])
    return f


AX = {'sec=' + k: sec(k) for k in SEC}
for ax in ('sect', 'ent', 'copy', 'adv', 'val', 'flen'):
    for v, fn in F.E[ax].items():
        AX['%s=%s' % (ax, v)] = fn

if __name__ == '__main__':
    base = F.drop(F.S0, ['T1', 'T2', 'T3'])
    base = F.prein(base)
    V = {}
    for ff, lp, ch in itertools.product('yn', ('first', 'for'), 'cel'):
        if ff == 'y' and lp == 'first':
            continue
        b = base
        if ff == 'n':
            b = F.ffinline(b)
        if lp == 'for':
            b = fl9k.looponly(b)
        for a, fn in AX.items():
            if ff == 'y' and a == 'sec=nfirst':
                continue
            try:
                s = fn(fl9i.ui(fl9k.CH[ch])(b))
            except Exception as e:
                continue
            V['ff=%s,lp=%s,ch=%s,%s' % (ff, lp, ch, a)] = s
    print(len(V))
    G.run(V, 'm', 25)
