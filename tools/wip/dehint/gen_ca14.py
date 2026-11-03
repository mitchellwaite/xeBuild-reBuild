"""F2 bodies with the manifest send lexically before the loop (goto), to get its literal first: tests whether chain order alone is what's left."""
import itertools
from importlib import util
import os

here = os.path.dirname(os.path.abspath(__file__))


def load(n):
    s = util.spec_from_file_location(n, os.path.join(here, n + '.py'))
    m = util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


g5, g7, g10 = load('gen_ca5'), load('gen_ca7'), load('gen_ca10')
LOOPS = {
    'a': 'i = 0;\nif (manifest.count > 0) goto send;\ncheck:\nif (%(t)s) {\n%(m)s\n}\ngoto done;\nsend:\ndo {\n%(b)s\n} while (%(c)s);\ngoto check;\ndone:\n',
    'b': 'i = 0;\nif (manifest.count <= 0) goto check;\ngoto send;\ncheck:\nif (%(t)s) {\n%(m)s\n}\ngoto done;\nsend:\ndo {\n%(b)s\n} while (%(c)s);\ngoto check;\ndone:\n',
    'c': 'if (manifest.count > 0) goto send;\ni = 0;\ncheck:\nif (%(t)s) {\n%(m)s\n}\ngoto done;\nsend:\ni = 0;\ndo {\n%(b)s\n} while (%(c)s);\ngoto check;\ndone:\n',
    'd': 'i = 0;\ngoto start;\ncheck:\nif (%(t)s) {\n%(m)s\n}\ngoto done;\nstart:\nif (manifest.count > 0) do {\n%(b)s\n} while (%(c)s);\ngoto check;\ndone:\n',
}
T = {k: g7.T[k] for k in ('and_ge', 'ge_ret', 'ret_ge')}
T['ret'] = 'ret'


def variants():
    for l, (bn, b), c, t, (hn, tl) in itertools.product(LOOPS, g5.INNER.items(), g5.CONDS, T, [('h9', 'd'), ('h1', 'a')]):
        body = 'uint32_t k = i;' + g5.send('k') + b('k')
        loop = LOOPS[l] % {'t': T[t], 'm': g5.MF, 'b': body, 'c': g5.CONDS[c]}
        prep = 'int prepSysex(void)\n{\n' + g10.HEADS[hn] + g10.TAIL[tl] + '\n}\n'
        yield '%s|%s|%s|%s|%s' % (l, bn, c, t, hn), prep + g5.HEAD.replace('@LOOP@', loop).replace('@TAIL@', ';')
