"""Attempt 3: natural loops plus inlined helpers (sendItem, sendManifest), which give high SSA
versions and a parameter conversion without itemsDone or a cast. Axes: helper x loop x increment x tail."""
import itertools

PREP = r'''int prepSysex(void)
{
	int r = netFormatSysex();

	if (r) {
		r = netMount(SYSEX, "\\SEP");
		if (!r) {
			log_printf(0, "ERROR: unable to mount sysex partition!\n");
			return 0;
		}
	} else
		log_printf(0, "ERROR: unable to format sysex partition!\n");
	if (r)
		return createSysexDirs();
	return 0;
}

'''
FRAME = r'''long sendAvatarData(const char *dir, uint32_t ver)
{
	int i;
	long ret;
@DECL@
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
@TAIL@
		}
@OUT@
		netUnmount(SYSEX);
		freeManifest();
	} else {
		log_printf(0, "***** WARNING: avatar data skipped, unable to load data!\n");
		ret = 1;
	}
	return ret;
}
'''
LOG = r'log_printf(1, "sending %%03d: 0x%%08x (%%d) bytes, %%s\n", %(n)s, %(e)slen, %(e)slen, %(e)spath);'
SEND = r'ret = netSendFile(%(e)spath, %(e)sdata, %(e)slen);'
FAIL = r'log_printf(0, "aborting sending avatar data, failed to send %%s\n", %(e)spath);'
MFS = r'log_printf(1, "sending manifest to %s\n", manifest.path);'
MFA = r'''if (!netSendFile(manifest.path, manifest.data, manifest.size)) {
	ret = 0;
	log_printf(0, "aborting sending avatar data, failed to send %s\n", manifest.path);
} else {
	log_printf(0, "success! Avatar data is successfully sent to the console!\n");
	netTimerEnd();
	ret = 1;
}'''
MFHELP = r'''static long sendManifest(void)
{
	log_printf(1, "sending manifest to %s\n", manifest.path);
	if (!netSendFile(manifest.path, manifest.data, manifest.size)) {
		log_printf(0, "aborting sending avatar data, failed to send %s\n", manifest.path);
		return 0;
	}
	log_printf(0, "success! Avatar data is successfully sent to the console!\n");
	netTimerEnd();
	return 1;
}

'''


def helper(kind):
    """returns (helper text, body that sends item i and sets ret, whether it logs the failure)"""
    v = {'n': 'i + 1', 'e': 'manifest.e[i].'}
    if kind == 'inl':
        return '', LOG % v + '\n' + SEND % v + '\n', False, FAIL % v
    if kind == 'ptr':
        w = {'n': 'i + 1', 'e': 'e->'}
        return '', 'struct manifestItem *e = &manifest.e[i];\n' + LOG % w + '\n' + SEND % w + '\n', False, FAIL % w
    w = {'n': 'n', 'e': 'e->'}
    if kind in ('ii', 'iu', 'is'):
        ty = {'ii': 'int', 'iu': 'uint32_t', 'is': 'size_t'}[kind]
        w['n'] = 'i + 1'
        h = 'static long sendItem(%s i)\n{\n\tstruct manifestItem *e = &manifest.e[i];\n\tlong ret;\n\n\t' % ty
        h += LOG % w + '\n\t' + SEND % w + '\n\tif (!ret)\n\t\t' + FAIL % w + '\n\treturn ret;\n}\n\n'
        return h, 'ret = sendItem(i);\n', True, ''
    if kind in ('pn', 'pn0'):
        h = 'static long sendItem(struct manifestItem *e, int n)\n{\n\tlong ret;\n\n\t'
        h += LOG % w + '\n\t' + SEND % w + '\n\tif (!ret)\n\t\t' + FAIL % w + '\n\treturn ret;\n}\n\n'
        return h, 'ret = sendItem(&manifest.e[i], i + 1);\n', True, ''
    if kind == 'pnr':  # helper without the log, caller logs the failure
        h = 'static long sendItem(struct manifestItem *e, int n)\n{\n\t' + LOG % w + '\n\treturn netSendFile(e->path, e->data, e->len);\n}\n\n'
        return h, 'ret = sendItem(&manifest.e[i], i + 1);\n', False, FAIL % {'e': 'manifest.e[i].'}
    raise KeyError(kind)


HELP = ['inl', 'ptr', 'ii', 'iu', 'is', 'pn', 'pnr']
LOOPS = {
    'wia': 'i = 0;\nwhile (i < manifest.count && ret) {\n%s}\n',
    'wri': 'i = 0;\nwhile (ret && i < manifest.count) {\n%s}\n',
    'fia': 'for (i = 0; i < manifest.count && ret;) {\n%s}\n',
    'fri': 'for (i = 0; ret && i < manifest.count;) {\n%s}\n',
    'dga': 'if (manifest.count > 0) {\ni = 0;\ndo {\n%s} while (i < manifest.count && ret);\n}\n',
    'dgr': 'if (manifest.count > 0) {\ni = 0;\ndo {\n%s} while (ret && i < manifest.count);\n}\n',
    'dg0': 'i = 0;\nif (manifest.count > 0) {\ndo {\n%s} while (i < manifest.count && ret);\n}\n',
}
INC = {
    'ifel': 'if (ret)\ni++;\nelse\n%(f)s\n',
    'nifel': 'if (!ret)\n%(f)s\nelse\ni++;\n',
    'ifif': 'if (ret)\ni++;\nif (!ret)\n%(f)s\n',
    'ififr': 'if (!ret)\n%(f)s\nif (ret)\ni++;\n',
    'add': 'i += ret != 0;\nif (!ret)\n%(f)s\n',
    'addl': 'if (!ret)\n%(f)s\ni += ret != 0;\n',
}
TAIL = {
    'if': 'if (ret) {\n' + MFS + '\n' + MFA + '\n}\n',
    'goto': 'if (!ret)\ngoto out;\n' + MFS + '\n' + MFA + '\n',
    'help': 'if (ret)\nret = sendManifest();\n',
    'help2': 'if (ret && !sendManifest())\nret = 0;\n',
}


def variants():
    for h, l, inc, t in itertools.product(HELP, LOOPS, INC, TAIL):
        ht, body, logged, f = helper(h)
        if logged:
            if inc not in ('ifel',):
                # helper logs: only the increment forms differ
                inctext = {'ifif': None}.get(inc, None)
                if inc == 'add':
                    b = body + 'i += ret != 0;\n'
                elif inc == 'nifel':
                    b = body + 'if (!ret)\nbreak;\ni++;\n'
                else:
                    continue
            else:
                b = body + 'if (ret)\ni++;\n'
        else:
            b = body + INC[inc] % {'f': f}
        src = PREP + ht + (MFHELP if t.startswith('help') else '')
        src += FRAME.replace('@DECL@', '').replace('@LOOP@', LOOPS[l] % b).replace('@TAIL@', TAIL[t]).replace('@OUT@', 'out:' if t == 'goto' else '')
        yield '|'.join((h, l, inc, t)), src
