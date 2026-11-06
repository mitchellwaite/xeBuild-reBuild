# mode_client attempt 5: -i / -p arms through a getArgs-style helper that returns the
# default (dummy) when the argument is missing; the "d"(i + 1) pins dropped.
# Base: src/mode_client.c.
I_OLD = '''			if (!argv[i + 1] || i + 1 == argc || ({ __asm__ ("" :: "d"(i + 1)); 0; }) || *argv[i + 1] == '-')
				arg = dummy;
			else {
				arg = argv[i + 1];
				i++;
				log_printf(0, "info dump path set to %s\\n", arg);
			}
			mode = 12;'''
P_OLD = '''			if (!argv[i + 1] || i + 1 == argc || ({ __asm__ ("" :: "d"(i + 1)); 0; }) || *argv[i + 1] == '-')
				arg = dummy;
			else {
				arg = argv[i + 1];
				i++;
				log_printf(0, "patch file set to %s\\n", arg);
			}
			mode = 7;'''


def arm(fn, msg, mode, form):
    if form == 'ne':
        return ('\t\t\targ = %s(argc, argv, &i, dummy);\n\t\t\tif (arg != dummy)\n'
                '\t\t\t\tlog_printf(0, "%s set to %%s\\n", arg);\n\t\t\tmode = %d;' % (fn, msg, mode))
    if form == 'eq':
        return ('\t\t\targ = %s(argc, argv, &i, dummy);\n\t\t\tif (arg == dummy)\n\t\t\t\t;\n\t\t\telse\n'
                '\t\t\t\tlog_printf(0, "%s set to %%s\\n", arg);\n\t\t\tmode = %d;' % (fn, msg, mode))
    if form == 'msg':
        return ('\t\t\targ = %s(argc, argv, &i, dummy, "%s set to %%s\\n");\n\t\t\tmode = %d;' % (fn, msg, mode))


HELP = {
    'a': '''static char *%s(int argc, char **argv, int *pi, char *def)
{
	int i = *pi;

	if (!argv[i + 1] || i + 1 == argc || *argv[i + 1] == '-')
		return def;
	*pi = i + 1;
	return argv[i + 1];
}

''',
    'b': '''static char *%s(int argc, char **argv, int *pi, char *def)
{
	int i = *pi;
	char *a = argv[i + 1];

	if (!a || i + 1 == argc || *a == '-')
		return def;
	*pi = i + 1;
	return a;
}

''',
    'm': '''static char *%s(int argc, char **argv, int *pi, char *def, const char *msg)
{
	int i = *pi;

	if (!argv[i + 1] || i + 1 == argc || *argv[i + 1] == '-')
		return def;
	*pi = i + 1;
	log_printf(0, msg, argv[i + 1]);
	return argv[i + 1];
}

''',
}
ANCHOR = 'int mode_client(int argc, char **argv)\n'
V = {}
for h in 'abm':
    forms = ['msg'] if h == 'm' else ['ne', 'eq']
    for form in forms:
        for inl in ('', 'inline '):
            # shared helper
            hs = HELP[h] % 'optArg'
            if inl:
                hs = hs.replace('static char', 'static inline char')
            V['sh_%s_%s%s' % (h, form, '_i' if inl else '')] = [
                (ANCHOR, hs + ANCHOR),
                (I_OLD, arm('optArg', 'info dump path', 12, form)),
                (P_OLD, arm('optArg', 'patch file', 7, form))]
            # one arm only (keeps the other arm's pin)
            V['i_%s_%s%s' % (h, form, '_i' if inl else '')] = [
                (ANCHOR, hs + ANCHOR), (I_OLD, arm('optArg', 'info dump path', 12, form))]
            V['p_%s_%s%s' % (h, form, '_i' if inl else '')] = [
                (ANCHOR, hs + ANCHOR), (P_OLD, arm('optArg', 'patch file', 7, form))]
