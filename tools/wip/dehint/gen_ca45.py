"""Attempt 4: the count cached in a local, reloaded at the bottom of the loop, so the header is only a condition and ch
copies it however the failure arm was threaded (do_while_loop_p), with the empty join that keeps H in place."""
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
DEAD = {
    'none': ('', '', '', ''),
    'ok': ('if (!ok)\ngoto out;\n', 'ok = 1;\n', 'ok = ret != 0;\n', '\tint ok;\n'),
    'fail': ('if (failed)\ngoto out;\n', 'failed = 0;\n', 'failed = !ret;\n', '\tint failed;\n'),
    'i0': ('if (i < 0)\ngoto out;\n', '', '', ''),
    'n0': ('if (n <= 0)\ngoto out;\n', '', '', ''),
}
INC = {
    'add': 'i += ret != 0;\nif (!ret)\n%(f)s\n',
    'addl': 'if (!ret)\n%(f)s\ni += ret != 0;\n',
    'ifel': 'if (ret)\ni++;\nelse\n%(f)s\n',
    'nifel': 'if (!ret)\n%(f)s\nelse\ni++;\n',
}
S = g.MFS + '\nsent = ' + MFCALL + ';\nbreak;\n'
T = 'if (!ret)\ngoto out;\n'
HEADS = {
    'R': T + 'if (i < n) {\n@D@} else {\n@S@}\n',
    'X': 'if (i < n) {\n' + T + '@D@} else {\n' + T + '@S@}\n',
    'E': 'if (i >= n || !ret) {\n' + T + '@D@@S@}\n',
    'B': 'if (i >= n) {\n' + T + '@D@@S@}\n' + T,
    'NE': 'if (i < n || !ret) {\n' + T + '@D@} else {\n@S@}\n',
}
NEXT = {
    'bot': ('', 'n = manifest.count;\n'),
}
ENDS = {
    'brk0': 'if (!sent) {\nret = 0;\n' + MFF + '} else {\n' + ARMS_OK + '}\n',
    'brk1': 'if (sent) {\n' + ARMS_OK + '} else {\nret = 0;\n' + MFF + '}\n',
}


def variants():
    for it, de, inc, h, en in itertools.product(ITEMS, DEAD, INC, HEADS, ENDS):
        v, decl, d = ITEMS[it]
        dt, init, upd, dd = DEAD[de]
        head = HEADS[h].replace('@S@', S).replace('@D@', dt)
        body = decl + g.LOG % v + '\n' + g.SEND % v + '\n' + upd + INC[inc] % {'f': g.FAIL % v} + 'n = manifest.count;\n'
        loop = 'i = 0;\nn = manifest.count;\n' + init + 'for (;;) {\n' + head + body + '}\n'
        src = g.PREP + g.FRAME.replace('@DECL@', '\tint sent, n;\n' + d + dd).replace('@LOOP@', loop).replace('@TAIL@', ENDS[en]).replace('@OUT@', 'out:')
        yield '|'.join((it, de, inc, h, en)), src
