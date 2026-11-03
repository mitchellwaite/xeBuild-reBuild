"""Attempt 4: gen_ca45 with the reload ahead of the failure test, so after ch the header's predecessor is a conditional
block and H isn't merged away from its place after the guard. Axes: item x dead test x bottom x head x arms."""
import itertools, os
from importlib import util

here = os.path.dirname(os.path.abspath(__file__))


def load(n):
    s = util.spec_from_file_location(n, os.path.join(here, n + '.py'))
    m = util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


g, g45 = load('gen_ca30'), load('gen_ca45')
ITEMS, DEAD, S, T, HEADS, ENDS = g45.ITEMS, g45.DEAD, g45.S, g45.T, g45.HEADS, g45.ENDS
INC = {
    'Nadd': 'n = manifest.count;\ni += ret != 0;\nif (!ret)\n%(f)s\n',
    'aNl': 'i += ret != 0;\nn = manifest.count;\nif (!ret)\n%(f)s\n',
    'Nifel': 'n = manifest.count;\nif (ret)\ni++;\nelse\n%(f)s\n',
    'Naddl': 'n = manifest.count;\nif (!ret)\n%(f)s\ni += ret != 0;\n',
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
