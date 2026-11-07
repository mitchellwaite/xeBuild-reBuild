"""Attempt 57: the static helpers (defaultBl60, loadXell, loadBl24) defined elsewhere in the file,
with static prototypes ahead of the loaders: between the loaders, after loadConsoleBlFiles, at the
end of the file, before loadBaseFile; and the three in other orders in place.
python tools/wip/dehint/bdgen/a46run.py tools/wip/dehint/bdgen/a57_order.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from a57lib import *

CON = 'int loadConsoleBlFiles(void)\n{'
PHB = 'void patchHeaderOpts(void)\n{'


def mv(where):
    def f(t):
        h, t = helpers(t)
        t = t.replace(HE, PROTO + HE, 1)
        if where == 'mid':
            t = t.replace(CON, h + CON, 1)
        elif where == 'after':
            t = t.replace(PHB, h + PHB, 1)
        elif where == 'end':
            t = t + '\n' + h
        elif where == 'top':
            t = t.replace('static int loadBaseFile(const char *name, struct fileent *e)\n{', PROTO.replace('static int loadBl24', 'static int loadBl24') + 'static int loadBaseFile(const char *name, struct fileent *e)\n{', 1)
            # put bodies after loadBaseFile
            k = t.index('\n}\n', t.index('static int loadBaseFile(const char *name, struct fileent *e)\n{')) + 3
            t = t[:k] + '\n' + h + t[k:]
        return t
    return f


def perm(order):
    def f(t):
        h, t = helpers(t)
        a = h.index('/* xell:'); b = h.index('/* case 24\'s file')
        parts = {'d': h[:a], 'x': h[a:b], 'b': h[b:]}
        nh = ''.join(parts[c] for c in order)
        if order.index('d') > order.index('b'):
            nh = 'static int defaultBl60(struct fileent *e);\n\n' + nh
        return t.replace(HE, nh + HE, 1)
    return f


V = {}
for w in ('mid', 'after', 'end', 'top'):
    V.update(cross(w, mv(w)))
for o in ('dbx', 'xdb', 'bdx', 'bxd'):
    V.update(cross(o, perm(o)))
