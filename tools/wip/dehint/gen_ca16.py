"""Chain with the cleanup block (Z) between the guard and the manifest send, polarity `count <= 0`: x prepSysex spelling, to get createSysexDirs' failure forwarder before the OK arm."""
import itertools
from importlib import util
import os

here = os.path.dirname(os.path.abspath(__file__))


def load(n):
    s = util.spec_from_file_location(n, os.path.join(here, n + '.py'))
    m = util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


g5, g10 = load('gen_ca5'), load('gen_ca10')
BODY = r'''
		i = 0;
		do {
			uint32_t k = i;
			log_printf(1, "sending %03d: 0x%08x (%d) bytes, %s\n", i + 1, manifest.e[k].len, manifest.e[k].len, manifest.e[k].path);
			ret = netSendFile(manifest.e[k].path, manifest.e[k].data, manifest.e[k].len);
			if (!ret)
				log_printf(0, "aborting sending avatar data, failed to send %s\n", manifest.e[k].path);
			i += ret != 0;
		} while (i < manifest.count && ret);
'''
ARMS = {
    'ifnot': r'''if (!ok) {
			ret = 0;
			log_printf(0, "aborting sending avatar data, failed to send %s\n", manifest.path);
		} else {
			log_printf(0, "success! Avatar data is successfully sent to the console!\n");
			netTimerEnd();
			ret = 1;
		}''',
    'if': r'''if (ok) {
			log_printf(0, "success! Avatar data is successfully sent to the console!\n");
			netTimerEnd();
			ret = 1;
		} else {
			ret = 0;
			log_printf(0, "aborting sending avatar data, failed to send %s\n", manifest.path);
		}''',
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
			if (manifest.count <= 0)
				goto mf;
			goto loop;
		}
out:
		netUnmount(SYSEX);
		freeManifest();
		return ret;
mf:
		log_printf(1, "sending manifest to %s\n", manifest.path);
		ok = netSendFile(manifest.path, manifest.data, manifest.size);
		goto check;
loop:
@BODY@
		if (ret)
			goto mf;
		goto out;
check:
		@ARMS@
		goto out;
	} else {
		log_printf(0, "***** WARNING: avatar data skipped, unable to load data!\n");
		ret = 1;
	}
	return ret;
}
'''


def variants():
    for h, t, a in itertools.product(g10.HEADS, g10.TAIL, ARMS):
        prep = 'int prepSysex(void)\n{\n' + g10.HEADS[h] + g10.TAIL[t] + '\n}\n'
        yield '%s%s|%s' % (h, t, a), prep + FRAME.replace('@BODY@', BODY).replace('@ARMS@', ARMS[a])
