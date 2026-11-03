"""Attempt 6: gen_ca80's `i = n + 1` stop loses the hoist: a second latch edge alive at cddce2, whose test forwprop4 folds (n > n + 1).
Left there: n loaded ahead of the ret test (the failure arm uses it) and two SSA-numbering cmps. So: failure arm uses the old n, reload only
on success. Axes: body x declaration order x item."""
import itertools, os
from importlib import util

here = os.path.dirname(os.path.abspath(__file__))
s = util.spec_from_file_location('gen_ca80', os.path.join(here, 'gen_ca80.py'))
g = util.module_from_spec(s)
s.loader.exec_module(g)

BODY = {
    # (statements after the send)
    'S1': 'i += ret != 0;\nif (!ret) {\n%(f)s\ni = n + 1;\n} else\nn = manifest.count;\n',
    'S1b': 'i += ret != 0;\nif (ret)\nn = manifest.count;\nelse {\n%(f)s\ni = n + 1;\n}\n',
    'S2': 'if (ret) {\ni++;\nn = manifest.count;\n} else {\n%(f)s\ni = n + 1;\n}\n',
    'S2b': 'if (ret) {\nn = manifest.count;\ni++;\n} else {\n%(f)s\ni = n + 1;\n}\n',
    'S3': 'if (!ret) {\n%(f)s\ni = n + 1;\n} else {\ni++;\nn = manifest.count;\n}\n',
    'S4': 'if (!ret) {\n%(f)s\ni = n;\n} else\nn = manifest.count;\ni += ret != 0;\n',
    'S5': 'if (!ret) {\n%(f)s\ni = n + 1;\n} else\nn = manifest.count;\ni += ret != 0;\n',
    'S6': 'i += ret != 0;\nif (!ret) {\ni = n + 1;\n%(f)s\n} else\nn = manifest.count;\n',
    'S7': 'n0 = n;\nn = manifest.count;\ni += ret != 0;\nif (!ret) {\n%(f)s\ni = n0 + 1;\n}\n',
    'S8': 'i += ret != 0;\nif (!ret) {\n%(f)s\ni = n + 1;\n}\nif (ret)\nn = manifest.count;\n',
    'S9': 'i += ret != 0;\nif (!ret) {\n%(f)s\ni = n + 1;\ncontinue;\n}\nn = manifest.count;\n',
    'S10': 'if (!ret) {\n%(f)s\ni = n + 1;\ncontinue;\n}\ni++;\nn = manifest.count;\n',
    'S11': 'i += ret != 0;\nif (!ret) {\n%(f)s\ni = n + 1;\ncontinue;\n}\nn = manifest.count;\n',
    'S12': 'if (!ret) {\n%(f)s\nn = i - 1;\n} else {\ni++;\nn = manifest.count;\n}\n',
    'S13': 'if (!ret) {\n%(f)s\nn = i;\n} else {\ni++;\nn = manifest.count;\n}\n',
    'S14': 'i += ret != 0;\nif (!ret) {\n%(f)s\nn = i;\n} else\nn = manifest.count;\n',
    'S15': 'i += ret != 0;\nif (!ret) {\n%(f)s\nn = i - 1;\n} else\nn = manifest.count;\n',
}
DECL = {
    'a': '\tint i;\n\tlong ret;\n\tint n;\n',
    'b': '\tint i, n;\n\tlong ret;\n',
    'c': '\tlong ret;\n\tint i, n;\n',
    'd': '\tint n, i;\n\tlong ret;\n',
    'e': '\tlong ret;\n\tint n, i;\n',
    'f': '\tint n;\n\tlong ret;\n\tint i;\n',
}
ITEMS = {
    'cast': 'struct manifestItem *e = &manifest.e[(size_t)i];\n',
    'u32': 'struct manifestItem *e = &manifest.e[(uint32_t)i];\n',
}
HEAD = 'i = 0;\nn = manifest.count;\nwhile (i < n) {\n'
TAIL = 'if (ret) {\n' + g.MFS + '\n' + g.ARMS + '}\n'
OLD = '\tint i;\n\tlong ret;\n\tint n;\n'


def variants():
    for b, d, it in itertools.product(BODY, DECL, ITEMS):
        body = ITEMS[it] + g.LOG + '\n' + g.SEND + '\n' + BODY[b] % {'f': g.FAIL}
        src = g.PREP + g.FRAME.replace('@LOOP@', HEAD + body + '}\n').replace('@TAIL@', TAIL)
        decl = DECL[d] + ('\tint n0;\n' if b == 'S7' else '')
        yield '|'.join((b, d, it)), src.replace(OLD, decl)
