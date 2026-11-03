"""gen_ca19 with the guard jumping to a post-loop test that keeps i live past pre: forwarders into the manifest head can't tail-merge, so it stays lexically after the loop test."""
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
GD = 'i = 0;\nif (manifest.count <= 0) goto t;\n'
TS = {
    'and': 'i >= manifest.count && ret',
    'rev': 'ret && i >= manifest.count',
    'bit': '(i >= manifest.count) & (ret != 0)',
    'bit2': '(ret != 0) & (i >= manifest.count)',
}
HEADS = {
    'a': 'if (i >= manifest.count || !ret) {\nt:\nif (%(t)s) {%(m)s}\nbreak;\n}\n',
    'b': 'if (!ret || i >= manifest.count) {\nt:\nif (%(t)s) {%(m)s}\nbreak;\n}\n',
    'c': 'if (i < manifest.count && ret) goto s;\nt:\nif (%(t)s) {%(m)s}\nbreak;\ns:\n',
    'd': 'if ((i >= manifest.count) | !ret) {\nt:\nif (%(t)s) {%(m)s}\nbreak;\n}\n',
}
SHAPES = {
    'fora': 'for (;; i += ret != 0) {\n%(d)s\n%(h)s\n%(k)s\n%(snd)s\n%(fl)s\n}\n',
    'forb': 'for (;;) {\n%(d)s\n%(h)s\n%(k)s\n%(snd)s\ni += ret != 0;\n%(fl)s\n}\n',
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
    for h, t, s, (kn, (d, k, x)) in itertools.product(HEADS, TS, SHAPES, KS.items()):
        fl = 'if (!ret) ' + g5.fail(x)
        head = HEADS[h] % {'m': MFH, 't': TS[t]}
        loop = GD + SHAPES[s] % {'d': d, 'h': head, 'k': k, 'snd': g5.send(x), 'fl': fl, 'f': g5.fail(x)}
        yield '%s|%s|%s|%s' % (h, t, s, kn), prep + FRAME.replace('@LOOP@', loop).replace('@ARMS@', g16.ARMS['ifnot'])
