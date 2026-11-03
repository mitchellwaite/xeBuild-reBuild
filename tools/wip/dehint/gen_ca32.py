"""Attempt 3: head `if (i >= count) { manifest; leave }` first, `ret` tested after it, so the loop is
entered at a load+cond header that ch can copy (guard, loop test, manifest head, preheader, body)."""
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
    'inl': (V, ''),
    'ptr': (P, 'struct manifestItem *e = &manifest.e[i];\n'),
    'ptrd': (P, 'e = &manifest.e[i];\n'),
}
INC = {
    'ifel': 'if (ret)\ni++;\nelse\n%(f)s\n',
    'nifel': 'if (!ret)\n%(f)s\nelse\ni++;\n',
    'add': 'i += ret != 0;\nif (!ret)\n%(f)s\n',
    'addl': 'if (!ret)\n%(f)s\ni += ret != 0;\n',
    'ifif': 'if (ret)\ni++;\nif (!ret)\n%(f)s\n',
    'ififr': 'if (!ret)\n%(f)s\nif (ret)\ni++;\n',
}
RTEST = {
    'brk': 'if (!ret)\nbreak;\n',
    'out': 'if (!ret)\ngoto out;\n',
}
LOOPS = {
    'for': 'i = 0;\nfor (;;) {\n%s}\n',
    'wh1': 'i = 0;\nwhile (1) {\n%s}\n',
    'fori': 'for (i = 0;;) {\n%s}\n',
}
SENT = 'if (i >= manifest.count) {\n' + g.MFS.replace('%', '%%') + '\nsent = ' + MFCALL + ';\n%s}\n'
# (head leave statement variants), text after the loop
ENDS = {
    'sg0': (SENT % 'goto sentit;\n', 'goto out;\nsentit:\nif (!sent) {\nret = 0;\n' + MFF + '} else {\n' + ARMS_OK + '}\n', '\tint sent;\n'),
    'sg1': (SENT % 'goto sentit;\n', 'goto out;\nsentit:\nif (sent) {\n' + ARMS_OK + '} else {\nret = 0;\n' + MFF + '}\n', '\tint sent;\n'),
    # ret carries the result and the item failure leaves through out; loop exit only from the head
    'rg': ('if (i >= manifest.count) {\n' + g.MFS + '\nret = ' + MFCALL + ';\nbreak;\n}\n',
           'if (!ret) {\n' + MFF + '} else {\n' + ARMS_OK + '}\n', ''),
    'rg1': ('if (i >= manifest.count) {\n' + g.MFS + '\nret = ' + MFCALL + ';\nbreak;\n}\n',
            'if (ret) {\n' + ARMS_OK + '} else {\n' + MFF + '}\n', ''),
    'arm': ('if (i >= manifest.count) {\n' + g.MFS + '\n' + g.MFA + '\nbreak;\n}\n', '', ''),
    'rgf': ('if (i >= manifest.count) {\n' + g.MFS + '\nif (!' + MFCALL + ')\ngoto mffail;\nbreak;\n}\n',
            ARMS_OK + 'goto out;\nmffail:\nret = 0;\n' + MFF, ''),
}


def variants():
    for it, inc, r, l, en in itertools.product(ITEMS, INC, RTEST, LOOPS, ENDS):
        v, decl = ITEMS[it]
        head, after, d = ENDS[en]
        if r == 'brk' and en != 'arm':
            # a break from `ret` would run the manifest's arms: only the goto can leave here
            continue
        body = decl + g.LOG % v + '\n' + g.SEND % v + '\n' + INC[inc] % {'f': g.FAIL % v}
        loop = LOOPS[l] % (head + RTEST[r] + body)
        need_out = 'goto out' in after or r == 'out'
        if it == 'ptrd':
            d += '\tstruct manifestItem *e;\n'
        src = g.PREP + g.FRAME.replace('@DECL@', d).replace('@LOOP@', loop).replace('@TAIL@', after).replace('@OUT@', 'out:' if need_out else '')
        yield '|'.join((it, inc, r, l, en)), src
