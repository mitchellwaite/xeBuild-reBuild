"""Attempt 5: the helper takes everything from prepSysex to the cleanup, so the arms join a real block, not the return block
(no early-return predictor on the manifest failure). Axes: item x guard x head x bottom x where the first log sits."""
import itertools, os
from importlib import util

here = os.path.dirname(os.path.abspath(__file__))
s = util.spec_from_file_location('gen_ca61', os.path.join(here, 'gen_ca61.py'))
m = util.module_from_spec(s)
s.loader.exec_module(m)
g = m.g
GUARDS = {
    'none': ('i = 0;\nn = manifest.count;\n', ''),
    'le': ('i = 0;\nn = manifest.count;\nif (n <= 0)\ngoto send;\n', 'send:\n'),
}
FRAME = r'''static long sendItems(void)
{
	int i, n, sent;
	long ret;
@D@
@LOGA@	ret = 1;
	if (prepSysex()) {
		log_printf(0, "success!\nSending avatar files to HDD partition...\n");
		log_printf(1, "sending %d items to xbox\n", manifest.count);
@LOOP@
		if (!sent) {
			ret = 0;
			log_printf(0, "aborting sending avatar data, failed to send %s\n", manifest.path);
		} else {
			log_printf(0, "success! Avatar data is successfully sent to the console!\n");
			netTimerEnd();
			ret = 1;
		}
	}
out:
	netUnmount(SYSEX);
	freeManifest();
	return ret;
}

long sendAvatarData(const char *dir, uint32_t ver)
{
	long ret;

	netTimerStart();
	log_printf(0, "loading avatar data...\n");
	ver &= ~0xf;
	addTitleId(ver);
	if (loadManifest(dir, ver)) {
@LOGB@		ret = sendItems();
	} else {
		log_printf(0, "***** WARNING: avatar data skipped, unable to load data!\n");
		ret = 1;
	}
	return ret;
}
'''
LOG = r'''	log_printf(0, "success!\nFormatting HDD partition...\n");
'''


def variants():
    for it, gd, h, b, lg in itertools.product(m.ITEMS, GUARDS, ('J', 'J4', 'K', 'B'), m.BOT, ('in', 'out')):
        if h == 'B' and gd == 'le':
            continue
        v, decl, d = m.ITEMS[it]
        init, label = GUARDS[gd]
        st = g.MFS + '\nsent = ' + m.MFCALL + ';\nbreak;\n'
        hd = m.HEADS[h].replace('@O@', 'goto out;')
        if h == 'B':
            hd = hd.replace('@S@', st)
            mid = ''
            it0 = ''
        else:
            mid = label + st
            it0 = 'item:;\n'
        body = it0 + decl + g.LOG % v + '\n' + g.SEND % v + '\n' + m.BOT[b] % {'f': g.FAIL % v}
        loop = init + 'for (;;) {\n' + hd + mid + body + '}\n'
        src = g.PREP + FRAME.replace('@D@', d).replace('@LOOP@', loop).replace('@LOGA@', LOG if lg == 'in' else '').replace('@LOGB@', LOG if lg == 'out' else '')
        yield '|'.join((it, gd, h, b, lg)), src
