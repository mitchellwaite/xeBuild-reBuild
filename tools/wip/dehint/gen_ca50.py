"""Attempt 4: spellings of the manifest path's two tests in gen_ca49's td shape, which set the manifest block's frequency:
at 5 the arms' 50% rounds so the failure arm wins bbro's tie and the arms swap. Axes: tests x flag x reload x arms x item."""
import itertools, os
from importlib import util

here = os.path.dirname(os.path.abspath(__file__))


def load(n):
    s = util.spec_from_file_location(n, os.path.join(here, n + '.py'))
    m = util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


g, g45 = load('gen_ca30'), load('gen_ca45')
ITEMS, S, T, ENDS = g45.ITEMS, g45.S, g45.T, g45.ENDS
ITEMS = {k: ITEMS[k] for k in ('cast', 'k')}
S0 = S.replace('break;\n', '')
HEADS = {
    'or': 'if (i >= n) {\nif (!ret || !ok)\ngoto out;\n@S@}\n' + T,
    'ro': 'if (i >= n) {\nif (!ok || !ret)\ngoto out;\n@S@}\n' + T,
    'nest': 'if (i >= n) {\nif (ret) {\nif (!ok)\ngoto out;\n@S@}\ngoto out;\n}\n' + T,
    'and': 'if (i >= n) {\nif (ret && ok) {\n@S@}\ngoto out;\n}\n' + T,
    'dna': 'if (i >= n) {\nif (ok && ret) {\n@S@}\ngoto out;\n}\n' + T,
    'nest2': 'if (i >= n) {\nif (ok) {\nif (!ret)\ngoto out;\n@S@}\ngoto out;\n}\n' + T,
    'td': 'if (i >= n) {\n' + T + 'if (!ok)\ngoto out;\n@S@}\n' + T,
    'tdb': 'if (i >= n) {\nif (!ret)\nbreak;\nif (!ok)\nbreak;\n@S0@sent = sent;\nbreak;\n}\n' + T,
    'hd': 'if (i >= n && !ok)\ngoto out;\nif (i >= n) {\n' + T + '@S@}\n' + T,
    'ht': 'if (i >= n && !ret)\ngoto out;\nif (i >= n) {\nif (!ok)\ngoto out;\n@S@}\n' + T,
    'tt': 'if (!ret)\ngoto out;\nif (i >= n) {\nif (!ok)\ngoto out;\n@S@}\n',
}
BOT = {
    'okN': 'ok = ret != 0;\nn = manifest.count;\ni += ok;\nif (!ret)\n%(f)s\n',
    'okNr': 'ok = ret != 0;\nn = manifest.count;\ni += ret != 0;\nif (!ret)\n%(f)s\n',
}


def variants():
    for it, h, b, en in itertools.product(ITEMS, HEADS, BOT, ENDS):
        if h == 'tdb':
            continue
        v, decl, d = ITEMS[it]
        head = HEADS[h].replace('@S@', S)
        body = decl + g.LOG % v + '\n' + g.SEND % v + '\n' + BOT[b] % {'f': g.FAIL % v}
        loop = 'i = 0;\nn = manifest.count;\nok = 1;\nfor (;;) {\n' + head + body + '}\n'
        src = g.PREP + g.FRAME.replace('@DECL@', '\tint sent, n, ok;\n' + d).replace('@LOOP@', loop).replace('@TAIL@', ENDS[en]).replace('@OUT@', 'out:')
        yield '|'.join((it, h, b, en)), src
