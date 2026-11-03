"""Attempt 5: le|J again. ch2's copy of addTitleId's load pops vrp1's freed PHIs (5, 2) and needs a version above ver's. So: extra
high-numbered names that die in vrp1/dce2, released after those PHIs. Axes: flag in the head tests x flag at the bottom x inits x item."""
import itertools, os
from importlib import util

here = os.path.dirname(os.path.abspath(__file__))


def load(n):
    s = util.spec_from_file_location(n, os.path.join(here, n + '.py'))
    m = util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


g, g31, g45 = load('gen_ca30'), load('gen_ca31'), load('gen_ca45')
MFF, ARMS_OK, MFCALL = g31.MFF, g31.ARMS_OK, g31.MFCALL
ITEMS = {'cast': g45.ITEMS['cast'], 'k': g45.ITEMS['k']}
ITEMS['more'] = ({'n': 'i + 1', 'e': 'e->'}, 'e = &manifest.e[(size_t)i];\nnum = i + 1;\n', '\tstruct manifestItem *e;\n\tint num;\n')
ITEMS['more']  = ({'n': 'num', 'e': 'e->'}, ITEMS['more'][1], ITEMS['more'][2])
TF = {'ret': 'ret', 'ok': 'ok', 'failed': '!failed', 'ok1': 'ok == 1', 'okgt': 'ok > 0'}
TM = {'ret': 'ret', 'ok': 'ok', 'failed': '!failed'}
UPD = {
    'okN': 'ok = ret != 0;\nn = manifest.count;\ni += ok;\nif (!ret)\n%(f)s\n',
    'Nok': 'n = manifest.count;\nok = ret != 0;\ni += ok;\nif (!ret)\n%(f)s\n',
    'okr': 'ok = ret != 0;\nn = manifest.count;\ni += ret != 0;\nif (!ret)\n%(f)s\n',
    'okk': 'ok = ret != 0;\nn = manifest.count;\ni += ok;\nif (!ok)\n%(f)s\n',
    'fail': 'failed = !ret;\nn = manifest.count;\ni += ret != 0;\nif (failed)\n%(f)s\n',
    'failr': 'failed = !ret;\nn = manifest.count;\ni += ret != 0;\nif (!ret)\n%(f)s\n',
    'both': 'ok = ret != 0;\nfailed = !ret;\nn = manifest.count;\ni += ok;\nif (failed)\n%(f)s\n',
    'plain': 'n = manifest.count;\ni += ret != 0;\nif (!ret)\n%(f)s\n',
}
INIT = {'ok1': 'ok = 1;\nfailed = 0;\n', 'none': ''}
HEADS = {
    'J': 'if (i < n) {\nif (%(tf)s)\ngoto item;\ngoto out;\n}\nif (!(%(tm)s))\ngoto out;\n',
    'J4': 'if (i >= n) {\nif (!(%(tm)s))\ngoto out;\n} else {\nif (%(tf)s)\ngoto item;\ngoto out;\n}\n',
}


def variants():
    for it, tf, tm, u, h in itertools.product(ITEMS, TF, TM, UPD, HEADS):
        need = TF[tf] + TM[tm] + UPD[u]
        if ('ok' in TF[tf] or 'ok' in TM[tm]) and 'ok =' not in UPD[u]:
            continue
        if ('failed' in TF[tf] or 'failed' in TM[tm]) and 'failed =' not in UPD[u]:
            continue
        v, decl, d = ITEMS[it]
        s = g.MFS + '\nsent = ' + MFCALL + ';\nbreak;\n'
        tail = 'if (!sent) {\nret = 0;\n' + MFF + '} else {\n' + ARMS_OK + '}\n'
        body = 'item:\n' + decl + g.LOG % v + '\n' + g.SEND % v + '\n' + UPD[u] % {'f': g.FAIL % v}
        if decl.startswith('uint32_t'):
            body = body.replace('item:\n', 'item:;\n')
        loop = 'i = 0;\nn = manifest.count;\n' + INIT['ok1'] + 'if (n <= 0)\ngoto send;\nfor (;;) {\n' + HEADS[h] % {'tf': TF[tf], 'tm': TM[tm]} + 'send:\n' + s + body + '}\n'
        src = g.PREP + g.FRAME.replace('@DECL@', '\tint sent, n, ok, failed;\n' + d).replace('@LOOP@', loop).replace('@TAIL@', tail).replace('@OUT@', 'out:')
        yield '|'.join((it, tf, tm, u, h)), src
