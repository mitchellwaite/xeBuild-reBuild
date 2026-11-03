"""MATCH shape with `e = &manifest.e[(uint32_t)i]` for k: plainer loop heads, fewer gotos."""
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
    'done': 'static int itemsDone(int i)\n{\n\treturn i >= manifest.count;\n}\n\n',
    'more': 'static int moreItems(int i)\n{\n\treturn i < manifest.count;\n}\n\n',
}
DONE = {'done': 'itemsDone(i)', 'more': '!moreItems(i)'}
MORE = {'done': '!itemsDone(i)', 'more': 'moreItems(i)'}
MFH = r'''
	log_printf(1, "sending manifest to %s\n", manifest.path);
	ok = netSendFile(manifest.path, manifest.data, manifest.size);
	goto check;
'''
SEND = r'''
	e = &manifest.e[(uint32_t)i];
	log_printf(1, "sending %03d: 0x%08x (%d) bytes, %s\n", i + 1, e->len, e->len, e->path);
	ret = netSendFile(e->path, e->data, e->len);
	i += ret != 0;
	if (!ret)
		log_printf(0, "aborting sending avatar data, failed to send %s\n", e->path);
'''
LOOPS = {
    # known good
    'a': 'for (;;) {\nif (%(d)s) {\nif (ret) goto mf;\nbreak;\n}\nif (!ret) break;\ngoto send;\nmf:%(m)s\nsend:%(s)s}\n',
    'b': 'for (;;) {\nif (%(d)s) {\nif (!ret) break;\ngoto mf;\n}\nif (ret) goto send;\nbreak;\nmf:%(m)s\nsend:%(s)s}\n',
    # plainer
    'c': 'for (;;) {\nif (ret && %(n)s) goto send;\nif (!ret) break;\nmf:%(m)s\nsend:%(s)s}\n',
    'd': 'while (ret) {\nif (%(n)s) goto send;\nmf:%(m)s\nsend:%(s)s}\n',
    'e': 'for (;;) {\nif (%(n)s) {\nif (ret) goto send;\nbreak;\n}\nif (!ret) break;\nmf:%(m)s\nsend:%(s)s}\n',
    'f': 'while (1) {\nif (%(d)s) {\nif (ret) goto mf;\nbreak;\n}\nif (ret) goto send;\nbreak;\nmf:%(m)s\nsend:%(s)s}\n',
    'g': 'for (;;) {\nif (!ret) break;\nif (%(n)s) goto send;\nmf:%(m)s\nsend:%(s)s}\n',
    'h': 'do {\nif (%(n)s) goto send;\nif (!ret) break;\nmf:%(m)s\nsend:%(s)s} while (1);\n',
    'i': 'for (;;) {\nif (%(d)s) {\nif (ret) goto mf;\nbreak;\n}\nif (!ret) break;\nif (0) {\nmf:%(m)s}\n%(s)s}\n',
}
GD = {
    'a': 'i = 0;\nif (manifest.count <= 0) goto mf;\n',
    'b': 'i = 0;\nif (manifest.count > 0) ; else goto mf;\n',
}


def variants():
    prep = 'int prepSysex(void)\n{\n' + g10.HEADS['h9'] + g10.TAIL['d'] + '\n}\n\n'
    decl = '__typeof__(manifest.e[0]) *e;\n'
    for hp, l, g in itertools.product(HELP, LOOPS, GD):
        loop = decl + GD[g] + LOOPS[l] % {'d': DONE[hp], 'n': MORE[hp], 'm': MFH, 's': SEND}
        yield '|'.join((hp, l, g)), prep + HELP[hp] + g18.FRAME.replace('@LOOP@', loop).replace('@ARMS@', g16.ARMS['ifnot'])
