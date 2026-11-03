"""Attempt 5: gen_ca56's idea again, now with one loop exit. The manifest path's only test reads ok, which dom2 can't thread (so nothing
merges the send into a thread copy and it keeps its place after the head); a failed send stops the loop with i = n, so the failure path needs
no test of its own and no `cmp` is left on it. Axes: test x update x item x arms x what the flag is."""
import itertools, os
from importlib import util

here = os.path.dirname(os.path.abspath(__file__))
s = util.spec_from_file_location('gen_ca64', os.path.join(here, 'gen_ca64.py'))
m64 = util.module_from_spec(s)
s.loader.exec_module(m64)
m = m64.m
g = m.g
MFF, ARMS_OK, MFCALL = m.MFF, m.ARMS_OK, m.MFCALL
TESTS = {'!ok': 'if (!ok)\ngoto out;\n', 'le': 'if (ok <= 0)\ngoto out;\n', '!ret': 'if (!ret)\ngoto out;\n', 'ifok': None}
UPD = {
    'okr': 'ok = ret != 0;\nn = manifest.count;\ni += ok;\nif (!ret) {\n%(f)s\ni = n;\n}\n',
    'okk': 'ok = ret != 0;\nn = manifest.count;\ni += ok;\nif (!ok) {\n%(f)s\ni = n;\n}\n',
    'okb': 'ok = ret != 0;\nn = manifest.count;\ni += ret != 0;\nif (!ret) {\n%(f)s\ni = n;\n}\n',
    'n0': 'ok = ret != 0;\nn = manifest.count;\ni += ok;\nif (!ret) {\n%(f)s\nn = 0;\n}\n',
    'Nok': 'n = manifest.count;\nok = ret != 0;\ni += ok;\nif (!ret) {\n%(f)s\ni = n;\n}\n',
    'ifel': 'ok = ret != 0;\nn = manifest.count;\nif (ret)\ni++;\nelse {\n%(f)s\ni = n;\n}\n',
    'plain': 'n = manifest.count;\ni += ret != 0;\nif (!ret) {\n%(f)s\ni = n;\n}\n',
    'early': 'ok = ret != 0;\nif (!ret) {\n%(f)s\ni = n;\n} else {\nn = manifest.count;\ni += ok;\n}\n',
}
ITEMS = {k: m.ITEMS[k] for k in ('cast', 'k', 'ptr')}
ENDS = {
    'sent': ('sent = ' + MFCALL + ';\nbreak;\n', 'if (!sent) {\nret = 0;\n' + MFF + '} else {\n' + ARMS_OK + '}\n'),
    'ok': ('ok = ' + MFCALL + ';\nbreak;\n', 'if (!ok) {\nret = 0;\n' + MFF + '} else {\n' + ARMS_OK + '}\n'),
    'ret': ('ret = ' + MFCALL + ';\nbreak;\n', 'if (!ret) {\n' + MFF + '} else {\n' + ARMS_OK + '}\n'),
}


def variants():
    for it, t, u, en in itertools.product(ITEMS, TESTS, UPD, ENDS):
        if t in ('!ok', 'le', 'ifok') and 'ok =' not in UPD[u]:
            continue
        v, decl, d = ITEMS[it]
        send, tail = ENDS[en]
        st = g.MFS + '\n' + send
        if t == 'ifok':
            head = 'if (i >= n) {\nif (ok) {\n' + st + '}\ngoto out;\n}\n'
        else:
            head = 'if (i >= n) {\n' + TESTS[t] + st + '}\n'
        body = decl + g.LOG % v + '\n' + g.SEND % v + '\n' + UPD[u] % {'f': g.FAIL % v}
        loop = 'i = 0;\nn = manifest.count;\nok = 1;\nfor (;;) {\n' + head + body + '}\n'
        src = g.PREP + g.FRAME.replace('@DECL@', '\tint sent, n, ok;\n' + d).replace('@LOOP@', loop).replace('@TAIL@', tail).replace('@OUT@', 'out:')
        yield '|'.join((it, t, u, en)), src
