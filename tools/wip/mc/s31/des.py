"""des.py : design harness. python des.py TAG 'ROK=J;J' 'X1=J;J' [rx] [t48]  (J = comma list of labels)"""
import sys, json, m, ev, inj48
sys.path.insert(0, r'..\s18'); import hsim
s0 = open('best_g7b_dup.c').read()
A = 'JUMP(c12, c11, p0, i0, c9, hdd4, hdd5, c2, c1, c10, u2, cdef, c8, c7, c3, s5);'
X1 = 'JUMP(i1, p1, hdd5, hdd4, c10, c9, c1, c7, cdef);'
C4 = 'case 4:\n\t\t\t\tif (cinfo->hwFlags & 0x20)'; C5 = 'case 5:\n\t\t\t\tif (cinfo->hwFlags & 0x20)'
R117o = '{ AT(p0) clientPatches(NULL); JUMP(i0); }'
SS = '} else if (!strnicmp(argv[i], "-s", 2)) {'
def chain(spec):
    return ' '.join('JMP(%s);' % j for j in spec.split(';') if j) or ';'
def build(rok='', x1='', rx=True, t48=True, extra=()):
    t = s0.replace(C4, 'case 4:\n\t\t\t\th4t: if (cinfo->hwFlags & 0x20)').replace(C5, 'case 5:\n\t\t\t\th5t: if (cinfo->hwFlags & 0x20)')
    t = t.replace(A, chain(rok)).replace(X1, chain(x1))
    if rx:
        p = t.rindex('JUMP(efail); }'); t = t[:p] + 'JMP(efail); }' + t[p + len('JUMP(efail); }'):]
        t = t.replace(R117o, R117o.replace('JUMP(i0)', 'JMP(i0)'))
    if t48:
        t = inj48.mk(t, (), inj48.TG['wbeb'])
        assert SS in t; t = t.replace(SS, SS + ' if (%s) goto k48l;' % inj48.W['p']('i + 10'), 1)
    for a, b in extra: assert a in t, a; t = t.replace(a, b)
    return t
SHOW = [129, 94, 107, 'x1', 110, 113, 108, 119, 120, 121, 128, 116, 132, 49, 115, 112, 103, 117, 130, 126, 125, 55]
def run(tag, fn=False, **kw):
    r = m.meas(build(**kw), tag, fncmp=fn)
    if 'err' in r: return None, r['err'][-300:]
    keys = dict(x.split(':', 1) for x in r['raw'][3].split()[1:])
    sc = ev.score_order(r['order'].split()[1:])[0]
    return sc, r
if __name__ == '__main__':
    tag = sys.argv[1]; kw = {}
    for a in sys.argv[2:]:
        k, v = a.split('=', 1); kw[k] = v if k in ('rok', 'x1') else bool(int(v))
    sc, r = run(tag, True, **kw)
    if sc is None: print('ERR', r); sys.exit()
    keys = dict(x.split(':', 1) for x in r['raw'][3].split()[1:])
    print('score', sc, 'fncmp', r['fncmp']); print(r['order'])
    print(' '.join('%s=%s' % (b, keys.get(str(b))) for b in SHOW))
