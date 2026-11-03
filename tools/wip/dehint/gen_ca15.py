"""Manifest send inside the loop, at its head (`if (i >= count) { send manifest; break; }`): MF lexically before the body with no goto."""
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
TEST = {'ge': 'i >= manifest.count', 'nlt': '!(i < manifest.count)'}
FORMS = {
    'whret': 'i = 0;\nwhile (ret) {\nif (%(t)s) {\n%(m)s\nbreak;\n}\n%(b)s\n}\n',
    'dowh': 'i = 0;\ndo {\nif (%(t)s) {\n%(m)s\nbreak;\n}\n%(b)s\n} while (ret);\n',
    'forret': 'for (i = 0; ret; ) {\nif (%(t)s) {\n%(m)s\nbreak;\n}\n%(b)s\n}\n',
    'inf': 'i = 0;\nfor (;;) {\nif (%(t)s) {\n%(m)s\nbreak;\n}\n%(b)s\nif (!ret) break;\n}\n',
    'else': 'i = 0;\nwhile (ret) {\nif (%(t)s) {\n%(m)s\nbreak;\n} else {\n%(b)s\n}\n}\n',
}
KS = {'k': ('uint32_t k = i;', 'k'), 'i': ('', 'i')}
PREP = {'h9': ('h9', 'd')}


def variants():
    prep = 'int prepSysex(void)\n{\n' + g10.HEADS['h9'] + g10.TAIL['d'] + '\n}\n'
    for f, t, (bn, b), (kn, (decl, x)) in itertools.product(FORMS, TEST, g5.INNER.items(), KS.items()):
        body = decl + g5.send(x) + b(x)
        loop = FORMS[f] % {'t': TEST[t], 'm': g5.MF, 'b': body}
        yield '%s|%s|%s|%s' % (f, t, bn, kn), prep + g5.HEAD.replace('@LOOP@', loop).replace('@TAIL@', ';')
