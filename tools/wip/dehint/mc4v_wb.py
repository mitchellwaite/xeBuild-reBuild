# mode_client attempt 4: -wb and -bp arms as calls to static helpers (see mc4v_eb.py); base
# build/mc/b4c.c (E(reboot) shape + -eb's oneArg).
WB_OLD = '''		} else if (E(!strnicmp(argv[i], "-wb", 3))) {
			j = i + 1;
			a = argv[j];
			if (j == argc || !a || *a == '-')
				{ client_usage(3, argv[i]); }
			{ int k = i + 2; b = argv[k];
			if (!b || k == argc || *b == '-')
				client_usage(4, argv[i]); }
			start = b;
			if (mode)
				client_usage(5, argv[i]);
			i += 2;
			arg = argv[i - 1];
'''
BP_OLD = '''		} else if (E(!strnicmp(argv[i], "-bp", 3))) {
			if (!argv[i + 1] || i + 1 == argc || *argv[i + 1] == '-')
				client_usage(3, argv[i]);
			__asm__("" :: "a"(i + 1));
			b = argv[i + 2];
			j = i + 2;
			if (j == argc || !b || *b == '-')
				client_usage(4, argv[i]);
			start = b;
			if (mode)
				client_usage(5, argv[i]);
			i = j;
			arg = argv[i - 1];
'''
H_WB = {
 'a': '''static char *wbArgs(int argc, char **argv, int i, int mode, char **arg2)
{
	int j = i + 1;
	char *a = argv[j], *b;

	if (j == argc || !a || *a == '-')
		client_usage(3, argv[i]);
	{ int k = i + 2; b = argv[k];
	if (!b || k == argc || *b == '-')
		client_usage(4, argv[i]); }
	*arg2 = b;
	if (mode)
		client_usage(5, argv[i]);
	return argv[i + 1];
}

''',
 'b': '''static char *wbArgs(int argc, char **argv, int i, int mode, char **arg2)
{
	int j = i + 1, k = i + 2;
	char *a = argv[j], *b = argv[k];

	if (j == argc || !a || *a == '-')
		client_usage(3, argv[i]);
	if (!b || k == argc || *b == '-')
		client_usage(4, argv[i]);
	*arg2 = b;
	if (mode)
		client_usage(5, argv[i]);
	return a;
}

''',
}
H_BP = {
 'a': '''static char *bpArgs(int argc, char **argv, int i, int mode, char **arg2)
{
	char *b;
	int j;

	if (!argv[i + 1] || i + 1 == argc || *argv[i + 1] == '-')
		client_usage(3, argv[i]);
	__asm__("" :: "a"(i + 1));
	b = argv[i + 2];
	j = i + 2;
	if (j == argc || !b || *b == '-')
		client_usage(4, argv[i]);
	*arg2 = b;
	if (mode)
		client_usage(5, argv[i]);
	return argv[i + 1];
}

''',
 'np': '''static char *bpArgs(int argc, char **argv, int i, int mode, char **arg2)
{
	char *b;
	int j;

	if (!argv[i + 1] || i + 1 == argc || *argv[i + 1] == '-')
		client_usage(3, argv[i]);
	b = argv[i + 2];
	j = i + 2;
	if (j == argc || !b || *b == '-')
		client_usage(4, argv[i]);
	*arg2 = b;
	if (mode)
		client_usage(5, argv[i]);
	return argv[i + 1];
}

''',
}
WB_NEW = '''		} else if (!strnicmp(argv[i], "-wb", 3)) {
			arg = wbArgs(argc, argv, i, mode, &start);
			i += 2;
'''
BP_NEW = '''		} else if (!strnicmp(argv[i], "-bp", 3)) {
			arg = bpArgs(argc, argv, i, mode, &start);
			i += 2;
'''
ANCH = 'static char *oneArg('
V = {}
for k, h in H_WB.items():
    V['wb_' + k] = [(WB_OLD, WB_NEW), (ANCH, h + ANCH)]
for k, h in H_BP.items():
    V['bp_' + k] = [(BP_OLD, BP_NEW), (ANCH, h + ANCH)]
    for k2, h2 in H_WB.items():
        V['bp_%s_wb_%s' % (k, k2)] = [(BP_OLD, BP_NEW), (WB_OLD, WB_NEW), (ANCH, h + h2 + ANCH)]
