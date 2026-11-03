"""F1 family (`if (ret)` tail: manifest literal first) on the matching prepSysex."""
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
GUARD = {
    'plain': 'if (manifest.count > 0) {\ni = 0;\ndo {\n%(b)s\n} while (%(c)s);\n}\n',
    'exp': 'if (__builtin_expect(manifest.count > 0, 1)) {\ni = 0;\ndo {\n%(b)s\n} while (%(c)s);\n}\n',
    'flag': 'n = manifest.count > 0;\nif (n) {\ni = 0;\ndo {\n%(b)s\n} while (%(c)s);\n}\n',
    'flag2': 'if (manifest.count <= 0) n = 0; else n = 1;\nif (n) {\ni = 0;\ndo {\n%(b)s\n} while (%(c)s);\n}\n',
}


def variants():
    prep = 'int prepSysex(void)\n{\n' + g10.HEADS['h9'] + g10.TAIL['d'] + '\n}\n'
    for g, (bn, b), c in itertools.product(GUARD, g5.INNER.items(), g5.CONDS):
        body = 'uint32_t k = i;' + g5.send('k') + b('k')
        loop = GUARD[g] % {'c': g5.CONDS[c], 'b': body}
        tail = 'if (ret) {\n%s\n}' % g5.MF
        yield '%s|%s|%s' % (g, bn, c), prep + g5.HEAD.replace('@LOOP@', loop).replace('@TAIL@', tail).replace('\tint i;\n', '\tint i, n;\n')
