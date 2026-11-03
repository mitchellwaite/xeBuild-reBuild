"""Attempt 3: gen_ca33's E head, with the item failure's log between the `ret` test and the manifest send.
That block has no edge to the manifest send, so crited1 puts the guard's forwarder in front of it (split_edge_bb_loc)."""
import itertools, os
from importlib import util

here = os.path.dirname(os.path.abspath(__file__))


def load(n):
    s = util.spec_from_file_location(n, os.path.join(here, n + '.py'))
    m = util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


g, g31 = load('gen_ca30'), load('gen_ca31')
V, P = g31.V, g31.P
MFCALL, MFF, ARMS_OK = g31.MFCALL, g31.MFF, g31.ARMS_OK
ITEMS = {
    'inl': (V, '', ''),
    'ptrf': (P, 'e = &manifest.e[i];\n', '\tstruct manifestItem *e;\n'),
    'ptrc': (P, 'e = &manifest.e[(size_t)i];\n', '\tstruct manifestItem *e;\n'),
    'ptrl': (P, 'struct manifestItem *e = &manifest.e[i];\n', ''),
    'k': ({'n': 'i + 1', 'e': 'manifest.e[k].'}, 'uint32_t k = i;\n', ''),
}
INC = {
    'add': 'i += ret != 0;\n',
    'if': 'if (ret)\ni++;\n',
}
SEND = g.MFS + '\nsent = ' + MFCALL + ';\n'
HEADS = {
    'E': 'if (i >= manifest.count || !ret) {\nif (!ret) {\n@F@\ngoto out;\n}\n@S@%(l)s}\n',
    'E2': 'if (!ret || i >= manifest.count) {\nif (!ret) {\n@F@\ngoto out;\n}\n@S@%(l)s}\n',
    'R': 'if (!ret) {\n@F@\ngoto out;\n}\nif (i >= manifest.count) {\n@S@%(l)s}\n',
}
LOOPS = {
    'for': 'i = 0;\nfor (;;) {\n%s}\n',
    'fori': 'for (i = 0;;) {\n%s}\n',
}
ENDS = {
    'brk1': ('break;\n', 'if (sent) {\n' + ARMS_OK + '} else {\nret = 0;\n' + MFF + '}\n'),
    'brk0': ('break;\n', 'if (!sent) {\nret = 0;\n' + MFF + '} else {\n' + ARMS_OK + '}\n'),
}


def variants():
    for it, inc, h, l, en in itertools.product(ITEMS, INC, HEADS, LOOPS, ENDS):
        v, decl, d = ITEMS[it]
        leave, after = ENDS[en]
        if it in ('ptrl', 'k'):
            # scoped index or pointer: the failure log at the head can't use it
            f = g.FAIL % V
        else:
            f = g.FAIL % v
        head = HEADS[h].replace('@S@', SEND.replace('%', '%%')).replace('@F@', f.replace('%', '%%')) % {'l': leave}
        body = decl + g.LOG % v + '\n' + g.SEND % v + '\n' + INC[inc]
        loop = LOOPS[l] % (head + body)
        src = g.PREP + g.FRAME.replace('@DECL@', '\tint sent;\n' + d).replace('@LOOP@', loop).replace('@TAIL@', after).replace('@OUT@', 'out:')
        yield '|'.join((it, inc, h, l, en)), src
