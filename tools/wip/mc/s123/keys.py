from rm import *
inv = {v: k for k, v in PM.items()}
pp, pg, pfirst = r4sim.load('pf/mc.bbro')
def where(pre, g, b):
    out = []
    for i, e in enumerate(pre):
        if (e[0] == 'ins' and e[2] == b) or (e[0] in ('push', 'chg') and e[1] == b): out.append(('pre%d' % i, e))
    for h in g:
        for j, e in enumerate(g[h]):
            if (e[0] == 'ins' and e[2] == b) or (e[0] in ('push', 'chg') and e[1] == b): out.append(('g%d.%d' % (h, j), e))
    return out
for b in (49, 108, 129, 122, 146, 145, 55, 62, 33, 29, 69, 147, 81, 131, 152, 35, 42, 53, 79, 75):
    print(b, 'ours', where(pre, g, b)); print('   prof', [(w, tuple(PM.get(x, x) if isinstance(x, int) and abs(x) > 1 else x for x in e)) for w, e in where(pp, pg, inv.get(b))])
