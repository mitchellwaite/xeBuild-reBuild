"""Attempt 5: gen_ca69's head with gen_ca68's flag: ok is the function's result and the success arm doesn't reassign it, so the manifest
send has a live PHI <1 (guard), ok (head)> at pre. The forwarders can't tail-merge, the send stays after the head, and dom3/vrp2 fold the PHI to 1
afterwards. Axes: test x update x send's arms x item x sent's type."""
import itertools, os
from importlib import util

here = os.path.dirname(os.path.abspath(__file__))
s = util.spec_from_file_location('gen_ca68', os.path.join(here, 'gen_ca68.py'))
m68 = util.module_from_spec(s)
s.loader.exec_module(m68)
m = m68.m
g = m.g
MFF, MFCALL, OKLOG = m.MFF, m.MFCALL, m68.OKLOG
UPD = {
    'okr': 'ok = ret != 0;\nn = manifest.count;\ni += ok;\nif (!ret) {\n%(f)s\ni = n;\n}\n',
    'okk': 'ok = ret != 0;\nn = manifest.count;\ni += ok;\nif (!ok) {\n%(f)s\ni = n;\n}\n',
    'okb': 'ok = ret != 0;\nn = manifest.count;\ni += ret != 0;\nif (!ret) {\n%(f)s\ni = n;\n}\n',
    'Nok': 'n = manifest.count;\nok = ret != 0;\ni += ok;\nif (!ret) {\n%(f)s\ni = n;\n}\n',
    'early': 'ok = ret != 0;\nif (!ret) {\n%(f)s\ni = n;\n} else {\nn = manifest.count;\ni += ok;\n}\n',
    'n0': 'ok = ret != 0;\nn = manifest.count;\ni += ok;\nif (!ret) {\n%(f)s\nn = 0;\n}\n',
}
HEADS = {
    'not': 'if (i >= n) {\nif (!ok)\ngoto out;\n@S@}\n',
    'ifok': 'if (i >= n) {\nif (ok) {\n@S@}\ngoto out;\n}\n',
    'and': 'if (i >= n && ok) {\n@S@}\nif (i >= n)\ngoto out;\n',
    'le': 'if (i >= n) {\nif (ok <= 0)\ngoto out;\n@S@}\n',
}
ENDS = {
    'sent': ('sent = ' + MFCALL + ';\nbreak;\n', 'if (!sent) {\nok = 0;\n' + MFF + '} else {\n' + OKLOG + '}\n'),
    'sent1': ('sent = ' + MFCALL + ';\nbreak;\n', 'if (sent) {\n' + OKLOG + '} else {\nok = 0;\n' + MFF + '}\n'),
    'ret': ('ret = ' + MFCALL + ';\nbreak;\n', 'if (!ret) {\nok = 0;\n' + MFF + '} else {\n' + OKLOG + '}\n'),
}
ITEMS = {k: m.ITEMS[k] for k in ('cast', 'k', 'ptr')}
FRAME = m68.FRAME.replace('\t\t}\n\t\tnetUnmount', '\t\t}\nout:\n\t\tnetUnmount')


def variants():
    for it, h, u, en, to in itertools.product(ITEMS, HEADS, UPD, ENDS, ('long', 'int')):
        v, decl, d = ITEMS[it]
        send, tail = ENDS[en]
        head = HEADS[h].replace('@S@', g.MFS + '\n' + send)
        body = decl + g.LOG % v + '\n' + g.SEND % v + '\n' + UPD[u] % {'f': g.FAIL % v}
        loop = 'i = 0;\nn = manifest.count;\nfor (;;) {\n' + head + body + '}\n'
        src = g.PREP + FRAME.replace('@TO@', to).replace('@TR@', 'long').replace('@D@', '\tint sent;\n' + d).replace('@LOOP@', loop).replace('@TAIL@', tail)
        yield '|'.join((it, h, u, en, to)), src
