"""prepSysex spellings (mount failure colder than createSysexDirs) x tails/loops around the 12-line shape."""
import itertools

FMT = 'log_printf(0, "ERROR: unable to format sysex partition!\\n");'
MNT = 'log_printf(0, "ERROR: unable to mount sysex partition!\\n");'
PREPS = {
    'p0': 'if (netFormatSysex()) {\nif (netMount(SYSEX, "\\\\SEP"))\nreturn createSysexDirs();\n' + MNT + '\n} else\n' + FMT + '\nreturn 0;',
    'p1': 'if (!netFormatSysex()) {\n' + FMT + '\nreturn 0;\n}\nif (!netMount(SYSEX, "\\\\SEP")) {\n' + MNT + '\nreturn 0;\n}\nreturn createSysexDirs();',
    'p2': 'if (netFormatSysex()) {\nif (!netMount(SYSEX, "\\\\SEP")) {\n' + MNT + '\nreturn 0;\n}\nreturn createSysexDirs();\n}\n' + FMT + '\nreturn 0;',
    'p3': 'int ret = 0;\nif (netFormatSysex()) {\nif (netMount(SYSEX, "\\\\SEP"))\nret = createSysexDirs();\nelse\n' + MNT + '\n} else\n' + FMT + '\nreturn ret;',
    'p4': 'if (!netFormatSysex()) {\n' + FMT + '\n} else {\nif (netMount(SYSEX, "\\\\SEP"))\nreturn createSysexDirs();\n' + MNT + '\n}\nreturn 0;',
    'p5': 'if (!netFormatSysex())\n' + FMT + '\nelse if (!netMount(SYSEX, "\\\\SEP"))\n' + MNT + '\nelse\nreturn createSysexDirs();\nreturn 0;',
    'p6': 'if (netFormatSysex()) {\nif (!netMount(SYSEX, "\\\\SEP"))\n' + MNT + '\nelse\nreturn createSysexDirs();\n} else\n' + FMT + '\nreturn 0;',
    'p7': 'int ret = 0;\nif (!netFormatSysex())\n' + FMT + '\nelse if (!netMount(SYSEX, "\\\\SEP"))\n' + MNT + '\nelse\nret = createSysexDirs();\nreturn ret;',
    'p8': 'if (netFormatSysex()) {\nif (netMount(SYSEX, "\\\\SEP")) {\nif (createSysexDirs())\nreturn 1;\nreturn 0;\n}\n' + MNT + '\n} else\n' + FMT + '\nreturn 0;',
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

SEND = r'''
	uint32_t k = i;
	log_printf(1, "sending %03d: 0x%08x (%d) bytes, %s\n", i + 1, manifest.e[k].len, manifest.e[k].len, manifest.e[k].path);
	ret = netSendFile(manifest.e[k].path, manifest.e[k].data, manifest.e[k].len);
'''
FAIL = 'log_printf(0, "aborting sending avatar data, failed to send %s\\n", manifest.e[k].path);'
INNER = {
    'ifelse': 'if (ret) i++; else ' + FAIL,
    'ifnot': 'if (!ret) ' + FAIL + ' else i++;',
    'add': 'if (!ret) ' + FAIL + '\ni += ret != 0;',
}
CONDS = {'and': '(i < manifest.count) & (ret != 0)', 'i_ret': 'i < manifest.count && ret'}
FORMS = {
    'gd': 'if (manifest.count > 0) {\ni = 0;\ndo {\n%(b)s\n} while (%(c)s);\n}\n',
    'gd1': 'i = 0;\nif (manifest.count > 0) do {\n%(b)s\n} while (%(c)s);\n',
    'gd2': 'if (manifest.count > 0) {\ni = 0;\ndo {\n%(b)s\n} while (%(c)s);\nif (!ret) goto out;\n}\n',
    'gd3': 'if (manifest.count > 0) {\ni = 0;\ndo {\n%(b)s\n} while (%(c)s);\nif (ret) goto mf;\ngoto out;\n}\nmf:\n',
    'lt': 'if (0 < manifest.count) {\ni = 0;\ndo {\n%(b)s\n} while (%(c)s);\n}\n',
    'ge': 'if (manifest.count >= 1) {\ni = 0;\ndo {\n%(b)s\n} while (%(c)s);\n}\n',
    'le': 'if (manifest.count <= 0) ;\nelse {\ni = 0;\ndo {\n%(b)s\n} while (%(c)s);\n}\n',
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
    'gotoout': 'if (!ret) goto out;\n' + MF,
    'plain': MF,
}


def variants():
    for p, (bn, b), c, f, t in itertools.product(PREPS, INNER.items(), CONDS, FORMS, TAILS):
        if (f in ('gd2', 'gd3')) != (t == 'plain'):
            continue
        prep = 'int prepSysex(void)\n{\n' + PREPS[p] + '\n}\n'
        loop = FORMS[f] % {'c': CONDS[c], 'b': SEND + b}
        yield '%s|%s|%s|%s|%s' % (p, bn, c, f, t), prep + HEAD.replace('@LOOP@', loop).replace('@TAIL@', TAILS[t])
