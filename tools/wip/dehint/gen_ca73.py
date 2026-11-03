"""Attempt 5: gen_ca66 Q1 and Q2 (no entry goto, no helper, nothing dead, only the arms off because the send's block is 8, under bbro's 10).
`ok > 0` as the manifest path's test adds opcode positive for the send, as `<= 0` did for the dead test. Axes: head x test x update x arms x item."""
import itertools, os
from importlib import util

here = os.path.dirname(os.path.abspath(__file__))
s = util.spec_from_file_location('gen_ca68', os.path.join(here, 'gen_ca68.py'))
m68 = util.module_from_spec(s)
s.loader.exec_module(m68)
m = m68.m
g = m.g
MFF, MFCALL, ARMS_OK = m.MFF, m.MFCALL, m.ARMS_OK
S = g.MFS + '\nsent = ' + MFCALL + ';\nbreak;\n'
HEADS = {
    'A': 'if (i >= n) {\nif (@M@)\ngoto send;\ngoto out;\n}\nif (@I@)\ngoto item;\ngoto out;\nsend:\n' + S + 'item:;\n',
    'B': 'if (i >= n) {\nif (@M@)\ngoto send;\n} else if (@I@)\ngoto item;\ngoto out;\nsend:\n' + S + 'item:;\n',
    'C': 'if (i < n) {\nif (@I@)\ngoto item;\n} else if (@M@)\ngoto send;\ngoto out;\nsend:\n' + S + 'item:;\n',
}
TM = {'okgt': 'ok > 0', 'okge': 'ok >= 1', 'ok': 'ok', 'ret': 'ret'}
TI = {'ret': 'ret', 'ok': 'ok', 'okgt': 'ok > 0'}
UPD = {
    'okr': 'ok = ret != 0;\nn = manifest.count;\ni += ok;\nif (!ret)\n%(f)s\n',
    'okb': 'ok = ret != 0;\nn = manifest.count;\ni += ret != 0;\nif (!ret)\n%(f)s\n',
    'Nok': 'n = manifest.count;\nok = ret != 0;\ni += ok;\nif (!ret)\n%(f)s\n',
}
ENDS = {
    'sent': 'if (!sent) {\nret = 0;\n' + MFF + '} else {\n' + ARMS_OK + '}\n',
    'sent1': 'if (sent) {\n' + ARMS_OK + '} else {\nret = 0;\n' + MFF + '}\n',
}
ITEMS = {
    'cast': ({'n': 'i + 1', 'e': 'e->'}, 'struct manifestItem *e = &manifest.e[(size_t)i];\n'),
    'k': ({'n': 'i + 1', 'e': 'manifest.e[k].'}, 'size_t k = i;\n'),
}


def variants():
    for it, h, tm, ti, u, en in itertools.product(ITEMS, HEADS, TM, TI, UPD, ENDS):
        v, decl = ITEMS[it]
        head = HEADS[h].replace('@M@', TM[tm]).replace('@I@', TI[ti])
        body = decl + g.LOG % v + '\n' + g.SEND % v + '\n' + UPD[u] % {'f': g.FAIL % v}
        loop = 'i = 0;\nn = manifest.count;\nok = 1;\nfor (;;) {\n' + head + body + '}\n'
        src = g.PREP + g.FRAME.replace('@DECL@', '\tint sent, n, ok;\n').replace('@LOOP@', loop).replace('@TAIL@', ENDS[en]).replace('@OUT@', 'out:')
        yield '|'.join((it, h, tm, ti, u, en)), src
