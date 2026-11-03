"""Attempt 5: `if (ret)` in the positive sense. FRE turns it into the `_40 = ret != 0` that `i += ret != 0` computes, and dom2 can't
thread a test on _40, so it does the dead test's job with nothing dead in the source. Axes: head x bottom x item x arms x helper."""
import itertools, os
from importlib import util

here = os.path.dirname(os.path.abspath(__file__))
s = util.spec_from_file_location('gen_ca64', os.path.join(here, 'gen_ca64.py'))
m64 = util.module_from_spec(s)
s.loader.exec_module(m64)
m = m64.m
g = m.g
T = 'if (!ret)\ngoto out;\n'
S = g.MFS + '\nsent = ' + m.MFCALL + ';\nbreak;\n'
HEADS = {
    # manifest path positive, in an if body: reads best
    'P1': 'if (i >= n) {\nif (ret) {\n' + S + '}\ngoto out;\n}\n' + T,
    'P1e': 'if (i >= n) {\nif (ret) {\n' + S + '} else\ngoto out;\n}\n' + T,
    'P2': 'if (i >= n) {\nif (ret) {\n' + S + '}\ngoto out;\n}\nif (ret == 0)\ngoto out;\n',
    'P3': 'if (i < n) {\n' + T + '} else {\nif (ret) {\n' + S + '}\ngoto out;\n}\n',
    'P4': 'if (i >= n) {\nif (ret != 0) {\n' + S + '}\ngoto out;\n}\n' + T,
    # item path positive too
    'P5': 'if (i >= n) {\nif (ret) {\n' + S + '}\ngoto out;\n}\nif (ret)\ngoto item;\ngoto out;\nitem:;\n',
    'P6': 'if (i < n) {\nif (ret)\ngoto item;\ngoto out;\n}\nif (ret) {\n' + S + '}\ngoto out;\nitem:;\n',
    # both tests first
    'P7': 'if (ret) {\nif (i >= n) {\n' + S + '}\n} else\ngoto out;\n',
    'P8': 'if (!ret)\ngoto out;\nif (i >= n) {\n' + S + '}\n',
    # the negative test kept on the manifest path, then a positive one: two live tests of one value
    'P9': 'if (i >= n) {\n' + T + 'if (ret) {\n' + S + '}\ngoto out;\n}\n' + T,
    'P10': 'if (i >= n && ret) {\n' + S + '}\n' + T,
    'P11': 'if (i >= n) {\nif (ret) {\n' + S + '}\nbreak2;\n}\n' + T,
}
del HEADS['P11']
BOT = dict(m.BOT)
BOT['ok'] = 'ok = ret != 0;\nn = manifest.count;\ni += ok;\nif (!ret)\n%(f)s\n'
ITEMS = {k: m.ITEMS[k] for k in ('cast', 'k', 'ptr')}
MFF, ARMS_OK = m.MFF, m.ARMS_OK
TAIL = {
    'sent': 'if (!sent) {\nret = 0;\n' + MFF + '} else {\n' + ARMS_OK + '}\n',
}
FLAT = g.FRAME


def variants():
    for it, h, b, kind in itertools.product(ITEMS, HEADS, BOT, ('flat', 'help')):
        v, decl, d = ITEMS[it]
        body = decl + g.LOG % v + '\n' + g.SEND % v + '\n' + BOT[b] % {'f': g.FAIL % v}
        loop = 'i = 0;\nn = manifest.count;\n' + ('ok = 1;\n' if b == 'ok' else '') + 'for (;;) {\n' + HEADS[h] + body + '}\n'
        if kind == 'flat':
            src = g.PREP + FLAT.replace('@DECL@', '\tint sent, n, ok;\n' + d).replace('@LOOP@', loop).replace('@TAIL@', TAIL['sent']).replace('@OUT@', 'out:')
        else:
            src = g.PREP + m64.FRAME.replace('@D@', d + '\tint ok;\n').replace('@LOOP@', loop).replace('@BODY@', m64.BODIES['a'])
        yield '|'.join((it, h, b, kind)), src
