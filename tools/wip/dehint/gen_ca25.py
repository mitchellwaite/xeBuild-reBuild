"""MATCH shape (gen_ca22 le|a|forb with an accessor for the count in the head test): which borderline parts can go, and how plain can the loop get."""
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
HELP = {
    'count': 'static int itemCount(void)\n{\n\treturn manifest.count;\n}\n\n',
    'done': 'static int itemsDone(int i)\n{\n\treturn i >= manifest.count;\n}\n\n',
    'more': 'static int moreItems(int i)\n{\n\treturn i < manifest.count;\n}\n\n',
}
HEADT = {'count': 'i >= itemCount()', 'done': 'itemsDone(i)', 'more': '!moreItems(i)'}
MFH = r'''
	log_printf(1, "sending manifest to %s\n", manifest.path);
	ok = netSendFile(manifest.path, manifest.data, manifest.size);
	goto check;
'''
HEADS = {
    'a': 'if (%(t)s) {\nif (ret) goto mf;\nbreak;\n}\nif (!ret) break;\ngoto send;\nmf:%(m)s\nsend:\n',
    'b': 'if (%(t)s) {\nif (!ret) break;\ngoto mf;\n}\nif (ret) goto send;\nbreak;\nmf:%(m)s\nsend:\n',
}
LOOPS = {'for': 'for (;;) {\n%s}\n', 'while': 'while (1) {\n%s}\n'}
KD = {
    'k': ('uint32_t k;\n', 'k = i;\n', 'k', ''),
    'kb': ('', '{\nuint32_t k = i;\n', 'k', '}\n'),
    'ki': ('int k;\n', 'k = i;\n', 'k', ''),
    'i': ('', '', 'i', ''),
}
INC = {
    'b4': 'i += ret != 0;\n%(fl)s\n',
    'if': 'if (ret) i++;\n%(fl)s\n',
    'ifelse': 'if (ret) i++; else %(f)s\n',
    'ifnot': 'if (!ret) %(f)s else i++;\n',
    'after': '%(fl)s\ni += ret != 0;\n',
}
SND = {
    'p1': lambda x: g5.send(x),
}
PREPS = {
    'h9d': g10.HEADS['h9'] + g10.TAIL['d'],
}


def variants():
    for hp, h, l, kd, inc, p in itertools.product(HELP, HEADS, LOOPS, KD, INC, PREPS):
        d, kk, x, end = KD[kd]
        fl = 'if (!ret) ' + g5.fail(x)
        head = HEADS[h] % {'t': HEADT[hp], 'm': MFH}
        body = kk + g5.send(x) + INC[inc] % {'fl': fl, 'f': g5.fail(x)} + end
        loop = d + 'i = 0;\nif (manifest.count <= 0) goto mf;\n' + LOOPS[l] % (head + body)
        prep = 'int prepSysex(void)\n{\n' + PREPS[p] + '\n}\n\n' + HELP[hp]
        yield '|'.join((hp, h, l, kd, inc, p)), prep + g18.FRAME.replace('@LOOP@', loop).replace('@ARMS@', g16.ARMS['ifnot'])
