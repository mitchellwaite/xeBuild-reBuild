"""Explicit guard `if (count <= 0) goto mf`, then a head-tested loop holding the manifest head: the loop test stays between guard and manifest."""
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
GD = 'i = 0;\nif (manifest.count <= 0) goto mf;\n'
HEADS = {
    'd': 'if (i >= manifest.count || !ret) {\nif (ret) {\nmf: %(m)s}\nbreak;\n}\n',
    'e': 'if (i >= manifest.count) {\nif (ret) {\nmf: %(m)s}\nbreak;\n}\nif (!ret) break;\n',
    'f': 'if (!ret || i >= manifest.count) {\nif (ret) {\nmf: %(m)s}\nbreak;\n}\n',
    'g': 'if (!ret) break;\nif (i >= manifest.count) {\nmf: %(m)s}\n',
    'h': 'if (i < manifest.count && ret) {\n%(s)s\ncontinue;\n}\nif (ret) {\nmf: %(m)s}\nbreak;\n',
}
SHAPES = {
    'fora': 'for (;; i += ret != 0) {\n%(d)s\n%(h)s\n%(k)s\n%(b)s\n}\n',
    'forb': 'for (;;) {\n%(d)s\n%(h)s\n%(k)s\n%(snd)s\ni += ret != 0;\n%(fl)s\n}\n',
    'forc': 'for (;;) {\n%(d)s\n%(h)s\n%(k)s\n%(snd)s\n%(fl)s\ni += ret != 0;\n}\n',
    'ford': 'for (;;) {\n%(d)s\n%(h)s\n%(k)s\n%(snd)s\nif (ret) i++; else %(f)s\n}\n',
}
KS = {
    'k1': ('uint32_t k = i;', '', 'k'),
    'k2': ('uint32_t k;', 'k = i;', 'k'),
    'i': ('', '', 'i'),
}
FRAME = g18.FRAME


def variants():
    prep = 'int prepSysex(void)\n{\n' + g10.HEADS['h9'] + g10.TAIL['d'] + '\n}\n'
    for h, s, (kn, (d, k, x)) in itertools.product(HEADS, SHAPES, KS.items()):
        if h == 'h':
            continue
        fl = 'if (!ret) ' + g5.fail(x)
        snd = g5.send(x)
        head = HEADS[h] % {'m': MFH}
        loop = GD + SHAPES[s] % {'d': d, 'h': head, 'k': k, 'b': snd + fl, 'snd': snd, 'fl': fl, 'f': g5.fail(x)}
        yield '%s|%s|%s' % (h, s, kn), prep + FRAME.replace('@LOOP@', loop).replace('@ARMS@', g16.ARMS['ifnot'])
