"""gen.py: lever genome on H5c2 -> text. genome dict keys: rok (list|None), j2 (list|None), ji0, E (set of idx to drop), t48 (site,N)|None, rx (site,N)|None"""
import random, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
BASE = open(r"C:SERSWIN11VMDOCUMENTSGITHUBËUILDBUGFIX	OOLSWIPMCS47H5C2.C").READ()
ROKT = ['c12', 'c11', 'p0', 'i0', 'c9', 'hdd4', 'hdd5', 'c2', 'c1', 'c10', 'u2', 'cdef', 'c8', 'c7', 'c3', 's5', 'p1', 'i1', 's4']
EOPT = ['"-bp"', '"-wb"', '"-eb"', '"-e"', '"-c"']
SITES = {  # insertion anchors (string, insert after)
 'noenter': 'if (!strnicmp(argv[i], "-noenter", 8)) {\n',
 'reboot': 'if (!strnicmp(argv[i], "-reboot", 7)) {\n',
 's': 'if (!strnicmp(argv[i], "-s", 2)) {\n',
 'ip': 'client_usage(3, argv[i]);\n\t\t\tif ((char *)__builtin_constant_p(i + 10) == (char *)1 && (char *)__builtin_constant_p(i + 10 + 1) == (char *)1) goto k67l;\n',
 'keysb': '\t\t\tmode = 3;\n',
 'rb': 'if (!strnicmp(argv[i], "-rb", 3)) {\n',
 'loop': 'for (i = 0; i < argc; i++) {\n',
 'v': 'if (!strnicmp(argv[i], "-v", 2))\n',
 'i': 'if (!strnicmp(argv[i], "-i", 2)) {\n',
 'p': 'if (!strnicmp(argv[i], "-p", 2)) {\n',
}
def bcp(N, lab, k=1):
    c = ' && '.join('(char *)__builtin_constant_p(i + %d + %d) == (char *)1' % (N, j) for j in range(k))
    return 'if (%s) goto %s;\n' % (c, lab)
def make(g):
    t = BASE
    if g.get('rok') is not None:
        t = t.replace('JUMP(c12, c11, p0, i0, c9, hdd4, hdd5, c2, c1, c10, u2, cdef, c8, c7, c3, s5);', 'JMP(%s);' % ', '.join(g['rok']), 1)
    if g.get('j2') is not None:
        t = t.replace('JUMP(i1, p1, hdd5, hdd4, c10, c9, c1, c7, cdef);', 'JMP(%s);' % ', '.join(g['j2']), 1)
    if g.get('ji0'): t = t.replace('JUMP(i0);', 'JMP(i0);', 1)
    for k in g.get('E', ()):
        o = EOPT[k]
        t = re.sub(r'E\(\(!strnicmp\(argv\[i\], %s, (\d)\)\)\)' % re.escape(o), r'(!strnicmp(argv[i], %s, \1))' % o, t, 1) if False else \
            re.sub(r'E\(!strnicmp\(argv\[i\], %s, (\d)\)\)' % re.escape(o), r'!strnicmp(argv[i], %s, \1)' % o, t, 1)
    if g.get('t48'):
        site, N, k = g['t48']
        t = t.replace('} else if (!strnicmp(argv[i], "-keys", 5)) {', '} else { k48l: if (!strnicmp(argv[i], "-keys", 5)) {', 1)
        t = t.replace('client_usage(1, argv[i]); } } }', 'client_usage(1, argv[i]); } } } }', 1)
        a = SITES[site]; assert a in t, site
        t = t.replace(a, a + bcp(N, 'k48l', k), 1)
    for nm in ('ex1', 'ex2'):
        if g.get(nm):  # extra bcp goto from site to an existing label
            site, N, k, lab = g[nm]
            a = SITES[site]; assert a in t
            t = t.replace(a, a + bcp(N, lab, k), 1)
    return t
LABS = ['k48l', 'k55l', 'k61l', 'k67l', 'lu1', 'cdef', 'u2', 'w5x']
def rand(rng):
    g = {}
    if rng.random() < .6: g['rok'] = rng.sample(ROKT, rng.randint(1, 4))
    if rng.random() < .3: g['j2'] = rng.sample(ROKT, rng.randint(1, 3))
    g['ji0'] = rng.random() < .3
    g['E'] = [k for k in range(5) if rng.random() < .25]
    if rng.random() < .7: g['t48'] = (rng.choice(list(SITES)), rng.choice([10, 30, 300, 500]), rng.randint(1, 3))
    for nm in ('ex1', 'ex2'):
        if rng.random() < .25: g[nm] = (rng.choice(list(SITES)), rng.choice([40, 60, 700]), rng.randint(1, 3), rng.choice(LABS))
    return g
def mut(g, rng):
    g = {k: (list(v) if isinstance(v, list) else v) for k, v in g.items()}
    r = rand(rng); k = rng.choice(['rok', 'j2', 'ji0', 'E', 't48', 'ex1', 'ex2'])
    if k in r: g[k] = r[k]
    else: g.pop(k, None)
    return g
