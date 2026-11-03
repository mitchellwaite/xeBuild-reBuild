"""Attempt 4: a `failed = !ret` flag for the loop head, and i += ret != 0: FRE can't unify the two (gen_ca36's
`ok = ret != 0` shared one name, so setne stayed), so dom3 folds the increment, and the head's test on `failed`
stays in gimple until RTL removes it, which keeps the failure's block in front of the manifest send."""
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
# what the flag's set by, the increment and the log, in order
INC = {
    'fil': 'failed = !ret;\ni += ret != 0;\nif (!ret)\n%(f)s\n',
    'fli': 'failed = !ret;\nif (!ret)\n%(f)s\ni += ret != 0;\n',
    'lfi': 'if (!ret)\n%(f)s\nfailed = !ret;\ni += ret != 0;\n',
    'ilf': 'i += ret != 0;\nif (!ret)\n%(f)s\nfailed = !ret;\n',
    'ifl': 'i += ret != 0;\nfailed = !ret;\nif (!ret)\n%(f)s\n',
    'lif': 'if (!ret)\n%(f)s\ni += ret != 0;\nfailed = !ret;\n',
    'fiflog': 'failed = !ret;\ni += ret != 0;\nif (failed)\n%(f)s\n',
    'f_elseinc': 'failed = !ret;\nif (ret)\ni++;\nelse\n%(f)s\n',
    'f_incif': 'failed = !ret;\nif (ret)\ni++;\nif (!ret)\n%(f)s\n',
}
S = g.MFS + '\nsent = ' + MFCALL + ';\nbreak;\n'
HEADS = {
    'E': 'if (i >= manifest.count || failed) {\nif (failed)\ngoto out;\n@S@}\n',
    'E2': 'if (failed || i >= manifest.count) {\nif (failed)\ngoto out;\n@S@}\n',
    'R': 'if (failed)\ngoto out;\nif (i >= manifest.count) {\n@S@}\n',
    'I': 'if (i < manifest.count && !failed)\ngoto send_item;\nif (failed)\ngoto out;\n@S@send_item:\n',
    'A': 'if (i >= manifest.count) {\nif (!failed)\ngoto send_manifest;\ngoto out;\n}\nif (failed)\ngoto out;\ngoto send_item;\nsend_manifest:\n@S@send_item:\n',
    'A1': 'if (i >= manifest.count) {\nif (failed)\ngoto out;\n@S@}\nif (failed)\ngoto out;\n',
}
ENDS = {
    'brk0': 'if (!sent) {\nret = 0;\n' + MFF + '} else {\n' + ARMS_OK + '}\n',
    'brk1': 'if (sent) {\n' + ARMS_OK + '} else {\nret = 0;\n' + MFF + '}\n',
}


def variants():
    for it, inc, h, en in itertools.product(ITEMS, INC, HEADS, ENDS):
        v, decl, d = ITEMS[it]
        f = g.FAIL % v
        head = HEADS[h].replace('@S@', S)
        body = decl + g.LOG % v + '\n' + g.SEND % v + '\n' + INC[inc] % {'f': f}
        loop = 'i = 0;\nfailed = 0;\nfor (;;) {\n' + head + body + '}\n'
        src = g.PREP + g.FRAME.replace('@DECL@', '\tint sent, failed;\n' + d).replace('@LOOP@', loop).replace('@TAIL@', ENDS[en]).replace('@OUT@', 'out:')
        yield '|'.join((it, inc, h, en)), src
