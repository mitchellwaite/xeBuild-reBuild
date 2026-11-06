# mode_client attempt 3: option arms as getArgs calls (gcc may inline the NULL-arg ones)
EB = '''			if (!argv[i + 1] || i + 1 == argc || *argv[i + 1] == '-')
				client_usage(3, argv[i]);
			if (mode)
				client_usage(5, argv[i]);
			arg = argv[++i];
			log_printf(0, "erase block set to %s\\n", arg);'''
BP = '''			if (!argv[i + 1] || i + 1 == argc || *argv[i + 1] == '-')
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
WB = '''			j = i + 1;
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
GEB = '''			arg = getArgs(argc, argv, &i, mode, 1, NULL, NULL);
			log_printf(0, "erase block set to %s\\n", arg);'''
GBP = '''			arg = getArgs(argc, argv, &i, mode, 1, &start, NULL);
'''
V = {
    'eb': [(EB, GEB)],
    'bp': [(BP, GBP)],
    'wb': [(WB, GBP)],
    'bpwb': [(BP, GBP), (WB, GBP)],
    'all3': [(BP, GBP), (WB, GBP), (EB, GEB)],
}
