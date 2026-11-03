"""Attempt 3: loop head with `i >= count` and `ret` both, manifest head between them, for loops ch can copy.
Wanted: fail arm's thread out of the loop only after ch, so the old header keeps a conditional predecessor."""
import itertools, os
from importlib import util

here = os.path.dirname(os.path.abspath(__file__))


def load(n):
    s = util.spec_from_file_location(n, os.path.join(here, n + '.py'))
    m = util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


g, g31 = load('gen_ca30'), load('gen_ca31')
V, P = g31.V, g31.P
MFCALL, MFF, ARMS_OK = g31.MFCALL, g31.MFF, g31.ARMS_OK
ITEMS = {
    'inl': (V, ''),
    'ptr': (P, 'struct manifestItem *e = &manifest.e[i];\n'),
}
INC = {
    'ifel': 'if (ret)\ni++;\nelse\n%(f)s\n',
    'nifel': 'if (!ret)\n%(f)s\nelse\ni++;\n',
    'add': 'i += ret != 0;\nif (!ret)\n%(f)s\n',
    'addl': 'if (!ret)\n%(f)s\ni += ret != 0;\n',
    'ifif': 'if (ret)\ni++;\nif (!ret)\n%(f)s\n',
    'ififr': 'if (!ret)\n%(f)s\nif (ret)\ni++;\n',
}
SEND = g.MFS + '\nsent = ' + MFCALL + ';\n'
HEADS = {
    # %(l)s leaves after the manifest send
    'A': 'if (i >= manifest.count) {\nif (!ret)\ngoto out;\n' + '@S@' + '%(l)s}\nif (!ret)\ngoto out;\n',
    'A2': 'if (i >= manifest.count) {\nif (ret) {\n' + '@S@' + '%(l)s}\ngoto out;\n}\nif (!ret)\ngoto out;\n',
    'B': 'if (i >= manifest.count && ret) {\n' + '@S@' + '%(l)s}\nif (!ret)\ngoto out;\n',
    'R': 'if (!ret)\ngoto out;\nif (i >= manifest.count) {\n' + '@S@' + '%(l)s}\n',
    'E': 'if (i >= manifest.count || !ret) {\nif (!ret)\ngoto out;\n' + '@S@' + '%(l)s}\n',
    'E2': 'if (!ret || i >= manifest.count) {\nif (!ret)\ngoto out;\n' + '@S@' + '%(l)s}\n',
}
LOOPS = {
    'for': 'i = 0;\nfor (;;) {\n%s}\n',
    'whr': 'i = 0;\nwhile (ret) {\n%s}\n',
}
ENDS = {
    'brk1': ('break;\n', 'if (sent) {\n' + ARMS_OK + '} else {\nret = 0;\n' + MFF + '}\n'),
    'brk0': ('break;\n', 'if (!sent) {\nret = 0;\n' + MFF + '} else {\n' + ARMS_OK + '}\n'),
}


def variants():
    for it, inc, h, l, en in itertools.product(ITEMS, INC, HEADS, LOOPS, ENDS):
        v, decl = ITEMS[it]
        leave, after = ENDS[en]
        head = HEADS[h].replace('@S@', SEND.replace('%', '%%')) % {'l': leave}
        body = decl + g.LOG % v + '\n' + g.SEND % v + '\n' + INC[inc] % {'f': g.FAIL % v}
        loop = LOOPS[l] % (head + body)
        if l == 'whr':
            after = 'if (ret) {\n' + after + '}\n'
        src = g.PREP + g.FRAME.replace('@DECL@', '\tint sent;\n').replace('@LOOP@', loop).replace('@TAIL@', after).replace('@OUT@', 'out:')
        yield '|'.join((it, inc, h, l, en)), src
