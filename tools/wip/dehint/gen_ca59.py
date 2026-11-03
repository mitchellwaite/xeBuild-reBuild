"""Attempt 5: gen_ca58's le|J (no dead test, .rdata right, only addTitleId's cmp order off: ch2 takes a low free-list name for the
copied load). Spellings that release a different number of SSA names before ch2. Axes: guard/init x head x reload x item x arms."""
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
ITEMS = {'cast': g45.ITEMS['cast'], 'k': g45.ITEMS['k']}
ITEMS['ke'] = ({'n': 'i + 1', 'e': 'e->'}, 'uint32_t k = i;\ne = &manifest.e[k];\n', '\tstruct manifestItem *e;\n')
T = 'if (!ret)\ngoto out;\n'
GUARD = {
    'le': 'i = 0;\nn = manifest.count;\nif (n <= 0)\ngoto send;\n',
    'mc': 'i = 0;\nif (manifest.count <= 0)\ngoto send;\nn = manifest.count;\n',
    'mc2': 'if (manifest.count <= 0)\ngoto send;\ni = 0;\nn = manifest.count;\n',
    'ngt': 'i = 0;\nn = manifest.count;\nif (n > 0)\ngoto item;\ngoto send;\n',
    'nogi': 'n = manifest.count;\nif (n <= 0)\ngoto send;\nfor (i = 0;;) {\n',
    'i0item': 'n = manifest.count;\nif (n <= 0)\ngoto send;\ni = 0;\ngoto item;\n',
    'i0forif': 'i = 0;\nn = manifest.count;\nif (n <= 0)\ngoto send;\ngoto item;\n',
}
HEADS = {
    'J': 'if (i < n) {\nif (ret)\ngoto item;\ngoto out;\n}\n' + T,
    'J4': 'if (i >= n) {\n' + T + '} else {\nif (ret)\ngoto item;\ngoto out;\n}\n',
    'K': 'if (i < n && ret)\ngoto item;\n' + T,
    'Jk': 'if (i < n) {\nif (ret)\ngoto item;\ngoto out;\n} else if (!ret)\ngoto out;\n',
    'L': 'if (!ret)\ngoto out;\nif (i < n)\ngoto item;\n',
}
BOT = {
    'Nadd': 'n = manifest.count;\ni += ret != 0;\nif (!ret)\n%(f)s\n',
    'add': 'i += ret != 0;\nn = manifest.count;\nif (!ret)\n%(f)s\n',
    'tmp': 'i += ret != 0;\nif (!ret)\n%(f)s\nn = manifest.count;\n',
    'ifel': 'n = manifest.count;\nif (ret)\ni++;\nelse\n%(f)s\n',
}
ENDS = {
    'sent': ('sent = ', 'if (!sent) {\nret = 0;\n' + MFF + '} else {\n' + ARMS_OK + '}\n'),
    'if': ('if (!' + MFCALL + ') {\nret = 0;\n' + MFF + '} else {\n' + ARMS_OK + '}\nbreak;\n', ''),
    'if2': ('if (' + MFCALL + ') {\n' + ARMS_OK + '} else {\nret = 0;\n' + MFF + '}\nbreak;\n', ''),
}


def variants():
    for it, gd, h, b, en in itertools.product(ITEMS, GUARD, HEADS, BOT, ENDS):
        v, decl, d = ITEMS[it]
        init = GUARD[gd]
        if en == 'sent':
            s = g.MFS + '\n' + ENDS[en][0] + MFCALL + ';\nbreak;\n'
        else:
            s = g.MFS + '\n' + ENDS[en][0]
        tail = ENDS[en][1]
        body = 'item:;\n' + decl + g.LOG % v + '\n' + g.SEND % v + '\n' + BOT[b] % {'f': g.FAIL % v}
        opener = '' if init.endswith('{\n') else 'for (;;) {\n'
        loop = init + opener + HEADS[h] + 'send:\n' + s + body + '}\n'
        src = g.PREP + g.FRAME.replace('@DECL@', '\tint sent, n;\n' + d).replace('@LOOP@', loop).replace('@TAIL@', tail).replace('@OUT@', 'out:')
        yield '|'.join((it, gd, h, b, en)), src
