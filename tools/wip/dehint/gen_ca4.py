"""Flag-driven loops: i only advances on success, so scev sees PHI<i, i+1> until dom3 threads it."""
import itertools

PREP = r'''
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
'''

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

SEND = r'''
	log_printf(1, "sending %03d: 0x%08x (%d) bytes, %s\n", i + 1, manifest.e[i].len, manifest.e[i].len, manifest.e[i].path);
	ret = netSendFile(manifest.e[i].path, manifest.e[i].data, manifest.e[i].len);
'''
FAIL = 'log_printf(0, "aborting sending avatar data, failed to send %s\\n", manifest.e[i].path);'

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

# advance + failure inside the loop; `fi`: failure logged in the loop
INNER = {
    'ifelse': SEND + 'if (ret) i++; else ' + FAIL,
    'ifnot': SEND + 'if (!ret) ' + FAIL + ' else i++;',
    'if2': SEND + 'if (!ret) ' + FAIL + '\nif (ret) i++;',
    'if2b': SEND + 'if (ret) i++;\nif (!ret) ' + FAIL,
    'brk': SEND + 'if (!ret) { ' + FAIL + ' break; }\ni++;',
    'add': SEND + 'if (!ret) ' + FAIL + '\ni += ret != 0;',
}
INNER_OUT = {
    'ifa': SEND + 'if (ret) i++;',
    'brka': SEND + 'if (!ret) break;\ni++;',
    'adda': SEND + 'i += ret != 0;',
}
CONDS = {
    'ret_i': 'ret && i < manifest.count',
    'i_ret': 'i < manifest.count && ret',
}
FORMS = {
    'wh': 'i = 0;\nwhile (%(c)s) {\n%(b)s\n}\n',
    'for': 'for (i = 0; %(c)s; ) {\n%(b)s\n}\n',
    'gd': 'if (manifest.count > 0) {\ni = 0;\ndo {\n%(b)s\n} while (%(c)s);\n}\n',
    'gd1': 'i = 0;\nif (manifest.count > 0) do {\n%(b)s\n} while (%(c)s);\n',
}
TAILS = {
    'ifret': 'if (ret) {\n' + MF + '\n}',
    'ifnot': 'if (!ret) ' + FAIL + '\nelse {\n' + MF + '\n}',
    'if0': 'if (ret == 0) ;\nelse {\n' + MF + '\n}',
    'ieq': 'if (i >= manifest.count) {\n' + MF + '\n}',
}


def variants():
    for (bn, b), c, f, t in itertools.product(list(INNER.items()) + list(INNER_OUT.items()), CONDS, FORMS, TAILS):
        out = bn in INNER_OUT
        if out != (t == 'ifnot'):
            continue
        loop = FORMS[f] % {'c': CONDS[c], 'b': b.replace('%', '%')}
        yield '%s|%s|%s|%s' % (bn, c, f, t), PREP + HEAD.replace('@LOOP@', loop).replace('@TAIL@', TAILS[t])
