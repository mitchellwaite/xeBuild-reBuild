"""Attempt 6: `for` with i++ in the step, where the failure arm's `i = n` gives the n + 1 of gen_ca81 for free. Axes: step form x body x item x decl."""
import itertools, os
from importlib import util

here = os.path.dirname(os.path.abspath(__file__))
s = util.spec_from_file_location('gen_ca80', os.path.join(here, 'gen_ca80.py'))
g = util.module_from_spec(s)
s.loader.exec_module(g)

BODY = {
    'F1': 'if (!ret) {\n%(f)s\ni = n;\n} else\nn = manifest.count;\n',
    'F2': 'if (ret)\nn = manifest.count;\nelse {\n%(f)s\ni = n;\n}\n',
    'F3': 'n = manifest.count;\nif (!ret) {\n%(f)s\ni = n;\n}\n',
    'F5': 'if (!ret) {\n%(f)s\ni = n;\ncontinue;\n}\nn = manifest.count;\n',
    'F6': 'if (!ret) {\ni = n;\n%(f)s\n} else\nn = manifest.count;\n',
    'F7': 'if (!ret) {\n%(f)s\nn = 0;\n} else\nn = manifest.count;\n',
    'F8': 'if (!ret) {\n%(f)s\nn = i;\n} else\nn = manifest.count;\n',
    'F9': 'if (!ret) {\n%(f)s\nn = i + 1;\n} else\nn = manifest.count;\n',
    'F10': 'n = ret ? manifest.count : 0;\nif (!ret)\n%(f)s\n',
}
HEADS = {
    'in': 'n = manifest.count;\nfor (i = 0; i < n; i++) {\n',
    'wh': 'i = 0;\nn = manifest.count;\nwhile (i < n) {\n@@',
}
DECL = {
    'a': '\tint i;\n\tlong ret;\n\tint n;\n',
    'b': '\tint i, n;\n\tlong ret;\n',
    'c': '\tlong ret;\n\tint i, n;\n',
}
ITEMS = {
    'cast': 'struct manifestItem *e = &manifest.e[(size_t)i];\n',
    'plain': 'struct manifestItem *e = &manifest.e[i];\n',
    'ku': 'uint32_t k = i;\nstruct manifestItem *e = &manifest.e[k];\n',
}
TAIL = 'if (ret) {\n' + g.MFS + '\n' + g.ARMS + '}\n'
OLD = '\tint i;\n\tlong ret;\n\tint n;\n'


def variants():
    for b, h, d, it in itertools.product(BODY, HEADS, DECL, ITEMS):
        body = ITEMS[it] + g.LOG + '\n' + g.SEND + '\n' + BODY[b] % {'f': g.FAIL}
        if h == 'wh':
            body += 'i++;\n'
        head = HEADS[h].replace('@@', '')
        src = g.PREP + g.FRAME.replace('@LOOP@', head + body + '}\n').replace('@TAIL@', TAIL)
        yield '|'.join((b, h, d, it)), src.replace(OLD, DECL[d])
