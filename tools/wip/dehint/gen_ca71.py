"""Attempt 5: can the landed text get simpler while the dead test stays? One exit (i = n on failure, no second `if (!ret) goto out`), body-scoped
index and pointer spellings, ok only where needed. Axes: dead test x exit x item x increment x arms."""
import itertools, os
from importlib import util

here = os.path.dirname(os.path.abspath(__file__))
s = util.spec_from_file_location('gen_ca68', os.path.join(here, 'gen_ca68.py'))
m68 = util.module_from_spec(s)
s.loader.exec_module(m68)
m = m68.m
g = m.g
MFF, MFCALL, ARMS_OK = m.MFF, m.MFCALL, m.ARMS_OK
T = 'if (!ret)\ngoto out;\n'
DEAD = {
    'letm': 'if (ok <= 0) {\nnetTimerEnd();\ngoto out;\n}\n',
    'nottm': 'if (!ok) {\nnetTimerEnd();\ngoto out;\n}\n',
    'lelog': 'if (ok <= 0) {\n' + MFF + 'goto out;\n}\n',
    'notlog': 'if (!ok) {\n' + MFF + 'goto out;\n}\n',
}
EXIT = {
    'two': (T, ''),
    'one': ('', 'i = n;\n'),
    'zero': ('', 'n = 0;\n'),
}
INC = {
    'ok': 'ok = ret != 0;\nn = manifest.count;\ni += ok;\n',
    'okr': 'ok = ret != 0;\nn = manifest.count;\ni += ret != 0;\n',
}
ITEMS = {
    'cast': ({'n': 'i + 1', 'e': 'e->'}, 'e = &manifest.e[(size_t)i];\n', '\tstruct manifestItem *e;\n'),
    'castb': ({'n': 'i + 1', 'e': 'e->'}, 'struct manifestItem *e = &manifest.e[(size_t)i];\n', ''),
    'ku': ({'n': 'i + 1', 'e': 'manifest.e[k].'}, 'uint32_t k = i;\n', ''),
    'kue': ({'n': 'i + 1', 'e': 'e->'}, 'uint32_t k = i;\nstruct manifestItem *e = &manifest.e[k];\n', ''),
    'ks': ({'n': 'i + 1', 'e': 'manifest.e[k].'}, 'size_t k = i;\n', ''),
    'kse': ({'n': 'i + 1', 'e': 'e->'}, 'size_t k = i;\nstruct manifestItem *e = &manifest.e[k];\n', ''),
    'plus': ({'n': 'i + 1', 'e': 'e->'}, 'struct manifestItem *e = manifest.e + (size_t)i;\n', ''),
    'kplus': ({'n': 'i + 1', 'e': 'e->'}, 'size_t k = i;\nstruct manifestItem *e = manifest.e + k;\n', ''),
}


def variants():
    for it, de, ex, inc in itertools.product(ITEMS, DEAD, EXIT, INC):
        v, decl, d = ITEMS[it]
        t2, stop = EXIT[ex]
        head = 'if (i >= n) {\n' + T + DEAD[de] + g.MFS + '\nok = ' + MFCALL + ';\nbreak;\n}\n' + t2
        f = g.FAIL % v
        tail = 'if (!ret) {\n' + f + '\n' + stop + '}\n' if stop else 'if (!ret)\n' + f + '\n'
        body = decl + g.LOG % v + '\n' + g.SEND % v + '\n' + INC[inc] + tail
        if it == 'cast' or not decl.startswith('struct') and not decl.startswith('uint32_t') and not decl.startswith('size_t'):
            pass
        loop = 'i = 0;\nn = manifest.count;\nok = 1;\nfor (;;) {\n' + head + body + '}\n'
        arms = 'if (!ok) {\nret = 0;\n' + MFF + '} else {\n' + ARMS_OK + '}\n'
        src = g.PREP + g.FRAME.replace('@DECL@', '\tint n, ok;\n' + d).replace('@LOOP@', loop).replace('@TAIL@', arms).replace('@OUT@', 'out:')
        yield '|'.join((it, de, ex, inc)), src
