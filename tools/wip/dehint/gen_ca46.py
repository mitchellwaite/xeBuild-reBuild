"""Attempt 4: failure leaves from the body (`if (!ret) { log; goto out; }`), i += ret != 0 ahead of the test (not an IV
until sink + dom3 fold it), the count cached so ch copies a condition-only header, reloaded before the failure test so
H's only predecessor is a conditional block and it isn't merged away from its place after the guard."""
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
    'ret': ('if (!ret)\ngoto out;\n', '', '', ''),
    'i0': ('if (i < 0)\ngoto out;\n', '', '', ''),
    'n0': ('if (n <= 0)\ngoto out;\n', '', '', ''),
}
# %(u)s dead flag's update, %(f)s failure log, N the reload
BOT = {
    'uNi': '%(u)sn = manifest.count;\ni += ret != 0;\nif (!ret) {\n%(f)s\ngoto out;\n}\n',
    'Nui': 'n = manifest.count;\n%(u)si += ret != 0;\nif (!ret) {\n%(f)s\ngoto out;\n}\n',
    'uiN': '%(u)si += ret != 0;\nn = manifest.count;\nif (!ret) {\n%(f)s\ngoto out;\n}\n',
    'ui_N': '%(u)si += ret != 0;\nif (!ret) {\n%(f)s\ngoto out;\n}\nn = manifest.count;\n',
    'ui_elseN': '%(u)si += ret != 0;\nif (ret)\nn = manifest.count;\nelse {\n%(f)s\ngoto out;\n}\n',
}
S = g.MFS + '\nsent = ' + MFCALL + ';\nbreak;\n'
HEADS = {
    'P': 'if (i >= n) {\n@D@@S@}\n',
    'N': 'if (i < n) {\n@D@} else {\n@S@}\n',
}
ENDS = {
    'brk0': 'if (!sent) {\nret = 0;\n' + MFF + '} else {\n' + ARMS_OK + '}\n',
    'brk1': 'if (sent) {\n' + ARMS_OK + '} else {\nret = 0;\n' + MFF + '}\n',
}


def variants():
    for it, de, bot, h, en in itertools.product(ITEMS, DEAD, BOT, HEADS, ENDS):
        v, decl, d = ITEMS[it]
        dt, init, upd, dd = DEAD[de]
        head = HEADS[h].replace('@S@', S).replace('@D@', dt)
        body = decl + g.LOG % v + '\n' + g.SEND % v + '\n' + BOT[bot] % {'u': upd, 'f': g.FAIL % v}
        loop = 'i = 0;\nn = manifest.count;\n' + init + 'for (;;) {\n' + head + body + '}\n'
        src = g.PREP + g.FRAME.replace('@DECL@', '\tint sent, n;\n' + d + dd).replace('@LOOP@', loop).replace('@TAIL@', ENDS[en]).replace('@OUT@', 'out:')
        yield '|'.join((it, de, bot, h, en)), src
