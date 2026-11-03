"""Attempt 5: plainest spellings of the while near miss (gen_ca67 W|z5, gen_ca68): one result variable, `for` or `while`, the tail nested in
`if (ret)`. Only the hoist is expected to be left. Axes: loop x stop x tail x item."""
import itertools, os
from importlib import util

here = os.path.dirname(os.path.abspath(__file__))
s = util.spec_from_file_location('gen_ca68', os.path.join(here, 'gen_ca68.py'))
m68 = util.module_from_spec(s)
s.loader.exec_module(m68)
m = m68.m
g = m.g
MFF, MFCALL, ARMS_OK, OKLOG = m.MFF, m.MFCALL, m.ARMS_OK, m68.OKLOG
LOOPS = {
    'wh': 'i = 0;\nn = manifest.count;\nwhile (i < n) {\n@B@}\n',
    'for': 'n = manifest.count;\nfor (i = 0; i < n;) {\n@B@}\n',
}
STOP = {
    'iN': 'n = manifest.count;\ni += ret != 0;\nif (!ret) {\n%(f)s\ni = n;\n}\n',
    'Ni': 'i += ret != 0;\nn = manifest.count;\nif (!ret) {\n%(f)s\ni = n;\n}\n',
    'el': 'n = manifest.count;\ni += ret != 0;\nif (ret == 0) {\n%(f)s\ni = n;\n}\n',
}
TAILS = {
    'ifret': 'if (ret) {\n' + g.MFS + '\nif (!' + MFCALL + ') {\nret = 0;\n' + MFF + '} else {\n' + ARMS_OK + '}\n}\n',
    'ifret2': 'if (ret) {\n' + g.MFS + '\nret = ' + MFCALL + ';\nif (!ret) {\n' + MFF + '} else {\n' + ARMS_OK + '}\n}\n',
    'goto': 'if (!ret)\ngoto out;\n' + g.MFS + '\nif (!' + MFCALL + ') {\nret = 0;\n' + MFF + '} else {\n' + ARMS_OK + '}\n',
    'sent': 'if (ret) {\n' + g.MFS + '\nsent = ' + MFCALL + ';\nif (!sent) {\nret = 0;\n' + MFF + '} else {\n' + ARMS_OK + '}\n}\n',
}
ITEMS = {
    'cast': ({'n': 'i + 1', 'e': 'e->'}, 'struct manifestItem *e = &manifest.e[(size_t)i];\n'),
    'ku': ({'n': 'i + 1', 'e': 'manifest.e[k].'}, 'uint32_t k = i;\n'),
    'ks': ({'n': 'i + 1', 'e': 'manifest.e[k].'}, 'size_t k = i;\n'),
}


def variants():
    for it, l, st, t in itertools.product(ITEMS, LOOPS, STOP, TAILS):
        v, decl = ITEMS[it]
        body = decl + g.LOG % v + '\n' + g.SEND % v + '\n' + STOP[st] % {'f': g.FAIL % v}
        loop = LOOPS[l].replace('@B@', body)
        src = g.PREP + g.FRAME.replace('@DECL@', '\tint n, sent;\n').replace('@LOOP@', loop).replace('@TAIL@', TAILS[t]).replace('@OUT@', 'out:' if t == 'goto' else '')
        yield '|'.join((it, l, st, t)), src
