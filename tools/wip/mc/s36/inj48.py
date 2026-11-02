"""inj48.py BASE.c : T48 tuning: label before the -keys test (else-if chain wrapped), bcp goto from loop top."""
import sys, json, m, ev
sys.path.insert(0, r'..\s18'); import hsim
K = '} else if (!strnicmp(argv[i], "-keys", 5)) {'
U = 'client_usage(1, argv[i]);\n\t}'
H = '\t\tif (!strnicmp(argv[i], "help", 2)'
B = lambda v: '__builtin_constant_p(%s)' % v
P = lambda v: '(char *)%s == (char *)1' % B(v)
Q = lambda v: '%s == 3' % B(v)
W = {'p': lambda v: P(v), 'q': lambda v: Q(v), 'b': lambda v: B(v),
     'pq': lambda v: '%s && %s' % (P(v), Q(v + ' + 1')), 'pp': lambda v: '%s && %s' % (P(v), P(v + ' + 1')),
     'qq': lambda v: '%s && %s' % (Q(v), Q(v + ' + 1')),
     'ppp': lambda v: '%s && %s && %s' % (P(v), P(v + ' + 1'), P(v + ' + 2')),
     'pqq': lambda v: '%s && %s && %s' % (P(v), Q(v + ' + 1'), Q(v + ' + 2'))}
def mk(s, ws, toggles=()):
    t = s.replace(K, '} else { k48l: if (!strnicmp(argv[i], "-keys", 5)) {').replace(U, 'client_usage(1, argv[i]); }\n\t}')
    inj = ''.join('if (%s) goto k48l;\n' % W[w]('i + %d' % (10 * (n + 1))) for n, w in enumerate(ws))
    t = t.replace(H, inj + H)
    for a, b in toggles: assert a in t, a; t = t.replace(a, b)
    return t
WB = ('if (E(!strnicmp(argv[i], "-wb", 3)))', 'if (!strnicmp(argv[i], "-wb", 3))')
EB = ('if (E(!strnicmp(argv[i], "-eb", 3)))', 'if (!strnicmp(argv[i], "-eb", 3))')
BP = ('if (E(!strnicmp(argv[i], "-bp", 3)))', 'if (!strnicmp(argv[i], "-bp", 3))')
TG = {'': (), 'wb': (WB,), 'eb': (EB,), 'wbeb': (WB, EB), 'bpwb': (BP, WB), 'bpeb': (BP, EB)}
if __name__ == '__main__':
    s = open(sys.argv[1]).read()
    for tg in sys.argv[2].split(','):
        for ws in [(), ('p',), ('q',), ('b',), ('pq',), ('pp',), ('qq',), ('ppp',), ('pqq',), ('p', 'p'), ('q', 'q'), ('b', 'b')]:
            r = m.meas(mk(s, ws, TG[tg]), 'i48', fncmp=True)
            if 'err' in r: print(tg, ws, 'ERR', r['err'][-300:]); continue
            try:
                R, k = hsim.load(r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\build\v\mc29\slot_i48'); g = R[2]['g'].get(1048)
            except Exception as e: g = repr(e)
            print(tg, ws, ev.score_order(r['order'].split()[1:])[0], r['fncmp'], r['raw'][0][:75], str(g)[:200], flush=True)
