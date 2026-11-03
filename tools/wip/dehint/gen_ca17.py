"""Chain A+guard, prepSysex's inlined blocks (Z), manifest head, loop, arms, cleanup: Z with no new literals, OK arm still falling into the cleanup."""
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
T = {
    'a': 'if (ret)\n\tgoto mf;\ngoto out;',
    'b': 'if (!ret)\n\tgoto out;\ngoto mf;',
}
P = {
    'a': 'if (prepSysex())\n\tgoto ready;\ngoto out;',
    'b': 'if (!prepSysex())\n\tgoto out;\ngoto ready;',
}
G = {
    'a': 'if (manifest.count <= 0)\n\tgoto mf;\ngoto loop;',
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
		goto prep;
ready:
		log_printf(0, "success!\nSending avatar files to HDD partition...\n");
		log_printf(1, "sending %d items to xbox\n", manifest.count);
		@G@
prep:
		@P@
mf:
		log_printf(1, "sending manifest to %s\n", manifest.path);
		ok = netSendFile(manifest.path, manifest.data, manifest.size);
		goto check;
loop:
@BODY@
		@T@
check:
		@ARMS@
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
    for h, t, a, tt, p in itertools.product(['h9', 'h5', 'h1'], ['d', 'a'], g16.ARMS, T, P):
        prep = 'int prepSysex(void)\n{\n' + g10.HEADS[h] + g10.TAIL[t] + '\n}\n'
        src = FRAME.replace('@BODY@', g16.BODY).replace('@ARMS@', g16.ARMS[a]).replace('@T@', T[tt]).replace('@P@', P[p]).replace('@G@', G['a'])
        yield '%s%s|%s|%s|%s' % (h, t, a, tt, p), prep + src
