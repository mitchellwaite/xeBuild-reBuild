"""Attempt 3: partial win candidates. gen_ca33's copied head (no guard jump into the loop, no accessor), with the
block before the manifest send ending in `goto send_item` so crited1 puts the guard's forwarder there."""
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
    'u32': ({'n': 'i + 1', 'e': 'e->'}, 'e = &manifest.e[(uint32_t)i];\n', '\tstruct manifestItem *e;\n'),
    'plus': ({'n': 'i + 1', 'e': 'e->'}, 'e = manifest.e + i;\n', '\tstruct manifestItem *e;\n'),
    'num': ({'n': 'n', 'e': 'e->'}, 'e = &manifest.e[i];\nn = i + 1;\n', '\tstruct manifestItem *e;\n\tint n;\n'),
    'numb': ({'n': 'n', 'e': 'e->'}, 'n = i + 1;\ne = &manifest.e[i];\n', '\tstruct manifestItem *e;\n\tint n;\n'),
}
INC = {
    'addl': 'if (!ret)\n%(f)s\ni += ret != 0;\n',
    'add': 'i += ret != 0;\nif (!ret)\n%(f)s\n',
    'ifel': 'if (ret)\ni++;\nelse\n%(f)s\n',
    'nifel': 'if (!ret)\n%(f)s\nelse\ni++;\n',
}
S = g.MFS + '\nsent = ' + MFCALL + ';\nbreak;\n'
HEADS = {
    # no `send_manifest` label needed: T falls out of the head only through the manifest
    'E': 'if (i >= manifest.count || !ret) {\nif (ret)\ngoto send_manifest;\ngoto out;\n}\ngoto send_item;\nsend_manifest:\n@S@send_item:\n',
    'E2': 'if (i >= manifest.count || !ret) {\nif (!ret)\ngoto out;\ngoto send_manifest;\n}\ngoto send_item;\nsend_manifest:\n@S@send_item:\n',
    'A': 'if (i >= manifest.count) {\nif (ret)\ngoto send_manifest;\ngoto out;\n}\nif (!ret)\ngoto out;\ngoto send_item;\nsend_manifest:\n@S@send_item:\n',
    'A1': 'if (i >= manifest.count && ret)\ngoto send_manifest;\nif (!ret)\ngoto out;\ngoto send_item;\nsend_manifest:\n@S@send_item:\n',
    'I': 'if (i < manifest.count && ret)\ngoto send_item;\nif (!ret)\ngoto out;\n@S@send_item:\n',
    'N': 'if (i >= manifest.count) {\nif (!ret)\ngoto out;\n}\nelse if (ret)\ngoto send_item;\nelse\ngoto out;\n@S@send_item:\n',
}
ENDS = {
    'brk1': 'if (sent) {\n' + ARMS_OK + '} else {\nret = 0;\n' + MFF + '}\n',
    'brk0': 'if (!sent) {\nret = 0;\n' + MFF + '} else {\n' + ARMS_OK + '}\n',
}


def variants():
    for it, inc, h, en in itertools.product(ITEMS, INC, HEADS, ENDS):
        v, decl, d = ITEMS[it]
        f = g.FAIL % v
        head = HEADS[h].replace('@S@', S)
        body = decl + g.LOG % v + '\n' + g.SEND % v + '\n' + INC[inc] % {'f': f}
        loop = 'i = 0;\nfor (;;) {\n' + head + body + '}\n'
        src = g.PREP + g.FRAME.replace('@DECL@', '\tint sent;\n' + d).replace('@LOOP@', loop).replace('@TAIL@', ENDS[en]).replace('@OUT@', 'out:')
        yield '|'.join((it, inc, h, en)), src
