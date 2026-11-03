"""gen_ca22 le|a|forb spellings: the latch cmp order hangs on which SSA version the i copy gets (free list), so sweep natural spellings around it."""
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
MFH = {
    'ok': r'''
	log_printf(1, "sending manifest to %s\n", manifest.path);
	ok = netSendFile(manifest.path, manifest.data, manifest.size);
	goto check;
''',
    'ret': r'''
	log_printf(1, "sending manifest to %s\n", manifest.path);
	ret = netSendFile(manifest.path, manifest.data, manifest.size);
	goto check;
''',
}
ARMS = {
    'ok': g16.ARMS['ifnot'],
    'ret': g16.ARMS['ifnot'].replace('!ok', '!ret'),
}
GD = {
    'a': 'i = 0;\nif (manifest.count <= 0) goto mf;\n',
    'b': 'if (manifest.count <= 0) goto mf;\ni = 0;\n',
    'c': 'if (manifest.count > 0) i = 0; else goto mf;\n',
}
HT = {
    'ge': 'i >= manifest.count',
    'le': 'manifest.count <= i',
    'nlt': '!(i < manifest.count)',
}
TT = {'a': 'if (ret) goto mf;\nbreak;', 'b': 'if (!ret) break;\ngoto mf;'}
H2 = {'a': 'if (!ret) break;\ngoto send;', 'b': 'if (ret) goto send;\nbreak;'}
KD = {
    'k': ('uint32_t k;\n', 'k = i;\n', 'k'),
    'ki': ('int k;\n', 'k = i;\n', 'k'),
    'kb': ('', '{\nuint32_t k = i;\n', 'k'),
}
INC = {'b4': 'i += ret != 0;\n%(fl)s\n', 'if': 'if (ret) i++;\n%(fl)s\n'}


def variants():
    prep = 'int prepSysex(void)\n{\n' + g10.HEADS['h9'] + g10.TAIL['d'] + '\n}\n'
    for g, ht, tt, h2, kd, inc, m in itertools.product(GD, HT, TT, H2, KD, INC, MFH):
        d, kk, x = KD[kd]
        fl = 'if (!ret) ' + g5.fail(x)
        head = 'if (%s) {\n%s\n}\n%s\nmf:%s\nsend:\n' % (HT[ht], TT[tt], H2[h2], MFH[m])
        body = kk + g5.send(x) + INC[inc] % {'fl': fl}
        if kd == 'kb':
            body += '}\n'
        loop = d + GD[g] + 'for (;;) {\n' + head + body + '}\n'
        yield '|'.join((g, ht, tt, h2, kd, inc, m)), prep + g18.FRAME.replace('@LOOP@', loop).replace('@ARMS@', ARMS[m])
