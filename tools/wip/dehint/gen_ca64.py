"""Attempt 5: everything after addTitleId in a static helper called once, so the loop's PHIs are numbered above ver's and the frame
(else arm, join, return) stays as it was, which keeps the frequencies. Axes: item x guard x head x bottom x helper's parameters."""
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
FRAME = r'''static long sendItems(const char *dir, uint32_t ver)
{
	int i, n, sent;
	long ret;
@D@
	if (loadManifest(dir, ver)) {
		log_printf(0, "success!\nFormatting HDD partition...\n");
		ret = 1;
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
	} else {
		log_printf(0, "***** WARNING: avatar data skipped, unable to load data!\n");
		ret = 1;
	}
	return ret;
}

long sendAvatarData(const char *dir, uint32_t ver)
{
@BODY@
}
'''
BODIES = {
    'a': r'''	netTimerStart();
	log_printf(0, "loading avatar data...\n");
	ver &= ~0xf;
	addTitleId(ver);
	return sendItems(dir, ver);''',
    'b': r'''	long ret;

	netTimerStart();
	log_printf(0, "loading avatar data...\n");
	ver &= ~0xf;
	addTitleId(ver);
	ret = sendItems(dir, ver);
	return ret;''',
}


def variants():
    for it, gd, h, b, bd in itertools.product(m.ITEMS, GUARDS, ('J', 'J4', 'K', 'B'), m.BOT, BODIES):
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
        src = g.PREP + FRAME.replace('@D@', d).replace('@LOOP@', loop).replace('@BODY@', BODIES[bd])
        yield '|'.join((it, gd, h, b, bd)), src
