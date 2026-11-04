"""flx6.py <state label> [extra 'line:var' already inserted, comma-separated]: one dead test anywhere.
For each statement boundary in parseIni's sections and each var, insert `if (v < -1) buf[0] = 1;`.
The total only drops if this replaces several; the aim is fewer tests, not another hint.
Writes x6_<tag>.txt.  Label's ties to beat are printed with the base score."""
import os, re, sys
import fllib as L, flx as X, flx3 as A, flx4 as F

VARS = (os.environ.get('VARS') or 'off,pos,len,nul,comma,i,n,end,size').split(',')
START = '\tsize = iniPreParse(buf, size);\n'
BODY = {'t': '%sif (%s < -1)\n%s\tbuf[0] = 1;\n'}


def points(s):
    a = s.index('/* [version] */')
    b = s.index('/* offset of the value after `key` in buf')
    a = s.index('\n', a) + 1
    out = []
    i = a
    while i < b:
        j = s.index('\n', i) + 1
        ln = s[i:j]
        st = ln.strip()
        prev = s[s.rindex('\n', 0, i - 1) + 1:i].strip()
        ok = st and not st.startswith(('else', '}', 'case', '/*', 'break')) and not ln.startswith('}')
        if ok and (prev.endswith((';', '{', '}'))) and not prev.startswith(('if', 'for', 'else if')) or (ok and prev.endswith(';') and prev.startswith(('if ', 'else'))):
            out.append(i)
        i = j
    return out


def insert(s, pos, v):
    ln = s[pos:s.index('\n', pos)]
    ind = ln[:len(ln) - len(ln.lstrip())]
    return s[:pos] + '%sif (%s < -1)\n%s\tbuf[0] = 1;\n' % (ind, v, ind) + s[pos:]


if __name__ == '__main__':
    fl, dead, ch = F.parse(sys.argv[1])
    base = A.apply(X.gen(dead, fl), ch)
    print('base', L.score(L.compile(base, None, 'b6'))[:3])
    pts = points(base)
    print(len(pts), 'points')
    V, meta = {}, {}
    for p in pts:
        lineno = base.count('\n', 0, p) + 1
        for v in VARS:
            n = '%d_%s' % (lineno, v)
            V[n] = insert(base, p, v)
            meta[n] = base[p:base.index('\n', p)].strip()[:60]
    print(len(V))
    tag = os.environ.get('TAG', 'a')
    rs = L.sweep(V, prefix='ds', show=0)
    with open(L.BD + '/x6_%s.txt' % tag, 'w', newline='\n') as f:
        for n, (sc, st, fd, sd) in rs:
            f.write('%s\t%s\t%s\t%s\n' % (sc, n, meta[n], fd))
    for n, (sc, st, fd, sd) in rs[:30]:
        print(sc, n, meta[n], fd)
    from collections import Counter
    print(sorted(Counter(r[0] for n, r in rs).items())[:12])
