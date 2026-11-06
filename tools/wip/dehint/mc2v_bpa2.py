# mode_client -bp arm without the pin: first-test shapes x second-test shapes
import itertools, os, runpy
OLD = runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mc2v_bpa.py'))['OLD']
FIRST = {
    'f0': '''			if (!argv[i + 1] || i + 1 == argc || *argv[i + 1] == '-')
				client_usage(3, argv[i]);
''',
    'fa': '''			a = argv[i + 1];
			if (i + 1 == argc || !a || *a == '-')
				client_usage(3, argv[i]);
''',
    'fa2': '''			a = argv[i + 1];
			if (!a || i + 1 == argc || *a == '-')
				client_usage(3, argv[i]);
''',
    'fj': '''			j = i + 1;
			a = argv[j];
			if (j == argc || !a || *a == '-')
				client_usage(3, argv[i]);
''',
    'fj2': '''			j = i + 1;
			a = argv[j];
			if (!a || j == argc || *a == '-')
				client_usage(3, argv[i]);
''',
}
SECOND = {
    's0': '''			b = argv[i + 2];
			j = i + 2;
			if (j == argc || !b || *b == '-')
				client_usage(4, argv[i]);
''',
    'sk': '''			j = i + 2;
			b = argv[j];
			if (j == argc || !b || *b == '-')
				client_usage(4, argv[i]);
''',
    'sk2': '''			j = i + 2;
			b = argv[j];
			if (!b || j == argc || *b == '-')
				client_usage(4, argv[i]);
''',
    'sb': '''			{ int k = i + 2; b = argv[k];
			if (!b || k == argc || *b == '-')
				client_usage(4, argv[i]); }
''',
    'sb2': '''			{ int k = i + 2; b = argv[k];
			if (k == argc || !b || *b == '-')
				client_usage(4, argv[i]); }
''',
}
END = {
    'e0': '''			i = j;
			arg = argv[i - 1];
''',
    'e2': '''			i += 2;
			arg = argv[i - 1];
''',
}
V = {}
for f, s, e in itertools.product(FIRST, SECOND, END):
    if s.startswith('sb') and e == 'e0':
        continue
    if f.startswith('fj') and e == 'e0' and s == 's0':
        pass
    V['%s_%s_%s' % (f, s, e)] = [(OLD, FIRST[f] + SECOND[s] + '''			start = b;
			if (mode)
				client_usage(5, argv[i]);
''' + END[e])]
