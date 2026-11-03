"""Attempt 5: the send loop in a static helper called once, so its PHIs get versions above ver's when it's inlined (gen_ca59: the
PHIs vrp1 frees are what ch2 hands addTitleId's copied load). Axes: guard x head x bottom x item x how failure leaves x what the helper holds."""
import itertools, os
from importlib import util

here = os.path.dirname(os.path.abspath(__file__))


def load(n):
    s = util.spec_from_file_location(n, os.path.join(here, n + '.py'))
    m = util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


g, g31, g45 = load('gen_ca30'), load('gen_ca31'), load('gen_ca45')
MFF, ARMS_OK, MFCALL = g31.MFF, g31.ARMS_OK, g31.MFCALL
ITEMS = {'cast': g45.ITEMS['cast'], 'k': g45.ITEMS['k'], 'ptr': g45.ITEMS['ptr']}
GUARD = {
    'none': ('i = 0;\nn = manifest.count;\nret = 1;\n', ''),
    'le': ('i = 0;\nn = manifest.count;\nret = 1;\nif (n <= 0)\ngoto send;\n', 'send:\n'),
}
HEADS = {
    'J': 'if (i < n) {\nif (ret)\ngoto item;\n@O@\n}\nif (!ret)\n@O@\n',
    'J4': 'if (i >= n) {\nif (!ret)\n@O@\n} else {\nif (ret)\ngoto item;\n@O@\n}\n',
    'K': 'if (i < n && ret)\ngoto item;\nif (!ret)\n@O@\n',
    'B': 'if (i >= n) {\nif (!ret)\n@O@\n@S@\n}\nif (!ret)\n@O@\n',
}
BOT = {
    'Nadd': 'n = manifest.count;\ni += ret != 0;\nif (!ret)\n%(f)s\n',
    'add': 'i += ret != 0;\nn = manifest.count;\nif (!ret)\n%(f)s\n',
}
OUTS = {'r0': 'return 0;', 'rr': 'return ret;'}
KIND = {
    # helper returns the whole result
    'whole': 'if (prepSysex())\nret = sendItems();\n',
    'wholer': 'if (prepSysex())\nreturn_me\n',
}
TAIL = {
    's0': ('if (!sent) {\n' + MFF + 'return 0;\n}\n' + ARMS_OK.replace('ret = 1;\n', '') + 'return 1;\n'),
    's1': ('if (sent) {\n' + ARMS_OK.replace('ret = 1;\n', '') + 'return 1;\n}\n' + MFF + 'return 0;\n'),
    's2': ('if (!sent) {\nret = 0;\n' + MFF + '} else {\n' + ARMS_OK + '}\nreturn ret;\n'),
}
FRAME = r'''static long sendItems(void)
{
	int i, n, sent;
	long ret;
@D@
	log_printf(0, "success!\nSending avatar files to HDD partition...\n");
	log_printf(1, "sending %d items to xbox\n", manifest.count);
@LOOP@
@TAIL@
}

long sendAvatarData(const char *dir, uint32_t ver)
{
	long ret;

	netTimerStart();
	log_printf(0, "loading avatar data...\n");
	ver &= ~0xf;
	addTitleId(ver);
	if (loadManifest(dir, ver)) {
		log_printf(0, "success!\nFormatting HDD partition...\n");
		ret = 1;
		if (prepSysex())
			ret = sendItems();
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
    for it, gd, h, b, o, t in itertools.product(ITEMS, GUARD, HEADS, BOT, OUTS, TAIL):
        v, decl, d = ITEMS[it]
        init, label = GUARD[gd]
        if h == 'B' and gd == 'le':
            continue
        s = g.MFS + '\nsent = ' + MFCALL + ';\nbreak;\n'
        hd = HEADS[h].replace('@O@', OUTS[o])
        if '@S@' in hd:
            hd = hd.replace('@S@', label + s)
            mid = ''
        else:
            mid = label + s
        item = 'item:\n' if 'goto item' in hd else ''
        if item and decl.startswith('uint32_t'):
            item = 'item:;\n'
        body = item + decl + g.LOG % v + '\n' + g.SEND % v + '\n' + BOT[b] % {'f': g.FAIL % v}
        loop = init + 'for (;;) {\n' + hd + mid + body + '}\n'
        src = g.PREP + FRAME.replace('@D@', d).replace('@LOOP@', loop).replace('@TAIL@', TAIL[t])
        yield '|'.join((it, gd, h, b, o, t)), src
