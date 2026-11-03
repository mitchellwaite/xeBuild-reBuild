"""Attempt 4: gen_ca43's dead test on a flag dom3 can't fold by threading through the head (which would copy H to the
chain's end and hoist i = 0), but vrp2 can without any copy: `sent = ret`, a nop conversion, so FRE and DOM see a
different name, and VRP's PHI<1, sent_new> is nonzero once the failure arm has left."""
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
FLAG = {'sent': ('sent', ''), 'ok': ('ok', '\tint ok;\n')}
ORDER = {
    # f: flag assignment, %(x)s
    'fil': '%(x)s = ret;\ni += ret != 0;\nif (!ret)\n%(f)s\n',
    'ifl': 'i += ret != 0;\n%(x)s = ret;\nif (!ret)\n%(f)s\n',
    'ilf': 'i += ret != 0;\nif (!ret)\n%(f)s\n%(x)s = ret;\n',
    'fli': '%(x)s = ret;\nif (!ret)\n%(f)s\ni += ret != 0;\n',
    'lfi': 'if (!ret)\n%(f)s\n%(x)s = ret;\ni += ret != 0;\n',
    'lif': 'if (!ret)\n%(f)s\ni += ret != 0;\n%(x)s = ret;\n',
    'send': '%(x)s = ret = @SEND@;\ni += ret != 0;\nif (!ret)\n%(f)s\n',
    'sendl': '%(x)s = ret = @SEND@;\nif (!ret)\n%(f)s\ni += ret != 0;\n',
}
S = g.MFS + '\n%(x)s = ' + MFCALL + ';\nbreak;\n'
LEAVE = {'out': 'goto out;\n', 'brk': 'break;\n'}
HEADS = {
    # the dead test in the then arm, in front of the manifest send
    'ND': 'if (!ret)\ngoto out;\nif (i < manifest.count) {\nif (!%(x)s)\n%(l)s} else {\n@S@}\n',
    'TD': 'if (i < manifest.count) {\nif (!ret)\ngoto out;\nif (!%(x)s)\n%(l)s} else {\nif (!ret)\ngoto out;\n@S@}\n',
    'DT': 'if (i < manifest.count) {\nif (!%(x)s)\n%(l)s if (!ret)\ngoto out;\n} else {\nif (!ret)\ngoto out;\n@S@}\n',
    # the flag is the only test on the item path
    'D1': 'if (i < manifest.count) {\nif (!%(x)s)\n%(l)s} else {\nif (!ret)\ngoto out;\n@S@}\n',
}
ENDS = {
    'brk0': 'if (!%(x)s) {\nret = 0;\n' + MFF.replace('%', '%%') + '} else {\n' + ARMS_OK.replace('%', '%%') + '}\n',
    'brk1': 'if (%(x)s) {\n' + ARMS_OK.replace('%', '%%') + '} else {\nret = 0;\n' + MFF.replace('%', '%%') + '}\n',
}


def variants():
    for it, fl, o, h, le, en in itertools.product(ITEMS, FLAG, ORDER, HEADS, LEAVE, ENDS):
        v, decl, d = ITEMS[it]
        x, dd = FLAG[fl]
        if le == 'brk' and fl != 'sent':
            continue  # falls out to the arms on a stale flag: only meaningful for sent
        head = HEADS[h].replace('@S@', S.replace('%s', '%%s')) % {'x': x, 'l': LEAVE[le]}
        send = (g.SEND % v).replace('ret = ', '', 1).rstrip(';')
        inc = ORDER[o].replace('@SEND@', send)
        sendline = '' if '@SEND@' in ORDER[o] else g.SEND % v + '\n'
        body = decl + g.LOG % v + '\n' + sendline + inc % {'x': x, 'f': g.FAIL % v}
        loop = 'i = 0;\n' + x + ' = 1;\nfor (;;) {\n' + head + body + '}\n'
        src = g.PREP + g.FRAME.replace('@DECL@', ('\tint sent;\n' if fl == 'sent' else '\tint sent;\n' + dd) + d).replace('@LOOP@', loop).replace(
            '@TAIL@', ENDS[en] % {'x': 'sent'}).replace('@OUT@', 'out:')
        yield '|'.join((it, fl, o, h, le, en)), src
