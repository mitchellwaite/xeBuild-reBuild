"""Attempt 3: the manifest send inside the loop at its head, reached from a natural head test.
ch's copy goes right after the entry (guard, loop test, manifest head), and split_edge_bb_loc puts
the preheader after the manifest head, which is the reference's chain, with no labels."""
import itertools, os
from importlib import util

here = os.path.dirname(os.path.abspath(__file__))
s = util.spec_from_file_location('gen_ca30', os.path.join(here, 'gen_ca30.py'))
g = util.module_from_spec(s)
s.loader.exec_module(g)

V = {'n': 'i + 1', 'e': 'manifest.e[i].'}
P = {'n': 'i + 1', 'e': 'e->'}
ARMS_OK = 'log_printf(0, "success! Avatar data is successfully sent to the console!\\n");\nnetTimerEnd();\nret = 1;\n'
MFF = 'log_printf(0, "aborting sending avatar data, failed to send %s\\n", manifest.path);\n'
MFCALL = 'netSendFile(manifest.path, manifest.data, manifest.size)'

ITEMS = {
    'inl': (V, ''),
    'ptr': (P, 'struct manifestItem *e = &manifest.e[i];\n'),
}
INC = {
    'ifel': 'if (ret)\ni++;\nelse\n%(f)s\n',
    'nifel': 'if (!ret)\n%(f)s\nelse\ni++;\n',
    'add': 'i += ret != 0;\nif (!ret)\n%(f)s\n',
    'addl': 'if (!ret)\n%(f)s\ni += ret != 0;\n',
}
# loop forms: %(head)s test+manifest, %(b)s item body
LOOPS = {
    'whr': 'i = 0;\nwhile (ret) {\n%(head)s%(b)s}\n',
    'forr': 'for (i = 0; ret;) {\n%(head)s%(b)s}\n',
    'dor': 'i = 0;\ndo {\n%(head)s%(b)s} while (ret);\n',
    'inf': 'i = 0;\nfor (;;) {\n%(head)s%(b)s\nif (!ret)\nbreak;\n}\n',
}
# head + after-loop: (how the head leaves, text after the loop, extra decl)
ENDS = {
    # sent flag, arms after the loop; item failure leaves with sent unset
    'sent0': ('if (i >= manifest.count) {\n' + g.MFS + '\nsent = ' + MFCALL + ';\nbreak;\n}\n',
              'if (ret) {\nif (!sent) {\nret = 0;\n' + MFF + '} else {\n' + ARMS_OK + '}\n}\n', '\tint sent;\n'),
    # same, with arms if (sent) first
    'sent1': ('if (i >= manifest.count) {\n' + g.MFS + '\nsent = ' + MFCALL + ';\nbreak;\n}\n',
              'if (ret) {\nif (sent) {\n' + ARMS_OK + '} else {\nret = 0;\n' + MFF + '}\n}\n', '\tint sent;\n'),
    # ret carries the manifest's result too, item failure jumps to out
    'ret': ('if (i >= manifest.count) {\n' + g.MFS + '\nret = ' + MFCALL + ';\ngoto mfdone;\n}\n',
            'goto out;\nmfdone:\nif (!ret) {\n' + MFF + '} else {\n' + ARMS_OK + '}\n', ''),
    # arms in place
    'arm': ('if (i >= manifest.count) {\n' + g.MFS + '\n' + g.MFA + '\nbreak;\n}\n', '', ''),
    # arms reached by goto
    'gf': ('if (i >= manifest.count) {\n' + g.MFS + '\nif (!' + MFCALL + ')\ngoto mffail;\nbreak;\n}\n',
           'if (ret) {\n' + ARMS_OK + '}\ngoto out;\nmffail:\nret = 0;\n' + MFF, ''),
    # else-branch spelling
    'els': ('if (i >= manifest.count) {\n' + g.MFS + '\nsent = ' + MFCALL + ';\nbreak;\n} else {\n',
            'if (ret) {\nif (!sent) {\nret = 0;\n' + MFF + '} else {\n' + ARMS_OK + '}\n}\n', '\tint sent;\n'),
}


def variants():
    for it, inc, l, en in itertools.product(ITEMS, INC, LOOPS, ENDS):
        v, decl = ITEMS[it]
        head, after, d = ENDS[en]
        body = decl + g.LOG % v + '\n' + g.SEND % v + '\n' + INC[inc] % {'f': g.FAIL % v}
        if en == 'els':
            body += '}\n'
        loop = LOOPS[l] % {'head': head, 'b': body}
        need_out = 'goto out' in after
        src = g.PREP + g.FRAME.replace('@DECL@', d).replace('@LOOP@', loop).replace('@TAIL@', after).replace('@OUT@', 'out:' if need_out else '')
        yield '|'.join((it, inc, l, en)), src
