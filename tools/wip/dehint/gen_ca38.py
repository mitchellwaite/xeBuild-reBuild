"""Attempt 3: `while (ok)` over the manifest head, with ok a flag separate from ret. A header that is only a condition is
never do-while to ch, and vrp1 can't thread an `ok` test from a `ret` test, so the head stays and ch copies both tests."""
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
    'k': ({'n': 'i + 1', 'e': 'manifest.e[k].'}, 'uint32_t k = i;\n', ''),
}
INC = {
    'a': 'ok = ret != 0;\ni += ok;\nif (!ret)\n%(f)s\n',
    'c': 'ok = ret != 0;\ni += ok;\nif (!ok)\n%(f)s\n',
    'd': 'ok = ret != 0;\nif (!ret)\n%(f)s\ni += ok;\n',
    'l': 'ok = ret != 0;\nif (!ok)\n%(f)s\ni += ok;\n',
    'n': 'ok = ret != 0;\nif (ok)\ni++;\nelse\n%(f)s\n',
    'o': 'if (ret)\ni++;\nelse\n%(f)s\nok = ret != 0;\n',
    'p': 'i += ret != 0;\nif (!ret)\n%(f)s\nok = ret != 0;\n',
    'q': 'if (!ret)\n%(f)s\nelse\ni++;\nok = ret != 0;\n',
    'r': 'if (ret)\ni++;\nelse {\n%(f)s\nok = 0;\n}\n',
    's': 'if (!ret) {\n%(f)s\nok = 0;\n} else\ni++;\n',
    't': 'i += ret != 0;\nif (!ret) {\n%(f)s\nok = 0;\n}\n',
}
LOOPS = {
    'wh': 'i = 0;\nok = 1;\nwhile (ok) {\n%s}\n',
    'for': 'ok = 1;\nfor (i = 0; ok;) {\n%s}\n',
    'do': 'i = 0;\ndo {\n%s} while (ok);\n',
}
HEADS = {
    's': 'if (i >= manifest.count) {\n' + g.MFS + '\nsent = ' + MFCALL + ';\nbreak;\n}\n',
    'g': 'if (i >= manifest.count) {\n' + g.MFS + '\nsent = ' + MFCALL + ';\ngoto sentit;\n}\n',
}
ENDS = {
    's1': ('s', 'if (ok) {\nif (sent) {\n' + ARMS_OK + '} else {\nret = 0;\n' + MFF + '}\n}\n'),
    's0': ('s', 'if (ok) {\nif (!sent) {\nret = 0;\n' + MFF + '} else {\n' + ARMS_OK + '}\n}\n'),
    'g1': ('g', 'goto out;\nsentit:\nif (sent) {\n' + ARMS_OK + '} else {\nret = 0;\n' + MFF + '}\n'),
    'g0': ('g', 'goto out;\nsentit:\nif (!sent) {\nret = 0;\n' + MFF + '} else {\n' + ARMS_OK + '}\n'),
}


def variants():
    for it, inc, l, en in itertools.product(ITEMS, INC, LOOPS, ENDS):
        v, decl, d = ITEMS[it]
        hk, after = ENDS[en]
        f = g.FAIL % v
        body = decl + g.LOG % v + '\n' + g.SEND % v + '\n' + INC[inc] % {'f': f}
        loop = LOOPS[l] % (HEADS[hk] + body)
        src = g.PREP + g.FRAME.replace('@DECL@', '\tint sent, ok;\n' + d).replace('@LOOP@', loop).replace('@TAIL@', after).replace('@OUT@', 'out:' if hk == 'g' else '')
        yield '|'.join((it, inc, l, en)), src
