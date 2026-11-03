"""Flag-driven loops x separate index local x tails x prepSysex spelling."""
import itertools

PREPS = {
    'p0': r'''
int prepSysex(void)
{
	if (netFormatSysex()) {
		if (netMount(SYSEX, "\\SEP"))
			return createSysexDirs();
		log_printf(0, "ERROR: unable to mount sysex partition!\n");
	} else
		log_printf(0, "ERROR: unable to format sysex partition!\n");
	return 0;
}
''',
    'p1': r'''
int prepSysex(void)
{
	if (!netFormatSysex()) {
		log_printf(0, "ERROR: unable to format sysex partition!\n");
		return 0;
	}
	if (!netMount(SYSEX, "\\SEP")) {
		log_printf(0, "ERROR: unable to mount sysex partition!\n");
		return 0;
	}
	return createSysexDirs();
}
''',
}

HEAD = r'''
long sendAvatarData(const char *dir, uint32_t ver)
{
	int i;
	long ret;

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
		netUnmount(SYSEX);
		freeManifest();
	} else {
		log_printf(0, "***** WARNING: avatar data skipped, unable to load data!\n");
		ret = 1;
	}
	return ret;
}
'''

KS = {
    'i': ('', 'i'),
    'u': ('uint32_t k = i;', 'k'),
    'n': ('int k = i;', 'k'),
}


def send(x):
    return r'''
	log_printf(1, "sending %%03d: 0x%%08x (%%d) bytes, %%s\n", i + 1, manifest.e[X].len, manifest.e[X].len, manifest.e[X].path);
	ret = netSendFile(manifest.e[X].path, manifest.e[X].data, manifest.e[X].len);
'''.replace('X', x).replace('%%', '%')


def fail(x):
    return 'log_printf(0, "aborting sending avatar data, failed to send %s\\n", manifest.e[' + x + '].path);'


INNER = {
    'add': lambda x: 'if (!ret) ' + fail(x) + '\ni += ret != 0;',
    'addb': lambda x: 'i += ret != 0;\nif (!ret) ' + fail(x),
    'ifelse': lambda x: 'if (ret) i++; else ' + fail(x),
    'ifnot': lambda x: 'if (!ret) ' + fail(x) + ' else i++;',
    'if2': lambda x: 'if (!ret) ' + fail(x) + '\nif (ret) i++;',
    'if2b': lambda x: 'if (ret) i++;\nif (!ret) ' + fail(x),
}
CONDS = {'i_ret': 'i < manifest.count && ret', 'ret_i': 'ret && i < manifest.count', 'and': '(i < manifest.count) & (ret != 0)'}
FORMS = {
    'wh': 'i = 0;\nwhile (%(c)s) {\n%(b)s\n}\n',
    'for': 'for (i = 0; %(c)s; ) {\n%(b)s\n}\n',
    'gd': 'if (manifest.count > 0) {\ni = 0;\ndo {\n%(b)s\n} while (%(c)s);\n}\n',
    'gd1': 'i = 0;\nif (manifest.count > 0) do {\n%(b)s\n} while (%(c)s);\n',
}
MF = r'''
	log_printf(1, "sending manifest to %s\n", manifest.path);
	if (!netSendFile(manifest.path, manifest.data, manifest.size)) {
		ret = 0;
		log_printf(0, "aborting sending avatar data, failed to send %s\n", manifest.path);
	} else {
		log_printf(0, "success! Avatar data is successfully sent to the console!\n");
		netTimerEnd();
		ret = 1;
	}
'''
TAILS = {
    'ifret': 'if (ret) {\n' + MF + '\n}',
    'ieq': 'if (i >= manifest.count) {\n' + MF + '\n}',
}


def variants():
    for k, (bn, b), c, f, t, p in itertools.product(KS, INNER.items(), CONDS, FORMS, TAILS, PREPS):
        decl, x = KS[k]
        body = decl + send(x) + b(x)
        loop = FORMS[f] % {'c': CONDS[c], 'b': body}
        yield '%s|%s|%s|%s|%s|%s' % (k, bn, c, f, t, p), PREPS[p] + HEAD.replace('@LOOP@', loop).replace('@TAIL@', TAILS[t])
