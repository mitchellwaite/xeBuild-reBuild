"""The guard-correct bodies (gen_ca7 v71, v4, v78, v413, v25) x every prepSysex spelling."""
import itertools
from importlib import util
import os

here = os.path.dirname(os.path.abspath(__file__))


def load(n):
    s = util.spec_from_file_location(n, os.path.join(here, n + '.py'))
    m = util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


g5, g6, g7 = load('gen_ca5'), load('gen_ca6'), load('gen_ca7')
BODIES = [('add', 'and', 'gd', 'ge_ret'), ('add', 'i_ret', 'wh', 'and_ge'), ('add', 'and', 'gd1', 'ge_ret'),
          ('if2', 'and', 'gd1', 'ret_ge'), ('add', 'i_ret', 'gd1', 'and_ge'), ('add', 'and', 'gd', 'and_ge')]

EXTRA = {
    'p9': 'if (!netFormatSysex())\n' + g6.FMT + '\nelse {\nif (!netMount(SYSEX, "\\\\SEP"))\n' + g6.MNT + '\nelse\nreturn createSysexDirs();\n}\nreturn 0;',
    'p10': 'int ret = 0;\nif (netFormatSysex()) {\nif (!netMount(SYSEX, "\\\\SEP"))\n' + g6.MNT + '\nelse\nret = createSysexDirs();\n} else\n' + g6.FMT + '\nreturn ret;',
    'p11': 'if (netFormatSysex()) {\nif (netMount(SYSEX, "\\\\SEP") == 0)\n' + g6.MNT + '\nelse\nreturn createSysexDirs();\n} else\n' + g6.FMT + '\nreturn 0;',
    'p12': 'if (netFormatSysex()) {\nuint32_t m = netMount(SYSEX, "\\\\SEP");\nif (m)\nreturn createSysexDirs();\n' + g6.MNT + '\n} else\n' + g6.FMT + '\nreturn 0;',
}


def variants():
    preps = dict(g6.PREPS, **EXTRA)
    for p, (bn, c, f, t) in itertools.product(preps, BODIES):
        x = 'k'
        body = 'uint32_t k = i;' + g5.send(x) + g5.INNER[bn](x)
        loop = g5.FORMS[f] % {'c': g5.CONDS[c], 'b': body}
        tail = 'if (%s) {\n%s\n}' % (g7.T[t], g5.MF)
        prep = 'int prepSysex(void)\n{\n' + preps[p] + '\n}\n'
        yield '%s|%s|%s|%s|%s' % (p, bn, c, f, t), prep + g5.HEAD.replace('@LOOP@', loop).replace('@TAIL@', tail)
