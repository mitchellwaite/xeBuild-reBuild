"""Attempt 5: a4nodead with a real second predecessor for the manifest send, so dom2's thread copy can't swallow it.
Axes: how the zero-count path reaches the send (goto into the head, or a do-while with the send after it) x head x bottom x arms."""
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
ITEMS = {k: g45.ITEMS[k] for k in ('cast', 'k')}
T = 'if (!ret)\ngoto out;\n'
S = g.MFS + '\nsent = ' + MFCALL + ';\nbreak;\n'
GUARD = {'le': 'if (n <= 0)\ngoto send;\n', 'lt': 'if (i >= n)\ngoto send;\n', 'not': 'if (!n)\ngoto send;\n'}
HEADS = {
    'B': 'if (i >= n) {\n' + T + 'send:\n' + S + '}\n' + T,
    'X': 'if (i < n) {\n' + T + '} else {\n' + T + 'send:\n' + S + '}\n',
    'R': T + 'if (i >= n) {\nsend:\n' + S + '}\n',
    'J': 'if (i < n) {\nif (ret)\ngoto item;\ngoto out;\n}\n' + T + 'send:\n' + S + 'item:\n',
    'K': 'if (i < n && ret)\ngoto item;\n' + T + 'send:\n' + S + 'item:\n',
}
BOT = {
    'Nadd': 'n = manifest.count;\ni += ret != 0;\nif (!ret)\n%(f)s\n',
    'add': 'i += ret != 0;\nn = manifest.count;\nif (!ret)\n%(f)s\n',
    'Nifel': 'n = manifest.count;\nif (ret)\ni++;\nelse\n%(f)s\n',
    'addB': 'i += ret != 0;\nif (!ret)\n%(f)s\nn = manifest.count;\n',
}
ENDS = {
    'brk0': 'if (!sent) {\nret = 0;\n' + MFF + '} else {\n' + ARMS_OK + '}\n',
    'brk1': 'if (sent) {\n' + ARMS_OK + '} else {\nret = 0;\n' + MFF + '}\n',
}


def variants():
    for it, gd, h, b, en in itertools.product(ITEMS, GUARD, HEADS, BOT, ENDS):
        v, decl, d = ITEMS[it]
        body = decl + g.LOG % v + '\n' + g.SEND % v + '\n' + BOT[b] % {'f': g.FAIL % v}
        loop = 'i = 0;\nn = manifest.count;\n' + GUARD[gd] + 'for (;;) {\n' + HEADS[h] + body + '}\n'
        src = g.PREP + g.FRAME.replace('@DECL@', '\tint sent, n;\n' + d).replace('@LOOP@', loop).replace('@TAIL@', ENDS[en]).replace('@OUT@', 'out:')
        yield '|'.join((it, gd, h, b, en)), src
    # do-while with the send after it: the zero-count path reaches the send by its own edge
    for it, b, t, gd in itertools.product(ITEMS, BOT, ('if', 'goto'), ('if', 'for')):
        v, decl, d = ITEMS[it]
        body = decl + g.LOG % v + '\n' + g.SEND % v + '\n' + BOT[b] % {'f': g.FAIL % v}
        if gd == 'if':
            loop = 'i = 0;\nn = manifest.count;\nif (n > 0) {\ndo {\n' + body + '} while (i < n && ret);\n}\n'
        else:
            loop = 'n = manifest.count;\nfor (i = 0; i < n && ret;) {\n' + body + '}\n'
        arm = 'if (!netSendFile(manifest.path, manifest.data, manifest.size)) {\nret = 0;\n' + MFF + '} else {\n' + ARMS_OK + '}\n'
        tail = 'if (ret) {\n' + g.MFS + '\n' + arm + '}\n' if t == 'if' else T + g.MFS + '\n' + arm
        src = g.PREP + g.FRAME.replace('@DECL@', '\tint n;\n' + d).replace('@LOOP@', loop).replace('@TAIL@', tail).replace('@OUT@', 'out:' if t == 'goto' else '')
        yield '|'.join(('post', it, b, t, gd)), src
