"""gen_ca19 shape, with a block that has no edge to the manifest head lexically right before it, so crited1 puts the guard's forwarder there and not right after the guard. Increment before the failure log: the loop test stays in place."""
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
GD = {
    'le': 'i = 0;\nif (manifest.count <= 0) goto mf;\n',
    'leg': 'i = 0;\nif (manifest.count <= 0) goto mf;\ngoto send;\n',
}
HEADS = {
    # test, flag test, manifest head, body
    'a': 'if (i >= manifest.count) {\nif (ret) goto mf;\nbreak;\n}\nif (!ret) break;\ngoto send;\nmf:%(m)s\nsend:\n',
    'b': 'if (i < manifest.count) {\nif (!ret) break;\ngoto send;\n}\nif (!ret) break;\nmf:%(m)s\nsend:\n',
    'c': 'if (i < manifest.count) {\nif (ret) goto send;\nbreak;\n}\nif (!ret) break;\nmf:%(m)s\nsend:\n',
    'd': 'if (i < manifest.count) {\nif (ret) goto send;\nbreak;\n}\nif (ret) {\nmf:%(m)s}\nbreak;\nsend:\n',
    'e': 'if (i < manifest.count && ret) goto send;\nif (!ret) break;\nmf:%(m)s\nsend:\n',
    'f': 'if (i >= manifest.count) {\nif (!ret) break;\nmf:%(m)s}\nif (!ret) break;\nsend:\n',
}
SHAPES = {
    'fora': 'for (;; i += ret != 0) {\n%(h)s\n%(k)s\n%(snd)s\n%(fl)s\n}\n',
    'forb': 'for (;;) {\n%(h)s\n%(k)s\n%(snd)s\ni += ret != 0;\n%(fl)s\n}\n',
}
KS = {
    'k1': ('uint32_t k;', 'k = i;', 'k'),
    'i': ('', '', 'i'),
}


def variants():
    prep = 'int prepSysex(void)\n{\n' + g10.HEADS['h9'] + g10.TAIL['d'] + '\n}\n'
    for g, h, s, (kn, (d, k, x)) in itertools.product(GD, HEADS, SHAPES, KS.items()):
        fl = 'if (!ret) ' + g5.fail(x)
        head = HEADS[h] % {'m': MFH}
        loop = d + '\n' + GD[g] + SHAPES[s] % {'h': head, 'k': k, 'snd': g5.send(x), 'fl': fl}
        yield '%s|%s|%s|%s' % (g, h, s, kn), prep + g18.FRAME.replace('@LOOP@', loop).replace('@ARMS@', g16.ARMS['ifnot'])
