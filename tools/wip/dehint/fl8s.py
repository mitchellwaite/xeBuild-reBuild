"""fl8s.py: dead tests anywhere in parseIni on top of a base drop state, with the conversion flippers that move ties A and C (fl8e).  Each test is still a trick,
so this only looks for a way to fewer tests: k tests in place of T1-T3.
  python fl8s.py one DROPS            base + one test at each site x cond x arm x flipper
  python fl8s.py two DROPS N [seed]   base + two random tests
  python fl8s.py show 'DROPS|FLIP|site:cond:arm,site:cond:arm'
Labels `DROPS|FLIP|tests`."""
import random, re, sys
import fllib as L, fl6lib as F, fl8lib as T
import fl8e as X

FLIP = ['', 'pre_u', 'gfs_u', 'pre_u+gfs_u', 'fs_fr1']
CONDS = ['off < -1', 'off < 0']
ARMS = ['*buf = 0;', '*buf = 0;\n@buf[size] = 0;', 'xb.nFirmware = 0;']
PA = "uint32_t parseIni(char *path)\n{"
PB = "\tfree(buf);\n\tlog_printf(1, \"------ ini parsing completed"
S0 = "\t/* [<console>bl<blSuffix>]"


def sites(s):
    """offsets of line starts in parseIni from the bl section on where a statement can go"""
    i, j = s.index(S0), s.index(PB)
    r = []
    prev = ''
    pos = i
    for ln in s[i:j].splitlines(True):
        st = ln.strip()
        if st and not st.startswith(('else', '/*', '*/', 'sic')) and prev.endswith((';', '{', '}')) and not st.startswith(('} else',)) or st.startswith('} else') and prev.endswith((';', '}')):
            if not prev.startswith('return') or st.startswith('}'):
                r.append(pos)
        if st and not st.startswith('/*') and not st.endswith('*/'):
            prev = st
        pos += len(ln)
    return r


def ins(s, tests):
    """tests [(site, cond, arm)] with site an index into sites(s) of the base"""
    ss = sites(s)
    for p, c, a in sorted(tests, key=lambda t: -t[0]):
        off = ss[p]
        e = s.index('\n', off)
        ln = s[off:e]
        ind = re.match(r'\t*', ln).group(0)
        if ln.strip().startswith('}'):
            ind += '\t'
        body = ARMS[a].replace('@', ind + '\t')
        s = s[:off] + "%sif (%s) {\n%s\t%s\n%s}\n" % (ind, CONDS[c], ind, body, ind) + s[off:]
    return s


def state(d, flip, tests):
    s = F.drop(T.S0, [x for x in d.split(',') if x])
    s = ins(s, tests)
    if flip:
        s = X.ALL[flip](s) if flip in X.ALL else T.E['e'][flip](s)
    return s


def parse(tt):
    return [tuple(int(x) for x in t.split(':')) for t in tt.split(',') if t]


def lab(d, fl, ts):
    return '%s|%s|%s' % (d, fl, ','.join('%d:%d:%d' % t for t in ts))


def run(V, name):
    rs = T.run(V, name, 0)
    for r in rs[:20]:
        print(r[0], r[1], r[3])
    print(len(rs))


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'one':
        d = sys.argv[2]
        n = len(sites(F.drop(T.S0, [x for x in d.split(',') if x])))
        print('sites', n)
        V = {}
        for fl in FLIP:
            for p in range(n):
                for c in range(len(CONDS)):
                    for a in range(len(ARMS)):
                        ts = [(p, c, a)]
                        V[lab(d, fl, ts)] = state(d, fl, ts)
        run(V, 'one')
    elif cmd == 'two':
        d = sys.argv[2]
        N = int(sys.argv[3])
        random.seed(int(sys.argv[4]) if len(sys.argv) > 4 else 1)
        n = len(sites(F.drop(T.S0, [x for x in d.split(',') if x])))
        V = {}
        while len(V) < N:
            ps = random.sample(range(n), 2)
            ts = [(p, random.randrange(len(CONDS)), random.randrange(len(ARMS))) for p in ps]
            fl = random.choice(FLIP)
            V[lab(d, fl, ts)] = state(d, fl, ts)
        run(V, 'two')
    else:
        d, fl, tt = sys.argv[2].split('|')
        s = state(d, fl, parse(tt))
        open(T.os.path.join(T.A8, 'show.c'), 'w', newline='\n').write(s)
        T.show(s)
