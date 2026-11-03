"""Guard from a copied loop header: a single-exit loop gets PRED_LOOP_ITERATIONS_GUESSED, so the copied guard is ~99% (predictable_edge_p: ce1 won't speculate i = 0)."""
import itertools
from importlib import util
import os

here = os.path.dirname(os.path.abspath(__file__))


def load(n):
    s = util.spec_from_file_location(n, os.path.join(here, n + '.py'))
    m = util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


g5, g10 = load('gen_ca5'), load('gen_ca10')
FAIL = g5.fail('k')
INNER = {
    'add': 'if (!ret) ' + FAIL + '\ni += ret != 0;',
    'ifelse': 'if (ret) i++; else ' + FAIL,
    'ifnot': 'if (!ret) ' + FAIL + ' else i++;',
    'if2': 'if (!ret) ' + FAIL + '\nif (ret) i++;',
    'if2b': 'if (ret) i++;\nif (!ret) ' + FAIL,
    'addb': 'i += ret != 0;\nif (!ret) ' + FAIL,
    'plus': 'i++;\nif (!ret) ' + FAIL,
}
CONDS = {
    'and': '(i < manifest.count) & (ret != 0)',
    'and2': '(ret != 0) & (i < manifest.count)',
    'i_ret': 'i < manifest.count && ret',
    'ret_i': 'ret && i < manifest.count',
}
FORMS = {
    'wh': 'i = 0;\nwhile (%(c)s) {\n%(b)s\n}\n',
    'for': 'for (i = 0; %(c)s; ) {\n%(b)s\n}\n',
    'wret': 'ret = 1;\ni = 0;\nwhile (%(c)s) {\n%(b)s\n}\n',
}
TAILS = {'ifret': 'if (ret) {\n%s\n}' % g5.MF, 'not': 'if (!ret) ;\nelse {\n%s\n}' % g5.MF}
KS = {'u': 'uint32_t k = i;', 'n': 'int k = i;', 'p': 'const int k = i;'}


def variants():
    prep = 'int prepSysex(void)\n{\n' + g10.HEADS['h9'] + g10.TAIL['d'] + '\n}\n'
    for (bn, b), c, f, t, k in itertools.product(INNER.items(), CONDS, FORMS, TAILS, KS):
        body = KS[k] + g5.send('k') + b
        loop = FORMS[f] % {'c': CONDS[c], 'b': body}
        yield '%s|%s|%s|%s|%s' % (bn, c, f, t, k), prep + g5.HEAD.replace('@LOOP@', loop).replace('@TAIL@', TAILS[t])
