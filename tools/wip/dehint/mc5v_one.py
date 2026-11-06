# mode_client attempt 5: -e / -c arms through oneArg (shared helper, so called 2-3 times;
# max-inline-insns-auto is 30 and oneArg's size is 31: `static inline` lifts that limit to
# max-inline-insns-single).  Base: src/mode_client.c.
E_OLD = '''			if (!argv[i + 1] || i + 1 == argc || *argv[i + 1] == '-')
				client_usage(3, argv[i]);
			if (mode)
				client_usage(5, argv[i]);
			arg = argv[i + 1];
			i++;
			log_printf(0, "setting avatar'''
E_NEW = '''			arg = oneArg(argc, argv, &i, mode);
			log_printf(0, "setting avatar'''
C_OLD = '''			if (!argv[i + 1] || i + 1 == argc || *argv[i + 1] == '-')
				client_usage(3, argv[i]);
			if (mode)
				client_usage(5, argv[i]);
			arg = argv[i + 1];
			i++;
			log_printf(0, "setting xbox'''
C_NEW = '''			arg = oneArg(argc, argv, &i, mode);
			log_printf(0, "setting xbox'''
INL = [('static char *oneArg(', 'static inline char *oneArg(')]
V = {
    'e': [(E_OLD, E_NEW)],
    'c': [(C_OLD, C_NEW)],
    'ec': [(E_OLD, E_NEW), (C_OLD, C_NEW)],
    'e_i': [(E_OLD, E_NEW)] + INL,
    'c_i': [(C_OLD, C_NEW)] + INL,
    'ec_i': [(E_OLD, E_NEW), (C_OLD, C_NEW)] + INL,
    'inl': INL,
    'inl_all': INL + [('static char *bpArgs(', 'static inline char *bpArgs('),
                      ('static char *wbArgs(', 'static inline char *wbArgs(')],
}
W_OLD = '''			a = argv[i + 1];
			if (i + 1 == argc || !a || *a == '-')
				client_usage(3, argv[i]);
			if (mode) { client_usage(5, argv[i]); }'''
W_NEW = '''			a = argv[i + 1];
			if (!a || i + 1 == argc || *a == '-')
				client_usage(3, argv[i]);
			if (mode) { client_usage(5, argv[i]); }'''
R_OLD = '''			if (i + 1 == argc || !a || *a == '-')
				{ r3x:'''
R_NEW = '''			if (!a || i + 1 == argc || *a == '-')
				{ r3x:'''
V.update({
    'e_w': [(E_OLD, E_NEW), (W_OLD, W_NEW)],
    'c_w': [(C_OLD, C_NEW), (W_OLD, W_NEW)],
    'e_r': [(E_OLD, E_NEW), (R_OLD, R_NEW)],
    'c_r': [(C_OLD, C_NEW), (R_OLD, R_NEW)],
    'w': [(W_OLD, W_NEW)],
    'r': [(R_OLD, R_NEW)],
})
