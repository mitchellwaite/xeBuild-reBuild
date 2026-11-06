# mode_client attempt 4: oneArg spellings (base build/mc/b4f.c): pointer-index form like
# wbArgs/bpArgs/getArgs, and the other one-argument arms (-r, -w, -e, -c) through it.
OLD = '''static char *oneArg(int argc, char **argv, int i, int mode)
{
	if (!argv[i + 1] || i + 1 == argc || *argv[i + 1] == '-')
		client_usage(3, argv[i]);
	if (mode)
		client_usage(5, argv[i]);
	return argv[i + 1];
}
'''
PI = '''static char *oneArg(int argc, char **argv, int *pi, int mode)
{
	int i = *pi;

	if (!argv[i + 1] || i + 1 == argc || *argv[i + 1] == '-')
		client_usage(3, argv[i]);
	if (mode)
		client_usage(5, argv[i]);
	*pi = i + 1;
	return argv[i + 1];
}
'''
CALL_OLD = '\t\t\targ = oneArg(argc, argv, i, mode);\n\t\t\ti++;\n'
CALL_PI = '\t\t\targ = oneArg(argc, argv, &i, mode);\n'
E_OLD = '''			if (!argv[i + 1] || i + 1 == argc || *argv[i + 1] == '-')
				client_usage(3, argv[i]);
			if (mode)
				client_usage(5, argv[i]);
			arg = argv[i + 1];
			i++;
			log_printf(0, "setting avatar'''
E_NEW = '''			arg = oneArg(argc, argv, i, mode);
			i++;
			log_printf(0, "setting avatar'''
C_OLD = '''			if (!argv[i + 1] || i + 1 == argc || *argv[i + 1] == '-')
				client_usage(3, argv[i]);
			if (mode)
				client_usage(5, argv[i]);
			arg = argv[i + 1];
			i++;
			log_printf(0, "setting xbox'''
C_NEW = '''			arg = oneArg(argc, argv, i, mode);
			i++;
			log_printf(0, "setting xbox'''
V = {
    'pi': [(OLD, PI), (CALL_OLD, CALL_PI)],
    'e': [(E_OLD, E_NEW)],
    'c': [(C_OLD, C_NEW)],
    'ec': [(E_OLD, E_NEW), (C_OLD, C_NEW)],
}
