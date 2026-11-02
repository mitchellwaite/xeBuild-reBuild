"""d31.py: s29 des.build (rok/x1/rx/t48) + loop trace-end JMP sites. python d31.py TAG 'rok=..' 'L=site:t,t/site:t' [rx=0] [t48=0]"""
import sys, json, m, ev, des, loopsites
from multiprocessing import Pool
SHOW = [129, 'k94', 107, 109, 'x1', 110, 113, 108, 119, 120, 121, 128, 116, 132, 49, 115, 112, 103, 55, 126, 125, 117, 130]
def build(rok='', x1='', L='', rx=True, t48=True):
    t = des.build(rok=rok, x1=x1, rx=rx, t48=t48)
    for s in [x for x in L.split('/') if x]:
        a, b = s.split(':'); t = loopsites.add(t, a, b.split(','))
    return t
def run(a):
    tag, kw = a
    try: r = m.meas(build(**kw), tag, fncmp=True)
    except Exception as e: return kw, None, repr(e)
    if 'err' in r: return kw, None, r['err'][-200:]
    keys = dict(x.split(':', 1) for x in r['raw'][3].split()[1:])
    return kw, (ev.score_order(r['order'].split()[1:])[0], r['fncmp']), r['order'] + '\n  ' + ' '.join('%s=%s' % (b, keys.get(str(b))) for b in SHOW)
def parse(args):
    kw = {}
    for a in args:
        k, v = a.split('=', 1); kw[k] = v if k in ('rok', 'x1', 'L') else bool(int(v))
    return kw
if __name__ == '__main__':
    # file of designs, one per line: args separated by ' | '
    lines = [l.strip() for l in open(sys.argv[1]) if l.strip() and not l.startswith('#')]
    J = [('d%s_%d' % (sys.argv[2], i), parse(l.split(' | '))) for i, l in enumerate(lines)]
    for kw, sc, o in Pool(8).map(run, J): print(kw, sc); print(' ', o)
