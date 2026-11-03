"""Attempt 3: an `ok` flag beside ret, so vrp1 can't thread the failure arm through the head (the loop stays
not-do-while, ch copies the head), with the increment before the failure log (empty latch, head not thread-copied)."""
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
    'ptr': ({'n': 'i + 1', 'e': 'e->'}, 'e = &manifest.e[i];\n', '\tstruct manifestItem *e;\n'),
    'cast': ({'n': 'i + 1', 'e': 'e->'}, 'e = &manifest.e[(size_t)i];\n', '\tstruct manifestItem *e;\n'),
    'inl': ({'n': 'i + 1', 'e': 'manifest.e[i].'}, '', ''),
}
# after the send; `ok` is what the head tests (TEST)
INC = {
    'a': 'ok = ret != 0;\ni += ok;\nif (!ret)\n%(f)s\n',
    'b': 'ok = ret != 0;\nif (ok)\ni++;\nif (!ret)\n%(f)s\n',
    'c': 'ok = ret != 0;\ni += ok;\nif (!ok)\n%(f)s\n',
    'd': 'ok = ret != 0;\nif (!ret)\n%(f)s\ni += ok;\n',
    'e': 'ok = !!ret;\ni += ok;\nif (!ret)\n%(f)s\n',
    'f': 'ok = ret != 0;\nif (!ret)\n%(f)s\nif (ok)\ni++;\n',
    'g': 'ok = ret != 0;\nif (!ok)\n%(f)s\nif (ret)\ni++;\n',
    'h': 'ok = ret != 0;\nif (!ret)\n%(f)s\ni = ok ? i + 1 : i;\n',
    'j': 'ok = ret != 0;\nif (ret)\ni++;\nif (!ret)\n%(f)s\n',
    'k': 'ok = ret != 0;\nif (ret)\ni++;\nelse\n%(f)s\n',
    'l': 'ok = ret != 0;\nif (!ok)\n%(f)s\ni += ret != 0;\n',
    'm': 'if (!ret)\n%(f)s\nok = ret != 0;\nif (ok)\ni++;\n',
}
S = g.MFS + '\nsent = ' + MFCALL + ';\nbreak;\n'
HEADS = {
    'I': 'if (i < manifest.count && ok)\ngoto send_item;\nif (!ok)\ngoto out;\n@S@send_item:\n',
    'A': 'if (i >= manifest.count) {\nif (ok)\ngoto send_manifest;\ngoto out;\n}\nif (!ok)\ngoto out;\ngoto send_item;\nsend_manifest:\n@S@send_item:\n',
    'Ar': 'if (i >= manifest.count) {\nif (ret)\ngoto send_manifest;\ngoto out;\n}\nif (!ok)\ngoto out;\ngoto send_item;\nsend_manifest:\n@S@send_item:\n',
    'E': 'if (i >= manifest.count || !ok) {\nif (!ok)\ngoto out;\n@S@}\n',
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
        loop = 'i = 0;\nok = 1;\nfor (;;) {\n' + head + body + '}\n'
        src = g.PREP + g.FRAME.replace('@DECL@', '\tint sent, ok;\n' + d).replace('@LOOP@', loop).replace('@TAIL@', ENDS[en]).replace('@OUT@', 'out:')
        yield '|'.join((it, inc, h, en)), src
