"""Attempt 4: simplify gen_ca53's match. Axes: item access x flag update x dead test's arm x whether ok doubles as sent x how
the count starts x where the locals live."""
import itertools, os
from importlib import util

here = os.path.dirname(os.path.abspath(__file__))


def load(n):
    s = util.spec_from_file_location(n, os.path.join(here, n + '.py'))
    m = util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


g, g31, g45 = load('gen_ca30'), load('gen_ca31'), load('gen_ca45')
T = g45.T
MFCALL, MFF, ARMS_OK = g31.MFCALL, g31.MFF, g31.ARMS_OK
ITEMS = {
    'inl': ({'n': 'i + 1', 'e': 'manifest.e[i].'}, '', ''),
    'ptr': ({'n': 'i + 1', 'e': 'e->'}, 'e = &manifest.e[i];\n', '\tstruct manifestItem *e;\n'),
    'cast': ({'n': 'i + 1', 'e': 'e->'}, 'e = &manifest.e[(size_t)i];\n', '\tstruct manifestItem *e;\n'),
    'u32': ({'n': 'i + 1', 'e': 'e->'}, 'e = &manifest.e[(uint32_t)i];\n', '\tstruct manifestItem *e;\n'),
    'plus': ({'n': 'i + 1', 'e': 'e->'}, 'e = manifest.e + i;\n', '\tstruct manifestItem *e;\n'),
    'k': ({'n': 'i + 1', 'e': 'manifest.e[k].'}, 'uint32_t k = i;\n', ''),
    'pk': ({'n': 'i + 1', 'e': 'e->'}, 'uint32_t k = i;\ne = &manifest.e[k];\n', '\tstruct manifestItem *e;\n'),
}
BOT = {
    'okN': 'ok = ret != 0;\nn = manifest.count;\ni += ok;\nif (!ret)\n%(f)s\n',
    'okNr': 'ok = ret != 0;\nn = manifest.count;\ni += ret != 0;\nif (!ret)\n%(f)s\n',
    'Nok': 'n = manifest.count;\nok = ret != 0;\ni += ok;\nif (!ret)\n%(f)s\n',
    'okNl': 'ok = ret != 0;\ni += ok;\nn = manifest.count;\nif (!ret)\n%(f)s\n',
    'lit': 'ok = ret != 0;\nif (!ret)\n%(f)s\nn = manifest.count;\ni += ok;\n',
}
ARM = {
    'log': '{\n' + MFF + 'goto out;\n}\n',
    'ret0': '{\nret = 0;\n' + MFF + 'goto out;\n}\n',
    'tm': '{\nnetTimerEnd();\ngoto out;\n}\n',
    'free': '{\nfreeManifest();\ngoto out;\n}\n',
}
FLAG = {'sent': ('sent', '\tint sent, n, ok;\n'), 'ok': ('ok', '\tint n, ok;\n')}
START = {
    'seq': ('i = 0;\nn = manifest.count;\nok = 1;\nfor (;;) {\n', '}\n'),
    'for': ('ok = 1;\nfor (i = 0, n = manifest.count;;) {\n', '}\n'),
    'cnt': ('n = manifest.count;\nok = 1;\nfor (i = 0;;) {\n', '}\n'),
}


def variants():
    for it, b, a, fl, st in itertools.product(ITEMS, BOT, ARM, FLAG, START):
        v, decl, d = ITEMS[it]
        x, dd = FLAG[fl]
        s = g.MFS + '\n' + x + ' = ' + MFCALL + ';\nbreak;\n'
        head = 'if (i >= n) {\n' + T + 'if (ok <= 0)\n' + ARM[a] + s + '}\n' + T
        body = decl + g.LOG % v + '\n' + g.SEND % v + '\n' + BOT[b] % {'f': g.FAIL % v}
        a0, a1 = START[st]
        after = 'if (!' + x + ') {\nret = 0;\n' + MFF + '} else {\n' + ARMS_OK + '}\n'
        src = g.PREP + g.FRAME.replace('@DECL@', dd + d).replace('@LOOP@', a0 + head + body + a1).replace('@TAIL@', after).replace('@OUT@', 'out:')
        yield '|'.join((it, b, a, fl, st)), src
