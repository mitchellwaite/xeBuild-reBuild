# s135: arg-loop restructurings of best34; each variant = list of (old,new) replacements or a function
import subprocess, sys, os
D = os.path.dirname(os.path.abspath(__file__))
base = open(os.path.join(D, sys.argv[1] if len(sys.argv) > 1 else 'best34.c')).read()
TAG = sys.argv[2] if len(sys.argv) > 2 else ''
RB_OLD = '''			if (reboot == 1)
				log_printf(0, "shutdown superseded by reboot, ignoring -s in favor of -reboot\\n");
			log_printf(0, "setting reboot on completion\\n");
			reboot = 2;'''
S_OLD = '''			if (reboot == 2)
				log_printf(0, "reboot has already been set on command line, ignoring -s\\n");
			else {
				log_printf(0, "setting shutdown on completion\\n");
				reboot = 1;
			}'''
HELP = '''		if (!strnicmp(argv[i], "help", 2) || !strnicmp(argv[i], "-?", 2) || !strnicmp(argv[i], "/?", 2))
			client_usage(0, NULL);
		if (!strnicmp(argv[i], "-noenter", 8)) {'''
TAIL = '\t\telse\n\t\t\tclient_usage(1, argv[i]);\n\t}'
V = {}
V['rb_ifelse'] = [(RB_OLD, '''			if (reboot == 1) {
				log_printf(0, "shutdown superseded by reboot, ignoring -s in favor of -reboot\\n");
				log_printf(0, "setting reboot on completion\\n");
			} else
				log_printf(0, "setting reboot on completion\\n");
			reboot = 2;''')]
V['rb_setfirst'] = [(RB_OLD, '''			j = reboot;
			reboot = 2;
			if (j == 1)
				log_printf(0, "shutdown superseded by reboot, ignoring -s in favor of -reboot\\n");
			log_printf(0, "setting reboot on completion\\n");''')]
V['rb_flag'] = [(RB_OLD, RB_OLD.replace('if (reboot == 1)', 'if (reboot & 1)'))]
V['s_sel'] = [(S_OLD, '''			log_printf(0, reboot == 2 ? "reboot has already been set on command line, ignoring -s\\n" : "setting shutdown on completion\\n");
			if (reboot != 2)
				reboot = 1;''')]
V['s_neg'] = [(S_OLD, '''			if (reboot != 2) {
				log_printf(0, "setting shutdown on completion\\n");
				reboot = 1;
			} else
				log_printf(0, "reboot has already been set on command line, ignoring -s\\n");''')]
V['s_cont'] = [(S_OLD, '''			if (reboot == 2) {
				log_printf(0, "reboot has already been set on command line, ignoring -s\\n");
				continue;
			}
			log_printf(0, "setting shutdown on completion\\n");
			reboot = 1;''')]
V['s_tern'] = [(S_OLD, '''			if (reboot == 2)
				log_printf(0, "reboot has already been set on command line, ignoring -s\\n");
			else
				log_printf(0, "setting shutdown on completion\\n");
			reboot = reboot == 2 ? 2 : 1;''')]
V['s_flag'] = [(S_OLD, S_OLD.replace('if (reboot == 2)', 'if (reboot & 2)'))]
V['rb_s_flag'] = V['rb_flag'] + V['s_flag']
V['help_elif'] = [(HELP, HELP.replace('\t\tif (!strnicmp(argv[i], "-noenter"', '\t\telse if (!strnicmp(argv[i], "-noenter"'))]
V['help_sep'] = [(HELP, '''		if (!strnicmp(argv[i], "help", 2))
			client_usage(0, NULL);
		if (!strnicmp(argv[i], "-?", 2))
			client_usage(0, NULL);
		if (!strnicmp(argv[i], "/?", 2))
			client_usage(0, NULL);
		if (!strnicmp(argv[i], "-noenter", 8)) {''')]
V['help_a'] = [(HELP, '''		a = argv[i];
		if (!strnicmp(a, "help", 2) || !strnicmp(a, "-?", 2) || !strnicmp(a, "/?", 2))
			client_usage(0, NULL);
		if (!strnicmp(argv[i], "-noenter", 8)) {''')]
V['noenter_cont'] = [('''			promptEnter = 0;
		} else if (!strnicmp(argv[i], "-reboot", 7)) {''', '''			promptEnter = 0;
			continue;
		}
		if (!strnicmp(argv[i], "-reboot", 7)) {''')]
V['reboot_cont'] = [('''			reboot = 2;
		} else if (E(!strnicmp(argv[i], "-bp", 3))) {''', '''			reboot = 2;
			continue;
		}
		if (E(!strnicmp(argv[i], "-bp", 3))) {''')]
V['nr_cont'] = V['noenter_cont'] + V['reboot_cont']
V['s_contchain'] = [('''				reboot = 1;
			}
		} else if (!strnicmp(argv[i], "-keys", 5)) {''', '''				reboot = 1;
			}
			continue;
		}
		if (!strnicmp(argv[i], "-keys", 5)) {''')]
V['ip_cont'] = [('''			log_printf(0, "setting forced IP to %s\\n", ip);
		} else if (!strnicmp(argv[i], "-r", 2)) {''', '''			log_printf(0, "setting forced IP to %s\\n", ip);
			continue;
		}
		if (!strnicmp(argv[i], "-r", 2)) {''')]
V['v_first'] = [('''		} else if (!strnicmp(argv[i], "-v", 2))
			log_verbose_flag(argv[i][2]);
		else''', '''		} else'''), ('''		if (!strnicmp(argv[i], "-noenter", 8)) {''', '''		if (!strnicmp(argv[i], "-v", 2))
			log_verbose_flag(argv[i][2]);
		else if (!strnicmp(argv[i], "-noenter", 8)) {''')]
V['nma_1'] = [('if (NO_MODE_ARG(mode, arg)) {', 'if (!mode || !arg) {')]
V['nma_2'] = [('if (NO_MODE_ARG(mode, arg)) {', 'if (!arg || !mode) {')]
V['nma_3'] = [('if (NO_MODE_ARG(mode, arg)) {', 'if (!(mode && arg)) {')]
V['ip_i'] = [('''			ip = argv[++i];
			log_printf(0, "setting forced IP''', '''			i++;
			ip = argv[i];
			log_printf(0, "setting forced IP''')]
V['r_a'] = [('''			arg = argv[++i];
			log_printf(0, "setting read filename''', '''			arg = a;
			i++;
			log_printf(0, "setting read filename''')]
V['w_a'] = [('''			arg = argv[++i];
			log_printf(0, "setting write filename''', '''			arg = a;
			i++;
			log_printf(0, "setting write filename''')]
V['rw_a'] = V['r_a'] + V['w_a']
V['e_a'] = [('''			if (!argv[i + 1] || i + 1 == argc || *argv[i + 1] == '-')
				client_usage(3, argv[i]);
			if (mode)
				client_usage(5, argv[i]);
			arg = argv[++i];
			log_printf(0, "setting avatar''', '''			a = argv[i + 1];
			if (!a || i + 1 == argc || *a == '-')
				client_usage(3, argv[i]);
			if (mode)
				client_usage(5, argv[i]);
			arg = argv[++i];
			log_printf(0, "setting avatar''')]
I_OLD = '''			if (!argv[i + 1] || i + 1 == argc || *argv[i + 1] == '-')
				arg = dummy;
			else {
				arg = argv[++i];
				log_printf(0, "info dump path set to %s\\n", arg);
			}'''
P_OLD = I_OLD.replace('info dump path', 'patch file')
V['i_neg'] = [(I_OLD, '''			if (argv[i + 1] && i + 1 != argc && *argv[i + 1] != '-') {
				arg = argv[++i];
				log_printf(0, "info dump path set to %s\\n", arg);
			} else
				arg = dummy;''')]
V['p_neg'] = [(P_OLD, V['i_neg'][0][1].replace('info dump path', 'patch file'))]
V['i_pre'] = [(I_OLD, '''			arg = dummy;
			if (!(!argv[i + 1] || i + 1 == argc || *argv[i + 1] == '-')) {
				arg = argv[++i];
				log_printf(0, "info dump path set to %s\\n", arg);
			}''')]
V['p_pre'] = [(P_OLD, V['i_pre'][0][1].replace('info dump path', 'patch file'))]
V['keys_order'] = [('''			mode = 3;
			arg = dummy;''', '''			arg = dummy;
			mode = 3;''')]
V['v_inv'] = [('''		} else if (!strnicmp(argv[i], "-v", 2))
			log_verbose_flag(argv[i][2]);
		else
			client_usage(1, argv[i]);''', '''		} else {
			if (strnicmp(argv[i], "-v", 2))
				client_usage(1, argv[i]);
			log_verbose_flag(argv[i][2]);
		}''')]
V['while'] = [('	for (i = 0; i < argc; i++) {', '	i = 0;\n	while (i < argc) {'), (TAIL, '\t\telse\n\t\t\tclient_usage(1, argv[i]);\n\t\ti++;\n\t}')]
V['v_a'] = [('''			log_verbose_flag(argv[i][2]);''', '''			{ a = argv[i]; log_verbose_flag(a[2]); }''')]
def swap_blocks(src, h1, h2, end):
    a = src.index(h1); b = src.index(h2); c = src.index(end)
    assert a < b < c
    return src[:a] + src[b:c] + src[a:b] + src[c:]
def EI(o, n, e=False):
    return ('} else if (E(!strnicmp(argv[i], "%s", %d))) {' if e else '} else if (!strnicmp(argv[i], "%s", %d)) {') % (o, n)
S = {}
# pairwise swaps of adjacent mutually exclusive tests (prefixes distinct, so at most one matches)
S['sw_rb_wb'] = lambda s: swap_blocks(s, EI('-rb', 3), EI('-wb', 3, 1), EI('-eb', 3, 1))
S['sw_wb_eb'] = lambda s: swap_blocks(s, EI('-wb', 3, 1), EI('-eb', 3, 1), EI('-s', 2))
S['sw_s_keys'] = lambda s: swap_blocks(s, EI('-s', 2), EI('-keys', 5), EI('-ip', 3))
S['sw_keys_ip'] = lambda s: swap_blocks(s, EI('-keys', 5), EI('-ip', 3), EI('-r', 2))
S['sw_r_w'] = lambda s: swap_blocks(s, EI('-r', 2), EI('-w', 2), EI('-e', 2, 1))
S['sw_e_c'] = lambda s: swap_blocks(s, EI('-e', 2, 1), EI('-c', 2, 1), EI('-i', 2))
S['sw_c_i'] = lambda s: swap_blocks(s, EI('-c', 2, 1), EI('-i', 2), EI('-p', 2))
S['sw_i_p'] = lambda s: swap_blocks(s, EI('-i', 2), EI('-p', 2), '} else if (!strnicmp(argv[i], "-v", 2))')
S['sw_bp_rb'] = lambda s: swap_blocks(s, EI('-bp', 3, 1), EI('-rb', 3), EI('-wb', 3, 1))
# -reboot must stay before -r (prefix); -s after -reboot? "-s" doesn't prefix-match "-reboot": ok
S['sw_reboot_bp'] = lambda s: swap_blocks(s, EI('-reboot', 7), EI('-bp', 3, 1), EI('-rb', 3))
def tail_label(s, lab, code):
    return s.replace(TAIL, '\t\telse\n\t\t\tclient_usage(1, argv[i]);\n\t\tcontinue;\n\t%s:\n\t\tclient_usage(%s, argv[i]);\n\t}' % (lab, code), 1)
def mk_goto(names, code):
    def f(s):
        lab = 'bad%d' % code
        if lab + ':' not in s: s = tail_label(s, lab, code)
        for n in names:
            h = s.index(n); t = 'client_usage(%d, argv[i]);' % code; e = s.index(t, h)
            s = s[:e] + 'goto %s;' % lab + s[e + len(t):]
        return s
    return f
ALL3 = ['"-bp", 3', '"-wb", 3', '"-eb", 3', '"-ip", 3', '"-r", 2', '"-w", 2', '"-e", 2', '"-c", 2']
S['g3_ip'] = mk_goto(['"-ip", 3'], 3)
S['g3_ec'] = mk_goto(['"-e", 2', '"-c", 2'], 3)
S['g3_rw'] = mk_goto(['"-r", 2', '"-w", 2'], 3)
S['g3_eb'] = mk_goto(['"-eb", 3'], 3)
S['g3_all'] = mk_goto(ALL3, 3)
S['g5_rw'] = mk_goto(['"-r", 2', '"-w", 2'], 5)
S['g5_ec'] = mk_goto(['"-e", 2', '"-c", 2'], 5)
S['g5_all'] = mk_goto(['"-bp", 3', '"-wb", 3', '"-eb", 3', '"-r", 2', '"-w", 2', '"-e", 2', '"-c", 2'], 5)
S['g35_all'] = lambda s: mk_goto(ALL3, 3)(mk_goto(['"-bp", 3', '"-wb", 3', '"-eb", 3', '"-r", 2', '"-w", 2', '"-e", 2', '"-c", 2'], 5)(s))
def mk_codevar(names, codes):
    def f(s):
        if 'bad:' not in s:
            s = s.replace('\tint j;\n', '\tint j;\n\tint bc;\n', 1)
            s = s.replace(TAIL, '\t\telse\n\t\t\tclient_usage(1, argv[i]);\n\t\tcontinue;\n\tbad:\n\t\tclient_usage(bc, argv[i]);\n\t}', 1)
        for code in codes:
            for n in names:
                h = s.index(n); t = 'client_usage(%d, argv[i]);' % code; e = s.index(t, h)
                s = s[:e] + '{ bc = %d; goto bad; }' % code + s[e + len(t):]
        return s
    return f
S['cv_ip'] = mk_codevar(['"-ip", 3'], [3])
S['cv_r'] = mk_codevar(['"-r", 2'], [3, 5])
S['cv_rw'] = mk_codevar(['"-r", 2', '"-w", 2'], [3, 5])
S['cv_ec'] = mk_codevar(['"-e", 2', '"-c", 2'], [3, 5])
S['cv_all'] = mk_codevar(['"-wb", 3', '"-eb", 3', '"-ip", 3', '"-r", 2', '"-w", 2', '"-e", 2', '"-c", 2'], [3, 5])
def run(name, src):
    p = os.path.join(D, 'v', TAG + name + '.c'); open(p, 'w', newline='\n').write(src)
    r = subprocess.run(['sh', os.path.join(D, '..', 's101', 'f2.sh'), p], capture_output=True, text=True)
    return r.stdout.strip()
only = set(sys.argv[3:])
for n, reps in V.items():
    if only and n not in only: continue
    s = base
    ok = all(o in s for o, _ in reps)
    for o, nw in reps: s = s.replace(o, nw, 1)
    print(n, run(n, s) if ok else 'NOAPPLY', flush=True)
for n, f in S.items():
    if only and n not in only: continue
    try: s = f(base)
    except Exception as e: print(n, 'ERR', e); continue
    print(n, run(n, s), flush=True)
