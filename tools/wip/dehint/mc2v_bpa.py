# mode_client -bp arm without the "a"(i + 1) pin
OLD = '''			if (!argv[i + 1] || i + 1 == argc || *argv[i + 1] == '-')
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
T1 = '''			if (!argv[i + 1] || i + 1 == argc || *argv[i + 1] == '-')
				client_usage(3, argv[i]);
'''
TAIL = '''			if (mode)
				client_usage(5, argv[i]);
'''
V = {
    'plain': [(OLD, OLD.replace('			__asm__("" :: "a"(i + 1));\n', ''))],
    'arg_early': [(OLD, T1 + '''			arg = argv[i + 1];
			b = argv[i + 2];
			j = i + 2;
			if (j == argc || !b || *b == '-')
				client_usage(4, argv[i]);
			start = b;
''' + TAIL + '''			i = j;
''')],
    'arg_a': [(OLD, '''			a = argv[i + 1];
			if (!a || i + 1 == argc || *a == '-')
				client_usage(3, argv[i]);
			b = argv[i + 2];
			j = i + 2;
			if (j == argc || !b || *b == '-')
				client_usage(4, argv[i]);
			start = b;
''' + TAIL + '''			i = j;
			arg = a;
''')],
    'arg_a2': [(OLD, '''			a = argv[i + 1];
			if (!a || i + 1 == argc || *a == '-')
				client_usage(3, argv[i]);
			b = argv[i + 2];
			j = i + 2;
			if (j == argc || !b || *b == '-')
				client_usage(4, argv[i]);
			start = b;
''' + TAIL + '''			i = j;
			arg = argv[i - 1];
''')],
    'i_plus': [(OLD, T1 + '''			b = argv[i + 2];
			j = i + 2;
			if (j == argc || !b || *b == '-')
				client_usage(4, argv[i]);
			start = b;
''' + TAIL + '''			arg = argv[i + 1];
			i = j;
''')],
    'i_inc': [(OLD, T1 + '''			b = argv[i + 2];
			j = i + 2;
			if (j == argc || !b || *b == '-')
				client_usage(4, argv[i]);
			start = b;
''' + TAIL + '''			i++;
			arg = argv[i];
			i++;
''')],
    'i_k': [(OLD, T1 + '''			j = i + 2;
			b = argv[j];
			if (j == argc || !b || *b == '-')
				client_usage(4, argv[i]);
			start = b;
''' + TAIL + '''			i = j;
			arg = argv[i - 1];
''')],
}

K = V['i_k'][0][1]
def kv(new):
    return [(OLD, new)]
V['k_scope'] = kv(T1 + '''			{ int k = i + 2; b = argv[k];
			if (k == argc || !b || *b == '-')
				client_usage(4, argv[i]);
			start = b;
''' + TAIL.replace('\t\t\t', '\t\t\t') + '''			i = k; }
			arg = argv[i - 1];
''')
V['k_scope2'] = kv(T1 + '''			{ int k = i + 2; b = argv[k];
			if (k == argc || !b || *b == '-')
				client_usage(4, argv[i]); }
			start = b;
''' + TAIL + '''			i += 2;
			arg = argv[i - 1];
''')
V['k_j_b'] = kv(T1 + '''			j = i + 2;
			b = argv[j];
			if (!b || j == argc || *b == '-')
				client_usage(4, argv[i]);
			start = b;
''' + TAIL + '''			i = j;
			arg = argv[i - 1];
''')
V['k_ipl2'] = kv(T1 + '''			j = i + 2;
			b = argv[j];
			if (j == argc || !b || *b == '-')
				client_usage(4, argv[i]);
			start = b;
''' + TAIL + '''			i += 2;
			arg = argv[i - 1];
''')
V['k_start'] = kv(T1 + '''			j = i + 2;
			start = argv[j];
			if (j == argc || !start || *start == '-')
				client_usage(4, argv[i]);
''' + TAIL + '''			i = j;
			arg = argv[i - 1];
''')
V['k_jarg'] = kv(T1 + '''			j = i + 2;
			b = argv[j];
			if (j == argc || !b || *b == '-')
				client_usage(4, argv[i]);
			start = b;
''' + TAIL + '''			arg = argv[j - 1];
			i = j;
''')
