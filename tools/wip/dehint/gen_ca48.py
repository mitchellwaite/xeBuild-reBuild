"""Attempt 4: gen_ca47 with no ret test on the manifest path: i only advances on success, so `i >= n` already means no
failure. The manifest send then has real predecessors (guard, H) and isn't merged into a thread copy at the chain's end."""
import itertools, os
from importlib import util

here = os.path.dirname(os.path.abspath(__file__))


def load(n):
    s = util.spec_from_file_location(n, os.path.join(here, n + '.py'))
    m = util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


g, g45, g47 = load('gen_ca30'), load('gen_ca45'), load('gen_ca47')
ITEMS, DEAD, S, T, ENDS, INC = g45.ITEMS, g45.DEAD, g45.S, g45.T, g45.ENDS, g47.INC
ITEMS = dict(ITEMS)
HEADS = {
    'Y': 'if (i >= n) {\n@D@@S@}\n' + T,
    'Y2': 'if (i < n) {\n' + T + '@D@} else {\n@S@}\n',
    'Y3': 'if (i < n) {\n@D@' + T + '} else {\n@S@}\n',
}
LOOPS = {
    'nb': ('n = manifest.count;\n', ''),
}


def variants():
    for it, de, inc, h, en in itertools.product(ITEMS, DEAD, INC, HEADS, ENDS):
        v, decl, d = ITEMS[it]
        dt, init, upd, dd = DEAD[de]
        head = HEADS[h].replace('@S@', S).replace('@D@', dt)
        body = decl + g.LOG % v + '\n' + g.SEND % v + '\n' + upd + INC[inc] % {'f': g.FAIL % v}
        loop = 'i = 0;\nn = manifest.count;\n' + init + 'for (;;) {\n' + head + body + '}\n'
        src = g.PREP + g.FRAME.replace('@DECL@', '\tint sent, n;\n' + d + dd).replace('@LOOP@', loop).replace('@TAIL@', ENDS[en]).replace('@OUT@', 'out:')
        yield '|'.join((it, de, inc, h, en)), src
