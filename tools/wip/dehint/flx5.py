"""flx5.py: initialisers on declarations (`int comma = 0;`): const assignments make SSA names that
early ccp frees, the natural counterpart of the dead tests.  Search: top-level vars in parseIni, loop
locals in each section, sampled and hill-climbed.
  flx5.py <N> <seed> <state label>  [p]
"""
import random, sys
import fllib as L, flx as X, flx3 as A, flx4 as F

TOP = ['size', 'off', 'end', 'pos', 'len', 'nul', 'comma', 'n', 'i', 'nbl', 'noCrc', 'crc', 's', 'e', 'p', 'buf', 'f']
FORS = {'bl': A.FORBL, 'raw': A.FORRAW, 'fl': A.FORFL, 'sec': A.FORSEC}
LOOPV = {'bl': ['comma', 'nul', 'len', 'noCrc', 'n'], 'raw': ['comma', 'nul', 'n'], 'fl': ['comma', 'nul', 'len', 'noCrc', 'n', 'crc', 's'], 'sec': ['comma', 'nul', 'len', 'noCrc', 'n']}
ANCHOR = '\tlog_printf(1, "\\n------ parsing ini at \'%s\' ------\\n", path);\n'


def inits(s, ch, top, loops=(), order=None):
    """top: var names initialised at the top; loops: 'bl.comma' style."""
    scoped = set()
    if ch.get('lenc'):
        scoped |= {'len', 'noCrc'}
    if ch.get('cn'):
        scoped |= {'comma', 'nul'}
    if ch.get('n'):
        scoped |= {'n'}
    if ch.get('p'):
        scoped |= {'p'}
    if ch.get('e'):
        scoped |= {'e'}
    if ch.get('s') in ('scope', 'both'):
        scoped |= {'s'}
    txt = ''
    for v in top:
        if v in scoped:
            raise ValueError('scoped')
        txt += '\t%s = 0;\n' % v
    if txt:
        s = L.sub(s, ANCHOR, txt + ANCHOR)
    for k in loops:
        lp, v = k.split('.')
        o = FORS[lp]
        if s.count(o) != 1:
            raise ValueError('loop')
        # after any decls the loop already has
        i = s.index(o) + len(o)
        while True:
            j = s.index('\n', i)
            ln = s[i:j]
            if ln.strip().startswith(('int ', 'uint32_t ')) or ln.strip() == '':
                i = j + 1
            else:
                break
        s = s[:i] + '\t\t\t%s = 0;\n' % v + s[i:]
    return s


if __name__ == '__main__':
    N = int(sys.argv[1])
    seed = int(sys.argv[2])
    fl, dead, ch = F.parse(sys.argv[3])
    p = float(sys.argv[4]) if len(sys.argv) > 4 else 0.3
    rng = random.Random(seed)
    base = A.apply(X.gen(dead, fl), ch)
    V, meta = {}, {}
    allloops = ['%s.%s' % (l, v) for l, vs in LOOPV.items() for v in vs]
    while len(V) < N:
        top = [v for v in TOP if rng.random() < p]
        rng.shuffle(top)
        lp = [v for v in allloops if rng.random() < p * 0.3]
        try:
            s = inits(base, ch, top, lp)
        except ValueError:
            continue
        n = str(len(V))
        V[n] = s
        meta[n] = (top, lp)
    rs = L.sweep(V, prefix='i%d' % seed, show=0)
    with open(L.BD + '/x5_%d.txt' % seed, 'w', newline='\n') as f:
        for n, (sc, st, fd, sd) in rs:
            f.write('%s\t%s\t%s\t%s\n' % (sc, meta[n], fd, sd))
    for n, (sc, st, fd, sd) in rs[:15]:
        print(sc, fd, sd, meta[n])
    print('errors', sum(1 for n, r in rs if r[0] >= 10**7))
