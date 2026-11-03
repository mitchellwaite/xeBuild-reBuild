"""Attempt 4: the arms after the loop written so bbro prefers the success arm from the manifest block in round 4 (the failure
arm leaves with a goto, so the two aren't 50/50), with the success arm still lexically last, for the crossjump into `out`."""
import itertools, os
from importlib import util

here = os.path.dirname(os.path.abspath(__file__))


def load(n):
    s = util.spec_from_file_location(n, os.path.join(here, n + '.py'))
    m = util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


g, g31, g45 = load('gen_ca30'), load('gen_ca31'), load('gen_ca45')
ITEMS, S, T = g45.ITEMS, g45.S, g45.T
MFF, ARMS_OK = g31.MFF, g31.ARMS_OK
ITEMS = {k: ITEMS[k] for k in ('cast', 'k')}
HEADS = {
    'td': 'if (i >= n) {\n' + T + 'if (!ok)\ngoto out;\n@S@}\n' + T,
    'dt': 'if (i >= n) {\nif (!ok)\ngoto out;\n' + T + '@S@}\n' + T,
}
BOT = {
    'okN': 'ok = ret != 0;\nn = manifest.count;\ni += ok;\nif (!ret)\n%(f)s\n',
    'okNr': 'ok = ret != 0;\nn = manifest.count;\ni += ret != 0;\nif (!ret)\n%(f)s\n',
    'Nokr': 'n = manifest.count;\nok = ret != 0;\ni += ret != 0;\nif (!ret)\n%(f)s\n',
}
ENDS = {
    'early': 'if (!sent) {\nret = 0;\n' + MFF + 'goto out;\n}\n' + ARMS_OK,
    'early2': 'if (!sent) {\n' + MFF + 'ret = 0;\ngoto out;\n}\n' + ARMS_OK,
    'lab': 'if (sent)\ngoto sent_ok;\nret = 0;\n' + MFF + 'goto out;\nsent_ok:\n' + ARMS_OK,
    'r0': 'ret = sent;\nif (!ret) {\n' + MFF + 'goto out;\n}\n' + ARMS_OK,
    'r0b': 'ret = sent;\nif (!ret)\n' + MFF + 'else {\n' + ARMS_OK + '}\n',
    'brk0': g45.ENDS['brk0'],
}


def variants():
    for it, h, b, en in itertools.product(ITEMS, HEADS, BOT, ENDS):
        v, decl, d = ITEMS[it]
        head = HEADS[h].replace('@S@', S)
        body = decl + g.LOG % v + '\n' + g.SEND % v + '\n' + BOT[b] % {'f': g.FAIL % v}
        loop = 'i = 0;\nn = manifest.count;\nok = 1;\nfor (;;) {\n' + head + body + '}\n'
        src = g.PREP + g.FRAME.replace('@DECL@', '\tint sent, n, ok;\n' + d).replace('@LOOP@', loop).replace('@TAIL@', ENDS[en]).replace('@OUT@', 'out:')
        yield '|'.join((it, h, b, en)), src
