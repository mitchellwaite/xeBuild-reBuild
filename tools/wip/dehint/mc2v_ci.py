# clientInfo: shapes for the success!/failed! literal order without the asm "i" hint
HINT = '''		/* .rdata order hint (testing success first flips the branch) */
		__asm__("" :: "i"("success!\\n"));
'''
TAIL = '''		if (!netDumpNand(path))
			log_printf(0, "failed!\\n");
		else
			log_printf(0, "success!\\n");
'''
def tail(new):
    return [(HINT, ''), (TAIL, new)]

V = {
    'nohint': [(HINT, '')],
    'succ_first': tail('''		if (netDumpNand(path))
			log_printf(0, "success!\\n");
		else
			log_printf(0, "failed!\\n");
'''),
    'ternary': tail('''		log_printf(0, netDumpNand(path) ? "success!\\n" : "failed!\\n");
'''),
    'ternary_not': tail('''		log_printf(0, !netDumpNand(path) ? "failed!\\n" : "success!\\n");
'''),
    'msgvar': tail('''		msg = "success!\\n";
		if (!netDumpNand(path))
			msg = "failed!\\n";
		log_printf(0, msg);
'''),
    'msgvar2': tail('''		msg = "failed!\\n";
		if (netDumpNand(path))
			msg = "success!\\n";
		log_printf(0, msg);
'''),
    'retvar': tail('''		i = netDumpNand(path);
		if (i)
			log_printf(0, "success!\\n");
		else
			log_printf(0, "failed!\\n");
'''),
    'retvar_not': tail('''		i = netDumpNand(path);
		if (!i)
			log_printf(0, "failed!\\n");
		else
			log_printf(0, "success!\\n");
'''),
    'early': tail('''		if (!netDumpNand(path)) {
			log_printf(0, "failed!\\n");
			return;
		}
		log_printf(0, "success!\\n");
'''),
    'early_s': tail('''		if (netDumpNand(path)) {
			log_printf(0, "success!\\n");
			return;
		}
		log_printf(0, "failed!\\n");
'''),
    'eq0': tail('''		if (netDumpNand(path) == 0)
			log_printf(0, "failed!\\n");
		else
			log_printf(0, "success!\\n");
'''),
    'ne0': tail('''		if (netDumpNand(path) != 0)
			log_printf(0, "success!\\n");
		else
			log_printf(0, "failed!\\n");
'''),
}
for k in ('msgvar', 'msgvar2'):
    V[k] = V[k] + [('	const char *out = NULL;\n', '	const char *out = NULL, *msg;\n')]

OUTIF = '''	if (out) {
		strcpy(path, dir);'''
OUTEND = '''			log_printf(0, "success!\\n");
	}
}'''
for nm in list(V):
    if nm.startswith(('succ', 'retvar', 'ne0', 'eq0', 'nohint', 'early')):
        V['ret_' + nm] = V[nm] + [(OUTIF, '''	if (!out)
		return;
	{
		strcpy(path, dir);''')]
        V['dirz_' + nm] = V[nm] + [(OUTIF, '''	if (out != NULL) {
		strcpy(path, dir);''')]
        V['bad_' + nm] = V[nm] + [('	if (bad && len) {\n', '	if (bad != NULL && len != 0) {\n')]
        V['strout_' + nm] = V[nm] + [('		strcpy(path, dir);\n', '		strcpy(path, out);\n')]

B = V['ret_succ_first']
INIT = '''	if (dir) {
		log_printf(0, "creating mydata folder output at %s\\n", dir);
		if (createDir(dir))
			out = dir;
		else
			log_printf(0, "unable to dump details to %s, disabling\\n", dir);
	}
'''
V['r2_init_else'] = B + [('	const char *out = NULL;\n', '	const char *out;\n'), (INIT, '''	out = NULL;
''' + INIT)]
V['r2_init_else2'] = B + [('	const char *out = NULL;\n', '	const char *out;\n'), (INIT, '''	if (dir) {
		log_printf(0, "creating mydata folder output at %s\\n", dir);
		if (createDir(dir))
			out = dir;
		else {
			log_printf(0, "unable to dump details to %s, disabling\\n", dir);
			out = NULL;
		}
	} else
		out = NULL;
''')]
V['r2_nodir'] = B + [(INIT, '''	if (dir) {
		log_printf(0, "creating mydata folder output at %s\\n", dir);
		if (!createDir(dir)) {
			log_printf(0, "unable to dump details to %s, disabling\\n", dir);
			dir = NULL;
		}
	}
'''), ('	const char *out = NULL;\n', ''), ('parseConsoleInfo(0, out, out, NULL);', 'parseConsoleInfo(0, dir, dir, NULL);'), ('	if (!out)\n		return;', '	if (!dir)\n		return;')]
V['r2_nobrace'] = B + [('''	if (!out)
		return;
	{
		strcpy(path, dir);''', '''	if (!out)
		return;
		strcpy(path, dir);'''), ('''			log_printf(0, "failed!\\n");
	}
}''', '''			log_printf(0, "failed!\\n");
}''')]
V['r2_eqnull'] = B + [('	if (!out)\n		return;', '	if (out == NULL)\n		return;')]
V['r2_loopwhile'] = B + [('''		for (i = len - 2; i >= 0; i -= 2) {
			log_printf(0, "0x%x", getBeU16(bad + i));
			if (i)
				log_printf(0, ",");
		}''', '''		i = len - 2;
		while (i >= 0) {
			log_printf(0, "0x%x", getBeU16(bad + i));
			if (i)
				log_printf(0, ",");
			i -= 2;
		}''')]
V['r2_loopi'] = B + [('''		for (i = len - 2; i >= 0; i -= 2) {
			log_printf(0, "0x%x", getBeU16(bad + i));
			if (i)
				log_printf(0, ",");
		}''', '''		for (i = len - 2; i >= 0; i -= 2) {
			log_printf(0, "0x%x", getBeU16(bad + i));
			if (i != 0)
				log_printf(0, ",");
		}''')]
V['r2_badscope'] = B + [('	uint8_t *bad;\n	int i;\n', ''), ('	bad = netGetBadBlocks(&len);\n	if (bad && len) {\n', '	{ uint8_t *bad = netGetBadBlocks(&len);\n	if (bad && len) { int i;\n'), ('''				log_printf(0, ",");
		}
	}''', '''				log_printf(0, ",");
		}
	} }''')]
