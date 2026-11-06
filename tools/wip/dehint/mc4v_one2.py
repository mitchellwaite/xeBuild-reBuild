# mode_client attempt 4: other one-argument arms through a helper (base build/mc/b4g.c =
# src after the expect removals).  oneArg itself is not inlined at 3 calls, so each arm gets
# its own copy here (eArg, cArg, rArg, wArg) to see what a call does to each arm.
import runpy, os
W = runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mc4v_one.py'))
H = '''static char *NAME(int argc, char **argv, int *pi, int mode)
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
ANCH = 'static char *oneArg('
def arm(old, name):
    return (old, old.split('\t\t\tif (!argv')[0] + '\t\t\targ = %s(argc, argv, &i, mode);\n\t\t\tlog_printf(0, "setting %s' % (name, old.rsplit('"setting ', 1)[1]))
E_OLD, C_OLD = W['E_OLD'], W['C_OLD']
V = {
    'e': [(E_OLD, '\t\t\targ = eArg(argc, argv, &i, mode);\n\t\t\tlog_printf(0, "setting avatar'), (ANCH, H.replace('NAME', 'eArg') + ANCH)],
    'c': [(C_OLD, '\t\t\targ = cArg(argc, argv, &i, mode);\n\t\t\tlog_printf(0, "setting xbox'), (ANCH, H.replace('NAME', 'cArg') + ANCH)],
}
V['ec'] = V['e'] + [(C_OLD, '\t\t\targ = cArg(argc, argv, &i, mode);\n\t\t\tlog_printf(0, "setting xbox'), (ANCH, H.replace('NAME', 'cArg') + ANCH)]
