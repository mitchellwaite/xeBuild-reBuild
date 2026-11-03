"""Guard jumps into the loop past its head test: `if (count > 0) goto send; for (;;) { if (i >= count) {MF head} send: ... }`. Loop has two entries until the guard's other edge is threaded out."""
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
    'gt': 'i = 0;\nif (manifest.count > 0) goto send;\n',
    'le': 'i = 0;\nif (manifest.count <= 0) goto top;\ngoto send;\n',
}
TESTS = {
    'ge': 'if (i >= manifest.count) {%(m)s}\n',
    'nlt': 'if (!(i < manifest.count)) {%(m)s}\n',
    'lt': 'if (i < manifest.count) goto send;\n%(m)s\n',
}
TAILS = {
    'brk': '%(snd)s\nif (!ret) {\n%(f)s\nbreak;\n}\ni++;\n',
    'got': '%(snd)s\nif (!ret) {\n%(f)s\ngoto out;\n}\ni++;\n',
    'add': '%(snd)s\nif (!ret) {\n%(f)s\nbreak;\n}\ni += ret != 0;\n',
    'flag': '%(snd)s\nif (!ret) %(f)s\ni += ret != 0;\nif (!ret) break;\n',
}
KS = {
    'i': ('', '', 'i'),
    'k1': ('uint32_t k;', 'k = i;', 'k'),
}
LOOP = {
    'for': 'for (;;) {\n%(d)s\ntop:\n%(t)s\nsend:\n%(k)s\n%(b)s\n}\n',
}


def variants():
    prep = 'int prepSysex(void)\n{\n' + g10.HEADS['h9'] + g10.TAIL['d'] + '\n}\n'
    for g, t, tl, (kn, (d, k, x)) in itertools.product(GD, TESTS, TAILS, KS.items()):
        head = TESTS[t] % {'m': MFH}
        b = TAILS[tl] % {'snd': g5.send(x), 'f': g5.fail(x)}
        loop = GD[g] + LOOP['for'] % {'d': d, 't': head, 'k': k, 'b': b}
        if d:
            # the declaration has to precede the labels' block entry
            loop = d + '\n' + loop.replace(d, '', 1)
        if g == 'gt':
            loop = loop.replace('top:\n', '')
        yield '%s|%s|%s|%s' % (g, t, tl, kn), prep + g18.FRAME.replace('@LOOP@', loop).replace('@ARMS@', g16.ARMS['ifnot'])
