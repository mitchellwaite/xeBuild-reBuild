"""Attempt 5: one loop exit. A failed send stops the loop by clearing the count (or jumping i to it), so the head is the only exit: loop
exit heuristics give it 9%, not 4.5%, and the manifest block's frequency doubles past bbro's 10 with no dead arm. Axes: head x bottom x item x helper."""
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
    'B': 'if (i >= n) {\n' + T + S + '}\n',
    'P': 'if (i >= n) {\nif (ret) {\n' + S + '}\ngoto out;\n}\n',
    'Q': 'if (i >= n) {\nif (ret)\ngoto send;\ngoto out;\n}\ngoto item;\nsend:\n' + S + 'item:;\n',
    'W': None,
    'WW': None,
}
BOT = {
    'z1': 'n = manifest.count;\ni += ret != 0;\nif (!ret) {\n%(f)s\nn = 0;\n}\n',
    'z2': 'i += ret != 0;\nif (ret)\nn = manifest.count;\nelse {\n%(f)s\nn = 0;\n}\n',
    'z3': 'if (ret) {\ni++;\nn = manifest.count;\n} else {\n%(f)s\nn = 0;\n}\n',
    'z4': 'n = manifest.count;\nif (ret)\ni++;\nelse {\n%(f)s\nn = 0;\n}\n',
    'z5': 'n = manifest.count;\ni += ret != 0;\nif (!ret) {\n%(f)s\ni = n;\n}\n',
    'z6': 'if (ret) {\ni++;\nn = manifest.count;\n} else {\n%(f)s\ni = n;\n}\n',
    'z7': 'n = manifest.count;\nif (ret)\ni++;\nelse {\n%(f)s\ni = n;\n}\n',
    'z8': 'n = ret ? manifest.count : 0;\ni += ret != 0;\nif (!ret)\n%(f)s\n',
    'z9': 'if (!ret) {\n%(f)s\nn = 0;\n} else\nn = manifest.count;\ni += ret != 0;\n',
}
ITEMS = {k: m.ITEMS[k] for k in ('cast', 'k', 'ptr')}
ITEMS['inl'] = m.g45.ITEMS['inl']
MFF, ARMS_OK = m.MFF, m.ARMS_OK
TAIL = 'if (!sent) {\nret = 0;\n' + MFF + '} else {\n' + ARMS_OK + '}\n'
ARM = 'if (!' + m.MFCALL + ') {\nret = 0;\n' + MFF + '} else {\n' + ARMS_OK + '}\n'


def variants():
    for it, h, b, kind in itertools.product(ITEMS, HEADS, BOT, ('flat', 'help')):
        v, decl, d = ITEMS[it]
        body = decl + g.LOG % v + '\n' + g.SEND % v + '\n' + BOT[b] % {'f': g.FAIL % v}
        if h == 'W':
            loop = 'i = 0;\nn = manifest.count;\nwhile (i < n) {\n' + body + '}\n' + T + g.MFS + '\nsent = ' + m.MFCALL + ';\n'
        elif h == 'WW':
            loop = 'i = 0;\nn = manifest.count;\nwhile (i < n) {\n' + body + '}\nif (!ret)\ngoto out;\n' + g.MFS + '\nsent = ' + m.MFCALL + ';\n'
            if b not in ('z1', 'z2'):
                continue
            body = body.replace('n = 0;', 'n = 0;')
        else:
            loop = 'i = 0;\nn = manifest.count;\nfor (;;) {\n' + HEADS[h] + body + '}\n'
        if kind == 'flat':
            src = g.PREP + g.FRAME.replace('@DECL@', '\tint sent, n, ok;\n' + d).replace('@LOOP@', loop).replace('@TAIL@', TAIL).replace('@OUT@', 'out:')
        else:
            src = g.PREP + m64.FRAME.replace('@D@', d + '\tint ok;\n').replace('@LOOP@', loop).replace('@BODY@', m64.BODIES['a'])
        yield '|'.join((it, h, b, kind)), src
