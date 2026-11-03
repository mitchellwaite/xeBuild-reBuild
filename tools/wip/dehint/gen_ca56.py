"""Attempt 5: no second test on the manifest path. That path's only test reads a flag separate from ret, so dom2 can't
thread it (the landed dead test's job) and it reads as the path's real test. Axes: item x test on the manifest path x test
on the item path x flag update x arms x where the flag starts."""
import itertools, os
from importlib import util

here = os.path.dirname(os.path.abspath(__file__))


def load(n):
    s = util.spec_from_file_location(n, os.path.join(here, n + '.py'))
    m = util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


g, g31, g45 = load('gen_ca30'), load('gen_ca31'), load('gen_ca45')
ITEMS, S = g45.ITEMS, g45.S
MFF, ARMS_OK, MFCALL = g31.MFF, g31.ARMS_OK, g31.MFCALL
ITEMS = {k: ITEMS[k] for k in ('cast', 'k')}
TM = {
    '!ok': 'if (!ok)\ngoto out;\n',
    'le': 'if (ok <= 0)\ngoto out;\n',
    'letm': 'if (ok <= 0) {\nnetTimerEnd();\ngoto out;\n}\n',
    '!oktm': 'if (!ok) {\nnetTimerEnd();\ngoto out;\n}\n',
}
TI = {'!ret': 'if (!ret)\ngoto out;\n', '!ok': 'if (!ok)\ngoto out;\n', 'le': 'if (ok <= 0)\ngoto out;\n'}
BOT = {
    'okN': 'ok = ret != 0;\nn = manifest.count;\ni += ok;\nif (!ret)\n%(f)s\n',
    'okNr': 'ok = ret != 0;\nn = manifest.count;\ni += ret != 0;\nif (!ret)\n%(f)s\n',
    'okNk': 'ok = ret != 0;\nn = manifest.count;\ni += ok;\nif (!ok)\n%(f)s\n',
}
ENDS = {'ok': 'if (!ok) {\nret = 0;\n' + MFF + '} else {\n' + ARMS_OK + '}\n', 'sent': g45.ENDS['brk0']}


def variants():
    for it, tm, ti, b, en in itertools.product(ITEMS, TM, TI, BOT, ENDS):
        v, decl, d = ITEMS[it]
        s = S if en == 'sent' else S.replace('sent =', 'ok =')
        head = 'if (i >= n) {\n' + TM[tm] + s + '}\n' + TI[ti]
        body = decl + g.LOG % v + '\n' + g.SEND % v + '\n' + BOT[b] % {'f': g.FAIL % v}
        loop = 'i = 0;\nn = manifest.count;\nok = 1;\nfor (;;) {\n' + head + body + '}\n'
        src = g.PREP + g.FRAME.replace('@DECL@', '\tint sent, n, ok;\n' + d).replace('@LOOP@', loop).replace('@TAIL@', ENDS[en]).replace('@OUT@', 'out:')
        yield '|'.join((it, tm, ti, b, en)), src
