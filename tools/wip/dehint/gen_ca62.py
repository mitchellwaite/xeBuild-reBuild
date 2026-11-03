"""Attempt 5: gen_ca61 with one exit (goto done), so the helper has no early-return predictors and the manifest arms keep 8/8."""
import itertools, os
from importlib import util

here = os.path.dirname(os.path.abspath(__file__))
s = util.spec_from_file_location('gen_ca61', os.path.join(here, 'gen_ca61.py'))
m = util.module_from_spec(s)
s.loader.exec_module(m)
g = m.g
TAILS = {'done': m.TAIL['s2'].replace('return ret;\n', 'done:\nreturn ret;\n')}
GUARDS = dict(m.GUARD)
GUARDS['mc'] = ('i = 0;\nret = 1;\nn = manifest.count;\nif (n <= 0)\ngoto send;\n', 'send:\n')


def variants():
    for it, gd, h, b in itertools.product(m.ITEMS, GUARDS, ('J', 'J4', 'K'), m.BOT):
        v, decl, d = m.ITEMS[it]
        init, label = GUARDS[gd]
        st = g.MFS + '\nsent = ' + m.MFCALL + ';\nbreak;\n'
        hd = m.HEADS[h].replace('@O@', 'goto done;')
        body = 'item:;\n' + decl + g.LOG % v + '\n' + g.SEND % v + '\n' + m.BOT[b] % {'f': g.FAIL % v}
        loop = init + 'for (;;) {\n' + hd + label + st + body + '}\n'
        yield '|'.join((it, gd, h, b)), g.PREP + m.FRAME.replace('@D@', d).replace('@LOOP@', loop).replace('@TAIL@', TAILS['done'])
