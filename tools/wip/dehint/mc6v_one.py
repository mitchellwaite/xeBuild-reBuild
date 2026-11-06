# mode_client attempt 6: -e through oneArg (attempt 5: 6 lines, the -w arm's ifcombine
# name order) with oneArg's body respelled, to change which SSA names the inlined body
# releases before ifcombine.  Base: src/mode_client.c.  Use with mc2try.py.
import itertools

ONE_OLD = '''static char *oneArg(int argc, char **argv, int *pi, int mode)
{
	int i = *pi;

	if (!argv[i + 1] || i + 1 == argc || *argv[i + 1] == '-')
		client_usage(3, argv[i]);
	if (mode)
		client_usage(5, argv[i]);
	*pi = i + 1;
	return argv[i + 1];
}'''
E_OLD = '''			if (!argv[i + 1] || i + 1 == argc || *argv[i + 1] == '-')
				client_usage(3, argv[i]);
			if (mode)
				client_usage(5, argv[i]);
			arg = argv[i + 1];
			i++;
			log_printf(0, "setting avatar'''
E_NEW = '''			arg = oneArg(argc, argv, &i, mode);
			log_printf(0, "setting avatar'''
C_OLD = E_OLD.replace('setting avatar', 'setting xbox')
C_NEW = E_NEW.replace('setting avatar', 'setting xbox')

# body pieces
DECL = {
    'i': '\tint i = *pi;\n',
    'ij': '\tint i = *pi;\n\tint j = i + 1;\n',
    'ia': '\tint i = *pi;\n\tchar *a = argv[i + 1];\n',
    'ija': '\tint i = *pi;\n\tint j = i + 1;\n\tchar *a = argv[j];\n',
}
TEST = {
    # name: (needs, text)
    'x': (None, "\tif (!argv[i + 1] || i + 1 == argc || *argv[i + 1] == '-')\n"),
    'xj': ('j', "\tif (!argv[j] || j == argc || *argv[j] == '-')\n"),
    'xa': ('a', "\tif (!a || i + 1 == argc || *a == '-')\n"),
    'xja': ('ja', "\tif (!a || j == argc || *a == '-')\n"),
    'yja': ('ja', "\tif (j == argc || !a || *a == '-')\n"),
    'ya': ('a', "\tif (i + 1 == argc || !a || *a == '-')\n"),
}
TAIL = {
    't0': '\t*pi = i + 1;\n\treturn argv[i + 1];\n',
    't1': '\t*pi = i + 1;\n\treturn argv[*pi];\n',
    't2': None,  # j / a forms below
    't3': '\ti++;\n\t*pi = i;\n\treturn argv[i];\n',
}


def bodies():
    out = {}
    for dn, d in DECL.items():
        for tn, (need, t) in TEST.items():
            if need == 'j' and 'j' not in dn:
                continue
            if need == 'a' and 'a' not in dn:
                continue
            if need == 'ja' and dn != 'ija':
                continue
            tails = dict(TAIL)
            tails['t2'] = None
            if 'j' in dn:
                tails['tj'] = '\t*pi = j;\n\treturn argv[j];\n'
            if 'a' in dn:
                tails['ta'] = '\t*pi = i + 1;\n\treturn a;\n'
            for an, tl in tails.items():
                if tl is None:
                    continue
                for mn in ('m0', 'm1'):
                    u = '\t\tclient_usage(3, argv[i]);\n'
                    m = '\tif (mode)\n\t\tclient_usage(5, argv[i]);\n'
                    if mn == 'm0':
                        body = d + '\n' + t + u + m + tl
                    else:
                        # tail first, then mode test (pi updated before the check)
                        if an in ('t3',):
                            continue
                        body = d + '\n' + t + u + tl.split('\treturn')[0] + m + '\treturn' + tl.split('\treturn')[1]
                    out['%s_%s_%s_%s' % (dn, tn, an, mn)] = body
    return out


V = {}
for k, b in bodies().items():
    new = 'static char *oneArg(int argc, char **argv, int *pi, int mode)\n{\n' + b + '}'
    V['e_' + k] = [(ONE_OLD, new), (E_OLD, E_NEW)]
    V['c_' + k] = [(ONE_OLD, new), (C_OLD, C_NEW)]
    V['n_' + k] = [(ONE_OLD, new)]

# -r / -w arms through oneArg (second call site), with oneArg's body variants
W_OLD = '''			a = argv[i + 1];
			if (i + 1 == argc || !a || *a == '-')
				client_usage(3, argv[i]);
			if (mode) { client_usage(5, argv[i]); }
			arg = argv[i + 1];
			i++;
			log_printf(0, "setting write'''
W_NEW = '''			arg = oneArg(argc, argv, &i, mode);
			log_printf(0, "setting write'''
R_OLD = '''			a = argv[i + 1];
			if (i + 1 == argc || !a || *a == '-')
				{ r3x: client_usage(3, argv[i]); }
			if (mode) { r5x: client_usage(5, argv[i]); }
			arg = argv[i + 1];
			i++;
			log_printf(0, "setting read'''
R_NEW = '''			arg = oneArg(argc, argv, &i, mode);
			log_printf(0, "setting read'''
for k, b in bodies().items():
    new = 'static char *oneArg(int argc, char **argv, int *pi, int mode)\n{\n' + b + '}'
    V['w_' + k] = [(ONE_OLD, new), (W_OLD, W_NEW)]
