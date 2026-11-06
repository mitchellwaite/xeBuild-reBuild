# mode_client attempt 4: the E() on -bp/-wb/-eb.  With param 50 the expect makes the
# strnicmp test exactly 50%; without it only the else edge (the next strnicmp) gets the call
# heuristic (71%).  The -rb arm is 50% naturally because its first statement is a call
# (getArgs).  These variants start the arm with a call to a static helper that ipa-inline
# (not einline) inlines, so the call is still there at profile_estimate.
EB_OLD = '''		} else if (E(!strnicmp(argv[i], "-eb", 3))) {
			if (!argv[i + 1] || i + 1 == argc || *argv[i + 1] == '-')
				client_usage(3, argv[i]);
			if (mode)
				client_usage(5, argv[i]);
			arg = argv[i + 1];
			i++;
'''
EB_NEW = '''		} else if (!strnicmp(argv[i], "-eb", 3)) {
			arg = oneArg(argc, argv, i, mode);
			i++;
'''
HELPER = '''static char *oneArg(int argc, char **argv, int i, int mode)
{
	if (!argv[i + 1] || i + 1 == argc || *argv[i + 1] == '-')
		client_usage(3, argv[i]);
	if (mode)
		client_usage(5, argv[i]);
	return argv[i + 1];
}

#define E(x)'''
V = {
    'eb_helper': [(EB_OLD, EB_NEW), ('#define E(x)', HELPER)],
    'eb_plain': [('E(!strnicmp(argv[i], "-eb", 3))', '!strnicmp(argv[i], "-eb", 3)')],
}
