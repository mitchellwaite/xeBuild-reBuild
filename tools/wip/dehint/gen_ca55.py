"""Attempt 4: fewer tests than gen_ca54's match (ret tested twice, ok once): head shapes, `while (ret)`, and which test holds the call."""
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
    'cast': ({'n': 'i + 1', 'e': 'e->'}, 'e = &manifest.e[(size_t)i];\n', '\tstruct manifestItem *e;\n'),
    'k': ({'n': 'i + 1', 'e': 'manifest.e[k].'}, 'uint32_t k = i;\n', ''),
}
TM = '{\nnetTimerEnd();\ngoto out;\n}\n'
TMB = '{\nnetTimerEnd();\nbreak;\n}\n'
S = g.MFS + '\nok = ' + MFCALL + ';\nbreak;\n'
D = 'if (ok <= 0)\n'
HEADS = {
    'base': ('for', 'if (i >= n) {\n' + T + D + TM + S + '}\n' + T),
    'tm_t2': ('for', 'if (i >= n) {\nif (!ret)\n' + TM + D + 'goto out;\n' + S + '}\n' + T),
    'tm_both': ('for', 'if (i >= n) {\nif (!ret)\n' + TM + D + TM + S + '}\n' + T),
    'tfirst': ('for', T + 'if (i >= n) {\n' + D + TM + S + '}\n'),
    'tm1': ('for', 'if (i >= n) {\nif (!ret)\n' + TM + S + '}\n' + T),
    'tm1le': ('for', 'if (i >= n) {\nif (ok <= 0 || !ret)\n' + TM + S + '}\n' + T),
    'tm1el': ('for', 'if (i >= n) {\nif (!ret || ok <= 0)\n' + TM + S + '}\n' + T),
    'eT': ('for', 'if (i < n) {\n' + T + '} else {\n' + T + D + TM + S + '}\n'),
    'whr': ('whr', 'if (i >= n) {\n' + D + TM + S + '}\n'),
    'dfirst': ('for', 'if (i >= n) {\n' + D + TM + T + S + '}\n' + T),
    'tD2': ('for', 'if (i >= n) {\n' + T + D + TM + S + '}\nif (ok <= 0)\ngoto out;\n'),
}
BOT = {
    'okN': 'ok = ret != 0;\nn = manifest.count;\ni += ok;\nif (!ret)\n%(f)s\n',
    'okNl': 'ok = ret != 0;\ni += ok;\nn = manifest.count;\nif (!ret)\n%(f)s\n',
}


def variants():
    for it, b, h in itertools.product(ITEMS, BOT, HEADS):
        v, decl, d = ITEMS[it]
        form, head = HEADS[h]
        body = decl + g.LOG % v + '\n' + g.SEND % v + '\n' + BOT[b] % {'f': g.FAIL % v}
        after = 'if (!ok) {\nret = 0;\n' + MFF + '} else {\n' + ARMS_OK + '}\n'
        if form == 'for':
            loop = 'i = 0;\nn = manifest.count;\nok = 1;\nfor (;;) {\n' + head + body + '}\n'
        else:
            loop = 'i = 0;\nn = manifest.count;\nok = 1;\nwhile (ret) {\n' + head + body + '}\n'
            after = 'if (!ret)\ngoto out;\n' + after
        src = g.PREP + g.FRAME.replace('@DECL@', '\tint n, ok;\n' + d).replace('@LOOP@', loop).replace('@TAIL@', after).replace('@OUT@', 'out:')
        yield '|'.join((it, b, h)), src
