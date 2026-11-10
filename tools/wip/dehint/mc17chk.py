#!/usr/bin/env python3
"""mode_client attempt 17: which of the landed shapes are load-bearing (one edit each on
today's src/mode_client.c, scored against build/mc/w17/reference.o).

python tools/wip/dehint/mc17chk.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc17lib as L

t = L.read_src(L.SRC)


def one(name, a, b, n=1):
    assert t.count(a) == n, (name, t.count(a))
    print('%-40s %s' % (name, L.fmt(L.score_text(t.replace(a, b), lay=True))), flush=True)


def comment_and_return(key):
    i = t.index(key)
    return t[t.rindex('/*', 0, i):t.index('return;', i) + len('return;')]


WRITTEN = '''if (!argv[i + 1] || i + 1 == argc || *argv[i + 1] == '-')
				client_usage(3, argv[i]);
'''
E_ARM = WRITTEN + '''			if (mode)
				client_usage(5, argv[i]);
			arg = argv[i + 1];
			i++;
			log_printf(0, "setting avatar'''
HELP = '''if (!strnicmp(argv[i], "help", 2) || !strnicmp(argv[i], "-?", 2) || !strnicmp(argv[i], "/?", 2))
			client_usage(0, NULL);'''
HELP3 = '''if (!strnicmp(argv[i], "help", 2))
			client_usage(0, NULL);
		if (!strnicmp(argv[i], "-?", 2))
			client_usage(0, NULL);
		if (!strnicmp(argv[i], "/?", 2))
			client_usage(0, NULL);'''
END = '''		if (reboot)
			netReboot(reboot);
		netDisconnect();
'''
END2 = '''		if (reboot) {
			netReboot(reboot);
			netDisconnect();
		} else
			netDisconnect();
'''
GUARD = '''		if (!reboot)
			client_usage(2, NULL);
		mode = 6;
'''
GUARD2 = '''		if (reboot)
			mode = 6;
		else
			client_usage(2, NULL);
'''

one('src', 'int mode_client', 'int mode_client')
one('mode = 6 gone (mode stays 0)', '\t\tmode = 6;\n', '')
one('case 6 gone, mode = 6 kept', '\t\tcase 6:\n\t\t\tbreak;\n', '')
one('netDisconnect in both reboot arms', END, END2)
one('-ip written out', 'ip = oneArg(argc, argv, &i, 0);', WRITTEN + '\t\t\tip = argv[i + 1];\n\t\t\ti++;')
one('-r / -w through oneArg', 'arg = fileArg(argc, argv, &i, mode);', 'arg = oneArg(argc, argv, &i, mode);', 2)
one('-eb through fileArg', 'arg = oneArg(argc, argv, &i, mode);', 'arg = fileArg(argc, argv, &i, mode);')
one('bpArgs: b = argv[i + 2]; j = i + 2;', 'client_usage(3, argv[i]);\n\tj++;\n\tb = argv[j];\n\tif (j == argc || !b',
    'client_usage(3, argv[i]);\n\tb = argv[i + 2];\n\tj = i + 2;\n\tif (j == argc || !b')
one("clientInfo's redundant return gone", comment_and_return('redundant return (end of the function)'), '')
one("clientBinPatch's redundant return gone", comment_and_return('redundant return (nothing'), '')
i = t.index('/* -e and -c test in place')
c = t[i:t.index('*/', i) + 2]
one('-e through oneArg', c + '\n\t\t\t' + E_ARM, 'arg = oneArg(argc, argv, &i, mode);\n\t\t\tlog_printf(0, "setting avatar')
one('help test in three ifs', HELP, HELP3)
one('guard as !(mode && arg)', 'if (!mode || !arg) {', 'if (!(mode && arg)) {')
one('usage(2) in the else', GUARD, GUARD2)
