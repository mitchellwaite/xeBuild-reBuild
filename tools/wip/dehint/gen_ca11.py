"""Matching prepSysex spellings x loop bodies, looking for the addTitleId cmp order (SSA numbering) and the most natural spelling."""
import itertools
from importlib import util
import os

here = os.path.dirname(os.path.abspath(__file__))


def load(n):
    s = util.spec_from_file_location(n, os.path.join(here, n + '.py'))
    m = util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


g5, g6, g7, g10 = load('gen_ca5'), load('gen_ca6'), load('gen_ca7'), load('gen_ca10')
HEADS = ['h1', 'h5', 'h9']
TAILS = ['a', 'd']
KV = {
    'u': ('uint32_t k = i;', 'int i;'),
    'U': ('k = i;', 'int i; uint32_t k;'),
}
T = dict(g7.T)
T.pop('ge')
T.pop('eq')


def variants():
    for h, tl, (bn, b), c, f, t, kv in itertools.product(HEADS, TAILS, g5.INNER.items(), g5.CONDS, g5.FORMS, T, KV):
        body = KV[kv][0] + g5.send('k') + b('k')
        loop = g5.FORMS[f] % {'c': g5.CONDS[c], 'b': body}
        tail = 'if (%s) {\n%s\n}' % (T[t], g5.MF)
        prep = 'int prepSysex(void)\n{\n' + g10.HEADS[h] + g10.TAIL[tl] + '\n}\n'
        src = prep + g5.HEAD.replace('@LOOP@', loop).replace('@TAIL@', tail).replace('\tint i;\n', '\t' + KV[kv][1] + '\n')
        yield '%s%s|%s|%s|%s|%s|%s' % (h, tl, bn, c, f, t, kv), src
