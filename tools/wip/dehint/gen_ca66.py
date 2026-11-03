"""Attempt 5: the two senses of the ret test, which FRE/dom2 treat as two values while `i += ret != 0` exists. Either the manifest path
tests `if (ret)` with the body's `if (!ret)`, or the body tests `if (ret)` and the head stays `if (!ret)`. Heads with the failing arm
in front of the manifest send. Axes: head x bottom x item x helper."""
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
    'B': 'if (i >= n) {\n' + T + S + '}\n' + T,
    'Q1': 'if (i >= n) {\nif (ret)\ngoto send;\ngoto out;\n}\nif (ret)\ngoto item;\ngoto out;\nsend:\n' + S + 'item:;\n',
    'Q2': 'if (i >= n) {\nif (ret)\ngoto send;\n} else if (ret)\ngoto item;\ngoto out;\nsend:\n' + S + 'item:;\n',
    'Q3': 'if (i >= n) {\nif (ret)\ngoto send;\ngoto out;\n}\n' + T + 'goto item;\nsend:\n' + S + 'item:;\n',
    'Q4': 'if (i < n) {\nif (ret)\ngoto item;\n} else if (ret)\ngoto send;\ngoto out;\nsend:\n' + S + 'item:;\n',
    'Q5': 'if (ret) {\nif (i >= n)\ngoto send;\ngoto item;\n}\ngoto out;\nsend:\n' + S + 'item:;\n',
    'Q6': 'if (!ret)\ngoto out;\nif (i < n)\ngoto item;\n' + S + 'item:;\n',
    'P1': 'if (i >= n) {\nif (ret) {\n' + S + '}\ngoto out;\n}\n' + T,
    'P3': 'if (i >= n) {\nif (!ret)\ngoto out;\n' + S + '} else if (ret == 0)\ngoto out;\n',
}
BOT = {
    'add': 'n = manifest.count;\ni += ret != 0;\nif (!ret)\n%(f)s\n',
    'cont': 'n = manifest.count;\ni += ret != 0;\nif (ret)\ncontinue;\n%(f)s\n',
    'elseN': 'i += ret != 0;\nif (ret)\nn = manifest.count;\nelse\n%(f)s\n',
    'Nelse': 'n = manifest.count;\ni += ret != 0;\nif (ret == 0)\n%(f)s\n',
    'ifn': 'i += ret != 0;\nn = manifest.count;\nif (ret != 0)\ncontinue;\n%(f)s\n',
    'ok': 'ok = ret != 0;\nn = manifest.count;\ni += ok;\nif (ok)\ncontinue;\n%(f)s\n',
    'ok2': 'ok = ret != 0;\nn = manifest.count;\ni += ok;\nif (!ok)\n%(f)s\n',
}
ITEMS = {k: m.ITEMS[k] for k in ('cast', 'k')}
MFF, ARMS_OK = m.MFF, m.ARMS_OK
TAIL = 'if (!sent) {\nret = 0;\n' + MFF + '} else {\n' + ARMS_OK + '}\n'


def variants():
    for it, h, b, kind in itertools.product(ITEMS, HEADS, BOT, ('flat', 'help')):
        v, decl, d = ITEMS[it]
        body = decl + g.LOG % v + '\n' + g.SEND % v + '\n' + BOT[b] % {'f': g.FAIL % v}
        loop = 'i = 0;\nn = manifest.count;\n' + ('ok = 1;\n' if b.startswith('ok') else '') + 'for (;;) {\n' + HEADS[h] + body + '}\n'
        if kind == 'flat':
            src = g.PREP + g.FRAME.replace('@DECL@', '\tint sent, n, ok;\n' + d).replace('@LOOP@', loop).replace('@TAIL@', TAIL).replace('@OUT@', 'out:')
        else:
            src = g.PREP + m64.FRAME.replace('@D@', d + '\tint ok;\n').replace('@LOOP@', loop).replace('@BODY@', m64.BODIES['a'])
        yield '|'.join((it, h, b, kind)), src
