"""ebl.py: bcp-only (no asm goto) dead-edge sources inside the clientEraseBlockI copy.
ebinj(text, [(src, w, tgt, n)]) ; src in SRC order, tgt forward label."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import inj48
W = dict(inj48.W)
W['qqq'] = lambda v: ' && '.join('__builtin_constant_p(%s) == 3' % (v + ' + %d' % k) for k in range(3))
W['pppp'] = lambda v: ' && '.join('(char *)__builtin_constant_p(%s) == (char *)1' % (v + ' + %d' % k) for k in range(4))
W['qp'] = lambda v: '__builtin_constant_p(%s) == 3 && (char *)__builtin_constant_p(%s + 1) == (char *)1' % (v, v)
W['bb'] = lambda v: '__builtin_constant_p(%s) && __builtin_constant_p(%s + 1)' % (v, v)
N = chr(92) + 'n'
ORDER = ['T', 'A', 'B', 'eerase', 'S', 'esucc', 'F', 'efail', 'E', 'eout', 'I', 'einv']
SRCS = ['T', 'A', 'B', 'S', 'F', 'E', 'I']
LABS = ['eerase', 'esucc', 'efail', 'eout', 'einv']
def fwd(src): i = ORDER.index(src); return [l for l in ORDER[i + 1:] if l in LABS and not (src == 'E' and l == 'eout') and not (src == 'I')]
def ebinj(t, items):
    s = t.index('static void clientEraseBlockI('); e = t.index('/* the option', s); c = t[s:e]
    by = {}
    for src, w, tgt, n in items: by.setdefault(src, []).append('if (%s) goto %s;\n' % (W[w]('block + %d' % n), tgt))
    def S(k): return ''.join(by.get(k, []))
    a = 'uint32_t block = myatoh32(sblock, -1);'; c = c.replace(a, a + S('T'), 1)
    a = 'if (block != -1) {'; c = c.replace(a, a + S('A'), 1)
    a = 'if (block < cinfo->nandSize / cinfo->blockSize) {'; c = c.replace(a, a + S('B'), 1)
    a = 'esucc: log_printf(0, "Success!' + N + '");'
    if 'S' in by: assert a in c; c = c.replace(a, '{ ' + S('S') + a + ' }', 1)
    a = '{ AT(efail) '; 
    if 'F' in by: assert a in c; c = c.replace(a, '{ ' + S('F') + 'AT(efail) ', 1)
    a = '{ eout: '
    if 'E' in by: assert a in c; c = c.replace(a, '{ ' + S('E') + 'eout: ', 1)
    return t[:s] + c + t[e:]
