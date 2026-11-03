"""Post-loop tests that keep i live at the manifest send: `if (ret && i >= count)` and friends."""
import itertools
from importlib import util
import os

_s = util.spec_from_file_location('g5', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen_ca5.py'))
g5 = util.module_from_spec(_s)
_s.loader.exec_module(g5)

C = 'manifest.count'
T = {
    'ret_ge': 'ret && i >= ' + C,
    'ge_ret': 'i >= ' + C + ' && ret',
    'ret_eq': 'ret && i == ' + C,
    'eq_ret': 'i == ' + C + ' && ret',
    'and_ge': '(i >= ' + C + ') & (ret != 0)',
    'ge': 'i >= ' + C,
    'eq': 'i == ' + C,
}


def variants():
    for k, (bn, b), c, f, t in itertools.product(['u', 'i'], g5.INNER.items(), g5.CONDS, g5.FORMS, T):
        decl, x = g5.KS[k]
        body = decl + g5.send(x) + b(x)
        loop = g5.FORMS[f] % {'c': g5.CONDS[c], 'b': body}
        tail = 'if (%s) {\n%s\n}' % (T[t], g5.MF)
        yield '%s|%s|%s|%s|%s' % (k, bn, c, f, t), g5.PREPS['p0'] + g5.HEAD.replace('@LOOP@', loop).replace('@TAIL@', tail)
