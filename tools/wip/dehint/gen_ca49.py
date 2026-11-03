"""Attempt 4: gen_ca47's best (count cached and reloaded ahead of the failure test, `ok` tested on the manifest path, which
dom3 only folds after sink). Axes: which tests the manifest path has, how i advances, flag spelling, arms, item access."""
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
ITEMS = {k: ITEMS[k] for k in ('cast', 'k', 'ptr')}
D = 'if (!ok)\ngoto out;\n'
HEADS = {
    'd': 'if (i >= n) {\n' + D + '@S@}\n' + T,
    'td': 'if (i >= n) {\n' + T + D + '@S@}\n' + T,
    'dt': 'if (i >= n) {\n' + D + T + '@S@}\n' + T,
    'dd': 'if (i >= n) {\n' + D + '@S@}\nif (!ok)\ngoto out;\n',
    'xd': 'if (i < n) {\n' + T + '} else {\n' + D + '@S@}\n',
    'xdd': 'if (i < n) {\n' + D + '} else {\n' + D + '@S@}\n',
}
BOT = {
    'okN': 'ok = ret != 0;\nn = manifest.count;\ni += ok;\nif (!ret)\n%(f)s\n',
    'okNr': 'ok = ret != 0;\nn = manifest.count;\ni += ret != 0;\nif (!ret)\n%(f)s\n',
    'Nok': 'n = manifest.count;\nok = ret != 0;\ni += ok;\nif (!ret)\n%(f)s\n',
    'iok': 'n = manifest.count;\ni += ret != 0;\nok = ret != 0;\nif (!ret)\n%(f)s\n',
    'nret': 'ok = !!ret;\nn = manifest.count;\ni += ok;\nif (!ret)\n%(f)s\n',
    'bang': 'ok = !ret;\nn = manifest.count;\ni += !ok;\nif (!ret)\n%(f)s\n',
}


def variants():
    for it, h, b, en in itertools.product(ITEMS, HEADS, BOT, ENDS):
        v, decl, d = ITEMS[it]
        head = HEADS[h].replace('@S@', S)
        init = 'ok = 1;\n'
        if b == 'bang':
            head = head.replace('!ok', 'ok')
            init = 'ok = 0;\n'
        body = decl + g.LOG % v + '\n' + g.SEND % v + '\n' + BOT[b] % {'f': g.FAIL % v}
        loop = 'i = 0;\nn = manifest.count;\n' + init + 'for (;;) {\n' + head + body + '}\n'
        src = g.PREP + g.FRAME.replace('@DECL@', '\tint sent, n, ok;\n' + d).replace('@LOOP@', loop).replace('@TAIL@', ENDS[en]).replace('@OUT@', 'out:')
        yield '|'.join((it, h, b, en)), src
