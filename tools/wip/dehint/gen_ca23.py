"""gen_ca22 le|a|forb (only the latch cmp operand order wrong: SSA versions, load before i + 1): compute the item number before the head test."""
import itertools
from importlib import util
import os

here = os.path.dirname(os.path.abspath(__file__))


def load(n):
    s = util.spec_from_file_location(n, os.path.join(here, n + '.py'))
    m = util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


g5, g10, g16, g18 = load('gen_ca5'), load('gen_ca10'), load('gen_ca16'), load('gen_ca18')
MFH = r'''
	log_printf(1, "sending manifest to %s\n", manifest.path);
	ok = netSendFile(manifest.path, manifest.data, manifest.size);
	goto check;
'''
SEND = r'''
	log_printf(1, "sending %03d: 0x%08x (%d) bytes, %s\n", N, manifest.e[X].len, manifest.e[X].len, manifest.e[X].path);
	ret = netSendFile(manifest.e[X].path, manifest.e[X].data, manifest.e[X].len);
'''
GD = 'i = 0;\nif (manifest.count <= 0) goto mf;\n'
TESTS = {
    'ge': 'if (i >= manifest.count) {\nif (ret) goto mf;\nbreak;\n}\nif (!ret) break;\ngoto send;\nmf:%(m)s\nsend:\n',
    'nge': 'if (n > manifest.count) {\nif (ret) goto mf;\nbreak;\n}\nif (!ret) break;\ngoto send;\nmf:%(m)s\nsend:\n',
}
TOP = {
    'n': 'n = i + 1;',
    'nk': 'n = i + 1;\nk = i;',
    'kn': 'k = i;\nn = i + 1;',
}
INC = {
    'add': 'i += ret != 0;',
    'if': 'if (ret) i = n;',
    'term': 'i = ret ? n : i;',
    'addn': 'i = n - !ret;',
}
BOT = {'k': 'k = i;', 'none': ''}


def variants():
    prep = 'int prepSysex(void)\n{\n' + g10.HEADS['h9'] + g10.TAIL['d'] + '\n}\n'
    for t, top, inc, x, nm in itertools.product(TESTS, TOP, INC, ['k', 'i'], ['n', 'i + 1']):
        if x == 'i' and 'k' in top:
            continue
        snd = SEND.replace('X', x).replace('N', nm)
        fl = 'if (!ret) ' + g5.fail(x)
        topc = TOP[top]
        bot = ''
        if x == 'k' and 'k' not in top:
            bot = 'k = i;'
        head = TESTS[t] % {'m': MFH}
        loop = 'uint32_t k;\nint n;\n' + GD + 'for (;;) {\n' + topc + '\n' + head + bot + '\n' + snd + INC[inc] + '\n' + fl + '\n}\n'
        yield '%s|%s|%s|%s|%s' % (t, top, inc, x, nm), prep + g18.FRAME.replace('@LOOP@', loop).replace('@ARMS@', g16.ARMS['ifnot'])
