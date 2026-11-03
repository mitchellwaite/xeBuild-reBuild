"""Attempt 4: no labels but `out`. The manifest send in the else arm, so the then arm (a test that leaves for `out` or
the item body) sits in front of it with no edge to it. Axes: head x item access x increment x arms after the loop."""
import itertools, os
from importlib import util

here = os.path.dirname(os.path.abspath(__file__))


def load(n):
    s = util.spec_from_file_location(n, os.path.join(here, n + '.py'))
    m = util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


g, g31 = load('gen_ca30'), load('gen_ca31')
MFCALL, MFF, ARMS_OK = g31.MFCALL, g31.MFF, g31.ARMS_OK
ITEMS = {
    'inl': ({'n': 'i + 1', 'e': 'manifest.e[i].'}, '', ''),
    'ptr': ({'n': 'i + 1', 'e': 'e->'}, 'e = &manifest.e[i];\n', '\tstruct manifestItem *e;\n'),
    'cast': ({'n': 'i + 1', 'e': 'e->'}, 'e = &manifest.e[(size_t)i];\n', '\tstruct manifestItem *e;\n'),
    'k': ({'n': 'i + 1', 'e': 'manifest.e[k].'}, 'uint32_t k = i;\n', ''),
}
INC = {
    'add': 'i += ret != 0;\nif (!ret)\n%(f)s\n',
    'addl': 'if (!ret)\n%(f)s\ni += ret != 0;\n',
    'ifel': 'if (ret)\ni++;\nelse\n%(f)s\n',
    'nifel': 'if (!ret)\n%(f)s\nelse\ni++;\n',
}
S = g.MFS + '\nsent = ' + MFCALL + ';\nbreak;\n'
HEADS = {
    'NE': 'if (i < manifest.count || !ret) {\nif (!ret)\ngoto out;\n} else {\n@S@}\n',
    'NE2': 'if (!ret || i < manifest.count) {\nif (!ret)\ngoto out;\n} else {\n@S@}\n',
    'NR': 'if (!ret)\ngoto out;\nif (i >= manifest.count) {\n@S@}\n',
    'NN': 'if (i < manifest.count) {\nif (!ret)\ngoto out;\n} else if (ret) {\n@S@} else\ngoto out;\n',
    'NF': 'if (i < manifest.count && !ret)\ngoto out;\nif (i >= manifest.count) {\nif (!ret)\ngoto out;\n@S@}\n',
}
LOOPS = {
    'for': 'i = 0;\nfor (;;) {\n%s}\n',
    'whr': 'i = 0;\nwhile (ret) {\n%s}\n',
}
ENDS = {
    'brk0': 'if (!sent) {\nret = 0;\n' + MFF + '} else {\n' + ARMS_OK + '}\n',
    'brk1': 'if (sent) {\n' + ARMS_OK + '} else {\nret = 0;\n' + MFF + '}\n',
}


def variants():
    for it, inc, h, en in itertools.product(ITEMS, INC, HEADS, ENDS):
        v, decl, d = ITEMS[it]
        head = HEADS[h].replace('@S@', S)
        body = decl + g.LOG % v + '\n' + g.SEND % v + '\n' + INC[inc] % {'f': g.FAIL % v}
        loop = LOOPS['for'] % (head + body)
        src = g.PREP + g.FRAME.replace('@DECL@', '\tint sent;\n' + d).replace('@LOOP@', loop).replace('@TAIL@', ENDS[en]).replace('@OUT@', 'out:')
        yield '|'.join((it, inc, h, en)), src
