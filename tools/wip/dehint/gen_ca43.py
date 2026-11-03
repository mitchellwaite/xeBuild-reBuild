"""Attempt 4: no labels but `out`: `if (i < count) {T; D} else {T2; manifest; break;}`, D being a dead test, either on a
flag that dom3 can only fold after sinking, or anything VRP knows. D's `continue` gives the latch two predecessors at ch
(so the head is copied, with an empty join), and D's own block has no edge to the manifest send (split_edge_bb_loc)."""
import itertools, os
from importlib import util

here = os.path.dirname(os.path.abspath(__file__))


def load(n):
    s = util.spec_from_file_location(n, os.path.join(here, n + '.py'))
    m = util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


g, g31 = load('gen_ca30'), load('gen_ca31')
MFCALL, MFF, ARMS_OK = g31.MFCALL, g31.MFF, g31.ARMS_OK
ITEMS = {
    'inl': ({'n': 'i + 1', 'e': 'manifest.e[i].'}, '', ''),
    'cast': ({'n': 'i + 1', 'e': 'e->'}, 'e = &manifest.e[(size_t)i];\n', '\tstruct manifestItem *e;\n'),
    'ptr': ({'n': 'i + 1', 'e': 'e->'}, 'e = &manifest.e[i];\n', '\tstruct manifestItem *e;\n'),
    'k': ({'n': 'i + 1', 'e': 'manifest.e[k].'}, 'uint32_t k = i;\n', ''),
}
# flag: D's test; inc: flag update + increment + log
DEAD = {
    'ok': ('!ok', 'ok = 1;\n', 'ok = ret != 0;\ni += ok;\nif (!ret)\n%(f)s\n', '\tint ok;\n'),
    'ok2': ('!ok', 'ok = 1;\n', 'ok = ret != 0;\ni += ret != 0;\nif (!ret)\n%(f)s\n', '\tint ok;\n'),
    'okl': ('!ok', 'ok = 1;\n', 'ok = !!ret;\nif (!ret)\n%(f)s\ni += ok;\n', '\tint ok;\n'),
    'fail': ('failed', 'failed = 0;\n', 'failed = !ret;\ni += ret != 0;\nif (!ret)\n%(f)s\n', '\tint failed;\n'),
    'i0': ('i < 0', '', 'i += ret != 0;\nif (!ret)\n%(f)s\n', ''),
    'il0': ('i < 0', '', 'if (!ret)\n%(f)s\ni += ret != 0;\n', ''),
    'cnt': ('manifest.count <= 0', '', 'i += ret != 0;\nif (!ret)\n%(f)s\n', ''),
    'none': (None, '', 'i += ret != 0;\nif (!ret)\n%(f)s\n', ''),
}
LEAVE = {'cont': 'continue;\n', 'out': 'goto out;\n'}
S = g.MFS + '\nsent = ' + MFCALL + ';\nbreak;\n'
# T: the item path's test, T2 the manifest path's
HEADS = {
    'TD': 'if (i < manifest.count) {\nif (!ret)\ngoto out;\n@D@} else {\nif (!ret)\ngoto out;\n@S@}\n',
    'DT': 'if (i < manifest.count) {\n@D@if (!ret)\ngoto out;\n} else {\nif (!ret)\ngoto out;\n@S@}\n',
    'ND': 'if (!ret)\ngoto out;\nif (i < manifest.count) {\n@D@} else {\n@S@}\n',
    'ED': 'if (i < manifest.count || !ret) {\nif (!ret)\ngoto out;\n@D@} else {\n@S@}\n',
}
ENDS = {
    'brk0': 'if (!sent) {\nret = 0;\n' + MFF + '} else {\n' + ARMS_OK + '}\n',
    'brk1': 'if (sent) {\n' + ARMS_OK + '} else {\nret = 0;\n' + MFF + '}\n',
}


def variants():
    for it, de, le, h, en in itertools.product(ITEMS, DEAD, LEAVE, HEADS, ENDS):
        v, decl, d = ITEMS[it]
        test, init, inc, dd = DEAD[de]
        dtext = 'if (%s)\n%s' % (test, LEAVE[le]) if test else ''
        head = HEADS[h].replace('@S@', S).replace('@D@', dtext)
        body = decl + g.LOG % v + '\n' + g.SEND % v + '\n' + inc % {'f': g.FAIL % v}
        loop = 'i = 0;\n' + init + 'for (;;) {\n' + head + body + '}\n'
        src = g.PREP + g.FRAME.replace('@DECL@', '\tint sent;\n' + d + dd).replace('@LOOP@', loop).replace('@TAIL@', ENDS[en]).replace('@OUT@', 'out:')
        yield '|'.join((it, de, le, h, en)), src
