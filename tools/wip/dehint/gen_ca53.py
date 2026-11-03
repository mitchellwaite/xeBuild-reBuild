"""Attempt 4: the manifest block must reach 10 (bbro round 3) from 5: a call in the dead test's then arm cancels the call
heuristic against the manifest send. Axes: then arm of the ret test and of the ok test, the ok test's spelling, arms, item."""
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
ARM = {
    'go': 'goto out;\n',
    'log': '{\n' + MFF + 'goto out;\n}\n',
    'ret0': '{\nret = 0;\n' + MFF + 'goto out;\n}\n',
    'tm': '{\nnetTimerEnd();\ngoto out;\n}\n',
}
TEST = {'!': '!ok', 'le': 'ok <= 0'}
BOT = {
    'okN': 'ok = ret != 0;\nn = manifest.count;\ni += ok;\nif (!ret)\n%(f)s\n',
    'okNr': 'ok = ret != 0;\nn = manifest.count;\ni += ret != 0;\nif (!ret)\n%(f)s\n',
}
ENDS = {'brk0': g45.ENDS['brk0'], 'lab': 'if (sent)\ngoto sent_ok;\nret = 0;\n' + MFF + 'goto out;\nsent_ok:\n' + ARMS_OK}


def variants():
    for it, a1, a2, te, b, en in itertools.product(ITEMS, ARM, ARM, TEST, BOT, ENDS):
        v, decl, d = ITEMS[it]
        head = 'if (i >= n) {\nif (!ret)\n' + ARM[a1] + 'if (' + TEST[te] + ')\n' + ARM[a2] + S + '}\n' + T
        body = decl + g.LOG % v + '\n' + g.SEND % v + '\n' + BOT[b] % {'f': g.FAIL % v}
        loop = 'i = 0;\nn = manifest.count;\nok = 1;\nfor (;;) {\n' + head + body + '}\n'
        src = g.PREP + g.FRAME.replace('@DECL@', '\tint sent, n, ok;\n' + d).replace('@LOOP@', loop).replace('@TAIL@', ENDS[en]).replace('@OUT@', 'out:')
        yield '|'.join((it, a1, a2, te, b, en)), src
