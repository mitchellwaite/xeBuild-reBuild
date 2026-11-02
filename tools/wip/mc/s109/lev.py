# lev.py: lever application on h0.c. apply(src, cfg) -> src
import re
H0 = open('h0.c').read()
WB_OLD = ' if ((char *)__builtin_constant_p(i + 60) == (char *)1 && (char *)__builtin_constant_p(i + 61) == (char *)1 && __builtin_constant_p(i + 777100)) goto wb3;'
WB3 = {'b': WB_OLD[1:], 'n': '', '2': 'if (__builtin_constant_p(i + 777100) && __builtin_constant_p(i + 778100)) goto wb3;',
       '1': 'if (__builtin_constant_p(i + 777100)) goto wb3;'}
def wb4(n):
    if n == 0: return ''
    return ' if (' + ' && '.join('__builtin_constant_p(i + %d)' % (888100 + 1000*k) for k in range(n)) + ') goto wb4;'
K_OLD = 'if ((char *)__builtin_constant_p(i + 30) == (char *)1 && (char *)__builtin_constant_p(i + 31) == (char *)1) goto k55l;'
K1 = 'if ((char *)__builtin_constant_p(i + 30) == (char *)1) goto k55l;'
E_OLD = "if (__builtin_constant_p(block+9)) goto eout_i; }"
E_NEW = " }"
C11_OLD = 'goto ndl; if (__builtin_constant_p(mode + 2400) && __builtin_constant_p(mode + 52400) && __builtin_constant_p(mode + 102400)) goto c11;'
SITES = ['AT(c1) ', 'AT(c2) ', 'AT(c3)  ', 'AT(c7)  ', 'AT(c8) ', 'AT(c9) ', 'AT(c11) ', 'AT(c12) ']
def chk(s, o):
    assert s.count(o) == 1, o[:60]
def apply(cfg):
    s = H0
    wb3, w4 = cfg.get('wb3', 'b'), cfg.get('wb4', 0)
    if wb3 != 'b' or w4:
        chk(s, WB_OLD); s = s.replace(WB_OLD, ' ' + WB3[wb3] + wb4(w4))
    if w4:
        o = 'client_usage(4, argv[i]); }'; chk(s, o); s = s.replace(o, '{ wb4: client_usage(4, argv[i]); } }')
    if cfg.get('c11', 3) != 3:
        i = s.index('fail: __attribute__((cold));'); seg = s[i:]
        o = '__builtin_constant_p(mode + 102400)) goto c11;'
        add = ''.join(' && __builtin_constant_p(mode + %d)' % (102400 + 50000*k) for k in range(1, cfg['c11'] - 2))
        seg = seg.replace(o, '__builtin_constant_p(mode + 102400)' + add + ') goto c11;', 1); s = s[:i] + seg
    if cfg.get('k', 2) == 1:
        chk(s, K_OLD); s = s.replace(K_OLD, K1)
    elif cfg.get('k', 2) == 0:
        chk(s, K_OLD); s = s.replace(K_OLD, '')
    if not cfg.get('e', 1):
        chk(s, E_OLD); s = s.replace(E_OLD, E_NEW)
    for lab, key, base in (('efail_i', 'pf', 9100), ('esucc_i', 'ps', 9200), ('eout_i', 'po', 9300), ('einv_i', 'pv', 9400)):
        site = cfg.get(key, -1)
        if site >= 0:
            n = cfg.get(key + 'n', 1)
            sa = SITES[site]; chk(s, sa)
            cond = ' && '.join('__builtin_constant_p(argc+%d)' % (base + 7*k) for k in range(n))
            s = s.replace(sa, sa + 'if (%s) goto %s; ' % (cond, lab), 1)
    return s
def name(cfg):
    return '_'.join('%s%s' % (k, v) for k, v in sorted(cfg.items()))
