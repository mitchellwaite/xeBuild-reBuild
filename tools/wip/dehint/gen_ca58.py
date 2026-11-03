"""Attempt 5: gen_ca57's J head (a block with no edge to the manifest send sits in front of it) with and without the entry guard's goto.
Axes: guard x head spelling x bottom x flag (ok beside ret or not) x item x arms."""
import itertools, os
from importlib import util

here = os.path.dirname(os.path.abspath(__file__))


def load(n):
    s = util.spec_from_file_location(n, os.path.join(here, n + '.py'))
    m = util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


g, g31, g45 = load('gen_ca30'), load('gen_ca31'), load('gen_ca45')
MFF, ARMS_OK, MFCALL = g31.MFF, g31.ARMS_OK, g31.MFCALL
ITEMS = dict(g45.ITEMS)
ITEMS = {k: ITEMS[k] for k in ('cast', 'k')}
ITEMS['u32'] = ({'n': 'i + 1', 'e': 'e->'}, 'e = &manifest.e[(uint32_t)i];\n', '\tstruct manifestItem *e;\n')
ITEMS['ke'] = ({'n': 'i + 1', 'e': 'e->'}, 'uint32_t k = i;\ne = &manifest.e[k];\n', '\tstruct manifestItem *e;\n')
T = 'if (!ret)\ngoto out;\n'
GUARD = {
    'none': ('i = 0;\nn = manifest.count;\n', ''),
    'le': ('i = 0;\nn = manifest.count;\nif (n <= 0)\ngoto send;\n', 'send:\n'),
    'lt': ('i = 0;\nn = manifest.count;\nif (i >= n)\ngoto send;\n', 'send:\n'),
    'ni': ('n = manifest.count;\ni = 0;\nif (n <= 0)\ngoto send;\n', 'send:\n'),
}
HEADS = {
    'J': 'if (i < n) {\nif (ret)\ngoto item;\ngoto out;\n}\n' + T,
    'J2': 'if (i < n) {\nif (!ret)\ngoto out;\ngoto item;\n}\n' + T,
    'J3': 'if (i < n) {\nif (!ret)\nbreak;\ngoto item;\n}\n' + T,
    'K': 'if (i < n && ret)\ngoto item;\n' + T,
    'J4': 'if (i >= n) {\n' + T + '} else {\nif (ret)\ngoto item;\ngoto out;\n}\n',
}
BOT = {
    'Nadd': 'n = manifest.count;\ni += ret != 0;\nif (!ret)\n%(f)s\n',
    'add': 'i += ret != 0;\nn = manifest.count;\nif (!ret)\n%(f)s\n',
    'okN': 'ok = ret != 0;\nn = manifest.count;\ni += ok;\nif (!ret)\n%(f)s\n',
    'okNr': 'ok = ret != 0;\nn = manifest.count;\ni += ret != 0;\nif (!ret)\n%(f)s\n',
    'Nok': 'n = manifest.count;\nok = ret != 0;\ni += ok;\nif (!ret)\n%(f)s\n',
}
ENDS = {
    'sent': ('sent = ', 'if (!sent) {\nret = 0;\n' + MFF + '} else {\n' + ARMS_OK + '}\n'),
    'ret': ('ret = ', 'if (!ret) {\n' + MFF + '} else {\n' + ARMS_OK + '}\n'),
}


def variants():
    for it, gd, h, b, en in itertools.product(ITEMS, GUARD, HEADS, BOT, ENDS):
        v, decl, d = ITEMS[it]
        init, label = GUARD[gd]
        s = g.MFS + '\n' + ENDS[en][0] + MFCALL + ';\nbreak;\n'
        tail = ENDS[en][1]
        body = 'item:\n' + decl + g.LOG % v + '\n' + g.SEND % v + '\n' + BOT[b] % {'f': g.FAIL % v}
        if decl.startswith('uint32_t'):  # a label can't precede a declaration
            body = body.replace('item:\n', 'item:;\n')
        loop = init + 'for (;;) {\n' + HEADS[h] + label + s + body + '}\n'
        if 'break;\ngoto item' in loop:
            continue_out = True
        src = g.PREP + g.FRAME.replace('@DECL@', '\tint sent, n, ok;\n' + d).replace('@LOOP@', loop).replace('@TAIL@', tail).replace('@OUT@', 'out:')
        yield '|'.join((it, gd, h, b, en)), src
