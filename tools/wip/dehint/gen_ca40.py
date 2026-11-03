"""Attempt 4: a block with real statements and no edge to the manifest send, in front of it, in the copied-head
shapes. Z is either the shared cleanup written out (tail merge or crossjump folds it into `out`) or a dead test."""
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
    'inl': (V, '', ''),
    'cast': (P, 'e = &manifest.e[(size_t)i];\n', '\tstruct manifestItem *e;\n'),
    'ptr': (P, 'e = &manifest.e[i];\n', '\tstruct manifestItem *e;\n'),
    'k': ({'n': 'i + 1', 'e': 'manifest.e[k].'}, 'uint32_t k = i;\n', ''),
}
INC = {
    'add': 'i += ret != 0;\nif (!ret)\n%(f)s\n',
    'addl': 'if (!ret)\n%(f)s\ni += ret != 0;\n',
    'ifel': 'if (ret)\ni++;\nelse\n%(f)s\n',
    'nifel': 'if (!ret)\n%(f)s\nelse\ni++;\n',
}
CL = 'netUnmount(SYSEX);\nfreeManifest();\n'
Z = {
    'T': 'if (!ret)\ngoto out;\n',
    'cl0': 'if (!ret) {\n' + CL + 'return 0;\n}\n',
    'clr': 'if (!ret) {\n' + CL + 'return ret;\n}\n',
    'ncl0': 'if (ret) {\n@S@} else {\n' + CL + 'return 0;\n}\n',
}
HEADS = {
    'E': 'if (i >= manifest.count || !ret) {\n@Z@@S@}\n',
    'E2': 'if (!ret || i >= manifest.count) {\n@Z@@S@}\n',
    'A': 'if (i >= manifest.count) {\n@Z@@S@}\nif (!ret)\ngoto out;\n',
    'I': 'if (i < manifest.count && ret)\ngoto send_item;\n@Z@@S@send_item:\n',
}
S = g.MFS + '\nsent = ' + MFCALL + ';\nbreak;\n'
AFTER = 'if (!sent) {\nret = 0;\n' + MFF + '} else {\n' + ARMS_OK + '}\n'


def variants():
    for it, inc, h, z in itertools.product(ITEMS, INC, HEADS, Z):
        v, decl, d = ITEMS[it]
        zz = Z[z]
        head = HEADS[h]
        if '@S@' in zz:
            head = head.replace('@Z@@S@', zz)
        else:
            head = head.replace('@Z@', zz)
        head = head.replace('@S@', S)
        body = decl + g.LOG % v + '\n' + g.SEND % v + '\n' + INC[inc] % {'f': g.FAIL % v}
        loop = 'i = 0;\nfor (;;) {\n' + head + body + '}\n'
        src = g.PREP + g.FRAME.replace('@DECL@', '\tint sent;\n' + d).replace('@LOOP@', loop).replace('@TAIL@', AFTER).replace('@OUT@', 'out:')
        yield '|'.join((it, inc, h, z)), src
