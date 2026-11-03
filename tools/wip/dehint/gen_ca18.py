"""Manifest head inside the loop, arms after it, in forms where the header gets copied (non-empty latch): the old header is the block after the guard."""
import itertools
from importlib import util
import os

here = os.path.dirname(os.path.abspath(__file__))


def load(n):
    s = util.spec_from_file_location(n, os.path.join(here, n + '.py'))
    m = util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


g5, g10, g16 = load('gen_ca5'), load('gen_ca10'), load('gen_ca16')
MFH = r'''
	log_printf(1, "sending manifest to %s\n", manifest.path);
	ok = netSendFile(manifest.path, manifest.data, manifest.size);
	goto check;
'''
FORMS = {
    'a': 'for (i = 0; ret; %(inc)s) {\n%(d)s\nif (i >= manifest.count) {%(m)s}\n%(k)s\n%(b)s\n}\n',
    'b': 'for (i = 0; ; %(inc)s) {\n%(d)s\nif (!ret) break;\nif (i >= manifest.count) {%(m)s}\n%(k)s\n%(b)s\n}\n',
    'c': 'i = 0;\nwhile (ret) {\n%(d)s\nif (i >= manifest.count) {%(m)s}\n%(k)s\n%(b)s\n%(inc)s;\n}\n',
    'd': 'for (i = 0; ; %(inc)s) {\n%(d)s\nif (i >= manifest.count || !ret) {\nif (ret) {%(m)s}\nbreak;\n}\n%(k)s\n%(b)s\n}\n',
    'e': 'for (i = 0; ; %(inc)s) {\n%(d)s\nif (i >= manifest.count) {\nif (ret) {%(m)s}\nbreak;\n}\nif (!ret) break;\n%(k)s\n%(b)s\n}\n',
    'f': 'for (i = 0; ; %(inc)s) {\n%(d)s\nif (!ret || i >= manifest.count) {\nif (ret) {%(m)s}\nbreak;\n}\n%(k)s\n%(b)s\n}\n',
}
INCS = {'add': 'i += ret != 0', 'tern': 'i = ret ? i + 1 : i', 'plain': 'i++'}
KS = {
    'k1': ('uint32_t k = i;', '', 'k'),
    'k2': ('uint32_t k;', 'k = i;', 'k'),
    'i': ('', '', 'i'),
}
FRAME = r'''
long sendAvatarData(const char *dir, uint32_t ver)
{
	int i;
	long ret;
	int ok;

	netTimerStart();
	log_printf(0, "loading avatar data...\n");
	ver &= ~0xf;
	addTitleId(ver);
	if (loadManifest(dir, ver)) {
		log_printf(0, "success!\nFormatting HDD partition...\n");
		ret = 1;
		if (prepSysex()) {
			log_printf(0, "success!\nSending avatar files to HDD partition...\n");
			log_printf(1, "sending %d items to xbox\n", manifest.count);
@LOOP@
			goto out;
check:
			@ARMS@
		}
out:
		netUnmount(SYSEX);
		freeManifest();
	} else {
		log_printf(0, "***** WARNING: avatar data skipped, unable to load data!\n");
		ret = 1;
	}
	return ret;
}
'''


def variants():
    prep = 'int prepSysex(void)\n{\n' + g10.HEADS['h9'] + g10.TAIL['d'] + '\n}\n'
    for f, inc, (kn, (d, k, x)) in itertools.product(FORMS, INCS, KS.items()):
        b = g5.send(x) + 'if (!ret) ' + g5.fail(x)
        loop = FORMS[f] % {'inc': INCS[inc], 'd': d, 'k': k, 'b': b, 'm': MFH}
        yield '%s|%s|%s' % (f, inc, kn), prep + FRAME.replace('@LOOP@', loop).replace('@ARMS@', g16.ARMS['ifnot'])
